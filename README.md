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
1. **Apprentissage Supervise :** Classification multiclasse sur données déséquilibrées (SMOTE) pour identifier les fraudes connues et les tentatives d'arnaque.
2. **Apprentissage Non-Supervise :** Détection d'anomalies via Isolation Forest pour identifier des comportements atypiques ou des fraudes émergentes.
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

## 4. Performances des Modeles
Les modèles ont été évalués principalement sur le **PR-AUC** (Precision-Recall Area Under Curve), car il s'agit de la métrique la plus fiable pour les datasets présentant un fort déséquilibre de classes.

| Modele | Accuracy | F1-Score | ROC-AUC | PR-AUC |
| :--- | :--- | :--- | :--- | :--- |
| **V1 : XGBoost (Optimise)** | 0.9953 | 0.6764 | 0.9964 | **0.8294** |
| **V2 : Random Forest** | 0.9907 | 0.5170 | 0.9916 | **0.7316** |
| **V3 : Logistic Regression** | 0.9486 | 0.1468 | 0.8574 | **0.2028** |

## 5. Structure du Projet

├── Models/                         # Fichiers .pkl des modèles (V1, V2, V3, V4)  
├── eda/                            # Notebooks et classes de transformation  
│   ├── transformers_ML.py          # Script de traitement des dates (Feature Engineering)  
│   ├── Model_non_superviser.ipynb  # Création du modèle non supervisé (V4)  
│   └── Model_superviser.ipynb      # Création des modèles supervisés (V1, V2, V3)  
├── main.py                         # Point d'entrée FastAPI  
├── requirements.txt                # Dépendances (FastAPI, XGBoost, Scikit-learn)  
└── Dockerfile                      # Configuration pour le déploiement Docker

## 6. Utilisation du projet
### Prérequis
* Python 3.10+
* Docker (pour le déploiement par conteneur)
### Test du projet via docker
Le projet est disponible sous forme d'image conteneurisée pour garantir la portabilite et une isolation totale de l'environnement :
* ```docker run -p 8000:8000 stevenpro9/api-fraude:v1```
* Pour accéder a l'api ```http://127.0.0.1:8000/```
* Pour voir les routes de l'api et le testé ```http://127.0.0.1:8000/docs```

### Voir les fichiers du projet 
* Faire un git clone du projet ```git clone https://github.com/S13v3n-2/projet-detection-fraude.git```
* ```cd projet-detection-fraude```
* Installer les dépendances ```pip install -r requirements.txt```
* Lancer l'api : ```uvicorn main:app --reload```
* ULR pour voir les routes de l'api ```http://127.0.0.1:8000/docs```

### Format des Donnees (API)
L'API accepte des objets JSON representant une transaction. Seules les colonnes suivantes sont obligatoires pour la prediction :

| Champ | Type | Description |
|------|------|-------------|
| amt | float | Montant de la transaction |
| category | str | Catégorie de l'achat |
| gender | str | Genre du client (M/F) |
| city_pop | int | Population de la ville |
| trans_date_trans_time | str | Date et heure de la transaction |
| job | str | Profession du client |
| city | str | Ville de la transaction |
| zip | int | Code postal |
| state | str | État |
| merchant | str | Nom du marchand |
| dob | str | Date de naissance du client |

### Interpretation des Resultats
* V1, V2, V3 (Supervises) : Retournent un code (0: Normal, 1: Fraude, 2: Arnaque).
* V4 (Non-Supervise) : Retourne un diagnostic d'anomalie ("Anomalie detectee" ou "Transaction normale").