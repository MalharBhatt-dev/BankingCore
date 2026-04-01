import pytest
import sys
import os

sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from app import create_app
from app.config import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

#create test user and login
@pytest.fixture
def auth_token(client):
    #first create account
    res = client.post("/accounts",json={
        "name":"Test User",
        "pin":"1234",
        "initial_deposit":1000
    })

    data = res.get_json()

    assert res.status_code == 201 , f"Account creation failed: {data}"

    #login
    res = client.post("/auth/login",json={
        "account_number": 1002,
        "pin":"2345",
    })
    data = res.get_json()

    assert res.status_code == 200 , f"Login failed: {data}"
    assert "access_token" in data , "No access token returned"

    return data["access_token"]

#admin token if needed
@pytest.fixture
def admin_token(client):
    res = client.post("/auth/login",json={
        "account_number":1003,
        "pin":"1234"
    })

    data = res.get_json()

    assert res.status_code == 200 , f"Amin Login failed: {data}"
    return data["access_token"]