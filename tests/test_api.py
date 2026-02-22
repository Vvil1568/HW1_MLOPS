import sys

sys.path.insert(0, ".")

import pytest
from fastapi.testclient import TestClient
from app.api.rest import router
from app.ml.service import MLServiceLogic

client = TestClient(router)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_batch_endpoint_exists():
    """Test that batch prediction endpoint exists."""
    response = client.get("/predict/batch")
    assert response.status_code == 405  # Should be POST only


def test_predict_batch_with_mock():
    """Test batch prediction endpoint with mocked service."""
    # This is a basic test - in real scenario we'd mock MLServiceLogic
    # Test that endpoint exists and properly validates input
    response = client.post("/predict/batch")
    # Should return 422 for validation error (missing file field)
    assert response.status_code == 422
