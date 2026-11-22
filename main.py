# ============================================
# ÉTAPE 0 : Importer les librairies
# ============================================
import yfinance as yf          # récupérer les données boursières
import pandas as pd            # manipuler les tableaux
import matplotlib.pyplot as plt  # faire des graphiques

# ============================================
# ÉTAPE 1 : Récupérer les données
# ============================================
# Les 5 actions du portefeuille + le S&P 500 (indice de référence)
tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "MC.PA", "^GSPC"]

# On télécharge uniquement le prix de clôture ("Close")
data = yf.download(tickers, start="2021-01-01", end="2026-01-01")["Close"]

# On affiche les 5 premières lignes pour vérifier
print(data.head())

# ============================================
# ÉTAPE 2 : Rendement total de chaque action
# ============================================
# Formule : (prix final - prix de départ) / prix de départ
prix_debut = data.iloc[0]    # première ligne
prix_fin = data.iloc[-1]     # dernière ligne
rendement = (prix_fin - prix_debut) / prix_debut * 100

print(rendement)

# ============================================
# ÉTAPE 3 : Rendements journaliers
# ============================================
# Variation de chaque jour par rapport à la veille
rendements_jour = data.pct_change()

print(rendements_jour.head())

# ============================================
# ÉTAPE 4 : Volatilité (le risque)
# ============================================
# Volatilité journalière = écart-type des rendements journaliers
volatilite = rendements_jour.std()
print(volatilite)

# Volatilité annuelle en % (252 = jours de bourse par an)
volatilite_annuelle = volatilite * (252 ** 0.5) * 100
print(volatilite_annuelle)

# ============================================
# ÉTAPE 5 : Drawdown (pire chute depuis un sommet)
# ============================================
# Évolution de 1 € investi
cumul = (1 + rendements_jour).cumprod()

# Plus haut atteint jusqu'à chaque jour
sommet = cumul.cummax()

# Baisse par rapport au sommet (en %)
drawdown = (cumul - sommet) / sommet * 100

# Pire chute de chaque action
print(drawdown.min())

# ============================================
# ÉTAPE 6 : Construire le portefeuille
# ============================================
# Les 5 actions (sans le S&P 500)
actions = ["AAPL", "MSFT", "NVDA", "AMZN", "MC.PA"]

# Poids : 20 % chacune
poids = [0.2, 0.2, 0.2, 0.2, 0.2]

# Rendement du portefeuille chaque jour
rendement_portefeuille = (rendements_jour[actions] * poids).sum(axis=1)

# Évolution de 1 € investi dans le portefeuille
cumul_portefeuille = (1 + rendement_portefeuille).cumprod()

print(cumul_portefeuille.tail())

# ============================================
# ÉTAPE 7 : Risque du portefeuille
# ============================================
# Volatilité annuelle du portefeuille en %
vol_portefeuille = rendement_portefeuille.std() * (252 ** 0.5) * 100

# Drawdown du portefeuille en %
sommet_p = cumul_portefeuille.cummax()
drawdown_p = (cumul_portefeuille - sommet_p) / sommet_p * 100

print("Volatilité annuelle :", vol_portefeuille)
print("Pire chute :", drawdown_p.min())

# ============================================
# ÉTAPE 8 : Comparaison avec le S&P 500
# ============================================
# Évolution de 1 € investi dans le S&P 500
cumul_sp500 = (1 + rendements_jour["^GSPC"]).cumprod()

# ============================================
# ÉTAPE 9 : Export CSV (pour Power BI)
# ============================================
# On regroupe les résultats dans un tableau
resultats = pd.DataFrame({
    "Portefeuille": cumul_portefeuille,
    "SP500": cumul_sp500
})

# On enregistre le tableau dans un fichier CSV
resultats.to_csv("resultats.csv")
# Ajout du drawdown du portefeuille dans le tableau des résultats
resultats["Drawdown_Portefeuille"] = drawdown_p
resultats.to_csv("resultats.csv")

# Statistiques de chaque action
stats_actions = pd.DataFrame({
    "Rendement_%": rendement,
    "Volatilite_annuelle_%": volatilite_annuelle,
    "Pire_chute_%": drawdown.min()
})
stats_actions.to_csv("stats_actions.csv")

# Composition du portefeuille
composition = pd.DataFrame({
    "Action": actions,
    "Poids_%": [20, 20, 20, 20, 20]
})
composition.to_csv("composition.csv", index=False)

# Chiffres clés du portefeuille
stats_portefeuille = pd.DataFrame({
    "Mesure": ["Rendement total %", "Volatilite annuelle %", "Pire chute %"],
    "Valeur": [(cumul_portefeuille.iloc[-1] - 1) * 100, vol_portefeuille, drawdown_p.min()]
})
stats_portefeuille.to_csv("stats_portefeuille.csv", index=False)

# ============================================
# ÉTAPE 10 : Graphique
# ============================================
plt.plot(cumul_portefeuille, label="Portefeuille")
plt.plot(cumul_sp500, label="S&P 500")

plt.title("Portefeuille vs S&P 500")
plt.legend()

plt.show()