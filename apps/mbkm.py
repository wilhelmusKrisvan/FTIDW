import dash
import pandas as pd
import dash_table as dt
import plotly.express as px
import dash_bootstrap_components as dbc
from apps import pmb, kbm, mbkm, kegiatan_kerjasama, tgsakhir, alumni, ppp, dosen
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from appConfig import app, server
from dash import html, dcc
import model.dao_mbkm as data

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

dfmahasiswambkm = data.getMahasiswaMBKMperSemester()
dfmitrambkm = data.getMitraMBKM()
dfjumlmitrambkm = data.getJumlMitraMBKMperSemester()
dfdosbingmbkm = data.getDosbingMBKMperSemester()
dfreratasksmbkm = data.getRerataSKSMBKMperSemester()

tabs_styles = {
    'background': '#FFFFFF',
    'color': '#b0b0b0',
    'border': 'white'
}

tab_style = {
    'background': "#FFFFFF",
    'border-bottom-color': '#ededed',
    'border-top-color': 'white',
    'border-left-color': 'white',
    'border-right-color': 'white',
    'color': '#b0b0b0',
    'align-items': 'center',
    'justify-content': 'center'
}

selected_style = {
    "background": "#FFFFFF",
    'align-items': 'center',
    'border-bottom': '2px solid',
    'border-top-color': 'white',
    'border-bottom-color': '#2780e3',
    'border-left-color': 'white',
    'border-right-color': 'white'
}

cont_style = {
    'padding': '0px',
    'justify-content': 'center',
    'margin-top': '25px'
}

cardgrf_style = {
    'border': '1px solid #fafafa',
    'border-radius': '10px',
    'padding': '10px',
    'box-shadow': '5px 10px 30px #ebedeb'
}

card_style = {
    'border': '1px solid #fafafa',
    'border-radius': '10px',
    'padding': '10px'
}

ttlgrf_style = {
    'textAlign': 'center',
    'padding': '10px',
    'color': 'black'
}

dftrmitraMBKM = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H5('Daftar Mitra MBKM', style=ttlgrf_style),
                dt.DataTable(
                    id='dfmitrambkm',
                    columns=[
                        {'name': i, 'id': i} for i in dfmitrambkm.columns
                    ],
                    data=dfmitrambkm.to_dict('records'),
                    sort_action='native',
                    sort_mode='multi',
                    style_table={'padding': '10px', 'overflowX': 'auto'},
                    style_header={'textAlign': 'center'},
                    style_data={'font-size': '80%', 'textAlign': 'center'},
                    style_cell={'width': 95},
                    page_size=10,
                )
            ], style=cardgrf_style),
        ], width=12)
    ], style={'margin-top': '10px'})
], style=cont_style)

# +grafcollapse
jumlmitraMBKM = dbc.Container([
    dbc.Card([
        html.H5('Jumlah Mitra MBKM per Semester',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody(
                dcc.Graph(id='grf_jumlmitrambkm')
            ),
            id='cll_grfjumlmitrambkm',
            n_clicks=0
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_jumlmitrambkm',
                columns=[
                    {'name': i, 'id': i} for i in dfjumlmitrambkm.columns],
                data=dfjumlmitrambkm.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'padding': '10px', 'overflowX': 'auto'},
                style_header={'textAlign': 'center'},
                style_data={'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 95},
                page_size=10,
                export_format='xlsx'
            ), style=cardgrf_style
        ),
        id='cll_tbljumlmitrambkm',
        is_open=False
    )
], style=cont_style)

# +grafcollapse
dosbingMBKM = dbc.Container([
    dbc.Card([
        html.H5('Jumlah Dosen Pembimbing MBKM',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody(
                dcc.Graph(id='grf_jumldosbingmbkm')
            ),
            id='cll_grfjumldosbingmbkm',
            n_clicks=0
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_dosbingmbkm',
                columns=[
                    {'name': i, 'id': i} for i in dfdosbingmbkm.columns
                ],
                data=dfdosbingmbkm.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'padding': '10px', 'overflowX': 'auto'},
                style_header={'textAlign': 'center'},
                style_data={'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 95},
                page_size=10,
                export_format='xlsx'
            ), style=cardgrf_style
        ),
        id='cll_tbljumldosbingmbkm',
        is_open=False
    )
], style=cont_style)

