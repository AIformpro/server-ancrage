
from flask import Flask, request, render_template_string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# 🔥 Initialisation de l'application Flask
app = Flask(__name__)

# 📌 Stockage des paramètres du projet
params = {
    "coût": np.random.uniform(100, 500),
    "délai": np.random.uniform(10, 50),
    "efficacité": np.random.uniform(50, 100),
    "imprévus": np.random.uniform(0, 20)
}

# 📌 Interface HTML avec affichage du graphique en direct
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot IA - Optimisation Projet</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; padding: 10px; text-align: center; }
        input, button { margin: 10px; padding: 10px; font-size: 16px; }
        .container { max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ccc; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🤖 Chatbot IA - Optimisation Projet</h2>
        <p>Entrez une commande pour ajuster les paramètres :</p>
        <form action="/" method="post">
            <input type="text" name="command" placeholder="Ex: ajuster coût 300" required>
            <button type="submit">Envoyer</button>
        </form>
        <h3>📝 Réponse du Chatbot :</h3>
        <p>{{ response }}</p>
        <h3>📊 Évolution des Paramètres :</h3>
        <img src="data:image/png;base64,{{ graph }}" alt="Graphique des paramètres">
    </div>
</body>
</html>
"""

def update_graph():
    """ Génère un graphique des paramètres et le convertit en base64 """
    plt.figure(figsize=(6, 4))
    plt.bar(params.keys(), params.values(), color=['blue', 'orange', 'green', 'red'])
    plt.xlabel("Paramètres")
    plt.ylabel("Valeurs")
    plt.title("État Actuel des Paramètres")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

@app.route("/", methods=["GET", "POST"])
def chatbot_interface():
    response = "Entrez une commande pour commencer."
    
    if request.method == "POST":
        command = request.form["command"].strip().lower()

        if command.startswith("ajuster "):
            try:
                parts = command.split()
                param = parts[1]
                value = float(parts[2])
                if param in params:
                    params[param] = max(0, min(value, 500))  # Empêcher les valeurs extrêmes
                    response = f"✅ {param} ajusté à {value}."
                else:
                    response = "❌ Paramètre inconnu. Utilisez : coût, délai, efficacité, imprévus."
            except (IndexError, ValueError):
                response = "❌ Format incorrect. Exemple : ajuster coût 300."
        elif command == "résultats":
            response = "📊 Mise à jour des résultats !"
        elif command == "exit":
            response = "👋 Session terminée."
        else:
            response = "❌ Commande inconnue. Essayez : ajuster [paramètre] [valeur], résultats, exit."
    
    graph = update_graph()
    return render_template_string(HTML_TEMPLATE, response=response, graph=graph)

if __name__ == "__main__":
    app.run(debug=True)
