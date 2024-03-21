import pytest

from fastapi.testclient import TestClient

from main import init_app

app = init_app()

    
client = TestClient(app)


def test_ready():
    response = client.get("/")
    assert response.status_code == 200

    