# +grafcollapse
mahasiswaMBKM = dbc.Container([
    dbc.Card([
        html.H5('Jumlah Mahasiswa MBKM',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody(
                dcc.Graph(id='grf_mahasiswambkm')
            ),
            id='cll_grfmahasiswambkm',
            n_clicks=0
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_mahasiswambkm',
                columns=[
                    {'name': i, 'id': i} for i in dfmahasiswambkm.columns
                ],
                data=dfmahasiswambkm.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'padding': '10px', 'overflowX': 'auto'},
                style_header={'textAlign': 'center'},
                style_data={'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 95},
                page_size=10,
                export_format='xlsx'
            ), style=cardgrf_style
        ),
        id='cll_tblmahasiswambkm',
        is_open=False
    )
], style=cont_style)

# +grafcollapse
reratasksMBKM = dbc.Container([
    dbc.Card([
        html.H5('Rata-rata Konversi SKS MBKM',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody(
                dcc.Graph(id='grf_reratasksmbkm')
            ),
            id='cll_grfreratasksmbkm',
            n_clicks=0
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_reratasksmbkm',
                columns=[
                    {'name': i, 'id': i} for i in dfreratasksmbkm.columns
                ],
                data=dfreratasksmbkm.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'padding': '10px', 'overflowX': 'auto'},
                style_header={'textAlign': 'center'},
                style_data={'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 95},
                page_size=10,
                export_format='xlsx'
            ), style=cardgrf_style
        ),
        id='cll_tblreratasksmbkm',
        is_open=False
    )
], style=cont_style)

#layout
mbkm = dbc.Container([
    html.Div([
        html.H1('Analisis MBKM',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Mahasiswa', value='mahasiswa',
                    children=[
                        mahasiswaMBKM,
                        reratasksMBKM
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Dosen Pembimbing', value='dosen',
                    children=[
                        dosbingMBKM
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Mitra', value='mitra',
                    children=[
                        jumlmitraMBKM,
                        dftrmitraMBKM
                    ],
                    style=tab_style, selected_style=selected_style)
        ], style=tabs_styles, value='mahasiswa')
    ])
], style=cont_style)

layout = html.Div([
    html.Div([mbkm], style={'margin-bottom': '50px'})
], style={'justify-content': 'center'})

#COLLAPSE CALLBACK
@app.callback(
    Output("cll_tblmahasiswambkm", "is_open"),
    [Input("cll_grfmahasiswambkm", "n_clicks")],
    [State("cll_tblmahasiswambkm", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("cll_tblreratasksmbkm", "is_open"),
    [Input("cll_grfreratasksmbkm", "n_clicks")],
    [State("cll_tblreratasksmbkm", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("cll_tbljumldosbingmbkm", "is_open"),
    [Input("cll_grfjumldosbingmbkm", "n_clicks")],
    [State("cll_tbljumldosbingmbkm", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

#GRAPH CALLBACK
@app.callback(
    Output('grf_mahasiswambkm','figure'),
    Input('grf_mahasiswambkm','id')
)
def grafMahasiswaMBKM(id):
    df=dfmahasiswambkm
    fig=px.bar(df,x=df['Semester'], y=df['Jumlah'], color=df['Bentuk'])
    fig.update_layout(barmode='group')
    return fig

@app.callback(
    Output('grf_reratasksmbkm','figure'),
    Input('grf_reratasksmbkm','id')
)
def grafRerataKonversiSKS(id):
    df=dfreratasksmbkm
    fig=px.line(df, x=df['Semester'], y=df['Jumlah SKS'])
    return fig

@app.callback(
    Output('grf_jumldosbingmbkm','figure'),
    Input('grf_jumldosbingmbkm','id')
)
def grafDosbingMBKM(id):
    df=dfdosbingmbkm
    fig=px.bar(df, x=df['Semester'], y=df['Jumlah Dosen'])
    fig.show

@app.callback(
    Output('grf_jumlmitrambkm','figure'),
    Input('grf_jumlmitrambkm','id')
)
def grafMitraMBKM(id):
    df=dfjumlmitrambkm
    fig=px.bar(df,x=df['Semester'], y=df['Jumlah Mitra'])
    return fig