from unittest.mock import patch

def test_admin_stats_mock(client,auth_headers):
   with patch("services.banking_services.BankingServices.get_total_balance") as mock:mock.return_value = 10000
   res=client.get("/admin/stats",headers=auth_headers)
   assert res.status_code in [200,403,401]

def test_locked_accounts(client,auth_headers):
    res =client.get("/admin/locked-accounts",headers=auth_headers)

    assert res.status_code in [200,403,401]