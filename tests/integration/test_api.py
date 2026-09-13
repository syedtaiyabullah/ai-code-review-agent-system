"""Integration tests for the API."""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "AI Code Review Agent"
    assert data["status"] == "running"


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model" in data


def test_supported_languages():
    """Test supported languages endpoint."""
    response = client.get("/api/v1/supported-languages")
    assert response.status_code == 200
    data = response.json()
    assert "languages" in data
    assert len(data["languages"]) > 0


def test_review_types():
    """Test review types endpoint."""
    response = client.get("/api/v1/review-types")
    assert response.status_code == 200
    data = response.json()
    assert "review_types" in data
    assert len(data["review_types"]) == 4


@pytest.mark.skipif(
    True,  # Skip by default to avoid API costs
    reason="Skipping actual LLM calls in CI"
)
def test_code_review_endpoint():
    """Test code review endpoint (integration test with LLM)."""
    code = '''
def divide(a, b):
    return a / b
'''
    
    response = client.post(
        "/api/v1/review",
        json={
            "code": code,
            "language": "python",
            "filename": "test.py",
            "review_types": ["bug"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "submission_id" in data
    assert "issues" in data
    assert "summary" in data


def test_code_review_empty_code():
    """Test review with empty code."""
    response = client.post(
        "/api/v1/review",
        json={
            "code": "   ",
            "language": "python",
            "review_types": ["bug"]
        }
    )
    
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_code_review_too_long():
    """Test review with code exceeding max length."""
    long_code = "x = 1\n" * 10000  # Exceed max_code_length
    
    response = client.post(
        "/api/v1/review",
        json={
            "code": long_code,
            "language": "python",
            "review_types": ["bug"]
        }
    )
    
    assert response.status_code == 400
    assert "too long" in response.json()["detail"].lower()
