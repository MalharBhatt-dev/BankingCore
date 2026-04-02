def test_missing_token(client):
    res=client.get("/accounts/1001")
    assert res.status_code == 400

def test_invalid_token(client):
    res=client.get("/accounts/1001",headers={"Authorization":"Bearer invalid"})
    assert res.status_code == 401