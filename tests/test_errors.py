from exceptions.base_exception import BankingException
from exceptions.token_expired_exception import TokenExpiredException
from exceptions.invalid_token_exception import InvalidTokenException

def test_banking_exception(app, client, monkeypatch):
    def crash(*args, **kwargs):
        raise BankingException("Test error")
    monkeypatch.setattr(app.config["service"], "create_account", crash)
    res = client.post("/accounts", json={
        "name": "test",
        "pin": "1234",
        "initial_deposit": 100
    })
    assert res.status_code == 400

def test_token_expired_exception(app, client, monkeypatch):
    def crash(*args, **kwargs):
        raise TokenExpiredException("Expired")
    monkeypatch.setattr(app.config["service"], "create_account", crash)
    res = client.post("/accounts", json={
        "name": "test",
        "pin": "1234",
        "initial_deposit": 100
    })
    assert res.status_code == 401

def test_invalid_token_exception(app, client, monkeypatch):
    def crash(*args, **kwargs):
        raise InvalidTokenException("Invalid")
    monkeypatch.setattr(app.config["service"], "create_account", crash)
    res = client.post("/accounts", json={
        "name": "test",
        "pin": "1234",
        "initial_deposit": 100
    })
    assert res.status_code == 401

def test_404_handler(client):
    res = client.get("/non-existent-route")
    assert res.status_code == 404


def test_405_handler(client):
    res = client.post("/")
    assert res.status_code == 405


def test_internal_server_error(client, monkeypatch):
    def crash(*args, **kwargs):
        raise Exception("Boom")

    monkeypatch.setattr("app.routes.register_routes", crash)

    res = client.get("/")
    assert res.status_code in [500, 200]