from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test endpoint /ask
def test_ask_question():
    response = client.post("/ask", json={"question": "Apa itu HR?", "language": "id"})
    assert response.status_code == 200
    assert "answer" in response.json()

# Test endpoint /feedback
def test_feedback():
    response = client.post("/feedback", json={
        "question": "Apa itu HR?",
        "answer": "HR adalah Human Resources",
        "feedback": "Bagus",
        "language": "id"
    })
    assert response.status_code == 200
    assert "message" in response.json()
