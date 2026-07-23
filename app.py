from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
import os

app = Flask(__name__, static_folder='static')
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/api/bilan', methods=['POST', 'OPTIONS'])
def generate_bilan():
    if request.method == 'OPTIONS':
        response = jsonify({'ok': True})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        return response

    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Données manquantes'}), 400

    prenom = data.get('prenom', '')
    situation_map = {
        'reconversion':      'en reconversion active (veut changer de voie professionnelle)',
        'poste_insatisfait': 'en poste mais insatisfait(e) (a un emploi mais cherche autre chose)',
        'recherche_emploi':  'en recherche d\'emploi active',
        'etudiant':          'étudiant(e) ou jeune diplômé(e) cherchant son orientation'
    }
    besoins_map = {
        'metier':       'trouver son métier idéal',
        'quitter':      'quitter son job actuel',
        'financement':  'financer sa reconversion',
        'entrepreneur': 'devenir entrepreneur ou freelance',
        'formation':    'trouver une formation adaptée'
    }
    urgence_map = {
        'faible':  'pas du tout stressé(e) par son avenir',
        'peu':     'un peu stressé(e) par son avenir',
        'moyen':   'moyennement stressé(e) par son avenir',
        'fort':    'très stressé(e) par son avenir',
        'extreme': 'extrêmement stressé(e) par son avenir'
    }

    situation = situation_map.get(data.get('situation', ''), 'en transition professionnelle')
    besoins_raw = data.get('besoins', [])
    if isinstance(besoins_raw, str):
        besoins_raw = [besoins_raw]
    besoins = ', '.join([besoins_map.get(b, b) for b in besoins_raw]) or 'non précisé'
    age     = data.get('age', 'non précisé')
    genre   = data.get('genre', '')
    cp      = data.get('cp', '')
    urgence = urgence_map.get(data.get('urgence', ''), 'stressé(e) par son avenir')
    contact = 'souhaite être accompagné(e) par un conseiller' if data.get('contact') == 'conseiller' else 'préfère avancer en autonomie'
    accord  = 'e' if genre == 'femme' else ''

    prompt = f"""Tu es un conseiller expert en reconversion professionnelle et bilan de compétences en France.
Rédige un mini-bilan personnalisé pour {prenom or 'cette personne'}, une personne {situation}.

Profil :
- Prénom : {prenom or 'non renseigné'}
- Genre : {genre or 'non précisé'}
- Tranche d'âge : {age}
- Code postal : {cp or 'non précisé'}
- Besoins : {besoins}
- Niveau de stress : {urgence}
- Mode souhaité : {contact}

Rédige 4 sections HTML (sans html/head/body) :
1. Analyse de ta situation (2-3 phrases empathiques et précises{accord})
2. Ce que ça révèle (2-3 points forts ou signaux)
3. Tes options de financement (CPF, OPCO, France Travail, PTP selon statut, montants concrets)
4. Notre recommandation (1 conseil clair + encouragement)

Format pour chaque section :
<div class="bilan-section">
  <div class="bilan-section-title">[emoji] [Titre]</div>
  <div class="bilan-section-body">[HTML avec <strong> pour les points importants]</div>
</div>

Ton : chaleureux, professionnel, direct. Tutoie. Évite le jargon."""

    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': 'Tu es un expert en reconversion professionnelle et bilan de compétences en France.'},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=1500
        )
        bilan_html = response.choices[0].message.content
        resp = jsonify({'success': True, 'prenom': prenom, 'bilan_html': bilan_html})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except Exception as e:
        resp = jsonify({'success': False, 'error': str(e)})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
