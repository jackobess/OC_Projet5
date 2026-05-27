from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
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
    age:                                    int = Field(default=35, description="Âge de l'employé (entier positif)")
    genre:                                  str = Field(default="M", description="'M' ou 'F'")
    niveau_education:                       int = Field(default=3, description="Niveau d'éducation (1 à 5)")
    statut_marital:                         str = Field(default="Marié(e)", description="'Marié(e)', 'Célibataire' ou 'Divorcé(e)'")
    poste:                                  str = Field(default="Cadre Commercial", description="Poste occupé (ex: Consultant, Manager, ...)")
    domaine_etude:                          str = Field(default="Infra & Cloud", description="Domaine d'étude (ex: Marketing, Autre, ...)")
    frequence_deplacement:                  str = Field(default="Occasionnel", description="'Aucun', 'Occasionnel' ou 'Frequent'")
    distance_domicile_travail:              int = Field(default=10, description="Distance domicile/travail en km")
    nb_formations_suivies:                  int = Field(default=3, description="Nombre de formations suivies")
    nombre_participation_pee:               int = Field(default=1, description="Nombre de participations au PEE")
    augmentation_salaire_prec_pct:          int = Field(default=15, description="Augmentation salariale précédente en %")
    heure_supplementaires:                  int = Field(default=0, description="Fait des heures supplémentaires : 0 (non) ou 1 (oui)")
    note_evaluation_actuelle:               int = Field(default=3, description="Note d'évaluation actuelle (1 à 4))")
    satisfaction_employee_equilibre_pro_perso: int = Field(default=3, description="Satisfaction équilibre pro/perso (1 à 4)")
    satisfaction_employee_equipe:           int = Field(default=3, description="Satisfaction équipe (1 à 4)")
    satisfaction_employee_nature_travail:   int = Field(default=3, description="Satisfaction nature du travail (1 à 4)")
    niveau_hierarchique_poste:              int = Field(default=2, description="Niveau hiérarchique du poste (1 à 5)")
    note_evaluation_precedente:             int = Field(default=3, description="Note d'évaluation précédente (1 à 4)")
    satisfaction_employee_environnement:    int = Field(default=3, description="Satisfaction environnement de travail (1 à 4)")
    annee_experience_totale:                int = Field(default=10, description="Années d'expérience totale")
    nombre_experiences_precedentes:         int = Field(default=2, description="Nombre d'expériences précédentes")
    revenu_mensuel:                         int = Field(default=5000, description="Revenu mensuel en euros")
    annees_dans_le_poste_actuel:            int = Field(default=3, description="Années dans le poste actuel")
    annees_dans_l_entreprise:               int = Field(default=5, description="Années dans l'entreprise")
    annees_depuis_la_derniere_promotion:    int = Field(default=2, description="Années depuis la dernière promotion")
    annes_sous_responsable_actuel:          int = Field(default=3, description="Années sous le responsable actuel")


    @field_validator('genre')
    def genre_valide(cls, v):
        if v not in ['M', 'F']:
            raise ValueError("genre doit être 'M' ou 'F'")
        return v

    @field_validator('frequence_deplacement')
    def deplacement_valide(cls, v):
        if v not in ['Aucun', 'Occasionnel', 'Frequent']:
            raise ValueError("doit être 'Aucun', 'Occasionnel' ou 'Frequent'")
        return v

    @field_validator('statut_marital')
    def statut_valide(cls, v):
        if v not in ['Marié(e)', 'Célibataire', 'Divorcé(e)']:
            raise ValueError("statut_marital invalide")
        return v

    @field_validator('heure_supplementaires')
    def heures_sup_valide(cls, v):
        if v not in [0, 1]:
            raise ValueError("heure_supplementaires doit être 0 (non) ou 1 (oui)")
        return v

    @field_validator(
        'satisfaction_employee_equilibre_pro_perso',
        'satisfaction_employee_equipe',
        'satisfaction_employee_nature_travail',
        'satisfaction_employee_environnement',
        'note_evaluation_precedente',
        'note_evaluation_actuelle'
    )
    def satisfaction_valide(cls, v):
        if v not in [1, 2, 3, 4]:
            raise ValueError("doit être entre 1 et 4")
        return v

    @field_validator('niveau_education')
    def education_valide(cls, v):
        if v not in [1, 2, 3, 4, 5]:
            raise ValueError("niveau_education doit être entre 1 et 5")
        return v

    @field_validator('niveau_hierarchique_poste')
    def hierarchie_valide(cls, v):
        if v not in [1, 2, 3, 4, 5]:
            raise ValueError("niveau_hierarchique_poste doit être entre 1 et 5")
        return v
    @field_validator('poste')
    
    def poste_valide(cls, v):
        postes = [
            'Assistant de Direction', 'Cadre Commercial', 'Consultant',
            'Directeur Technique', 'Manager', 'Représentant Commercial',
            'Ressources Humaines', 'Senior Manager', 'Tech Lead'
        ]
        if v not in postes:
            raise ValueError(f"poste invalide, valeurs acceptées : {postes}")
        return v

    @field_validator('domaine_etude')
    def domaine_valide(cls, v):
        domaines = [
            'Autre', 'Entrepreunariat', 'Infra & Cloud',
            'Marketing', 'Ressources Humaines', 'Transformation Digitale'
        ]
        if v not in domaines:
            raise ValueError(f"domaine_etude invalide, valeurs acceptées : {domaines}")
        return v


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