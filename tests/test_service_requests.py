def test_create_request(client,auth_headers):
    res = client.post("/requests",json={"query_type":"CHANGE_PIN","description":"Need to change pin"},headers=auth_headers)
    assert res.status_code == 201

def test_get_my_requests(client,auth_headers):
    res = client.get("/requests/my",headers=auth_headers)
    assert res.status_code == 200