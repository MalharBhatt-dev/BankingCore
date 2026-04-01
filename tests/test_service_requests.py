def test_create_request(client,auth_token):
    res = client.post("/requests",json={"request_type":"CHANGE_PIN","description":"Need to change pin"},headers={"Authorization":f"Bearer {auth_token}"})

    assert res.status_code == 201

def test_get_my_requests(client,auth_token):
    res = client.get("/requests/my",headers={"Authorization":f"Bearer {auth_token}"})

    assert res.status_code == 200