from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
importer os
demandes d'importation
from datetime import datetime

application = Flask(__name__, static_folder='static')
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# Configuration Airtable
AIRTABLE_TOKEN = os.environ.get('AIRTABLE_TOKEN', 'patruL5am2bu7F0Jz.459da3abb513463808cfe3fc42da35c4f6f1108e365703478c3256df97b53e1e')
AIRTABLE_BASE_ID = 'appwhkvPyDNMaymdF'
AIRTABLE_TABLE_ID = 'tbl8KI7jjVJibStl6'

def save_to_airtable(data, bilan_html=''):
    """Enregistrer un prospect dans Airtable."""
    étiquettes_situation = {
        'reconversion': 'En reconversion active',
        'poste_insatisfait': 'En poste mais insatisfait(e)',
        'recherche_emploi': 'En recherche d'emploi',
        'etudiant': 'Étudiant(e) / Jeune diplômé(e)'
    }
    besoins_labels = {
        'metier': 'Trouver son métier idéal',
        'quitter': 'Quitter son job actuel',
        'financement' : 'Financer sa reconversion',
        'entrepreneur' : 'Devenir entrepreneur / freelance',
        'formation': 'Trouver une formation adaptée'
    }
    étiquettes_urgence = {
        'faible' : '😌 Pas stressé(e)',
        'peu': '🙂 Un peu stressé(e)',
        'moyen': '😐 Moyennement stressé(e)',
        'fort' : '😟 Très stressé(e)',
        'extreme': '😰 Extrêmement stressé(e)'
    }

    besoins_raw = data.get('besoins', [])
    si isinstance (besoins_raw, str):
        besoins_raw = [besoins_raw]
    besoins_str = ', '.join([besoins_labels.get(b, b) for b in besoins_raw])

    enregistrement = {
        "champs" : {
            "Prénom": data.get('prenom', ''),
            "Email" : data.get('email', ''),
            "Téléphone": data.get('téléphone', ''),
            "Situation actuelle": situation_labels.get(data.get('situation', ''), data.get('situation', '')),
            "Besoins / Objectifs": besoins_str,
            "Code postal" : data.get('cp', ''),
            "Niveau d'urgence": urgence_labels.get(data.get('urgence', ''), data.get('urgence', '')),
            "Date de soumission": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            "Mini-bilan IA" : bilan_html[:10000] if bilan_html sinon ''
        }
    }

    essayer:
        réponse = requêtes.post(
            f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}',
            en-têtes={
                'Autorisation': f'Porteur {AIRTABLE_TOKEN}',
                'Content-Type': 'application/json'
            },
            json=enregistrement,
            délai d'attente=10
        )
        renvoyer response.status_code == 200
    sauf Exception comme e :
        print(f'Erreur Airtable: {e}')
        renvoyer Faux


@app.route('/')
def index():
    renvoie send_from_directory('static', 'index.html')

@app.route('/<chemin:nom_du_fichier>')
def static_files(filename):
    renvoie send_from_directory('static', nom_de_fichier)

@app.route('/api/bilan', methods=['POST', 'OPTIONS'])
def generate_bilan():
    si request.method == 'OPTIONS':
        réponse = jsonify({'ok': True})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        réponse de retour

    données = requête.get_json()
    sinon des données :
        return jsonify({'success': False, 'error': 'Données manquantes'}), 400

    prenom = data.get('prenom', '')
    situation_map = {
        'reconversion': 'en reconversion active (veut changer de voie professionnelle)',
        'poste_insatisfait': 'en poste mais insatisfait(e) (a un emploi mais cherche autre chose)',
        'recherche_emploi': 'en recherche d'emploi actif',
        'etudiant': 'étudiant(e) ou jeune diplômé(e) cherchant son orientation'
    }
    besoins_map = {
        'metier': 'trouver son métier idéal',
        'quitter': 'quitter fils job actuel',
        'financement' : 'financer sa reconversion',
        'entrepreneur' : 'devenir entrepreneur ou freelance',
        'formation': 'trouver une formation adaptée'
    }
    carte_urgence = {
        'faible': 'pas du tout stressé(e) par son avenir',
        'peu': 'un peu stressé(e) par son avenir',
        'moyen': 'moyennement stressé(e) par son avenir',
        'fort': 'très stressé(e) par son avenir',
        'extreme': 'extrêmement stressé(e) par son avenir'
    }

    situation = situation_map.get(data.get('situation', ''), 'en transition professionnelle')
    besoins_raw = data.get('besoins', [])
    si isinstance (besoins_raw, str):
        besoins_raw = [besoins_raw]
    besoins = ', '.join([besoins_map.get(b, b) for b in besoins_raw]) ou 'non précis'
    age = data.get('age', 'non précis')
    genre = data.get('genre', '')
    cp = data.get('cp', '')
    urgence = urgence_map.get(data.get('urgence', ''), 'stressé(e) par son avenir')
    contact = 'souhaite être accompagné(e) par un conseiller' if data.get('contact') == 'conseiller' else 'préfère avancer en autonomie'
    accord = 'e' si genre == 'femme' sinon ''

    prompt = f"""Tu es un conseiller bilan expert en reconversion professionnelle et de compétences en France.
Rédige un mini-bilan pour personnalisé {prenom ou 'cette personne'}, une personne {situation}.

Profil :
- Prénom : {prenom ou 'non renseigné'}
- Genre : {genre ou 'non précis'}
- Tranche d'âge : {age}
- Code postal : {cp ou 'non précis'}
- Besoins : {besoins}
- Niveau de stress : {urgence}
- Mode souhaité : {contact}

Rédige 4 sections HTML (sans html/head/body) :
1. Analyser la situation (2-3 phrases empathiques et précises{accord})
2. Ce que ça révèle (2-3 points forts ou signaux)
3. Tes options de financement (CPF, OPCO, France Travail, PTP selon statut, montants concrets)
4. Notre recommandation (1 conseil clair + encouragement)

Format pour chaque section :
<div class="bilan-section">
  <div class="bilan-section-title">[emoji] [Titre]</div>
  <div class="bilan-section-body">[HTML avec <strong> pour les points importants]</div>
</div>

Ton : chaleureux, professionnel, direct. Tutoie. Évite le jargon."""

    essayer:
        réponse = client.chat.completions.create(
            modèle='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': 'Tu es un expert en reconversion professionnelle et bilan de compétences en France.'},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=1500
        )
        bilan_html = response.choices[0].message.content

        # Enregistrement dans Airtable (en arrière-plan, sans bloquer la réponse)
        enregistrer_dans_airtable(données, bilan_html)

        resp = jsonify({'succès' : Vrai, 'prenom' : prenom, 'bilan_html' : bilan_html})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        retour resp
    sauf Exception comme e :
        resp = jsonify({'success': False, 'error': str(e)})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        retour resp, 500


@app.route('/api/prospect', methods=['POST', 'OPTIONS'])
def save_prospect():
    """Endpoint pour sauvegarder les données de contact (email/téléphone) dès la capture."""
    si request.method == 'OPTIONS':
        réponse = jsonify({'ok': True})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        réponse de retour

    données = requête.get_json()
    sinon des données :
        return jsonify({'success': False, 'error': 'Données manquantes'}), 400

    succès = enregistrer_dans_airtable(données)
    resp = jsonify({'success': success})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    retour resp


si __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
