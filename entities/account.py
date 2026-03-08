class Account:
    def __init__(self,account_number,account_holder_name,pin_hash,balance,created_at,failed_attempts,is_locked,role,account_type):
        self.account_number = account_number
        self.account_holder_name = account_holder_name
        self.pin_hash = pin_hash
        self.balance = balance
        self.created_at = created_at
        self.failed_attempts = failed_attempts
        self.is_locked = is_locked
        self.role = role
        self.account_type = account_type