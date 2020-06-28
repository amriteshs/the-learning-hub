from flask import *
import os
import psycopg2
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_bootstrap import Bootstrap
from rasa.nlu.model import Interpreter
from flasgger import Swagger


app = Flask(__name__, static_url_path = "/extra", static_folder = "extra")
app.config['SECRET_KEY'] = "secret key"

UPLOAD_FOLDER = 'questions'
ALLOWED_EXTENSIONS = set(['txt', 'tsv', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI']='postgres://comp9323_admin@comp9323:password_123@comp9323.postgres.database.azure.com:5432/postgres'
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
manage_login = LoginManager()
manage_login.init_app(app)
manage_login.login_view = 'login'
template = {
    "swagger": "2.0",
    "info": {
        "title": "The Learning Hub API",
        "description": ""
    }
}
Swagger(app, template = template)


@manage_login.user_loader
def load_user(user_id):
    return User_.query.get(int(user_id))


class User_(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(10))
    last_name = db.Column(db.String(10))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


from app import views
from app.models.livechat import *
