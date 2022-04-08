from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash_table as dt
from appConfig import app, User
from model.user import add_user, show_role, show_users, update_role, delete_user
from dash.dependencies import Input, Output, State
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
users = show_users()
options = [
    {'label': 'Admin', 'value': 'admin'},
    {'label': 'Dekanat', 'value': 'dekanat'},
    {'label': 'Dosen', 'value': 'dosen'}]

layout = dbc.Container([
    dbc.Card([
        dcc.Location(id='urlUserAdmin', refresh=True),
        html.H3('Add New User'),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dbc.Label('Username: '),
                dcc.Input(
                    id='newUsername',
                    className='form-control',
                    n_submit=0,
                    style={
                        'width': '90%','border-radius':'10px'
                    },
                ),
                html.Br(),
                dbc.Label('Password: '),
                dcc.Input(
                    id='newPwd1',
                    type='password',
                    className='form-control',
                    n_submit=0,
                    style={
                        'width': '90%','border-radius':'10px'
                    },
                ),
                html.Br(),
                dbc.Label('Retype Password: '),
                dcc.Input(
                    id='newPwd2',
                    type='password',
                    className='form-control',
                    n_submit=0,
                    style={
                        'width': '90%','border-radius':'10px'
                    },
                ),
                html.Br(),
            ], md=4),

            dbc.Col([
                dbc.Label('Email: '),
                dcc.Input(
                    id='newEmail',
                    type='email',
                    className='form-control',
                    n_submit=0,
                    style={
                        'width': '100%','border-radius':'10px'
                    },
                ),
                html.Br(),
                dbc.Label('Role '),
                dcc.Dropdown(
                    id='admin',
                    style={
                        'width': '100%','border-radius':'10px'
                    },
                    options=[
                        {'label': 'Admin', 'value': 'admin'},
                        {'label': 'Dekanat', 'value': 'dekanat'},
                        {'label': 'Dosen', 'value': 'dosen'},
                    ],
                    value='dosen',
                    clearable=False
                ),
                html.Br(),
                html.Br(),
                html.Button(
                    children='Create User',
                    id='createUserButton',
                    n_clicks=0,
                    type='submit',
                    style={'margin-top': '8px','border-radius':'10px'},
                    className='btn btn-primary btn-block'
                ),
                html.Br(),
                html.Div(id='createUserSuccess')
            ], md=4),
            dbc.Col([

            ], md=4)
        ]),
    ], className='jumbotron',style={'border-radius':'10px','padding':'2.5%','margin':'2.5%'}),

    dbc.Card([
        html.H3('Manage Users'),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dt.DataTable(
                    id='users',
                    columns=[{'name': 'Username', 'id': 'username'},
                             {'name': 'Email', 'id': 'email'},
                             {'name': 'Role', 'id': 'role'}],
                    page_size=10
                ),
            ], md=12),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Label('Username: '),
                dcc.Dropdown(id='uname',style={'border-radius':'10px'})
            ], width=4),
            dbc.Col([
                dbc.Label('Role: '),
                dcc.Dropdown(
                    options=[
                        {'label': 'Admin', 'value': 'admin'},
                        {'label': 'Dekanat', 'value': 'dekanat'},
                        {'label': 'Dosen', 'value': 'dosen'}
                    ], id='fillRole', style={'border-radius':'10px'})
            ], width=4),
            dbc.Col([
                html.Br(),
                html.Button(
                    children='UPDATE',
                    id='updateUserBtn',
                    n_clicks=0,
                    disabled=True,
                    type='submit',
                    style={'margin-top': '8px','border-radius':'10px'},
                    className='btn btn-primary btn-block'
                ),
                html.Div(id='updateUserSuccess'),
            ], width=2),
            dbc.Col([
                html.Br(),
                html.Button(
                    children='DELETE',
                    id='deleteUserBtn',
                    n_clicks=0,
                    disabled=True,
                    type='submit',
                    style={'margin-top': '8px','border-radius':'10px'},
                    className='btn btn-danger btn-block'
                ),
                html.Div(id='deleteUserSuccess')
            ], width=2),
        ]),
    ], className='jumbotron',style={'border-radius':'10px','padding':'2.5%','margin':'2.5%'})
], style={'margin-top': '25px'})


# CREATE USER BUTTON CLICKED / ENTER PRESSED - UPDATE DATABASE WITH NEW USER
@app.callback(Output('createUserSuccess', 'children'),
              [Input('createUserButton', 'n_clicks'),
               Input('newUsername', 'n_submit'),
               Input('newPwd1', 'n_submit'),
               Input('newPwd2', 'n_submit'),
               Input('newEmail', 'n_submit')],
              [State('newUsername', 'value'),
               State('newPwd1', 'value'),
               State('newPwd2', 'value'),
               State('newEmail', 'value'),
               State('admin', 'value')])
def createUser(n_clicks, usernameSubmit, newPassword1Submit, newPassword2Submit,
               newEmailSubmit, newUser, newPassword1, newPassword2, newEmail, admin):
    if (n_clicks > 0) or (usernameSubmit > 0) or (newPassword1Submit > 0) or \
            (newPassword2Submit > 0) or (newEmailSubmit > 0):

        if newUser and newPassword1 and newPassword2 and newEmail != '':
            if newPassword1 == newPassword2:
                if len(newPassword1) > 7:
                    try:
                        add_user(newUser, newPassword1, newEmail, admin)
                        return html.Div(children=['New User created'], className='text-success')
                    except Exception as e:
                        return html.Div(children=['New User not created: {e}'.format(e=e)], className='text-danger')
                else:
                    return html.Div(children=['New Password Must Be Minimum 8 Characters'], className='text-danger')
            else:
                return html.Div(children=['Passwords do not match'], className='text-danger')
        else:
            return html.Div(children=['Invalid details submitted'], className='text-danger')


