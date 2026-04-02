def test_create_account(client):
    res = client.post("/accounts",json={
        "name":"Test",
        "pin":"1234",
        "account_type":"SAVINGS",
        "initial_deposit":1000
    })

    assert res.status_code == 201

def test_get_balance(client,login_user,create_user):
    acc=create_user()
    auth_token=login_user(acc)["access_token"]
    res = client.get(f"/accounts/{acc}",headers={
        "Authorization":f"Bearer {auth_token}"
    })

    assert res.status_code == 200
    assert "balance" in res.get_json()

def test_get_balance_unauthorized(client):
    res = client.get("/accounts/1001")
    assert res.status_code == 400

def test_deposit(client,create_user,login_user):
    acc=create_user()
    auth_token=login_user(acc)["access_token"]
    res = client.post(f"/accounts/{acc}/deposit",json={"amount":200},headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code == 200

def test_deposit_negative_value(client,create_user,login_user):
    acc=create_user()
    auth_token=login_user(acc)["access_token"]    
    res = client.post(f"/accounts/{acc}/deposit",json={"amount":-100},headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code in [400,500]

def test_withdraw(client,create_user,login_user):
    acc=create_user()
    auth_token=login_user(acc)["access_token"]
    res = client.post(f"/accounts/{acc}/withdraw",json={"amount":200},headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code == 200

def test_withdraw_insufficient_balance(client,create_user,login_user):
    acc=create_user()
    auth_token=login_user(acc)["access_token"]
    res = client.post(f"/accounts/{acc}/withdraw",json={"amount":9999999},headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code != 200

def test_account_access_violation(client,create_user,login_user):
    acc1=create_user()
    acc2=create_user()
    auth_token=login_user(acc1)["access_token"]
    res=client.get(f"/accounts/{acc2}",headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code == 401