def test_transfer(client,create_user,login_user):
    acc=create_user()
    auth_token=login_user(acc)["access_token"]
    res = client.post(f"/accounts/{acc}/transfer",json={"to_account":1005,"amount":100},headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code == 200

def test_trasfer_to_self(client,create_user,login_user):
    acc=create_user()
    auth_token=login_user(acc)["access_token"]
    res=client.post(f"/accounts/{acc}/transfer",json={"to_account":acc,"amount":100},headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code == 400

def test_transfer_invalid_amount(client,create_user,login_user):
    acc1=create_user()
    acc2=create_user()
    auth_token=login_user(acc1)["access_token"]
    res=client.post(f"/accounts/{acc1}/transfer",json={"to_account":acc2,"amount":-10},headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code==400

def test_transaction_histroy(client,create_user,login_user):
    acc=create_user()
    auth_token=login_user(acc)["access_token"]
    res = client.get(f"/accounts/{acc}/transactions",headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code == 200
    assert "transactions" in res.get_json()