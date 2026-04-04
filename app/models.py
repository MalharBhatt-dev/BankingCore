from app.extensions import db
from datetime import datetime

class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.Integer, unique=True, nullable=False)
    account_holder_name = db.Column(db.String(100), nullable=False)
    pin_hash = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    failed_attempts = db.Column(db.Integer, default=0)
    is_locked = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default="user")
    account_type = db.Column(db.String(20), default="savings")
    employee_id = db.Column(db.String(50))

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.Integer)
    transaction_type = db.Column(db.String(50))
    amount = db.Column(db.Float)
    balance_after = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class ServiceRequest(db.Model):
    __tablename__ = "service_requests"

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.Integer)
    query_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default="PENDING")
    employee_id = db.Column(db.Integer)
    approved_by_employee = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)


class RequestSubmission(db.Model):
    __tablename__ = "request_submissions"

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer)
    account_number = db.Column(db.Integer)
    submission_data = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

class TokenBlacklist(db.Model):
    __tablename__ = "token_blacklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(255), unique=True)
    revoked_at = db.Column(db.DateTime)