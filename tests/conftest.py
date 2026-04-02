import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import warnings
warnings.filterwarnings("ignore")

from app import create_app
from app.config import TestConfig
from app.extensions import db   

@pytest.fixture(scope="session")
def app():
    app = create_app("app.config.TestConfig")
    app.config.update({
        "TESTING":True
    })
    with app.app_context():
        db.create_all()
        # yield app
        # db.drop_all()
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
def create_admin_user(client):
    def _create(name="AdminTest",pin="1234",deposit="1000"):
        res=client.post("/accounts",json={
            "name":name,
            "pin":pin,
            "initial_deposit":deposit,
            "account_type":"SAVINGS",
            "role":"admin"
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
    auth_token= login_user(acc)["access_token"]
    return {"Authorization":f"Bearer {auth_token}"}

from app.extensions import limiter
@pytest.fixture(autouse=True)
def disable_rate_limit():
    limiter.enabled = False

@pytest.fixture(autouse=True)
def cleanup(app):
    yield
    with app.app_context():
        db.session.remove()