from flask import g, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

limiter = Limiter(
    key_func=lambda: str(getattr(g, "account_number", get_remote_address())),
    enabled=lambda: current_app.config.get("RATELIMIT_ENABLED", True),  # ✅ KEY FIX
    default_limits=["100 per hour"]
)