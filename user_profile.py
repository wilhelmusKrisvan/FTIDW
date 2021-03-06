from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from appConfig import app
from model.user import update_password
from flask_login import current_user
from werkzeug.security import check_password_hash


layout = dbc.Container([
    html.Br(),
    dbc.Container([
        dcc.Location(id='urlProfile', refresh=True),
        html.H3('Profile'),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dbc.Label('Username:'),
                html.Br(),
                dbc.Label('Email:'),
            ], md=2),
            dbc.Col([
                dbc.Label(id='username', className='text-primary'),
                html.Br(),
                dbc.Label(id='email', className='text-primary'),
            ], md=4),
            dbc.Col([
                dbc.Label('Old Password: '),
                dcc.Input(
                    id='oldPassword',
                    type='password',
                    className='form-control',
                    placeholder='old password',
                    n_submit=0,
                    style={
                        'width' : '40%','border-radius':'10px'
                    },
                ),
                html.Br(),
                dbc.Label('New Password: '),
                dcc.Input(
                    id='newPassword1',
                    type='password',
                    className='form-control',
                    placeholder='new password',
                    n_submit=0,
                    style={
                        'width' : '40%','border-radius':'10px'
                    },
                ),
                dbc.Label('Retype New Password: '),
                dcc.Input(
                    id='newPassword2',
                    type='password',
                    className='form-control',
                    placeholder='retype new password',
                    n_submit=0,
                    style={
                        'width' : '40%','border-radius':'10px'
                    },
                ),
                html.Br(),
                html.Button(
                    children='Update Password',
                    id='updatePasswordButton',
                    n_clicks=0,
                    type='submit',
                    className='btn btn-primary btn-lg',
                    style={'border-radius':'10px'}
                ),
                html.Br(),
                html.Div(id='updateSuccess')
            ], md=6),
        ]),
    ], className='jumbotron',style={'border-radius':'10px'})
])

@app.callback(
    Output('username', 'children'),
    Output('email', 'children'),
    [Input('pageContent', 'children')])
def currentUserName(pageContent):
    try:
        username = current_user.username
        email = current_user.email
        return username,email
    except AttributeError:
        return '',''

# UPDATE PWD BUTTON CLICKED / ENTER PRESSED - UPDATE DATABASE WITH NEW PASSWORD
@app.callback(Output('updateSuccess', 'children'),
              [Input('updatePasswordButton', 'n_clicks'),
              Input('newPassword1', 'n_submit'),
              Input('newPassword2', 'n_submit')],
              [State('oldPassword', 'value'),
              State('newPassword1', 'value'),
               State('newPassword2', 'value')])
def changePassword(n_clicks, newPassword1Submit, newPassword2Submit,
                    oldPassword, newPassword1, newPassword2):
    if (n_clicks > 0) or (newPassword1Submit > 0) or (newPassword2Submit) > 0:
        if oldPassword==newPassword1:
            return html.Div(children=['The Old Password Cannot be The Same as The New Password'], className='text-danger')
        else:
            if check_password_hash(current_user.password, oldPassword) and newPassword1 == newPassword2:
                try:
                    update_password(current_user.username, newPassword1)
                    return html.Div(children=['Update Successful'], className='text-success')
                except Exception as e:
                    return html.Div(children=['Update Not Successful: {e}'.format(e=e)], className='text-danger')
            else:
                return html.Div(children=['Old Password Invalid'], className='text-danger')

# UPDATE PWD BUTTON CLICKED / ENTER PRESSED - RETURN RED BOXES IF OLD PWD IS NOT CURR PWD
@app.callback(Output('oldPassword', 'className'),
              [Input('updatePasswordButton', 'n_clicks'),
              Input('newPassword1', 'n_submit'),
              Input('newPassword2', 'n_submit')],
              [State('oldPassword', 'value'),
              State('newPassword1', 'value'),
               State('newPassword2', 'value')])
def validateOldPassword(n_clicks, newPassword1Submit, newPassword2Submit,
                    oldPassword, newPassword1, newPassword2):
    if (n_clicks > 0) or (newPassword1Submit > 0) or (newPassword2Submit) > 0:
        if check_password_hash(current_user.password, oldPassword):
            return 'form-control is-valid'
        else:
            return 'form-control is-invalid'
    else:
        return 'form-control'

# UPDATE PWD BUTTON CLICKED / ENTER PRESSED - RETURN RED BOXES IF NEW PASSWORDS ARE NOT THE SAME
@app.callback(Output('newPassword1', 'className'),Output('newPassword2', 'className'),
              [Input('updatePasswordButton', 'n_clicks'),
              Input('newPassword1', 'n_submit'),
              Input('newPassword2', 'n_submit')],
              [State('newPassword1', 'value'),
               State('newPassword2', 'value')])
def validatePassword(n_clicks, newPassword1Submit, newPassword2Submit, newPassword1, newPassword2):
    if (n_clicks > 0) or (newPassword1Submit > 0) or (newPassword2Submit) > 0:
        if newPassword1 == newPassword2:
            return 'form-control is-valid','form-control is-valid'
        else:
            return 'form-control is-invalid','form-control is-invalid'
    else:
        return 'form-control','form-control'