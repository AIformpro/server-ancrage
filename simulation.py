import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Définition des paramètres initiaux
np.random.seed(42)  # Assurer la reproductibilité
iterations = 100  # Nombre de cycles

# Variables clés du projet
params = {
    "coût": np.random.uniform(100, 500),
    "délai": np.random.uniform(10, 50),
    "efficacité": np.random.uniform(50, 100),
    "imprévus": np.random.uniform(0, 20)
}

# Fonction de simulation évolutive
def simulate_project(params, iterations):
    data = []  # Liste pour stocker les valeurs

    for i in range(iterations):
        params["coût"] += np.random.uniform(-5, 5)
        params["délai"] += np.random.uniform(-2, 2)
        params["efficacité"] += np.random.uniform(-1, 1)
        params["imprévus"] += np.random.uniform(-0.5, 0.5)

        # Normalisation pour éviter les valeurs incohérentes
        params["efficacité"] = max(50, min(100, params["efficacité"]))
        params["imprévus"] = max(0, min(20, params["imprévus"]))

        # Ajout des valeurs dans la liste
        data.append([i, params["coût"], params["délai"], params["efficacité"], params["imprévus"]])

    # Retourner le DataFrame
    return pd.DataFrame(data, columns=["Itération", "Coût", "Délai", "Efficacité", "Imprévus"])

# Exécution de la simulation
df_results = simulate_project(params, iterations)

# Vérification des données générées
if df_results is None or df_results.empty:
    print("❌ ERREUR : Le DataFrame est vide !")
else:
    print("✅ Données générées avec succès !")
    print(df_results.head())  # Affiche les 5 premières lignes pour vérification

    # Affichage du graphique
    plt.figure(figsize=(10, 6))
    plt.plot(df_results["Itération"], df_results["Coût"], label="Coût (€)", linestyle="--", marker="o")
    plt.plot(df_results["Itération"], df_results["Délai"], label="Délai (semaines)", linestyle="-.", marker="s")
    plt.plot(df_results["Itération"], df_results["Efficacité"], label="Efficacité (%)", linestyle="-", marker="d")
    plt.plot(df_results["Itération"], df_results["Imprévus"], label="Imprévus (%)", linestyle=":", marker="x")

    plt.xlabel("Itérations")
    plt.ylabel("Valeurs")
    plt.title("Évolution des paramètres du projet")
    plt.legend()
    plt.grid(True)
    plt.show()
