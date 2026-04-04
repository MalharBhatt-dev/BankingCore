from flask import Flask

app = Flask(__name__)
print("🔥 NEW BUILD RUNNING")

from app import create_app

print("🔥 USING CREATE_APP")

app = create_app()