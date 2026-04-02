from app.secret_key_generator import generate_secret_key
import warnings
warnings.filterwarnings("ignore")

def test_generate_secret_key():
    key=generate_secret_key()
    assert isinstance(key,str)
    assert len(key)>10