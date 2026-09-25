from fastapi.testclient import TestClient
from main import app


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200


def test_ask_returns_mock_sql():
    with TestClient(app) as client:
        response = client.post("/ask", json={"question": "herhangi bir soru"})
        assert response.status_code == 200
        assert response.json()["generated_sql"].upper().startswith("SELECT")


def test_ask_empty_question_rejected():
    with TestClient(app) as client:
        response = client.post("/ask", json={"question": ""})
        assert response.status_code == 422