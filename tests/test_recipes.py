# tests/test_recipes.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_generate_from_ingredients():
    response = client.post(
        "/api/v1/recipes/generate-from-ingredients",
        json={
            "ingredients": "bột mì, trứng, đường, bơ",
            "language": "vi"
        }
    )
    assert response.status_code == 200
    assert "data" in response.json()

def test_generate_from_trend():
    response = client.post(
        "/api/v1/recipes/generate-from-trend",
        json={
            "trend": "Matcha",
            "user_segment": "GenZ",
            "occasion": "Valentine",
            "language": "vi"
        }
    )
    assert response.status_code == 200
    assert "data" in response.json()