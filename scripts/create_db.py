# scripts/create_db.py
from app.database import engine, Base
from app.models_db import PredictionInput, PredictionOutput

Base.metadata.create_all(bind=engine)
print("Tables créées.")
