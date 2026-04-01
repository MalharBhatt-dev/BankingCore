def test_login_success(client):
    res = client.post("/accounts",json={
        "name":"user",
        "pin":"1234",
        "account_type":"SAVINGS",
        "initial_deposit":1000
    })

    data = res.get_json()
    account_number = data["account_number"]

    res=client.post("/auth/login",json={
        "account_number":account_number,
        "pin":"1234"
    })

    assert res.status_code == 200
    assert "access_token" in res.get_json()

def test_login_fail(client):
    res = client.post("/auth/login",json={
        "account_number":1003,
        "pin":"2345"
    })

    assert res.status_code == 401

def test_refresh_token(client):
    res = client.post("/auth/login",json={
        "account_number":1002,
        "pin":"2345"
    })

    data = res.get_json()
    refresh = data["refresh_token"]

    res2 = client.post("/auth/refresh",headers={
        "Authorization":f"Bearer {refresh}"
    })

    assert res2.status_code == 200