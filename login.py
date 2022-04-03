from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from flask_sqlalchemy import SQLAlchemy
from appConfig import app, User
from flask_login import login_user
from werkzeug.security import check_password_hash

db=SQLAlchemy()

layout = html.Div([
        dcc.Location(id='urlLogin', refresh=True),
        dbc.Container([
            html.Img(src='https://www.ukdw.ac.id/wp-content/uploads/2017/10/fti-ukdw.png',),
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Label('Username', htmlFor='floatingInput'),
                    ]),
                    html.Div([
                        #html.Label('Username', htmlFor='floatingInput'),
                        dcc.Input(
                            type='text',
                            className='form-control',
                            id='usernameBox',
                            placeholder='Username',
                            n_submit=0,style={'border-radius':'10px'}),
                    ], className='form-floating'),
                    html.Br(),
                    html.Div([
                        #html.H6('Password'),
                        html.Label('Password', htmlFor='floatingInput'),
                    ]),
                    html.Div([

                        dcc.Input(type='password', className='form-control', id='passwordBox', n_submit=0,style={'border-radius':'10px'}),
                    ], className='form-floating'),
                    html.Label(id='errorText',className='text-danger'),
                    html.Button('LOGIN', n_clicks=0, className='btn btn-lg btn-primary',
                                style={'margin-top': '25px', 'width': '100%','border-radius':'10px'}, id='loginButton')
                ], className='form-group'),
            ], style={'width': '25%','border-radius':'10px'}, className='card border-primary mb-3')
        ], style={'width': '100%', 'height': '90vh', 'align-items': 'center', 'display': 'flex','justify-content': 'center'}, fluid=True)
    ], style={'width': '100%', 'position': 'sticky', 'top': '0', 'zIndex': '3'})


# REDIRECT TO HOME IF LOGIN DETAILS ARE CORRECT
@app.callback(Output('urlLogin', 'pathname'),
              [Input('loginButton', 'n_clicks'),
              Input('usernameBox', 'n_submit'),
              Input('passwordBox', 'n_submit')],
              [State('usernameBox', 'value'),
               State('passwordBox', 'value')])
def sucess(n_clicks, usernameSubmit, passwordSubmit, username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            return '/home'
        else:
            pass
    else:
        pass
    db.session.commit()

# RETURN RED BOXES IF LOGIN DETAILS INCORRECT
@app.callback(Output('usernameBox', 'className'),Output('passwordBox', 'className'),Output('errorText', 'children'),
              [Input('loginButton', 'n_clicks'),
              Input('usernameBox', 'n_submit'),
              Input('passwordBox', 'n_submit')],
              [State('usernameBox', 'value'),
               State('passwordBox', 'value')])
def update_output(n_clicks, usernameSubmit, passwordSubmit, username, password):
    if (n_clicks > 0) or (usernameSubmit > 0) or (passwordSubmit) > 0:
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                return 'form-control','form-control',''
            else:
                return 'form-control is-invalid','form-control is-invalid','Username or Password is Invalid'
        else:
            return 'form-control is-invalid','form-control is-invalid','Username or Password is Invalid'
    else:
        return 'form-control','form-control',''