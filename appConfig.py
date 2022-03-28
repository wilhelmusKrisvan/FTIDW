# Dash app initialization
import dash
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
# DB User
from flask_sqlalchemy import SQLAlchemy
# User management initialization
import os
import warnings
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin
# from model.user import User as base
import configparser
from model.user import User

warnings.filterwarnings("ignore")
# connect = 'mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/operasional'
connect = 'mysql+pymysql://admin:admin@localhost:3333/ftidw'

db = SQLAlchemy()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
server = app.server
app.config.suppress_callback_exceptions = True

# config
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI=connect,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ENGINE_OPTIONS={
        "max_overflow": 0,
        "pool_pre_ping": True,
        "pool_recycle": 60 * 60,
        "pool_size": 30,
    }
)

db.init_app(server)

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


# Create User class with UserMixin
class User(UserMixin, User):
    pass


# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    db.session.remove()
    return user
