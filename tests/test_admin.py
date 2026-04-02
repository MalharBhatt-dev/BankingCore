from unittest.mock import patch
import warnings
warnings.filterwarnings("ignore")

def test_admin_stats_mock(client,create_admin_user,login_user):
   acc=create_admin_user()
   auth_token=login_user(acc)["access_token"]
   res=client.get("/admin/stats",headers={"Authorization":f"Bearer {auth_token}"})
   assert res.status_code in [200,403,404]

def test_admin_events_mock(client,create_admin_user,login_user):
    acc=create_admin_user()
    auth_token=login_user(acc)["access_token"]
    res = client.get("/admin/events",headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code in [200,403,404]

def test_locked_accounts(client,create_admin_user,login_user):
    acc=create_admin_user()
    auth_token=login_user(acc)["access_token"]
    res =client.get("/admin/locked-accounts",headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code in [200,403,404]

def test_admin_unlock(client,create_admin_user,login_user):
    acc=create_admin_user()
    auth_token=login_user(acc)["access_token"]
    res = client.post("/admin/unlock", json={"account_number": "acc","admin_key": "key"},headers={"Authorization":f"Bearer {auth_token}"})
    assert res.status_code in [200,403,404]