from app import create_app
from app.extensions import db
from flask_migrate import Migrate
from app.config import Config

app = create_app(Config)
migrate = Migrate(app, db)