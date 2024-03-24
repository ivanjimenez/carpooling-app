import pytest

@pytest.mark.asyncio
async def test_add_cars_valid(test_app):
    car_list = [
        {"id": 1, "seats": 4},
        {"id": 2, "seats": 6}
    ]
    response = test_app.put("/cars", json=car_list)
    assert response.status_code == 200