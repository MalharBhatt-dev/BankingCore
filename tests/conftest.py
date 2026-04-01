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

    with app.app_context():
        init_db()

    return app


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user_data(client):
    res = client.post("/accounts", json={
        "name": "Test User",
        "pin": "1234",
        "initial_deposit": 1000
    })

    data = res.get_json()
    return data["account_number"], "1234"

@pytest.fixture
def account_number(user_data):
    return user_data[0]


@pytest.fixture
def auth_token(client, user_data):
    account_number, pin = user_data

    res = client.post("/auth/login", json={
        "account_number": account_number,
        "pin": pin
    })

    return res.get_json()["access_token"]


# ✅ FIXED admin_token
@pytest.fixture
def admin_token(client):
    # create admin account
    res = client.post("/accounts", json={
        "name": "Admin",
        "pin": "1234",
        "initial_deposit": 1000
    })

    data = res.get_json()
    account_number = data["account_number"]

    # manually promote to admin (important)
    from database import DB_PATH
    import sqlite3

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE accounts SET role='admin' WHERE account_number=?",
        (account_number,)
    )
    conn.commit()
    conn.close()

    # login
    res = client.post("/auth/login", json={
        "account_number": account_number,
        "pin": "1234"
    })

    data = res.get_json()
    assert res.status_code == 200, f"Admin Login failed: {data}"

    return data["access_token"]