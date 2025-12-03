from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

myapp_obj = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

myapp_obj.config.from_mapping(
    SECRET_KEY = 'you-will-never-guess',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
)

db = SQLAlchemy(myapp_obj)
migrate = Migrate(myapp_obj, db)

login_manager = LoginManager()
login_manager.init_app(myapp_obj)
login_manager.login_view = 'login'

from app import routes, models
