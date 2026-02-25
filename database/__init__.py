import sqlite3
import os

#!PATH HANDLING↓import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "accounts.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# c.execute("""CREATE TABLE IF NOT EXISTS accounts (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     account_number INTEGER NOT NULL UNIQUE,
#     account_holder_name TEXT NOT NULL,
#     pin_hash TEXT NOT NULL,
#     balance REAL NOT NULL,
#     created_at TEXT NOT NULL,
#     failed_attempts INTEGER DEFAULT 0,
#     is_locked INTEGER DEFAULT 0
# );
# """)
# c.execute("""

#           CREATE TABLE IF NOT EXISTS transactions (
#     transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     account_number INTEGER NOT NULL,
#     transaction_type TEXT NOT NULL,   
#     amount REAL NOT NULL,
#     balance_after REAL not null,
#     timestamp TEXT NOT NULL,
#     FOREIGN KEY (account_number) REFERENCES accounts(account_number)
# );
# """)

# c.execute("""
# create table if not exists token_blacklist(
#           id integer primary key autoincrement,
#           jti text not null unique,
#           revoked_at text not null)
# """)

# c.execute("PRAGMA table_info(accounts)")
# columns = [row[1] for row in c.fetchall()]

# if "role" not in columns:
#     c.execute("ALTER TABLE accounts ADD COLUMN role TEXT DEFAULT 'user' ")

c.execute("update accounts set role ='admin' where account_number = 1003")
conn.commit()
conn.close()
