# TaskMate

Application web de gestion de tâches (catégories, priorités, dates limites, statistiques).
Projet de génie logiciel réalisé en binôme.

## Technologies
Python 3, Flask, SQLite, HTML/CSS/JavaScript, pytest, GitHub Actions.

## Installation

```bash
git clone https://github.com/zakaech/taskmate.git
cd taskmate
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

## Lancement

```bash
python run.py
```
Puis ouvrir http://127.0.0.1:5000

## Tests

```bash
pytest -v
```

## Architecture

```
app/
├── models.py        # classe Task
├── repository.py    # accès à la base (pattern Repository)
├── services.py      # logique métier et validation
├── routes.py        # API REST (Flask)
└── static/          # interface web (HTML, CSS, JS)
tests/               # tests unitaires et d'intégration
docs/                # cahier des charges, API, UML
```

## Documentation
- [Cahier des charges](docs/cahier-des-charges.md)
- [Contrat de l'API](docs/api.md)
- [Diagrammes UML](docs/uml.md)

## Workflow Git
`main` (stable) ← `develop` (intégration) ← `feature/*`.
Chaque fonctionnalité passe par une Pull Request relue par l'autre membre du binôme.

## Auteurs
- Zakariae Echaaouer : backend, tests unitaires, CI
- Amine Bounja : interface, tests d'intégration, documentation
