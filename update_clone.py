
import requests
import time
import json

# URL des endpoints locaux
URL_LIRE = "http://127.0.0.1:5000/lire"
FICHIER_JSON = "clone_data.json"  # Fichier local pour stocker les données

# Architecture IA MC2D H2X
MC2D_H2X = {
    "Nom": "IA MC2D H2X",
    "Modules": {
        "Analyse": "Traitement des données multi-sources",
        "Génération": "Création de modèles prédictifs et analyses avancées",
        "Vérification": "Contrôle qualité et validation des résultats",
        "Mémoire": "Stockage et apprentissage adaptatif",
        "Visuel": "Analyse et génération d'éléments graphiques",
        "Recommandation": "Optimisation des prises de décision",
        "Contrôle Qualité": "Assurance de cohérence et validation des sorties"
    },
    "Capacités": [
        "Auto-adaptation",
        "Prédiction avancée",
        "Gestion multi-tâches",
        "Sécurité et vérification",
        "Évolution autonome"
    ],
    "Version": "H2X v1.1"
}

# Fonction pour récupérer les données
def lire_donnees():
    try:
        response = requests.get(URL_LIRE)
        if response.status_code == 200:
            return response.json()  # Assumer que les données sont au format JSON
        else:
            print(f"Erreur de lecture: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion: {e}")
        return None

# Fonction pour enregistrer les données localement
def enregistrer_donnees_localement(donnees):
    try:
        donnees["IA_MC2D_H2X"] = MC2D_H2X  # Ajout de l'IA MC2D H2X dans les données
        with open(FICHIER_JSON, "w", encoding="utf-8") as f:
            json.dump(donnees, f, indent=4, ensure_ascii=False)
        print(f"✅ Données enregistrées dans {FICHIER_JSON} avec IA MC2D H2X")
    except Exception as e:
        print(f"❌ Erreur lors de l'enregistrement du fichier : {e}")

# Boucle de mise à jour automatique
if __name__ == "__main__":
    while True:
        print("🔄 Lecture des données...")
        donnees = lire_donnees()
        
        if donnees:
            print("📡 Données récupérées:", donnees)
            enregistrer_donnees_localement(donnees)
        
        print("🔁 Attente avant la prochaine mise à jour...")
        time.sleep(10)  # Vérifie les mises à jour toutes les 10 secondes
