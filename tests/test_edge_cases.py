def test_empty_payload(client):
    res=client.post("/accounts",json={})
    assert res.status_code in [400,500]

def test_large_deposit(client,create_user,login_user):
    acc=create_user()
    auth_token=login_user(acc)["access_token"]
    res=client.post(f"/accounts/{acc}/deposit",json={"amount":9999999999},headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code == 200