import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app

client = TestClient(app)


def test_register_and_login():
    # Register a new user
    reg_response = client.post(
        "/register",
        data={"username": "testuser", "password": "testpass"}
    )
    assert reg_response.status_code in (200, 201, 400)  # 400 if user exists

    # Login
    login_response = client.post(
        "/login",
        data={"username": "testuser", "password": "testpass"}
    )
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")
    assert token

    # Get profile with token
    profile_response = client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert profile_response.status_code == 200
    assert profile_response.json()["username"] == "testuser"
