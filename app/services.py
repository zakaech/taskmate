from datetime import date

from .models import Task

PRIORITIES = ("low", "medium", "high")


class ValidationError(ValueError):
    """Données invalides envoyées par l'utilisateur."""


class NotFoundError(LookupError):
    """La tâche demandée n'existe pas."""


class TaskService:
    """Logique métier : validation des données + règles de gestion."""

    def __init__(self, repository):
        self.repo = repository

    @staticmethod
    def _check_priority(priority):
        if priority not in PRIORITIES:
            raise ValidationError("La priorité doit être : low, medium ou high")

    @staticmethod
    def _check_date(due_date):
        if due_date:
            try:
                date.fromisoformat(due_date)
            except ValueError:
                raise ValidationError("La date doit être au format AAAA-MM-JJ")

    def create_task(self, data):
        title = (data.get("title") or "").strip()
        if not title:
            raise ValidationError("Le titre est obligatoire")
        priority = data.get("priority", "medium")
        self._check_priority(priority)
        due_date = data.get("due_date") or None
        self._check_date(due_date)
        task = Task(
            title=title,
            category=(data.get("category") or "General").strip(),
            priority=priority,
            due_date=due_date,
        )
        return self.repo.add(task)

    def get_task(self, task_id):
        task = self.repo.get(task_id)
        if task is None:
            raise NotFoundError(f"Tâche {task_id} introuvable")
        return task

    def list_tasks(self, category=None, priority=None, done=None, sort=None):
        return self.repo.list(
            category=category,
            priority=priority,
            done=done,
            sort_by_due=(sort == "due_date"),
        )

    def update_task(self, task_id, data):
        task = self.get_task(task_id)
        if "title" in data:
            title = (data["title"] or "").strip()
            if not title:
                raise ValidationError("Le titre est obligatoire")
            task.title = title
        if "category" in data:
            task.category = (data["category"] or "General").strip()
        if "priority" in data:
            self._check_priority(data["priority"])
            task.priority = data["priority"]
        if "due_date" in data:
            due_date = data["due_date"] or None
            self._check_date(due_date)
            task.due_date = due_date
        if "done" in data:
            task.done = bool(data["done"])
        return self.repo.update(task)

    def delete_task(self, task_id):
        if not self.repo.delete(task_id):
            raise NotFoundError(f"Tâche {task_id} introuvable")

    def stats(self):
        tasks = self.repo.list()
        done = sum(1 for t in tasks if t.done)
        return {"total": len(tasks), "done": done, "remaining": len(tasks) - done}