from flask import Flask
app = Flask(__name__)
from app import create_app
app = create_app()