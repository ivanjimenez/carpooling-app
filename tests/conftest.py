import pytest

from fastapi.testclient import TestClient

from app.app import init_app

app = init_app()

    
client = TestClient(app)

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client