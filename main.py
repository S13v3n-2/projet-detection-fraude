from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os

os.getcwd()
# Initialisation de l'API
app = FastAPI(
    title="Système de Détection de Fraude et d'Arnaque",
    description="API permettant de tester 4 modèles de détection de fraude (V1, V2, V3, V4)."
)

# Chargement des modèles au démarrage de l'API
# On renomme les modèles en V1, V2, V3, V4
models = {}
try:
    models["V1"] = joblib.load("Models/model_fraude_xgboost_final_2.pkl")
    models["V2"] = joblib.load("Models/model_rf_final.pkl")
    models["V3"] = joblib.load("Models/model_lr_final.pkl")
    models["V4"] = joblib.load("Models/model_unsup_final.pkl")
    print("Tous les modèles ont été chargés avec succès.")
except Exception as e:
    print(f"Erreur lors du chargement des modèles : {e}")

# Définition du schéma des données d'entrée
class Transaction(BaseModel):
    amt: float              # Montant de la transaction
    zip: int                # Code postal
    city_pop: int           # Population de la ville
    age_at_transaction: int # Age calculé au moment de la transaction
    unix_time: int          # Timestamp de la transaction
    state: str              # État (ex: 'NY')
    city: str               # Ville
    gender: str             # Genre ('M' ou 'F')
    category: str           # Catégorie d'achat
    merchant: str           # Nom du marchand
    job: str                # Métier du client

# Fonction utilitaire pour faire une prédiction, elle est réutilisée par toutes les routes
def make_prediction(model_name: str, data: Transaction):
    """
    Fonction qui effectue la prédiction pour un modèle donné.
    
    Paramètres :
    - model_name : nom du modèle (V1, V2, V3 ou V4)
    - data : objet Transaction contenant les données de la transaction
    
    Retourne :
    - Un dictionnaire avec le modèle utilisé, le code de prédiction et le résultat
    """
    # Vérifier si le modèle existe dans notre dictionnaire
    if model_name not in models:
        raise HTTPException(status_code=404, detail=f"Modèle {model_name} non trouvé.")
    
    # Convertir l'objet Transaction en DataFrame
    # .dict() transforme l'objet Pydantic en dictionnaire Python
    # pd.DataFrame([...]) crée un DataFrame avec une seule ligne
    input_df = pd.DataFrame([data.dict()])

    # Récupérer le modèle depuis le dictionnaire
    model = models[model_name]
    
    try:
        # Faire la prédiction avec le modèle
        # .predict() retourne un array numpy, on prend le premier élément [0]
        prediction = model.predict(input_df)[0]
        
        # Logique spécifique pour le modèle V4 (Isolation Forest - non supervisé)
        if model_name == "V4":
            # Pour Isolation Forest : 1 = anomalie, 0 = normal
            resultat = "Anomalie détectée" if prediction == 1 else "Transaction normale"
        else:
            # Pour les modèles supervisés V1, V2, V3
            # 0 = Normal, 1 = Vraie Fraude, 2 = Tentative d'arnaque client
            mapping = {0: "Normal", 1: "Vraie Fraude", 2: "Tentative d'arnaque client"}
            resultat = mapping.get(int(prediction), f"Classe {prediction}")

        return {
            "model_used": model_name,
            "prediction_code": int(prediction),
            "resultat": resultat
        }
    
    except Exception as e:
        # Afficher l'erreur dans la console pour le débogage
        print(f"DEBUG Erreur avec {model_name} : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {str(e)}")

# Routes de prédiction - Une route dédiée par modèle

@app.post("/predict/v1")
async def predict_v1(data: Transaction):
    """
    Route pour le modèle V1 (XGBoost).
    Modèle supervisé pour détecter les fraudes et arnaques.
    """
    return make_prediction("V1", data)

@app.post("/predict/v2")
async def predict_v2(data: Transaction):
    """
    Route pour le modèle V2 (Random Forest).
    Modèle supervisé pour détecter les fraudes et arnaques.
    """
    return make_prediction("V2", data)

@app.post("/predict/v3")
async def predict_v3(data: Transaction):
    """
    Route pour le modèle V3 (Logistic Regression).
    Modèle supervisé pour détecter les fraudes et arnaques.
    """
    return make_prediction("V3", data)

@app.post("/predict/v4")
async def predict_v4(data: Transaction):
    """
    Route pour le modèle V4 (Isolation Forest).
    Modèle non supervisé pour détecter les anomalies.
    """
    return make_prediction("V4", data)

# Route d'accueil
@app.get("/")
async def root():
    return {
        "message": "API de détection de fraude opérationnelle",
        "models_disponibles": {
            "V1": "XGBoost (supervisé)",
            "V2": "Random Forest (supervisé)",
            "V3": "Logistic Regression (supervisé)",
            "V4": "Isolation Forest (non supervisé)"
        },
        "routes": ["/predict/v1", "/predict/v2", "/predict/v3", "/predict/v4"],
        "documentation": "/docs"
    }