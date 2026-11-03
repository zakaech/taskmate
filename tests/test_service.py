import pytest

from app.repository import TaskRepository
from app.services import NotFoundError, TaskService, ValidationError


@pytest.fixture
def service(tmp_path):
    repo = TaskRepository(str(tmp_path / "test.db"))
    repo.init_db()
    return TaskService(repo)


def test_create_task_with_defaults(service):
    task = service.create_task({"title": "  Faire le projet  "})
    assert task.title == "Faire le projet"
    assert task.category == "General"
    assert task.priority == "medium"


def test_create_task_requires_title(service):
    with pytest.raises(ValidationError):
        service.create_task({"title": "   "})


def test_create_task_rejects_bad_priority(service):
    with pytest.raises(ValidationError):
        service.create_task({"title": "x", "priority": "urgent"})


def test_create_task_rejects_bad_date(service):
    with pytest.raises(ValidationError):
        service.create_task({"title": "x", "due_date": "31/12/2026"})


def test_get_unknown_task_raises(service):
    with pytest.raises(NotFoundError):
        service.get_task(42)


def test_update_task_partially(service):
    task = service.create_task({"title": "a", "priority": "low"})
    updated = service.update_task(task.id, {"done": True})
    assert updated.done is True
    assert updated.priority == "low"


def test_update_rejects_empty_title(service):
    task = service.create_task({"title": "a"})
    with pytest.raises(ValidationError):
        service.update_task(task.id, {"title": ""})


def test_delete_unknown_raises(service):
    with pytest.raises(NotFoundError):
        service.delete_task(42)


def test_stats(service):
    service.create_task({"title": "a"})
    t2 = service.create_task({"title": "b"})
    service.update_task(t2.id, {"done": True})
    assert service.stats() == {"total": 2, "done": 1, "remaining": 1}