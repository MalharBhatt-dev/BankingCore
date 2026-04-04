from flask_cors import CORS
from flask import Flask
from flask_talisman import Talisman
from repository.account_repository import AccountRepository
from repository.service_request_repository import ServiceRequestRepository
from services.banking_services import BankingServices
from services.service_request_service import ServiceRequestService
from app.extensions import limiter,db,migrate
from app.config import Config
import os
import logging
from logging.handlers import RotatingFileHandler

def create_app(config_class=Config):
    print("starting app...")
    try:
        app = Flask(__name__,static_folder="static",template_folder="templates")
        print("Flask created")
    
        CORS(app)
        limiter.init_app(app)
        app.config.from_object(config_class)
        print("config loaded")
        db.init_app(app)
        print("db inititaled.")
        migrate.init_app(app,db)
        print("migration completed.")
        #dependency injection
        repo = AccountRepository()
        service = BankingServices(repo,app.config["ADMIN_KEY"],app.logger)
        app.config["service"] = service

        #dependecy injection for service_request
        request_repo = ServiceRequestRepository()
        request_service = ServiceRequestService(request_repo,app.logger)
        app.config["request_service"] = request_service

        #loggin setup
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

        if not app.logger.handlers:
            if not app.config.get("TESTING"):
                log_dir = os.path.dirname(app.config["LOG_FILE"])
                if log_dir :
                    os.makedirs(log_dir,exist_ok=True)
                handler = RotatingFileHandler(app.config.get("LOG_FILE","banking_core.log"),maxBytes=10240,backupCount=5)
            else : 
                handler = logging.StreamHandler()

            handler.setFormatter(formatter)
            app.logger.addHandler(handler)
            app.logger.setLevel(app.config["LOG_LEVEL"])

        csp={
            "default-src":["'self'"],
            "script-src":["'self'","'unsafe-inline'"],
            "style-src":["'self'","'unsafe-inline'"]
            }

        Talisman(app,content_security_policy=csp,force_https=False)
        #register routes and errors
        from app.routes import register_routes
        from app.errors import register_error_handlers

        register_routes(app)
        register_error_handlers(app)

        return app
    
    except Exception as e:
        print("Crash",str(e))
        raise