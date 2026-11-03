# Contrat de l'API

Format des échanges : JSON.

## Objet Task
```json
{
  "id": 1,
  "title": "Réviser le cours",
  "category": "Ecole",
  "priority": "high",
  "due_date": "2026-11-15",
  "done": false
}
```

## Routes

| Méthode | Route | Description | Réponse |
|---------|-------|-------------|---------|
| GET | `/tasks` | Liste des tâches | 200 + liste |
| POST | `/tasks` | Crée une tâche | 201 + tâche |
| GET | `/tasks/<id>` | Détail d'une tâche | 200 / 404 |
| PUT | `/tasks/<id>` | Modifie une tâche (champs partiels) | 200 / 400 / 404 |
| DELETE | `/tasks/<id>` | Supprime une tâche | 204 / 404 |
| GET | `/tasks/stats` | Statistiques | 200 |

## Paramètres de `GET /tasks`
- `category=Ecole` : filtre par catégorie
- `priority=high` : filtre par priorité (`low`, `medium`, `high`)
- `done=true` ou `done=false` : filtre par statut
- `sort=due_date` : tri par date limite (les tâches sans date en dernier)

## Corps de `POST /tasks`
```json
{ "title": "Obligatoire", "category": "Optionnel", "priority": "medium", "due_date": "2026-11-15" }
```

## Statistiques
```json
{ "total": 5, "done": 2, "remaining": 3 }
```

## Erreurs
```json
{ "error": "Le titre est obligatoire" }
```
Codes : `400` données invalides, `404` tâche introuvable.