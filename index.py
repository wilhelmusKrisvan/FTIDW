import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from appConfig import app, server
from flask_login import logout_user, current_user
import login, page1


navBar = dbc.Navbar(
        children=[
            html.A(
                dbc.Row([
                    dbc.Col(html.Img(src='https://www.ukdw.ac.id/wp-content/uploads/2017/10/fti-ukdw.png', height="35px")),
                    dbc.Col(dbc.NavbarBrand('DATA WAREHOUSE'))
                ],align="center",),
                href='/'
            ),
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
            return page1.layout
        else:
            return login.layout

    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return login.layout
        else:
            return login.layout

    if pathname == '/page1':
        if current_user.is_authenticated:
            return page1.layout
        else:
            return login.layout

if __name__ == '__main__':
    app.run_server(debug=True)