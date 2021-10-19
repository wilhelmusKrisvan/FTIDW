import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

app = dash.Dash(__name__,suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.CERULEAN])
server = app.server

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

icon = 'https://amigogroup.co.id/wp-content/uploads/2021/04/Pin-1.png'
#icon = 'https://amigogroup.co.id/wp-content/uploads/2020/06/AmigoHeader-e1593098882452.png'
icnBrand = 'https://amigogroup.co.id/wp-content/uploads/2020/06/AmigoHeader-e1593098882452.png'

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Navbar(
        [
            html.A(
                dbc.Row([
                    dbc.Col(html.Img(src=icon, height="35px")),
                    dbc.Col(dbc.NavbarBrand('XYZ Group'))
                ],
                    align="center"),
                href='/'
            ),
        ],
        color='#375a7f',
        className='navbar navbar-expand-lg navbar-dark bg-primary',
        style={'width': '100%', 'position': 'sticky', 'top': '0', 'zIndex': '3'}
    ),
    html.Div(id='breadcrumb',children=[

    ]),
    # html.Div([
    #     dcc.Link(children=html.P('Home'),href='/'),
    #     html.P('>'),
    #     dcc.Link(children=html.P('Home'),href='/')
    # ],style={'display':'inline'}),
    html.Div(id='page-content',children=[

    ])
])

home = html.Div([
        dbc.Container([
            
            # dbc.Row([
            #     dbc.Col([
            #         dbc.CardLink([
            #             dbc.Card(
            #                 dbc.CardBody([
            #                     html.Div(html.Img(src='https://image.flaticon.com/icons/png/128/994/994430.png',height='100px'), style={'textAlign':'center'}),
            #                     html.P('Dashboard Transaksi Pengadaan Barang', className='card-title',
            #                            style={'textAlign': 'center', 'fontSize': 25, 'color': 'black'}),
            #                 ])
            #                 , className='btn btn-primary')
            #         ], href='apps/app1')
            #     ], width=12),
            # ], style={'width': '100%'})
        ], style={'height': '100vh', 'align-items': 'center', 'display': 'flex', 'justify-content':'center'}, fluid=True)
    ], style={'width': '100%', 'position': 'sticky', 'top': '0', 'zIndex': '3'}),


@app.callback(
    Output('breadcrumb', 'children'),
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/apps/app1':
        return html.Ol(className='breadcrumb',children=[
            html.Li(className='breadcrumb-item',children=dcc.Link(children=html.P('Home'),href='/'),),
            html.Li(className='breadcrumb-item active',children=html.P('Dashboard Transaksi Pengadaan Barang'),)
        ],style={'margin':'10px'}),None
    elif pathname == '/apps/app2':
        return html.Ol(className='breadcrumb',children=[
            html.Li(className='breadcrumb-item',children=dcc.Link(children=html.P('Home'),href='/'),),
            html.Li(className='breadcrumb-item active',children=html.P('Dashboard Pemesanan Pengadaan Barang'),)
        ],style={'margin':'10px'}),None
    elif pathname == '/':
        return None,home
    else:
        return None,home

if __name__ == '__main__':
    app.run_server(debug=True)
