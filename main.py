from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os

os.getcwd()
# 1. Initialisation de l'API
app = FastAPI(
    title="Système de Détection de Fraude et d'Arnaque",
    description="API permettant de tester 3 modèles supervisés et 1 modèle non-supervisé."
)

# 2. Chargement des modèles au démarrage de l'API
# Assure-toi que tes fichiers .pkl sont bien dans le dossier /Models
models = {}
# Modification de models en Models pour correspond au nom du dossier
try:
    models["xgboost"] = joblib.load("Models/model_fraude_xgboost_final_2.pkl")
    models["random_forest"] = joblib.load("Models/model_rf_final.pkl")
    models["logistic_regression"] = joblib.load("Models/model_lr_final.pkl")
    models["isolation_forest"] = joblib.load("Models/model_unsup_final.pkl")
    print(" Tous les modèles ont été chargés.")
except Exception as e:
    print(f"Erreur lors du chargement des modèles : {e}")

# 3. Définition du schéma des données d'entrée
# Ces champs correspondent aux caractéristiques utilisées dans tes notebooks
class Transaction(BaseModel):
    amt: float              # Montant de la transaction
    zip: int                # Code postal
    city_pop: int           # Population de la ville
    age_at_transaction: int # Âge calculé au moment de la transaction
    unix_time: int          # Timestamp de la transaction
    state: str              # État (ex: 'NY')
    city: str               # Ville
    gender: str             # Genre ('M' ou 'F')
    category: str           # Catégorie d'achat
    merchant: str           # Nom du marchand
    job: str                # Métier du client

# 4. Route de prédiction
@app.post("/predict/{model_name}")
async def predict(model_name: str, data: Transaction):
    """
    Model possible : xgboost, random_forest, logistic_regression ou isolation_forest
    """
    # Vérifier si le modèle demandé est chargé
    if model_name not in models:
        raise HTTPException(status_code=404, detail="Modèle non trouvé. Utilisez : xgboost, random_forest, logistic_regression ou isolation_forest.")
    
    # Transformer les données reçues en DataFrame (format attendu par tes Pipelines)
    input_df = pd.DataFrame([data.dict()])

    # Sélection du modèle
    model = models[model_name]
    
    try:
        # Faire la prédiction
        prediction = model.predict(input_df)[0]
        
        # Logique spécifique pour le modèle non-supervisé (Isolation Forest)
        if model_name == "isolation_forest":
            # Dans ton notebook IF, -1 est une anomalie et 1 est normal. 
            # Si tu as fait le mapping {-1:1, 1:0}, alors 1 = anomalie.
            resultat = "Anomalie détectée" if prediction == 1 else "Transaction normale"
        else:
            # Pour les modèles supervisés (0: Normal, 1: Fraude, 2: Arnaque Client)
            mapping = {0: "Normal", 1: "Vraie Fraude", 2: "Tentative d'arnaque client"}
            resultat = mapping.get(int(prediction), f"Classe {prediction}")

        return {
            "model_used": model_name,
            "prediction_code": int(prediction),
            "resultat": resultat
        }
    
    except Exception as e:
        # Ligne de debug : Afficher l'erreur exacte dans le terminal
        print(f"DEBUG Erreur : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {str(e)}")

# Route d'accueil
@app.get("/")
async def root():
    return {"message": "API de détection de fraude opérationnelle. Allez sur /docs pour tester."}