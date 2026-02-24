from flask import Flask
from repository.account_repository import AccountRepository
from services.banking_services import BankingServices
from app.config import Config
import os
import logging
from logging.handlers import RotatingFileHandler

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    #dependency injection
    repo = AccountRepository()
    service = BankingServices(repo,app.config["ADMIN_KEY"],app.logger)

    app.config["service"] = service

    os.makedirs(os.path.dirname(app.config["LOG_FILE"]), exist_ok=True)
    #loggin setup
    file_handler = RotatingFileHandler(app.config.get("LOG_FILE","banking_core.log"),maxBytes=10240,backupCount=5)

    file_handler.setLevel(app.config["LOG_LEVEL"])
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler.setFormatter(formatter)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(app.config["LOG_LEVEL"])

    #register routes and errors
    from app.routes import register_routes
    from app.errors import register_error_handlers

    register_routes(app)
    register_error_handlers(app)

    return app


