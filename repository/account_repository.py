import sqlite3
import os
from entities.account import Account
from entities.transaction import Transaction
from datetime import datetime

class AccountRepository:
    
    def __init__(self):

        #!PATH HANDLING↓import os
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        DB_PATH = os.path.join(BASE_DIR, "database", "accounts.db")

        self.conn = sqlite3.connect(DB_PATH,check_same_thread=False)
        self.conn.execute("PRAGMA foreign_key = ON")
        self.c = self.conn.cursor()

    def get_account(self,account_number):
        self.c.execute("""select account_number,account_holder_name,pin_hash,balance,created_at,failed_attempts,is_locked
                    from accounts 
                    where account_number = ?""",(account_number,))
        acc = self.c.fetchone()
        if acc is None:
            return None
        return Account(acc[0],acc[1],acc[2],acc[3],acc[4],acc[5],acc[6])
    
    def insert_account(self,account_number,name, pin_hash ,balance):
        created_at = datetime.now().strftime("%D-%M-%Y %H:%M:%S")
        failed_attempts = 0
        is_locked = 0
        self.c.execute("""insert into accounts (account_number, account_holder_name ,pin_hash,balance,created_at, failed_attempts,is_locked) values(? , ? , ? , ?, ?, ?, ?)""",(account_number , name , pin_hash , balance , created_at,failed_attempts,is_locked))
       

    def update_balance(self,account_number,new_balance):
        self.c.execute("""update accounts 
                       set balance = ? 
                       where account_number = ?"""
                       ,(new_balance,account_number))
        
#!After insert_transaction(), → Proper separation
#!     we achieve.            → Audit trail capability
#!                            → Foundation for atomic transactions ↓
    def insert_transaction(self,account_number,type,amount,balance_after):
        timestamp = datetime.now().isoformat()
        self.c.execute("""insert into transactions (account_number,transaction_type,amount,balance_after,timestamp) values (?,?,?,?,?)""",(account_number,type,amount,balance_after,timestamp))
    
    def get_last_account_number(self):
        self.c.execute("select max(account_number) from accounts")
        last_acc_no= self.c.fetchone()
        if last_acc_no is None or last_acc_no[0] is None:
            return None
        return last_acc_no[0]
    
    def get_transactions(self,account_number):
        self.c.execute("""select * from transactions where account_number = ? order by timestamp DESC""",(account_number,))
        rows = self.c.fetchall()
        transactions = []

        for row in rows:
            txn = Transaction(row[1],row[2],row[3],row[4],row[5])
            transactions.append(txn)
        return transactions
    
    def update_security_state(self,account_number,failed_attempts,is_locked):
        self.c.execute("""update accounts
                       set failed_attempts = ? , is_locked =?
                       where account_number = ?""",(failed_attempts,is_locked,account_number))
        
    def unlock_account(self,account_number):
        self.c.execute("""update accounts
                       set failed_attempts = 0 , is_locked = 0
                       where account_number = ?""",(account_number,))

    def commit(self):
        self.conn.commit()
    
    def rollback(self):
        self.conn.rollback()
    
    def close(self):
        self.conn.close()

# ac = AccountRepository()
# ac.get_account(1001)

#NOTE :
#?What is Repository Responsible For?
#? Repository only:→Talks to database,→Executes SQL,→Returns raw data.

#?Where should the database path logic go? Inside constructor or outside?
#?→ constructor — because connection belongs to repository instance.

#?Should repository check if account already exists?
#?→ No. That’s service layer responsibility.

#?Should repository generate account number?
#?→ No. Service layer responsibility.

#?Should repository commit automatically?
#?→ Yes for account creation (since it's a single operation).

