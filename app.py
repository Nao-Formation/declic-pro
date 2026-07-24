from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
import os
import requests
from datetime import datetime

app = Flask(__name__, static_folder='static')
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# Configuration Airtable
AIRTABLE_TOKEN = os.environ.get('AIRTABLE_TOKEN', 'patruL5am2bu7F0Jz.459da3abb513463808cfe3fc42da35c4f6f1108e365703478c3256df97b53e1e')
AIRTABLE_BASE_ID = 'appwhkvPyDNMaymdF'
AIRTABLE_TABLE_ID = 'tbl8KI7jVJibStl6'

def save_to_airtable(data, bilan_html=''):
    situation_labels = {
        'reconversion':      'En reconversion active',
        'poste_insatisfait': "En poste mais insatisfait(e)",
        'recherche_emploi':  "En recherche d'emploi",
        'etudiant':          'Etudiant(e) / Jeune diplome(e)'
    }
    besoins_labels = {
        'metier':       'Trouver son metier ideal',
        'quitter':      'Quitter son job actuel',
        'financement':  'Financer sa reconversion',
        'entrepreneur': 'Devenir entrepreneur / freelance',
        'formation':    'Trouver une formation adaptee'
    }
    urgence_labels = {
        'faible':  'Pas stresse(e)',
        'peu':     'Un peu stresse(e)',
        'moyen':   'Moyennement stresse(e)',
        'fort':    'Tres stresse(e)',
        'extreme': 'Extremement stresse(e)'
    }
    besoins_raw = data.get('besoins', [])
    if isinstance(besoins_raw, str):
        besoins_raw = [besoins_raw]
    besoins_str = ', '.join([besoins_labels.get(b, b) for b in besoins_raw])
    record = {
        "fields": {
            "Prenom": data.get('prenom', ''),
            "Email": data.get('email', ''),
            "Telephone": data.get('telephone', ''),
            "Situation actuelle": situation_labels.get(data.get('situation', ''), data.get('situation', '')),
            "Besoins / Objectifs": besoins_str,
            "Code postal": data.get('cp', ''),
            "Niveau d'urgence": urgence_labels.get(data.get('urgence', ''), data.get('urgence', '')),
            "Date de soumission": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            "Mini-bilan IA": bilan_html[:10000] if bilan_html else ''
        }
    }
    try:
        r = requests.post(
            f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}',
            headers={'Authorization': f'Bearer {AIRTABLE_TOKEN}', 'Content-Type': 'application/json'},
            json=record, timeout=10
         )
        return r.status_code == 200
    except Exception as e:
        print(f'Erreur Airtable: {e}')
        return False

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
        return jsonify({'success': False, 'err
