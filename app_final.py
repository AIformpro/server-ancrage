
from flask import Flask, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

# Chemin du fichier JSON
file_path = r"C:\Users\TABARY\memoire_IA\memoire_IA.json"

# Fonction pour lire la mémoire IA
def lire_memoire():
    if not os.path.exists(file_path):
        return {"error": "Fichier introuvable"}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"error": "Fichier JSON corrompu"}

# Fonction pour sauvegarder la mémoire IA
def sauvegarder_memoire(data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Route pour afficher la mémoire IA
@app.route('/lire', methods=['GET'])
def lire():
    return jsonify(lire_memoire())

# Mise à jour de la mémoire globale (connaissances et décisions)
@app.route('/memoire/update', methods=['POST'])
def mettre_a_jour_memoire():
    print("🔄 Requête reçue pour mise à jour mémoire IA")
    update_data = request.get_json()

    if not update_data:
        print("🚨 Erreur : JSON invalide ou absent")
        return jsonify({"error": "JSON invalide ou absent"}), 400

    print("📜 Contenu de la requête JSON :", update_data)
    
    data = lire_memoire()
    if "mémoire_globale" not in data:
        data["mémoire_globale"] = {"connaissances": [], "décisions": []}

    if "connaissances" in update_data:
        data["mémoire_globale"]["connaissances"].extend(update_data["connaissances"])

    if "décisions" in update_data:
        data["mémoire_globale"]["décisions"].extend(update_data["décisions"])

    data["config"]["dernière_mise_à_jour"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sauvegarder_memoire(data)
    return jsonify({"success": True, "message": "Mémoire mise à jour", "mémoire_globale": data["mémoire_globale"]})

# Route pour mettre à jour Clone_Fred avec ses améliorations IA
@app.route('/ia/update', methods=['POST'])
def mettre_a_jour_ia():
    print("🔄 Requête reçue pour mise à jour de Clone_Fred")
    update_data = request.get_json()

    if not update_data or "nom_IA" not in update_data or "modifications" not in update_data:
        print("🚨 Erreur : JSON invalide ou données incomplètes")
        return jsonify({"error": "JSON invalide ou données incomplètes"}), 400

    print("📜 Contenu de la requête JSON :", update_data)

    data = lire_memoire()
    ia_nom = update_data["nom_IA"]

    if "IA_conçues" not in data:
        data["IA_conçues"] = {}

    if ia_nom not in data["IA_conçues"]:
        data["IA_conçues"][ia_nom] = {
            "nom": ia_nom,
            "architecture": update_data["modifications"].get("architecture", "Non définie"),
            "algorithmes": update_data["modifications"].get("algorithmes", []),
            "compétences": update_data["modifications"].get("compétences", []),
            "évolution": update_data["modifications"].get("évolution", "En cours")
        }
    else:
        # Mettre à jour l'IA existante
        for key, value in update_data["modifications"].items():
            data["IA_conçues"][ia_nom][key] = value

    data["config"]["dernière_mise_à_jour"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sauvegarder_memoire(data)
    return jsonify({"success": True, "message": f"IA '{ia_nom}' mise à jour", "IA": data["IA_conçues"][ia_nom]})

# Route pour récupérer Clone_Fred
@app.route('/clone', methods=['GET'])
def lire_clone():
    data = lire_memoire()

    if "Clone_Fred" not in data:
        data["Clone_Fred"] = {
            "Nom_Complet": "Frédéric Tabary",
            "Nom": "Clone IA de Fred",
            "Personnalité": "Directe, efficace, orientée action.",
            "Compétences": [],
            "Évolution": "Apprentissage continu basé sur interactions.",
            "Décisions": [],
            "Dernière_Mise_à_Jour": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        sauvegarder_memoire(data)

    return jsonify(data["Clone_Fred"])

# Lancement du serveur Flask
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
