---
title: OC Projet 5
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

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

## Standards de code et CI/CD

- Branches nommées `feature/xxx`, `fix/xxx`, `test/xxx`
- Commits au format `type: description` (ex: `feat:`, `fix:`, `docs:`, `ci:`)
- Tout code mergé dans `main` passe par une Pull Request
- Les tests sont automatiquement lancés via GitHub Actions à chaque push
- Couverture de tests mesurée avec pytest-cov