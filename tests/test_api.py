import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add backend to path so we can import it
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from main import app

# TestClient simulates HTTP requests without running a real server
client = TestClient(app)

# ============ HEALTH TESTS ============

def test_health_endpoint_returns_200():
    response = client.get("/health")
    assert response.status_code == 200

def test_health_endpoint_returns_correct_data():
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"

# ============ ANALYSE VALIDATION TESTS ============

def test_analyse_rejects_non_pdf():
    response = client.post(
        "/analyse",
        files={"cv": ("test.txt", b"some text content", "text/plain")},
        data={"job_description": "We are looking for an AI Engineer with experience in Python and machine learning and LLM applications and cloud deployment."}
    )
    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]

def test_analyse_rejects_short_job_description():
    response = client.post(
        "/analyse",
        files={"cv": ("test.pdf", b"fake pdf content", "application/pdf")},
        data={"job_description": "Short description"}
    )
    assert response.status_code == 400

def test_analyse_rejects_missing_cv():
    response = client.post(
        "/analyse",
        data={"job_description": "We are looking for an AI Engineer with experience in Python and machine learning applications."}
    )
    assert response.status_code == 422

def test_analyse_rejects_missing_job_description():
    response = client.post(
        "/analyse",
        files={"cv": ("test.pdf", b"fake pdf content", "application/pdf")}
    )
    assert response.status_code == 422