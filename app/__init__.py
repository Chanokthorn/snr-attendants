from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder="profiles")
CORS(app, supports_credentials=True)
app.config.from_object(Config)
login = LoginManager(app)
db = SQLAlchemy(app)


def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            print('current user: ', current_user)
            if not current_user.is_authenticated:
                return "unauthorized" 
            print('current role: ', current_user.get_role())
            urole = current_user.get_role()
            if ( (urole != role) and (role != "ANY")):
                return "insufficient role permission"     
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

from app import routes, models