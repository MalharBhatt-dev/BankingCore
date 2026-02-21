class Transaction:
    def __init__(self,account_number,transaction_type,amount,balance_after,timestamp):
        self.account_number = account_number
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance_after = balance_after
        self.timestamp = timestamp