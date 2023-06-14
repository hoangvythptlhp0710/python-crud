from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    # v1
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    # v2
    login_manager.init_app(app)
    login_manager.login_message = "You must log in to access to the webpage"
    login_manager.login_view = "auth.login"

    # v3
    migrate = Migrate(app, db)
    from app import models



    return app
