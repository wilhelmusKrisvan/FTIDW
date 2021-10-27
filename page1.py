import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from appConfig import app
from flask_login import logout_user, current_user

icnBrand = 'https://www.ukdw.ac.id/wp-content/uploads/2017/10/fti-ukdw.png'

layoutAdmin = dbc.Container([

        html.H2('Page 1 Layout Admin'),
        html.Hr(),


], className="mt-4")

layout =dbc.Container([

        html.H2('Page 1 Layout User'),
        html.Hr(),


], className="mt-4")
