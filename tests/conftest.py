import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.config import TestConfig
from database import init_db


@pytest.fixture
def app():
    app = create_app(TestConfig)
    app.config.update({
        "TESTING":True
    })
    with app.app_context():
        init_db()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def create_user(client):
    def _create(name="Test",pin="1234",deposit=1000):
        res = client.post("/accounts",json={
            "name":name,
            "pin":pin,
            "account_type":"SAVINGS",
            "initial_deposit":deposit
        })
        return res.get_json()["account_number"]
    return _create

@pytest.fixture
def login_user(client):
    def _login(account_number,pin="1234"):
        res = client.post("/auth/login",json={
            "account_number":account_number,
            "pin":pin
        })
        return res.get_json()
    return _login

@pytest.fixture
def auth_headers(create_user,login_user):
    acc = create_user()
    tokens= login_user(acc)
    return {"Authorization":f"Bearer {tokens["access_token"]}"}