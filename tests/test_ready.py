import pytest

def test_ping(test_app):
    response = test_app.get('/')
    assert response.status_code == 200

