---
# Config d'affichage Hugging Face Spaces
title: OC Projet 5
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# OC Projet 5 - Déploiement d'un modèle de Machine Learning

API de prédiction d'attrition RH déployée sur Hugging Face Spaces, avec logging dans PostgreSQL (Neon) et pipeline CI/CD GitHub Actions.

---

## Stack technique

| Composant | Technologie |
|---|---|
| API | FastAPI + Pydantic |
| Modèle | Scikit-learn / LogisticRegression (P4) |
| BDD | PostgreSQL + SQLAlchemy |
| BDD cloud | Neon (PostgreSQL serverless) |
| Tests | Pytest + pytest-cov |
| CI/CD | GitHub Actions |
| Déploiement | Hugging Face Spaces (Docker) |

---

## Architecture

![Architecture](docs/archi.jpg)

---

## Installation

```bash
# Cloner le repo
git clone https://github.com/jackobess/OC_Projet5.git

cd OC_Projet5
pip install -r requirements.txt
```

---

## Configuration locale

Créer un fichier `.env` à la racine (=> `.gitignore`) :

```env
DATABASE_URL=postgresql://user:password@localhost:5432/oc_projet5
API_ENV=local
PYTHONPATH=.
```

Pour logguer sur la base Neon (cloud) remplacer l'url DATABASE_URL avec l'url du server 

---

## Lancement local (pour tests)

```bash
conda activate oc_projet5
uvicorn app.main:app --reload
```

API disponible sur `http://127.0.0.1:8000`  
Documentation Swagger : `http://127.0.0.1:8000/docs`

---

## API - Endpoints

### `GET /`
Vérifie que l'API est opérationnelle.

```json
{"message": "API opérationnelle"}
```

### `GET /health`
Retourne le statut, la version et l'environnement.

```json
{"status": "ok", "version": "1.0.0", "environment": "HF_Prod/local"}
```

### `POST /predict`
Prédit le risque d'attrition d'un employé.

**Exemple de requête :**
```bash
curl -X POST https://jackobess-oc-projet5.hf.space/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "genre": "M",
    "niveau_education": 3,
    "statut_marital": "Marié(e)",
    "poste": "Cadre Commercial",
    "domaine_etude": "Infra & Cloud",
    "frequence_deplacement": "Occasionnel",
    "distance_domicile_travail": 10,
    "nb_formations_suivies": 3,
    "nombre_participation_pee": 1,
    "augmentation_salaire_prec_pct": 15,
    "heure_supplementaires": 0,
    "note_evaluation_actuelle": 3,
    "satisfaction_employee_equilibre_pro_perso": 3,
    "satisfaction_employee_equipe": 3,
    "satisfaction_employee_nature_travail": 3,
    "niveau_hierarchique_poste": 2,
    "note_evaluation_precedente": 3,
    "satisfaction_employee_environnement": 3,
    "annee_experience_totale": 10,
    "nombre_experiences_precedentes": 2,
    "revenu_mensuel": 5000,
    "annees_dans_le_poste_actuel": 3,
    "annees_dans_l_entreprise": 5,
    "annees_depuis_la_derniere_promotion": 2,
    "annes_sous_responsable_actuel": 3
  }'
```

**Réponse :**
```json
{
  "prediction": 0,
  "label": "En poste",
  "probabilite_attrition": 0.2445
}
```

**Valeurs acceptées :**
- genre : `"M"` ou `"F"`
- statut_marital : `"Marié(e)"`, `"Célibataire"`, `"Divorcé(e)"`
- frequence_deplacement : `"Aucun"`, `"Occasionnel"`, `"Frequent"`
- heure_supplementaires : `0` ou `1`
- niveau_education, niveau_hierarchique_poste : `1` à `5`
- Satisfactions et notes : `1` à `4`

---

## Base de données

### Tables sources (dataset d'entraînement)
| Table | Description |
|---|---|
| `sirh` | Données RH brutes (1470 employés) |
| `eval` | Évaluations et satisfactions |
| `sondage` | Sondage RH, target `a_quitte_l_entreprise` |

### Tables de logging (interactions API)
| Table | Description |
|---|---|
| `prediction_inputs` | Features envoyées au modèle (loggué avant inférence) |
| `prediction_outputs` | Résultat + statut + erreurs (loggué après inférence, FK → inputs) |

Les tables de logging sont créées (si besoin) automatiquement au démarrage de l'API (`Base.metadata.create_all`), voir `app.models_db.py`.

---

## Tests automatiques (pytest/cov)

```bash
# Lancer les tests (simulation CI)
PYTHONPATH=. CI=true pytest tests/ -v --cov=app --cov-report=html

# Voir le rapport de couverture
start htmlcov/index.html
```

Couverture actuelle : **91%**

| Fichier | Couverture |
|---|---|
| `app/__version__.py` | 100% |
| `app/models_db.py` | 100% |
| `app/main.py` | 94% |
| `app/encoder.py` | 82% |
| `app/database.py` | 71% |

---

## CI/CD

À chaque push sur `main` ou `feature/**` :
1. **Test** — pytest + pytest-cov sur GitHub Actions
2. **Deploy** — push automatique vers Hugging Face Spaces  
  *inclure [skip-deploy] dans le message du commit pour pusher sans deployer*

En CI, la connexion BDD est mockée (`MagicMock`) => aucune dépendance réseau ni polution de la base de prod (Neon)

---

## Hugging Face Spaces

API en production : **https://jackobess-oc-projet5.hf.space**  
Documentation Swagger : **https://jackobess-oc-projet5.hf.space/docs**

Variables secrètes (DATABASE_URL et API_ENV) sont configurés dans HF Spaces Settings :

---

## Sécurité

- Credentials exclusivement via variables d'environnement (DATABASE_URL, HF_TOKEN) stockés dans `.env` en local ou dans ***secrets***
 pour  GitHub & HF
- `.env` dans `.gitignore` — jamais commité
- Aucun credential en dur dans le code

---

## Conventions

- Branches : `feature/xxx`, `fix/xxx`, `test/xxx`
- Commits : `feat:`, `fix:`, `docs:`, `ci:`, `chore:`
- Versions gérées via `app/__version__.py` et tags Git (ex: `v1.0.0`)
