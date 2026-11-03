from flask import Blueprint, current_app, jsonify, request

from .services import NotFoundError, ValidationError

bp = Blueprint("tasks", __name__)


def service():
    return current_app.config["TASK_SERVICE"]


@bp.errorhandler(ValidationError)
def handle_validation(error):
    return jsonify({"error": str(error)}), 400


@bp.errorhandler(NotFoundError)
def handle_not_found(error):
    return jsonify({"error": str(error)}), 404


@bp.get("/tasks")
def list_tasks():
    done = request.args.get("done")
    if done is not None:
        done = done.lower() == "true"
    tasks = service().list_tasks(
        category=request.args.get("category"),
        priority=request.args.get("priority"),
        done=done,
        sort=request.args.get("sort"),
    )
    return jsonify([t.to_dict() for t in tasks])


@bp.post("/tasks")
def create_task():
    task = service().create_task(request.get_json(silent=True) or {})
    return jsonify(task.to_dict()), 201


@bp.get("/tasks/stats")
def stats():
    return jsonify(service().stats())


@bp.get("/tasks/<int:task_id>")
def get_task(task_id):
    return jsonify(service().get_task(task_id).to_dict())


@bp.put("/tasks/<int:task_id>")
def update_task(task_id):
    task = service().update_task(task_id, request.get_json(silent=True) or {})
    return jsonify(task.to_dict())


@bp.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    service().delete_task(task_id)
    return "", 204