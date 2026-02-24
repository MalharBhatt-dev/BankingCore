import os
import logging
from dotenv import load_dotenv
class Config:
    load_dotenv()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 

    SECRET_KEY =os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is not set") 
    
    ADMIN_KEY = os.getenv("ADMIN_KEY")
    if not ADMIN_KEY:
        raise ValueError("ADMIN_KEY environment variable is not set")
    
    DEBUG = os.getenv("FLASK_DEBUG","false").lower() == "true"
    
    LOG_FILE = os.path.join(BASE_DIR, "logs", "banking_core.log")
    LOG_LEVEL = logging.INFO