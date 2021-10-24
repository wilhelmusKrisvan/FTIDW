# Dash app initialization
import dash
import dash_bootstrap_components as dbc

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
connect=connect='mysql+pymysql://wilhelmus:TAhug0r3ng!@localhost:3333/operasional'

db = SQLAlchemy()
config = configparser.ConfigParser()

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.COSMO])
server = app.server
app.config.suppress_callback_exceptions = True


# config
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI=connect,
    SQLALCHEMY_TRACK_MODIFICATIONS=False
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
    return User.query.get(int(user_id))

