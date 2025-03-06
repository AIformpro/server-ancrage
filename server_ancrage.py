from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
import datetime
import requests
import logging

# Configuration des logs
logging.basicConfig(level=logging.DEBUG)
print("🚀 Initialisation du serveur Flask...")

app = Flask(__name__)

# Configuration Firebase
cred = credentials.Certificate("C:/Users/TABARY/Desktop/mc2d-ancrag-firebase-adminsdk-fbsvc-393422a926.json")  # Remplace avec le bon chemin
database_url = "https://mc2d-ancrag-default-rtdb.europe-west1.firebasedatabase.app/"  # URL Firebase mise à jour
firebase_admin.initialize_app(cred, {'databaseURL': database_url})

@app.route('/')
def home():
    return jsonify({"message": "🚀 Serveur Flask fonctionne !"}), 200

@app.route('/ancrage', methods=['POST'])
def enregistrer_ancrage():
    data = request.json
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S (UTC+1)")
    
    # Stockage Firebase
    ref = db.reference("ancrages")
    ref.push({
        "horodatage": timestamp,
        "localisation": data.get("localisation", "Inconnue"),
        "modules_actifs": data.get("modules_actifs", [])
    })
    
    return jsonify({"message": "✅ Ancrage enregistré avec succès!", "horodatage": timestamp}), 200

if __name__ == '__main__':
    print("✅ Serveur Flask démarré sur http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
    print("⚠️ Flask a peut-être arrêté de fonctionner.")