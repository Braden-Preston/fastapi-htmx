from app.testing import *


def test_read_home_page(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello FastAPI 👋!"}
