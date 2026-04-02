def test_create_request(client,create_user,login_user):
    acc=create_user()
    auth_token=login_user(acc)["access_token"]
    res = client.post("/requests",json={"query_type":"CHANGE_PIN","description":"Need to change pin"},headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code == 201

def test_get_my_requests(client,create_user,login_user):
    acc=create_user()
    auth_token=login_user(acc)["access_token"]
    res = client.get("/requests/my",headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code == 200