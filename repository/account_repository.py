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
        

    def get_account(self,account_number):
        c = self.conn.cursor()
        c.execute("""select account_number,account_holder_name,pin_hash,balance,created_at,failed_attempts,is_locked,role
                    from accounts 
                    where account_number = ?""",(account_number,))
        acc = c.fetchone()
        if acc is None:
            return None
        
        return Account(acc[0],acc[1],acc[2],acc[3],acc[4],acc[5],acc[6],acc[7])
    
    def insert_account(self,account_number,name, pin_hash ,balance,role):
        created_at = datetime.now().strftime("%D-%M-%Y %H:%M:%S")
        failed_attempts = 0
        is_locked = 0
        c = self.conn.cursor()
        c.execute("""insert into accounts (account_number, account_holder_name ,pin_hash,balance,created_at, failed_attempts,is_locked,role) values(? , ? , ? , ?, ?, ?, ?, ?)""",(account_number , name , pin_hash , balance , created_at,failed_attempts,is_locked,role))
       

    def update_balance(self,account_number,new_balance):
        c = self.conn.cursor()
        c.execute("""update accounts 
                       set balance = ? 
                       where account_number = ?"""
                       ,(new_balance,account_number))
        
#!After insert_transaction(), → Proper separation
#!     we achieve.            → Audit trail capability
#!                            → Foundation for atomic transactions ↓
    def insert_transaction(self,account_number,type,amount,balance_after):
        c = self.conn.cursor()
        timestamp = datetime.now().isoformat()
        c.execute("""insert into transactions (account_number,transaction_type,amount,balance_after,timestamp) values (?,?,?,?,?)""",(account_number,type,amount,balance_after,timestamp))
    
    def get_last_account_number(self):
        c = self.conn.cursor()
        c.execute("select max(account_number) from accounts")
        last_acc_no= c.fetchone()
        if last_acc_no is None or last_acc_no[0] is None:
            return None
        return last_acc_no[0]
    
    def get_transactions(self,account_number):
        c = self.conn.cursor()
        c.execute("""select * from transactions where account_number = ? order by timestamp DESC""",(account_number,))
        rows = c.fetchall()
        transactions = []

        for row in rows:
            txn = Transaction(row[1],row[2],row[3],row[4],row[5])
            transactions.append(txn)
        return transactions
    
    def update_security_state(self,account_number,failed_attempts,is_locked):
        c = self.conn.cursor()
        c.execute("""update accounts
                       set failed_attempts = ? , is_locked =?
                       where account_number = ?""",(failed_attempts,is_locked,account_number))
        
    def unlock_account(self,account_number):
        c = self.conn.cursor()
        c.execute("""update accounts
                       set failed_attempts = 0 , is_locked = 0
                       where account_number = ?""",(account_number,))
    
    def get_total_balance(self):
        c=self.conn.cursor()
        c.execute("""select sum(balance) from accounts""")
        result = c.fetchone()
        return result[0] or 0

    def get_total_accounts_count(self):
        c=self.conn.cursor()
        c.execute("""select count(*) from accounts""")
        return c.fetchone()[0]
    
    def get_locked_accounts_count(self):
        c=self.conn.cursor()
        c.execute("""select count(*) from accounts where is_locked = 1""")
        return c.fetchone()[0]
    
    def get_locked_accounts(self):
        c =self.conn.cursor()
        c.execute("""select account_number,account_holder_name,failed_attempts
                  from accounts where is_locked = 1 order by account_number""")
        rows  = c.fetchall()
        result = []
        for row in rows :
            result.append({"account_number":row[0],
                           "name":row[1],
                           "failed_attempts":row[2]})
        return result


    def get_last_account_lock_event(self):
        c = self.conn.cursor()
        c.execute("""select account_number , transaction_type , timestamp
                  from transactions where transaction_type in ('ACCOUNT_LOCKED','ACCOUNT_UNLOCKED')
                  order by timestamp desc limit 1""")
        row = c.fetchone()
        if not row:
            return None
        return {"account_number":row[0],"event":row[1],"timestamp":row[2]}
    
    def get_security_events(self):
        c=self.conn.cursor()
        c.execute(""" SELECT account_number, transaction_type, balance_after, timestamp
        FROM transactions
        WHERE transaction_type IN ('ACCOUNT_LOCKED','ACCOUNT_UNLOCKED')
        ORDER BY timestamp DESC
        LIMIT 20""")
        rows = c.fetchall()
        events = []
        for row in rows:
            events.append(Transaction(row[0], row[1], 0, row[2], row[3]))
        return events

    def blacklist_jti(self,jti):
        c = self.conn.cursor()
        revoked_at = datetime.now().isoformat()
        c.execute("""insert into token_blacklist (jti,revoked_at) values (?,?)""",(jti,revoked_at))
        

    def is_token_blacklisted(self,jti):
        c = self.conn.cursor()
        c.execute("""select 1 from token_blacklist where jti = ?""",(jti,))
        return c.fetchone() is not None
    
    #~ Updating the account Porperties....
    def update_account_holder_name(self,account_number,account_holder_name):
        c= self.conn.cursor()
        c.execute("""update accounts set account_holder_name = ? where account_number = ?""",(account_holder_name,account_number))
        
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

