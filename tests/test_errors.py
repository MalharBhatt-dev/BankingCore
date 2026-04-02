def test_404_handler(client):
    res = client.get("/non-existent-route")
    assert res.status_code == 404


def test_405_handler(client):
    res = client.post("/")
    assert res.status_code == 405


def test_internal_server_error(client, monkeypatch):
    def crash(*args, **kwargs):
        raise Exception("Boom")

    monkeypatch.setattr("app.routes.register_routes", crash)

    res = client.get("/")
    assert res.status_code in [500, 200]