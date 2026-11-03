from flask import Flask

from .repository import TaskRepository
from .routes import bp
from .services import TaskService


def create_app(db_path="taskmate.db"):
    app = Flask(__name__, static_folder="static", static_url_path="/static")

    repo = TaskRepository(db_path)
    repo.init_db()
    app.config["TASK_SERVICE"] = TaskService(repo)

    app.register_blueprint(bp)

    @app.get("/")
    def index():
        return app.send_static_file("index.html")

    return app