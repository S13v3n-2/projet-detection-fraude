# FraudGuard : Optimisation du profit par la détection prédictive

## 1. Contexte Métier
L'industrie bancaire évolue d'une gestion de la fraude "passive" (remboursement après sinistre) vers une **posture active** (prévention en temps réel). 

L'enjeu :
* **Marge Nette :** Réduire les pertes directes liées aux transactions frauduleuses.
* **Conformité (Compliance) :** Répondre aux exigences de l'**ACPR** en France, qui sanctionne la "négligence structurelle" 
et l'incapacité à maintenir des systèmes de surveillance de blanchiment d'argent ou fraude robustes.
* **Réputation :** Garantir la confiance des clients en sécurisant leurs transactions sans dégrader l'expérience utilisateur.

## 2. Objectif du Projet
Développer des modèles d'apprentissage **supervisé** capable d'identifier les transactions frauduleuses avant leur compensation. 
* **Type de problème :** Classification binaire (Déséquilibrée).
* **Métriques clés :** Recall (pour la conformité) et F1-Score (pour l'équilibre entre détection et faux blocages).

Développer des modèles d'apprentissage **non-supervisé**
* Objectif : Détecter les fraudes émergentes et les comportements atypiques qui n'ont pas encore de précédents dans les données historiques.
* Valeur ajoutée : Permet de passer d'une simple détection de règles à une véritable analyse comportementale dynamique, 
identifiant des transactions "anormales" par rapport aux habitudes spécifiques d'un client.

## 3. Analyse des Données (Dataset)
Le projet utilise le dataset [Credit Card Fraud Detection](https://www.kaggle.com/datasets/kartik2112/fraud-detection) simulant des transactions réelles.

* **Volume :** ~1,85 million de transactions.
* **Variables clés :**
    * `amt` : Montant de la transaction.
    * `zip`, `lat`, `long` : Données géographiques pour l'analyse de distance.
    * `category` : Type de dépense (voyage, alimentation, etc.).
    * `is_fraud` : Variable cible (0 ou 1).
* **Contrainte majeure :** Le jeu de données présente un fort déséquilibre de classes (moins de 1% de fraudes), nécessitant des techniques de rééchantillonnage (SMOTE) ou des fonctions de coût adaptées.

## 4. Structure du Dépôt
* `notebooks/` : Exploration des données (EDA) et modélisation.
* `data/` : Fichier CSV du jeu de données.
* `src/` : Scripts de prétraitement et de scoring.
* `Models/` : Contient les modéles non-supervisé et superviser (fichier.plk)
* `main.py` : Contient le code de l'api

## 5. Utilisation du projet
1. Faire un git clone du projet
2. Installer les dépendances ```pip install -r requirements.txt```
3. Lancer l'api : ```uvicorn main:app --reload```
4. ULR pour voir les routes de l'api ```http://127.0.0.1:8000/docs```