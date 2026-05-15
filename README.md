This project has been created as part of the 42 curriculum by <cvilbois>

# Cosmic Data — Pydantic Models & Validation

42 Project — Discovering Pydantic through 3 space-themed exercises.

## Project Structure

```
cosmic_data/
├── .gitignore                   Git exclusions — NOT pushed (not required by subject)
├── README.md                    This file — NOT pushed (not required by subject)
├── setup.sh                     Automatic setup — NOT pushed (not required by subject)
│
├── ex0/                         DELIVERABLE — pushed
│   ├── venv/                    ignored by git
│   └── space_station.py         ← pushed
│
├── ex1/                         DELIVERABLE — pushed
│   ├── venv/                    ignored by git
│   └── alien_contact.py         ← pushed
│
├── ex2/                         DELIVERABLE — pushed
│   ├── venv/                    ignored by git
│   └── space_crew.py            ← pushed
│
├── tools/                       utilities (not a deliverable, ignored)
│   ├── data_generator.py
│   ├── data_exporter.py
│   └── generated_data/          created by setup.sh
│
└── tests/                       personal tests (not a deliverable, ignored)
    ├── test_ex0.py
    ├── test_ex1.py
    └── test_ex2.py
```

## Quickstart

```bash
# 1. Create venvs with Python 3.10 and install Pydantic
python3.10 -m venv ex0/venv && ex0/venv/bin/pip install pydantic
python3.10 -m venv ex1/venv && ex1/venv/bin/pip install pydantic
python3.10 -m venv ex2/venv && ex2/venv/bin/pip install pydantic

# 2. Run the official demos
ex0/venv/bin/python ex0/space_station.py
ex1/venv/bin/python ex1/alien_contact.py
ex2/venv/bin/python ex2/space_crew.py

# 3. Run the bonus batch tests (loads the generated JSON data)
ex0/venv/bin/python tests/test_ex0.py
ex1/venv/bin/python tests/test_ex1.py
ex2/venv/bin/python tests/test_ex2.py
```

## Quality Check

For each exercise:

```bash
cd ex0
source venv/bin/activate
pip install flake8 mypy
flake8 space_station.py        # should produce no output
mypy --strict space_station.py # should display "Success: no issues found"
deactivate
cd ..
```

## Git Submission

Only 4 items are versioned (everything else is ignored):

- `.gitignore`
- `ex0/space_station.py`
- `ex1/alien_contact.py`
- `ex2/space_crew.py`

```bash
git add .gitignore ex0/ ex1/ ex2/
git commit -m "Cosmic Data: ex0, ex1, ex2 - Pydantic models & validation"
git push
```

## Pydantic Concepts Covered

| Exercise | Concepts |
|----------|----------|
| ex0 | `BaseModel`, `Field` with constraints, optional types with `str \| None`, `ValidationError` handling |
| ex1 | `Enum` mixed with `str`, `@model_validator(mode='after')`, multiple business rules with `ValueError` |
| ex2 | Nested models (`list[CrewMember]`), cross-field validation, conditional constraints (long missions) |

## Allowed Modules

In accordance with the general subject instructions (III.1 and III.3):

- **Pydantic 2.x** (required for each exercise)
- Python standard library: `datetime`, `enum`, `json`, `csv`, etc.

No additional external modules are used. The `str | None` syntax (PEP 604, Python 3.10+) replaces `Optional[str]` to minimize imports.

---

# Cosmic Data — Modèles & Validation Pydantic

Projet 42 — Découverte de Pydantic à travers 3 exercices spatiaux.

## Arborescence

```
cosmic_data/
├── .gitignore                   Exclusions git — NON poussé (non requis par le sujet)
├── README.md                    Ce fichier — NON poussé (non requis par le sujet)
├── setup.sh                     Setup automatique — NON poussé (non requis par le sujet)
│
├── ex0/                         LIVRABLE — poussé
│   ├── venv/                    ignoré par git
│   └── space_station.py         ← poussé
│
├── ex1/                         LIVRABLE — poussé
│   ├── venv/                    ignoré par git
│   └── alien_contact.py         ← poussé
│
├── ex2/                         LIVRABLE — poussé
│   ├── venv/                    ignoré par git
│   └── space_crew.py            ← poussé
│
├── tools/                       outils (hors livrable, ignorés)
│   ├── data_generator.py
│   ├── data_exporter.py
│   └── generated_data/          créé par setup.sh
│
└── tests/                       tests perso (hors livrable, ignorés)
    ├── test_ex0.py
    ├── test_ex1.py
    └── test_ex2.py
```

## Quickstart

```bash
# 1. Créer les venvs avec Python 3.10 et installer Pydantic
python3.10 -m venv ex0/venv && ex0/venv/bin/pip install pydantic
python3.10 -m venv ex1/venv && ex1/venv/bin/pip install pydantic
python3.10 -m venv ex2/venv && ex2/venv/bin/pip install pydantic

# 2. Lancer les demos officielles
ex0/venv/bin/python ex0/space_station.py
ex1/venv/bin/python ex1/alien_contact.py
ex2/venv/bin/python ex2/space_crew.py

# 3. Lancer les tests batch bonus (chargent les donnees JSON generees)
ex0/venv/bin/python tests/test_ex0.py
ex1/venv/bin/python tests/test_ex1.py
ex2/venv/bin/python tests/test_ex2.py
```

## Vérification qualité

Pour chaque exercice :

```bash
cd ex0
source venv/bin/activate
pip install flake8 mypy
flake8 space_station.py        # doit ne rien afficher
mypy --strict space_station.py # doit afficher "Success: no issues found"
deactivate
cd ..
```

## Soumission Git

Seuls 4 éléments sont versionnés (le reste est ignoré) :

- `.gitignore`
- `ex0/space_station.py`
- `ex1/alien_contact.py`
- `ex2/space_crew.py`

```bash
git add .gitignore ex0/ ex1/ ex2/
git commit -m "Cosmic Data: ex0, ex1, ex2 - Pydantic models & validation"
git push
```

## Concepts Pydantic couverts

| Exercice | Concepts |
|----------|----------|
| ex0 | `BaseModel`, `Field` avec contraintes, types optionnels avec `str \| None`, gestion `ValidationError` |
| ex1 | `Enum` mixée avec `str`, `@model_validator(mode='after')`, règles métier multiples avec `ValueError` |
| ex2 | Modèles imbriqués (`list[CrewMember]`), validation cross-fields, contraintes conditionnelles (long missions) |

## Modules autorisés

Conformément aux instructions générales du sujet (III.1 et III.3) :

- **Pydantic 2.x** (requis pour chaque exercice)
- Bibliothèque standard Python : `datetime`, `enum`, `json`, `csv`, etc.

Aucun module externe supplémentaire n'est utilisé. La syntaxe `str | None` (PEP 604, Python 3.10+) remplace `Optional[str]` pour minimiser les imports.
