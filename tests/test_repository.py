import pytest

from app.models import Task
from app.repository import TaskRepository


@pytest.fixture
def repo(tmp_path):
    repository = TaskRepository(str(tmp_path / "test.db"))
    repository.init_db()
    return repository


def test_add_assigns_an_id(repo):
    task = repo.add(Task(title="Réviser le cours"))
    assert task.id is not None


def test_get_returns_saved_task(repo):
    saved = repo.add(Task(title="TP", category="Ecole", priority="high"))
    found = repo.get(saved.id)
    assert found.title == "TP"
    assert found.category == "Ecole"
    assert found.priority == "high"
    assert found.done is False


def test_get_unknown_returns_none(repo):
    assert repo.get(999) is None


def test_list_filters_by_category_priority_and_done(repo):
    repo.add(Task(title="a", category="Ecole", priority="high"))
    repo.add(Task(title="b", category="Maison", priority="low"))
    repo.add(Task(title="c", category="Ecole", priority="low", done=True))
    assert len(repo.list(category="Ecole")) == 2
    assert len(repo.list(priority="low")) == 2
    assert len(repo.list(done=True)) == 1
    assert len(repo.list(category="Ecole", priority="low")) == 1


def test_list_sorted_by_due_date_puts_empty_dates_last(repo):
    repo.add(Task(title="sans date"))
    repo.add(Task(title="tard", due_date="2026-12-31"))
    repo.add(Task(title="tot", due_date="2026-11-05"))
    titles = [t.title for t in repo.list(sort_by_due=True)]
    assert titles == ["tot", "tard", "sans date"]


def test_update_changes_values(repo):
    task = repo.add(Task(title="avant"))
    task.title = "après"
    task.done = True
    repo.update(task)
    found = repo.get(task.id)
    assert found.title == "après"
    assert found.done is True


def test_delete_removes_task(repo):
    task = repo.add(Task(title="x"))
    assert repo.delete(task.id) is True
    assert repo.get(task.id) is None
    assert repo.delete(task.id) is False