# app/__init__.py
from flask import Flask
from .auth import auth, oauth, github

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    oauth.init_app(app)

    app.register_blueprint(auth)

    return app

# config.py
import os
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'random_secret_key')
    GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
