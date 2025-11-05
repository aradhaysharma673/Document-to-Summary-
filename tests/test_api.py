from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_ready"] == True

def test_summarize_success():
    payload = {
        "text": "This is a test sentence. " * 20,
        "max_sentences": 3
    }
    response = client.post("/summarize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert data["sentences_count"] <= 3

def test_summarize_too_short():
    payload = {
        "text": "Too short",
        "max_sentences": 3
    }
    response = client.post("/summarize", json=payload)
    assert response.status_code == 422  # Validation error

def test_rate_limit():
    payload = {
        "text": "This is a test sentence. " * 20,
        "max_sentences": 3
    }
    
    # Make multiple requests
    for _ in range(12):
        response = client.post("/summarize", json=payload)
    
    # Last request should fail
    assert response.status_code == 429
