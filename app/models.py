from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Task:
    """Une tâche de la to-do list."""

    title: str
    category: str = "General"
    priority: str = "medium"  # low | medium | high
    due_date: Optional[str] = None  # format AAAA-MM-JJ
    done: bool = False
    id: Optional[int] = None

    def to_dict(self):
        return asdict(self)