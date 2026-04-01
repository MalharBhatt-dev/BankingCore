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


# ✅ FIXED auth_token
@pytest.fixture
def auth_token(client):
    # create account
    res = client.post("/accounts", json={
        "name": "Test User",
        "pin": "1234",
        "initial_deposit": 1000
    })

    data = res.get_json()
    assert res.status_code == 201, f"Account creation failed: {data}"

    account_number = data["account_number"]   # ✅ dynamic

    # login with SAME PIN
    res = client.post("/auth/login", json={
        "account_number": account_number,
        "pin": "1234"   # ✅ FIXED
    })

    data = res.get_json()
    assert res.status_code == 200, f"Login failed: {data}"
    assert "access_token" in data, "No access token returned"

    return data["access_token"]


# ✅ FIXED admin_token
@pytest.fixture
def admin_token(client):
    # create admin account
    res = client.post("/accounts", json={
        "name": "Admin",
        "pin": "1234",
        "initial_deposit": 0
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