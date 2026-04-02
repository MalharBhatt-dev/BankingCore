from app.extensions import db
from app.models import Account, Transaction
from sqlalchemy import func
from datetime import datetime


class AccountRepository:

    def get_account(self, account_number):
        return Account.query.filter_by(account_number=account_number).first()

    def insert_account(self, account_number, name, pin_hash, balance, role):
        acc = Account(
            account_number=account_number,
            account_holder_name=name,
            pin_hash=pin_hash,
            balance=balance,
            role=role
        )
        db.session.add(acc)

    def update_balance(self, account_number, new_balance):
        acc = self.get_account(account_number)
        if acc:
            acc.balance = new_balance

    def insert_transaction(self, account_number, txn_type, amount, balance_after):
        txn = Transaction(
            account_number=account_number,
            transaction_type=txn_type,
            amount=amount,
            balance_after=balance_after,
            timestamp=datetime.utcnow()
        )
        db.session.add(txn)

    def get_last_account_number(self):
        return db.session.query(func.max(Account.account_number)).scalar()

    def get_transactions(self, account_number):
        return Transaction.query.filter_by(account_number=account_number)\
            .order_by(Transaction.timestamp.desc()).all()

    def update_security_state(self, account_number, failed_attempts, is_locked):
        acc = self.get_account(account_number)
        if acc:
            acc.failed_attempts = failed_attempts
            acc.is_locked = is_locked

    def unlock_account(self, account_number):
        acc = self.get_account(account_number)
        if acc:
            acc.failed_attempts = 0
            acc.is_locked = False

    def get_total_balance(self):
        return db.session.query(func.sum(Account.balance)).scalar() or 0

    def get_total_accounts_count(self):
        return db.session.query(func.count(Account.account_number)).scalar()

    def get_locked_accounts_count(self):
        return Account.query.filter_by(is_locked=True).count()

    def get_locked_accounts(self):
        accounts = Account.query.filter_by(is_locked=True).order_by(Account.account_number).all()
        return [
            {
                "account_number": acc.account_number,
                "name": acc.account_holder_name,
                "failed_attempts": acc.failed_attempts
            }
            for acc in accounts
        ]

    def get_last_account_lock_event(self):
        txn = Transaction.query.filter(
            Transaction.transaction_type.in_(["ACCOUNT_LOCKED", "ACCOUNT_UNLOCKED"])
        ).order_by(Transaction.timestamp.desc()).first()

        if not txn:
            return None

        return {
            "account_number": txn.account_number,
            "event": txn.transaction_type,
            "timestamp": txn.timestamp
        }

    def get_security_events(self):
        return Transaction.query.filter(
            Transaction.transaction_type.in_(["ACCOUNT_LOCKED", "ACCOUNT_UNLOCKED"])
        ).order_by(Transaction.timestamp.desc()).limit(20).all()

    def blacklist_jti(self, jti):
        from app.models import TokenBlacklist
        entry = TokenBlacklist(jti=jti, revoked_at=datetime.utcnow())
        db.session.add(entry)

    def is_token_blacklisted(self, jti):
        from app.models import TokenBlacklist
        return TokenBlacklist.query.filter_by(jti=jti).first() is not None

    def update_account_holder_name(self, account_number, name):
        acc = self.get_account(account_number)
        if acc:
            acc.account_holder_name = name

    def update_pin(self, account_number, hashed_pin):
        acc = self.get_account(account_number)
        if acc:
            acc.pin_hash = hashed_pin

    def commit(self):
        db.session.commit()

    def rollback(self):
        db.session.rollback()