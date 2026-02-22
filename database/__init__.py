import sqlite3
import os

#!PATH HANDLING↓import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "accounts.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number INTEGER NOT NULL UNIQUE,
    account_holder_name TEXT NOT NULL,
    balance REAL NOT NULL,
    created_at TEXT NOT NULL,
    pin_hash TEXT NOT NULL,
    failed_attempts INTEGER DEFAULT 0,
    is_locked INTEGER DEFAULT 0
);
""")
c.execute("""

          CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number INTEGER NOT NULL,
    transaction_type TEXT NOT NULL,   
    amount REAL NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (account_number) REFERENCES accounts(account_number)
);
""")
conn.commit()
conn.close()
