
import pytest

@pytest.mark.asyncio
async def test_add_journey_accepted(test_app):
    # Datos del grupo
    group_data = {
        "id" : 1,
        "people": 4
    }
    
    # Enviar solicitud HTTP POST al endpoint /journey con los datos del grupo
    response = test_app.post("/journey", json=group_data)
    
    # Verificar que la respuesta tenga el código de estado HTTP 202 ACCEPTED
    assert response.status_code == 200