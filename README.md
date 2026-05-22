# OC_Projet5 - Déploiement d'un modèle de Machine Learning

## Description
API de prédiction de consommation énergétique de bâtiments (Projet 3 - OpenClassrooms).

## Stack technique
- FastAPI
- PostgreSQL / SQLAlchemy
- Scikit-learn / XGBoost
- Pytest
- GitHub Actions (CI/CD)

## Installation
```bash
pip install -r requirements.txt
```

## Lancement
```bash
uvicorn app.main:app --reload
```
## Conventions de branches
- `feature/xxx` — nouvelle fonctionnalité
- `fix/xxx` — correction de bug  
- `test/xxx` — ajout de tests