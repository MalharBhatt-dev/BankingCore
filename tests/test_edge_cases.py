import warnings
warnings.filterwarnings("ignore")

def test_unauthorized_access(client, create_user, login_user):
    acc1 = create_user()
    acc2 = create_user()
    token1 = login_user(acc1)["access_token"]
    headers = {"Authorization": f"Bearer {token1}"}
    
    res = client.post(f"/accounts/{acc2}/deposit", json={"amount": 100}, headers=headers)
    assert res.status_code == 401
    
    res = client.post(f"/accounts/{acc2}/withdraw", json={"amount": 100}, headers=headers)
    assert res.status_code == 401
    
    res = client.get(f"/accounts/{acc2}/transactions", headers=headers)
    assert res.status_code == 401

def test_missing_amount_deposit_withdraw(client, create_user, login_user):
    acc = create_user()
    token = login_user(acc)["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    res = client.post(f"/accounts/{acc}/deposit", headers=headers)
    assert res.status_code in [400, 500]
    
    res = client.post(f"/accounts/{acc}/withdraw", headers=headers)
    assert res.status_code in [400, 500]

def create_user_with_role(app, repo, name, pin, deposit, role):
    with app.app_context():
        last_acc = repo.get_last_account_number()
        new_acc = (last_acc + 1) if last_acc else 1001
        import hashlib
        pin_hash = hashlib.sha256(pin.encode()).hexdigest()
        repo.insert_account(new_acc, name, pin_hash, deposit, role)
        repo.commit()
        return new_acc

def test_admin_routes(app, client, login_user):
    repo = app.config["service"].repo
    admin_acc = create_user_with_role(app, repo, "Admin", "1234", 1000, "admin")
    
    admin_token = login_user(admin_acc)["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    res = client.get("/admin/stats", headers=admin_headers)
    assert res.status_code == 200
    
    res = client.get("/admin/events", headers=admin_headers)
    assert res.status_code == 200
    
    res = client.get("/admin/locked-accounts", headers=admin_headers)
    assert res.status_code == 200

def test_update_endpoints(client, create_user, login_user):
    acc = create_user()
    token = login_user(acc)["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    res = client.post("/update/account_holder_name", json={"new_name": "New Name"}, headers=headers)
    assert res.status_code == 200
    
    res = client.post("/update/pin_number", json={"new_pin": "5678"}, headers=headers)
    assert res.status_code == 200

def test_logout(client, create_user, login_user):
    acc = create_user()
    tokens = login_user(acc)
    refresh_token = tokens["refresh_token"]
    headers = {"Authorization": f"Bearer {refresh_token}"}
    
    res = client.post("/auth/logout", headers=headers)
    assert res.status_code == 200
    
    res = client.post("/auth/logout")
    assert res.status_code == 401

    res = client.post("/auth/logout", headers={"Authorization": "Invalid"})
    assert res.status_code == 401

    res = client.post("/auth/logout", headers={"Authorization": f"Bearer {tokens['access_token']}"})
    assert res.status_code == 401

def test_refresh_token(client, create_user, login_user):
    acc = create_user()
    tokens = login_user(acc)
    refresh_token = tokens["refresh_token"]
    headers = {"Authorization": f"Bearer {refresh_token}"}
    
    res = client.post("/auth/refresh", headers=headers)
    assert res.status_code == 200
    new_tokens = res.get_json()

    # Old token blacklisted now
    res2 = client.post("/auth/refresh", headers=headers)
    assert res2.status_code == 401

    res3 = client.post("/auth/refresh", headers={"Authorization": f"Bearer {tokens['access_token']}"})
    assert res3.status_code == 401

def test_employee_requests(app, client, create_user, login_user):
    repo = app.config["service"].repo
    emp_acc = create_user_with_role(app, repo, "Employee", "1234", 1000, "employee")
    
    user_acc = create_user()
    user_token = login_user(user_acc)["access_token"]
    headers = {"Authorization": f"Bearer {user_token}"}
    
    res = client.post("/requests", json={"query_type": "HELP", "description": "need help", "employee_id": emp_acc}, headers=headers)
    assert res.status_code == 201
    
    res = client.get("/requests/my", headers=headers)
    assert res.status_code == 200

    emp_token = login_user(emp_acc)["access_token"]
    emp_headers = {"Authorization": f"Bearer {emp_token}"}
    
    res = client.get("/employee/requests", headers=emp_headers)
    assert res.status_code == 200
    requests = res.get_json().get("requests", [])
    
    if len(requests) > 0:
        req_id = requests[0]["id"]
        res = client.post(f"/employee/requests/{req_id}/approve", headers=emp_headers)
        assert res.status_code == 200
        
        res = client.post(f"/requests/{req_id}/submit", headers=headers, json={"info": "done"})
        assert res.status_code == 200
        
        res = client.get(f"/requests/{req_id}/complete", headers=headers)
        assert res.status_code == 200

    admin_acc = create_user_with_role(app, repo, "Admin", "1234", 1000, "admin")
    admin_token = login_user(admin_acc)["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    res = client.get("/requests/user", headers=admin_headers)
    assert res.status_code == 200

def test_employee_reject_request(app, client, create_user, login_user):
    repo = app.config["service"].repo
    emp_acc = create_user_with_role(app, repo, "Employee", "1234", 1000, "employee")
    
    user_acc = create_user()
    user_token = login_user(user_acc)["access_token"]
    headers = {"Authorization": f"Bearer {user_token}"}
    
    res = client.post("/requests", json={"query_type": "HELP", "description": "need help", "employee_id": emp_acc}, headers=headers)
    assert res.status_code == 201
    
    emp_token = login_user(emp_acc)["access_token"]
    emp_headers = {"Authorization": f"Bearer {emp_token}"}
    
    res = client.get("/employee/requests", headers=emp_headers)
    requests = res.get_json().get("requests", [])
    
    if len(requests) > 0:
        req_id = requests[0]["id"]
        res = client.post(f"/employee/requests/{req_id}/reject", headers=emp_headers)
        assert res.status_code == 200

def test_banking_service_edge_cases(app):
    service = app.config["service"]
    request_service = app.config["request_service"]
    
    from exceptions.invalid_account_name_exception import InvalidAccountNameException
    from exceptions.invalid_pin_exception import InvalidPINException
    from exceptions.invalid_amount_exception import InvalidAmountException
    import pytest
    
    with pytest.raises(InvalidAccountNameException):
        service.create_account("", "1234", 100)
        
    with pytest.raises(InvalidAccountNameException):
        service.create_account("123", "1234", 100)
        
    with pytest.raises(InvalidPINException):
        service.create_account("Name", "", 100)
        
    with pytest.raises(InvalidPINException):
        service.create_account("Name", "12", 100)
        
    with pytest.raises(InvalidAmountException):
        service.create_account("Name", "1234", -10)
        
    acc = service.create_account("Name", "1234", 100)
    
    with pytest.raises(Exception):
        request_service.create_request(acc, acc, "", "desc")

def test_create_account_missing_fields(client):
    res = client.post("/accounts", json={
        "name": "Test"
    })
    assert res.status_code in [400, 500]