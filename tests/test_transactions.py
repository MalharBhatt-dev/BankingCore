import warnings
warnings.filterwarnings("ignore")

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

def test_transfer_invalid_account(client,create_user,login_user):
    acc=create_user()
    auth_token=login_user(acc)["access_token"]
    res=client.post(f"/accounts/{acc}/transfer",json={"to_account":"fake","amount":10},headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code==400

def test_transfer_invalid_amount(client,create_user,login_user):
    acc1=create_user()
    acc2=create_user()
    auth_token=login_user(acc1)["access_token"]
    res=client.post(f"/accounts/{acc1}/transfer",json={"to_account":acc2,"amount":-10},headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code==400

def test_transfer_insufficient_balance(client,create_user,login_user):
    acc1=create_user()
    acc2=create_user()
    auth_token=login_user(acc1)["access_token"]
    res=client.post(f"/accounts/{acc1}/transfer",json={"to_account":acc2,"amount":9999999999},headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code==400


def test_transfer_missing_fields(client, create_user, login_user):
    acc = create_user()
    token = login_user(acc)["access_token"]
    res = client.post(f"/accounts/{acc}/transfer",json={},headers={"Authorization": f"Bearer {token}"})
    assert res.status_code in [400, 500]

def test_transaction_histroy(client,create_user,login_user):
    acc=create_user()
    auth_token=login_user(acc)["access_token"]
    res = client.get(f"/accounts/{acc}/transactions",headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code == 200
    assert "transactions" in res.get_json()