# CREATE USER BUTTON CLICK / FORM SUBMIT - VALIDATE USERNAME
@app.callback(Output('newUsername', 'className'),
              [Input('createUserButton', 'n_clicks'),
               Input('newUsername', 'n_submit'),
               Input('newPwd1', 'n_submit'),
               Input('newPwd2', 'n_submit'),
               Input('newEmail', 'n_submit')],
              [State('newUsername', 'value')])
def validateUsername(n_clicks, usernameSubmit, newPassword1Submit,
                     newPassword2Submit, newEmailSubmit, newUsername):
    if (n_clicks > 0) or (usernameSubmit > 0) or (newPassword1Submit > 0) or \
            (newPassword2Submit > 0) or (newEmailSubmit > 0):

        if newUsername == None or newUsername == '':
            return 'form-control is-invalid'
        else:
            return 'form-control is-valid'
    else:
        return 'form-control'


# CREATE USER BUTTON CLICK / FORM SUBMIT - VALIDATE EMAIL
@app.callback(Output('newEmail', 'className'),
              [Input('createUserButton', 'n_clicks'),
               Input('newUsername', 'n_submit'),
               Input('newPwd1', 'n_submit'),
               Input('newPwd2', 'n_submit'),
               Input('newEmail', 'n_submit')],
              [State('newEmail', 'value')])
def validateEmail(n_clicks, usernameSubmit, newPassword1Submit,
                  newPassword2Submit, newEmailSubmit, newEmail):
    if (n_clicks > 0) or (usernameSubmit > 0) or (newPassword1Submit > 0) or \
            (newPassword2Submit > 0) or (newEmailSubmit > 0):

        if newEmail == None or newEmail == '':
            return 'form-control is-invalid'
        else:
            return 'form-control is-valid'
    else:
        return 'form-control'


# CREATE USER BUTTON CLICK / FORM SUBMIT - RED BOX IF PASSWORD DOES NOT MATCH
@app.callback(Output('newPwd1', 'className'), Output('newPwd2', 'className'),
              [Input('createUserButton', 'n_clicks'),
               Input('newUsername', 'n_submit'),
               Input('newPwd1', 'n_submit'),
               Input('newPwd2', 'n_submit'),
               Input('newEmail', 'n_submit')],
              [State('newPwd1', 'value'),
               State('newPwd2', 'value')])
def validatePassword(n_clicks, usernameSubmit, newPassword1Submit,
                     newPassword2Submit, newEmailSubmit, newPassword1, newPassword2):
    if (n_clicks > 0) or (usernameSubmit > 0) or (newPassword1Submit > 0) or \
            (newPassword2Submit > 0) or (newEmailSubmit > 0):

        if newPassword1 == newPassword2 and len(newPassword2) > 7:
            return 'form-control is-valid', 'form-control is-valid'
        else:
            return 'form-control is-invalid', 'form-control is-invalid'
    else:
        return 'form-control', 'form-control'


# UPDATE BUTTON CLICK / FORM SUBMIT - UPDATE NEW ROLE
@app.callback(Output('updateUserSuccess', 'children'),
              [Input('updateUserBtn', 'n_clicks')],
              [State('uname', 'value'),
               State('fillRole', 'value')])
def updateUser(n_clicks, Username, Role):
    if (n_clicks > 0):
        if Username and Role != '':
            user = User.query.filter_by(username=Username).first()
            db.session.close()
            if Role != user.role:
                try:
                    update_role(Username, Role)
                    return html.Div(children=['User updated'], className='text-success')
                except Exception as e:
                    return html.Div(children=['User not updated: {e}'.format(e=e)], className='text-danger')
            else:
                return html.Div(children=['User already have this Role'], className='text-danger')
        else:
            return html.Div(children=['Invalid details submitted'], className='text-danger')


# DELETE BUTTON CLICK / FORM SUBMIT - DELETE USER
@app.callback(Output('deleteUserSuccess', 'children'),
              [Input('deleteUserBtn', 'n_clicks')],
              [State('uname', 'value'), ])
def deleteUser(n_clicks, Username):
    if (n_clicks > 0):
        if Username != '' or Username != None:
            try:
                delete_user(Username)
                return html.Div(children=['User deleted'], className='text-success')
            except Exception as e:
                return html.Div(children=['User not deleted: {e}'.format(e=e)], className='text-danger')
        else:
            return html.Div(children=['Invalid details submitted'], className='text-danger')


# Switch Button
@app.callback(Output('updateUserBtn', 'disabled'),
              Output('deleteUserBtn', 'disabled'),
              Input('uname', 'value'), Input('fillRole', 'value'))
def switchButton(Fillusername, Fillrole):
    if Fillusername != None and Fillrole != None:
        return False, False
    elif Fillusername != None and Fillrole == None:
        return True, False
    else:
        return True, True

@app.callback(
    Output('users','data'),
    # Output('uname','options'),
    Input('createUserButton','n_click'),
    State('users','data')
)
def updateTable(btnCreate,data):
    if(btnCreate):
        return show_users()
    else:
        return show_users()