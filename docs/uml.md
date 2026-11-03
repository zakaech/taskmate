# Diagrammes UML

GitHub affiche automatiquement les diagrammes Mermaid ci-dessous.

## Diagramme de cas d'utilisation

```mermaid
flowchart LR
    U([Utilisateur])
    U --> UC1(Créer une tâche)
    U --> UC2(Modifier une tâche)
    U --> UC3(Supprimer une tâche)
    U --> UC4(Terminer une tâche)
    U --> UC5(Filtrer les tâches)
    U --> UC6(Trier par date limite)
    U --> UC7(Consulter les statistiques)
```

## Diagramme de classes

```mermaid
classDiagram
    class Task {
        +int id
        +str title
        +str category
        +str priority
        +str due_date
        +bool done
        +to_dict()
    }
    class TaskRepository {
        +init_db()
        +add(task)
        +get(task_id)
        +list(category, priority, done, sort_by_due)
        +update(task)
        +delete(task_id)
    }
    class TaskService {
        +create_task(data)
        +get_task(task_id)
        +list_tasks(...)
        +update_task(task_id, data)
        +delete_task(task_id)
        +stats()
    }
    class Routes {
        +list_tasks()
        +create_task()
        +update_task(id)
        +delete_task(id)
        +stats()
    }
    Routes --> TaskService
    TaskService --> TaskRepository
    TaskRepository --> Task
```

## Diagramme de séquence : création d'une tâche

```mermaid
sequenceDiagram
    actor U as Utilisateur
    participant UI as Interface (app.js)
    participant R as Routes (Flask)
    participant S as TaskService
    participant P as TaskRepository
    participant DB as SQLite

    U->>UI: Remplit le formulaire
    UI->>R: POST /tasks (JSON)
    R->>S: create_task(data)
    S->>S: Valide titre, priorité, date
    S->>P: add(task)
    P->>DB: INSERT INTO tasks
    DB-->>P: id
    P-->>S: task
    S-->>R: task
    R-->>UI: 201 + JSON
    UI-->>U: Affiche la nouvelle tâche