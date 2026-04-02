import os
import logging
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
load_dotenv(os.path.join(BASE_DIR,".env"))

class Config:

    BASE_DIR = BASE_DIR

    SECRET_KEY =os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is not set") 
    
    ADMIN_KEY = os.getenv("ADMIN_KEY")
    if not ADMIN_KEY:
        raise ValueError("ADMIN_KEY environment variable is not set")
    
    uri= os.getenv("DATABASE_URL")
    if uri and uri.startswith("postgres://"):
        uri=uri.replace("postgres://","postgresql://",1)

    SQLALCHEMY_DATABASE_URI = uri or "sqlite:///local.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = os.getenv("FLASK_DEBUG","0") == "1"
    
    LOG_FILE = os.path.join(BASE_DIR, "logs", "banking_core.log")
    LOG_LEVEL = logging.INFO

    LOG_TO_FILE = True

class TestConfig(Config):
    TESTING = True
    LOG_TO_FILE = False
    DATABASE = ":memory:"