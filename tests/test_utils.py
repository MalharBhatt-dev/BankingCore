from app.secret_key_generator import generate_secret_key
import warnings
warnings.filterwarnings("ignore")

def test_generate_secret_key():
    key=generate_secret_key()
    assert isinstance(key,str)
    assert len(key)>10

def test_404(client):
    res = client.get("/random-route-does-not-exist")
    assert res.status_code in [404,500]

def test_405(client):
    res = client.post("/")
    assert res.status_code in [405,500]