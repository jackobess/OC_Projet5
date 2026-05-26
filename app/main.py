from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from app.encoder import FeatureEncoder  # noqa - nécessaire pour charger le joblib

# Chargement du modèle
MODEL_PATH = Path("models/pipeline_p4.joblib")
model = joblib.load(MODEL_PATH)

app = FastAPI(
    title="OC Projet 5 - ML Model API",
    description="API de prédiction d'attrition RH (Projet 4 - OpenClassrooms)",
    version="0.1.0"
)

class EmployeeFeatures(BaseModel):
    age: int = 35
    genre: str = "M"
    niveau_education: int = 3
    statut_marital: str = "Marié(e)"
    poste: str = "Cadre Commercial"
    domaine_etude: str = "Infra & Cloud"
    frequence_deplacement: str = "Occasionnel"
    distance_domicile_travail: int = 10
    nb_formations_suivies: int = 3
    nombre_participation_pee: int = 1
    augmentation_salaire_prec_pct: int = 15
    heure_supplementaires: int = 0
    note_evaluation_actuelle: int = 3
    satisfaction_employee_equilibre_pro_perso: int = 3
    satisfaction_employee_equipe: int = 3
    satisfaction_employee_nature_travail: int = 3
    niveau_hierarchique_poste: int = 2
    note_evaluation_precedente: int = 3
    satisfaction_employee_environnement: int = 3
    annee_experience_totale: int = 10
    nombre_experiences_precedentes: int = 2
    revenu_mensuel: int = 5000
    annees_dans_le_poste_actuel: int = 3
    annees_dans_l_entreprise: int = 5
    annees_depuis_la_derniere_promotion: int = 2
    annes_sous_responsable_actuel: int = 3

@app.get("/")
def root():
    return {"message": "API opérationnelle"}

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}

@app.post("/predict")
def predict(data: EmployeeFeatures):
    df = pd.DataFrame([data.model_dump()])
    
    prediction = model.predict(df)[0]
    proba = model.predict_proba(df)[0]
    
    return {
        "prediction": int(prediction),
        "label": "A quitté" if prediction == 1 else "En poste",
        "probabilite_attrition": round(float(proba[1]), 4)
    }