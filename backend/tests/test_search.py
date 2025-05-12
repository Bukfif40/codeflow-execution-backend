import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app

client = TestClient(app)

def get_token():
    login_response = client.post(
        "/login",
        data={"username": "admin", "password": "adminpass"}
    )
    return login_response.json().get("access_token")

def test_search_google():
    token = get_token()
    assert token
    response = client.get(
        "/search",
        params={"query": "python", "provider": "serpapi"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "results" in data
    assert isinstance(data["results"], list)
    if data["results"]:
        assert "title" in data["results"][0]
        assert "link" in data["results"][0]
