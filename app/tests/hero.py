from app import client

def test_read_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello FastAPI 👋!"}
