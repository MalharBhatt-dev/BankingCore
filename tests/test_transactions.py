def test_transfer(client,auth_token,account_number):
    #create account
    client.post("/accounts",json={
        "name":"Receiver",
        "pin":"1234",
        "account_type":"SAVINGS",
        "initial_deposit":500
    })

    res = client.post(f"/accounts/{account_number}/transfer",json={"to_account":1005,"amount":100},headers={"Authorization":f"Bearer {auth_token}"})

    assert res.status_code == 200

def test_transaction_histroy(client,auth_token,account_number):
    res = client.get(f"/accounts/{account_number}/transactions",headers={"Authorization":f"Bearer {auth_token}"})

    assert res.status_code == 200
    assert "transactions" in res.get_json()