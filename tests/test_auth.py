def test_login_success(client,create_user,login_user):
    acc = create_user()
    res = login_user(acc)

    assert "access_token" in res

def test_login_fail(client):
    res = client.post("/auth/login",json={
        "account_number":1003,
        "pin":"2345"
    })

    assert res.status_code == 401

def test_login_invalid_pin(client,create_user):
    acc = create_user()

    res = client.post("/auth/login",json={
        "account_number":acc,
        "pin":"wrong"
    })

    assert res.status_code == 401

def test_refresh_token(client,create_user):
    acc = create_user()
    res = client.post("/auth/login",json={
        "account_number":acc,
        "pin":"1234"
    })

    data = res.get_json()
    refresh = data["refresh_token"]

    res2 = client.post("/auth/refresh",headers={
        "Authorization":f"Bearer {refresh}"
    })

    assert res2.status_code == 200

def test_refresh_invalid_token(client):
    res = client.post("/auth/refresh",headers={
        "Authorization":f"Bearer invalidtoken"
    })

    assert res.status_code == 401

def test_login_rate_limiter(client):
    for _ in range(6):
        client.post("/auth/login",json={
            "account_number":9999,
            "pin":"wrong"
        })