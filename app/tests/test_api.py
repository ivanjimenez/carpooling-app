from fastapi.testclient import TestClient
import pytest

def test_ping(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "OK", "message": "Car-pooling is ready"}

    



    