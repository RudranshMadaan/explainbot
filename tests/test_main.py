
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)


@patch("app.main.generate_explanation")
def test_explain_returns_answer(mock_generate):

    mock_generate.return_value = (
        "Recursion is when a function calls itself, "
        "like a set of Russian nesting dolls."
    )

    response = client.post(
        "/api/explain",
        json={
            "term": "recursion",
            "audience": "eli5"
        }
    )

    assert response.status_code == 200
    assert response.json()["term"] == "recursion"
    assert "like" in response.json()["answer"].lower()
    assert 1 <= len(
        [s for s in mock_generate.return_value.split(".") if s.strip()]
    ) <= 4

def test_empty_term_rejected():

    response = client.post(
        "/api/explain",
        json={
            "term": "",
            "audience": "eli5"
        }
    )

    assert response.status_code == 422


def test_oversized_term_rejected():

    response = client.post(
        "/api/explain",
        json={
            "term": "A" * 121,
            "audience": "eli5"
        }
    )

    assert response.status_code == 422


def test_invalid_audience_rejected():

    response = client.post(
        "/api/explain",
        json={
            "term": "recursion",
            "audience": "beginner"
        }
    )

    assert response.status_code == 422


def test_health_check():

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"ok": True}
