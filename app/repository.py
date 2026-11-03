import sqlite3

from .models import Task


class TaskRepository:
    """Pattern Repository : seule classe qui parle à la base SQLite."""

    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL DEFAULT 'General',
                    priority TEXT NOT NULL DEFAULT 'medium',
                    due_date TEXT,
                    done INTEGER NOT NULL DEFAULT 0
                )
                """
            )

    @staticmethod
    def _to_task(row):
        return Task(
            id=row["id"],
            title=row["title"],
            category=row["category"],
            priority=row["priority"],
            due_date=row["due_date"],
            done=bool(row["done"]),
        )

    def add(self, task):
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO tasks (title, category, priority, due_date, done) "
                "VALUES (?, ?, ?, ?, ?)",
                (task.title, task.category, task.priority, task.due_date, int(task.done)),
            )
            task.id = cur.lastrowid
        return task

    def get(self, task_id):
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return self._to_task(row) if row else None

    def list(self, category=None, priority=None, done=None, sort_by_due=False):
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []
        if category:
            query += " AND category = ?"
            params.append(category)
        if priority:
            query += " AND priority = ?"
            params.append(priority)
        if done is not None:
            query += " AND done = ?"
            params.append(int(done))
        if sort_by_due:
            query += " ORDER BY due_date IS NULL, due_date ASC, id ASC"
        else:
            query += " ORDER BY id ASC"
        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [self._to_task(r) for r in rows]

    def update(self, task):
        with self._connect() as conn:
            conn.execute(
                "UPDATE tasks SET title = ?, category = ?, priority = ?, "
                "due_date = ?, done = ? WHERE id = ?",
                (task.title, task.category, task.priority, task.due_date, int(task.done), task.id),
            )
        return task

    def delete(self, task_id):
        with self._connect() as conn:
            cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return cur.rowcount > 0