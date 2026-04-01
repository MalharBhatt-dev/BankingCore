def test_create_account(client):
    res = client.post("/accounts",json={
        "name":"Test",
        "pin":"1234",
        "account_type":"SAVINGS",
        "initial_deposit":1000
    })

    assert res.status_code == 201

def test_get_balance(client,auth_token,account_number):
    res = client.get(f"/accounts/{account_number}",headers={
        "Authorization":f"Bearer {auth_token}"
    })

    assert res.status_code == 200
    assert "balance" in res.get_json()

def test_deposit(client,auth_token,account_number):
    res = client.post(f"/accounts/{account_number}/deposit",json={"amount":200},headers={"Authorization":f"Bearer {auth_token}"})

    assert res.status_code == 200

def test_withdraw(client,auth_token,account_number):
    res = client.post(f"/accounts/{account_number}/withdraw",json={"amount":200},headers={"Authorization":f"Bearer {auth_token}"})

    assert res.status_code == 200