import pytest
from flask import g
import warnings
warnings.filterwarnings("ignore")

#! BYPASS DECORATORS
@pytest.fixture(autouse=True)
def mock_auth(monkeypatch):
    def fake_login_required(f):
        def wrapper(*args,**kwargs):
            g.account_number=12345
            return f(*args,**kwargs)
        return wrapper
    
    def fake_role_required(role):
        def decorator(f):
            def wrapper(*args,**kwargs):
                return f(*args,**kwargs)
            return wrapper
        return decorator
    monkeypatch.setattr("app.routes.login_required",fake_login_required)
    monkeypatch.setattr("app.routes.role_required",fake_role_required)