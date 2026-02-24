import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY","dev_secret_key")
    ADMIN_KEY = os.getenv("ADMIN_KEY","DEV_ADMIN_KEY")
    DEBUG= os.getenv("FLASK_DEBUG","True").lower() == "true"