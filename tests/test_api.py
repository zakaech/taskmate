"""Tests d'intégration : on appelle l'API complète (routes + service + base)."""


def create(client, **data):
    return client.post("/tasks", json=data)


def test_create_and_list(client):
    response = create(client, title="Projet GL", category="Ecole", priority="high")
    assert response.status_code == 201
    assert response.get_json()["id"] == 1

    tasks = client.get("/tasks").get_json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Projet GL"


def test_create_without_title_returns_400(client):
    response = create(client, category="Ecole")
    assert response.status_code == 400
    assert "titre" in response.get_json()["error"]


def test_get_unknown_returns_404(client):
    assert client.get("/tasks/99").status_code == 404


def test_update_marks_task_done(client):
    create(client, title="a")
    response = client.put("/tasks/1", json={"done": True})
    assert response.status_code == 200
    assert response.get_json()["done"] is True


def test_delete_task(client):
    create(client, title="a")
    assert client.delete("/tasks/1").status_code == 204
    assert client.get("/tasks").get_json() == []
    assert client.delete("/tasks/1").status_code == 404


def test_filters(client):
    create(client, title="a", category="Ecole", priority="high")
    create(client, title="b", category="Maison", priority="low")
    client.put("/tasks/2", json={"done": True})

    assert len(client.get("/tasks?category=Ecole").get_json()) == 1
    assert len(client.get("/tasks?priority=low").get_json()) == 1
    assert len(client.get("/tasks?done=true").get_json()) == 1
    assert len(client.get("/tasks?done=false").get_json()) == 1


def test_sort_by_due_date(client):
    create(client, title="tard", due_date="2026-12-31")
    create(client, title="tot", due_date="2026-11-05")
    tasks = client.get("/tasks?sort=due_date").get_json()
    assert [t["title"] for t in tasks] == ["tot", "tard"]


def test_stats(client):
    create(client, title="a")
    create(client, title="b")
    client.put("/tasks/1", json={"done": True})
    assert client.get("/tasks/stats").get_json() == {"total": 2, "done": 1, "remaining": 1}


def test_home_page_is_served(client):
    assert client.get("/").status_code == 200
