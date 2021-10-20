import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from appConfig import app
from flask_login import logout_user, current_user


icon = 'https://amigogroup.co.id/wp-content/uploads/2020/06/AmigoHeader-e1593098882452.png'
icnBrand = 'https://www.ukdw.ac.id/wp-content/uploads/2017/10/fti-ukdw.png'

layout = dbc.Container([

        html.H2('Page 1 Layout'),
        html.Hr(),


], className="mt-4")