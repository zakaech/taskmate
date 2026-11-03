import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(str(tmp_path / "api_test.db"))
    app.config["TESTING"] = True
    return app.test_client()
