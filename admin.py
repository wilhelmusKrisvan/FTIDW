import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
from appConfig import app, User
from model.user import add_user, show_role, show_users, update_role, delete_user
from dash.dependencies import Input, Output, State
from flask_login import current_user

users = show_users()
uname = users
options = [
    {'label': 'Admin', 'value': 'admin'},
    {'label': 'Dekanat', 'value': 'dekanat'},
    {'label': 'Dosen', 'value': 'dosen'}]

layout = dbc.Container([
    dbc.Container([
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
                        'width': '90%'
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
                        'width': '90%'
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
                        'width': '90%'
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
                        'width': '90%'
                    },
                ),
                html.Br(),
                dbc.Label('Role '),
                dcc.Dropdown(
                    id='admin',
                    style={
                        'width': '90%'
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
                    className='btn btn-primary btn-lg'
                ),
                html.Br(),
                html.Div(id='createUserSuccess')
            ], md=4),
            dbc.Col([

            ], md=4)
        ]),
    ], className='jumbotron'),

    dbc.Container([
        html.H3('Manage Users'),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dt.DataTable(
                    id='users',
                    columns=[{'name': 'Username', 'id': 'username'},
                             {'name': 'Email', 'id': 'email'},
                             {'name': 'Role', 'id': 'role'}],
                    data=show_users(),
                ),
            ], md=12),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Label('Username: '),
                dcc.Dropdown(options=[{'label': i['username'], 'value': i['username']} for i in uname], id='uname')
            ], width=4),
            dbc.Col([
                dbc.Label('Role: '),
                dcc.Dropdown(
                    options=[
                        {'label': 'Admin', 'value': 'admin'},
                        {'label': 'Dekanat', 'value': 'dekanat'},
                        {'label': 'Dosen', 'value': 'dosen'}
                    ], id='fillRole', )
            ], width=4),
            dbc.Col([
                html.Br(),
                html.Button(
                    children='UPDATE',
                    id='updateUserBtn',
                    n_clicks=0,
                    type='submit',
                    className='btn btn-primary btn-lg'
                ),
                html.Div(id='updateUserSuccess'),
            ], width=2),
            dbc.Col([
                html.Br(),
                html.Button(
                    children='DELETE',
                    id='deleteUserBtn',
                    n_clicks=0,
                    type='submit',
                    className='btn btn-danger btn-lg'
                ),
                html.Div(id='deleteUserSuccess')
            ], width=2),
        ]),
    ], className='jumbotron')
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
# @app.callback(Output('deleteUserSuccess', 'children'),
#               [Input('deleteUserBtn', 'n_clicks')],
#               [State('uname', 'value'), ])
# def deleteUser(n_clicks, Username):
#     if (n_clicks > 0):
#         if Username != '' or Username != None:
#             try:
#                 delete_user(Username)
#                 return html.Div(children=['User deleted'], className='text-success')
#             except Exception as e:
#                 return html.Div(children=['User not deleted: {e}'.format(e=e)], className='text-danger')
#         else:
#             return html.Div(children=['Invalid details submitted'], className='text-danger')
