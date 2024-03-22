# pylint: disable=redefined-outer-name
import pytest
from starlette.testclient import TestClient

from app.app import init_app

fast_api = init_app()

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(fast_api)
    yield client  # testing happens here