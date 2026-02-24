import os
import logging
from dotenv import load_dotenv
class Config:
    load_dotenv()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
    SECRET_KEY =os.getenv("SECRET_KEY","dev_secret_key") 
    ADMIN_KEY = os.getenv("ADMIN_KEY", "dev_admin_key")
    DEBUG = os.getenv("FLASK_DEBUG","TRUE").lower() == "true"
    LOG_FILE = os.path.join(BASE_DIR, "logs", "banking_core.log")
    LOG_LEVEL = logging.INFO