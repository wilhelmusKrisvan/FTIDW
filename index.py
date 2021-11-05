from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from appConfig import app, server
from flask_login import logout_user, current_user
import login, profile, admin
from apps import pmb,registrasi,kegiatan_kerjasama,tgsakhir,alumni,ppp
from apps import alumni,registrasi,kegiatan_kerjasama
import login, home

navBar = dbc.Navbar(
        children=[
        ],
        id='navBar',
        color='#375a7f',
        className='navbar navbar-expand-lg navbar-dark bg-primary',
        style={'width': '100%', 'position': 'sticky', 'top': '0', 'zIndex': '3'}
    )

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navBar,
    html.Div(id='pageContent')
], id='table-wrapper')

# HANDLE PAGE ROUTING - IF USER NOT LOGGED IN, ALWAYS RETURN TO LOGIN SCREEN
@app.callback(Output('pageContent', 'children'),
              [Input('url', 'pathname')])
def displayPage(pathname):
    if pathname == '/':
        if current_user.is_authenticated:
            return home.layout
        else:
            return login.layout

    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return login.layout
        else:
            return login.layout

    if pathname == '/home':
        if current_user.is_authenticated:
            return home.layout
        else:
            return login.layout

    if pathname == '/dashboard/alumni':
        if current_user.is_authenticated:
            return alumni.layout
        else:
            return login.layout

    if pathname == '/dashboard/registrasi':
        if current_user.is_authenticated:
            return registrasi.layout
        else:
            return registrasi.layout

    if pathname == '/dashboard/kegiatan-kerjasama':
        if current_user.is_authenticated:
            return kegiatan_kerjasama.layout
        else:
            return kegiatan_kerjasama.layout

    if pathname == '/dashboard/ppp':
        if current_user.is_authenticated:
            return ppp.layout
        else:
            return ppp.layout

    if pathname == '/dashboard/pmb':
        if current_user.is_authenticated:
            return pmb.layout
        else:
            return pmb.layout

    if pathname == '/dashboard/kp-skripsi-yudisium':
        if current_user.is_authenticated:
            return tgsakhir.layout
        else:
            return tgsakhir.layout

    if pathname == '/profile':
        if current_user.is_authenticated:
            return profile.layout
        else:
            return login.layout

    if pathname == '/admin':
        if current_user.is_authenticated:
            if current_user.role=='admin':
                return admin.layout
            else:
                return login.layout
        else:
            return login.layout

@app.callback(
    Output('navBar', 'children'),
    [Input('pageContent', 'children')])
def navBarPage(input1):
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            navBarContents = html.Div([
            html.Div([
                html.Div([
                    html.A(
                        dbc.Row([
                            dbc.Col(
                                html.Img(src='https://www.ukdw.ac.id/wp-content/uploads/2017/10/fti-ukdw.png',
                                         height="35px")),
                            dbc.Col(dbc.NavbarBrand('DASHBOARD'))
                        ], align="center", ),
                        href='/'
                    ),
                    dbc.NavLink('Page 1', href='/home'),
                ], className='navbar-nav mr-auto'),
                dbc.DropdownMenu(
                    right=True,
                    label=current_user.username,
                    children=[
                        dbc.DropdownMenuItem('Profile', href='/profile'),
                        dbc.DropdownMenuItem('Admin', href='/admin'),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem('Logout', href='/logout'),
                    ], color='rgb(39, 128, 227)',
                ),
            ], className='collapse navbar-collapse')
        ], className='container-fluid')
            return navBarContents
        else:
            navBarContents = html.Div([
            html.Div([
                html.Div([
                    html.A(
                        dbc.Row([
                            dbc.Col(
                                html.Img(src='https://www.ukdw.ac.id/wp-content/uploads/2017/10/fti-ukdw.png',
                                         height="35px")),
                            dbc.Col(dbc.NavbarBrand('DASHBOARD'))
                        ], align="center", ),
                        href='/'
                    ),
                    dbc.NavLink('Home', href='/home'),
                ], className='navbar-nav mr-auto'),
                dbc.DropdownMenu(
                    right=True,
                    label=current_user.username,
                    children=[
                        dbc.DropdownMenuItem('Profile', href='/profile'),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem('Logout', href='/logout'),
                    ], color='rgb(39, 128, 227)',style={'border-radius': '200px'}
                ),
            ], className='collapse navbar-collapse')
        ], className='container-fluid')
            return navBarContents
    else:
        return html.Div([
            html.Div([
                html.Div([
                    html.A(
                        dbc.Row([
                            dbc.Col(
                                html.Img(src='https://www.ukdw.ac.id/wp-content/uploads/2017/10/fti-ukdw.png',
                                         height="35px")),
                            dbc.Col(dbc.NavbarBrand('DASHBOARD'))
                        ], align="center", ),
                        href='/'
                    ),
                ], className='navbar-nav mr-auto'),
            ], className='collapse navbar-collapse')
        ], className='container-fluid')

if __name__ == '__main__':
    app.run_server(debug=False)
