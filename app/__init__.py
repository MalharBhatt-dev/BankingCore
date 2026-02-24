from flask import Flask
from repository.account_repository import AccountRepository
from services.banking_services import BankingServices
from app.config import Config

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    #dependency injection
    repo = AccountRepository()
    service = BankingServices(repo,app.config["ADMIN_KEY"])

    app.config["service"] = service

    #register routes and errors
    from app.routes import register_routes
    from app.errors import register_error_handlers

    register_routes(app)
    register_error_handlers(app)

    return app


