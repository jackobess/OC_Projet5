"""
models_db.py — Modèles ORM SQLAlchemy (tables de logging des prédictions).

  - prediction_inputs  : features envoyées au modèle (loggué AVANT inférence)
  - prediction_outputs : résultat du modèle (loggué APRÈS inférence, FK → inputs)
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from app.database import Base


class PredictionInput(Base):
    __tablename__ = "prediction_inputs"

    id        = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now(datetime.timezone.utc))
    source = Column(String(20), nullable=True)  # "local", "HF_Prod", etc.

    age                                       = Column(Integer)
    genre                                     = Column(String(1))
    niveau_education                          = Column(Integer)
    statut_marital                            = Column(String(20))
    poste                                     = Column(String(50))
    domaine_etude                             = Column(String(50))
    frequence_deplacement                     = Column(String(20))
    distance_domicile_travail                 = Column(Integer)
    nb_formations_suivies                     = Column(Integer)
    nombre_participation_pee                  = Column(Integer)
    augmentation_salaire_prec_pct             = Column(Integer)
    heure_supplementaires                     = Column(Integer)
    note_evaluation_actuelle                  = Column(Integer)
    satisfaction_employee_equilibre_pro_perso = Column(Integer)
    satisfaction_employee_equipe              = Column(Integer)
    satisfaction_employee_nature_travail      = Column(Integer)
    niveau_hierarchique_poste                 = Column(Integer)
    note_evaluation_precedente                = Column(Integer)
    satisfaction_employee_environnement       = Column(Integer)
    annee_experience_totale                   = Column(Integer)
    nombre_experiences_precedentes            = Column(Integer)
    revenu_mensuel                            = Column(Integer)
    annees_dans_le_poste_actuel               = Column(Integer)
    annees_dans_l_entreprise                  = Column(Integer)
    annees_depuis_la_derniere_promotion       = Column(Integer)
    annes_sous_responsable_actuel             = Column(Integer)


class PredictionOutput(Base):
    __tablename__ = "prediction_outputs"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    timestamp     = Column(DateTime, default=datetime.utcnow)
    input_id      = Column(Integer, ForeignKey("prediction_inputs.id"), nullable=False)
    prediction    = Column(Integer,      nullable=True)
    probabilite   = Column(Float,        nullable=True)
    statut        = Column(String(10),   default="success")
    error_code    = Column(String(50),   nullable=True)
    error_message = Column(String(255),  nullable=True)
