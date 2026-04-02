def user_payload(name="Test User"):
    return {
        "name":name,
        "pin":"1234",
        "account_type":"SAVINGS",
        "initial_deposit":1000
    }

def transfer_payload(to_account,amount=100):
    return {
        "to_account":to_account,
        "amount":amount
    }