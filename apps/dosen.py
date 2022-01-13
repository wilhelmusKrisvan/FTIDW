import dash
import pandas as pd
import dash_table as dt
import plotly.express as px
import dash_bootstrap_components as dbc
from apps import pmb, kbm, kegiatan_kerjasama, tgsakhir, alumni, ppp
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from appConfig import app, server
from dash import html, dcc
import model.dao_dosen as data

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

dfpersendosens3 = data.getDosenS3()
dfjabfung = data.getJabfungperTahun()
dfpersenjabfung = data.getPersentaseJabfungperTahun()
dfdosentetapinf = data.getDosenTetapINF()
dfdosenindustri = data.getDosenIndustriPraktisi()

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

dosens3 = dbc.Container([
    dbc.Card([
        html.H5('Dosen S3',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody(
                dcc.Graph(id='grf_dosens3')
            ),
            id='cll_dosens3',
            n_clicks=0
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            html.H5('Persentase Dosen S3', style=ttlgrf_style),
            dt.DataTable(
                id='tbl_dosens3',
                columns=[{"name": i, "id": i} for i in dfpersendosens3.columns],
                data=dfpersendosens3.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                page_size=10,
                export_format='xlsx'
            ), style=cardgrf_style
        ),
        id='cll_tbldosens3',
        is_open=False
    )
], style=cont_style)

jumljabfungDosen = dbc.Container([
    dbc.Card([
        html.H5('Jumlah Jabfung Dosen per Tahun',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody(
                dcc.Graph(id='grf_jabfungth')
            ),
            id='cll_jabfungth',
            n_clicks=0
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            html.H5('Jumlah Jabfung Dosen per Tahun', style=ttlgrf_style),
            dt.DataTable(
                id='tbl_jabfungth',
                columns=[{"name": i, "id": i} for i in dfjabfung.columns],
                data=dfjabfung.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                page_size=10,
                export_format='xlsx'
            ), style=cardgrf_style
        ),
        id='cll_jabfungth',
        is_open=False
    )
], style=cont_style)

persenjabfungthDosen = dbc.Container([
    dbc.Card([
        html.H5('Persentase Jabfung Dosen per Tahun',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody(
                dcc.Graph(id='grf_persenjabfungth')
            ),
            id='cll_persenjabfungth',
            n_clicks=0
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            html.H5('Persentase Jabfung Dosen per Tahun', style=ttlgrf_style),
            dt.DataTable(
                id='tbl_persenjabfungth',
                columns=[{"name": i, "id": i} for i in dfpersenjabfung.columns],
                data=dfpersenjabfung.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                page_size=10,
                export_format='xlsx'
            ), style=cardgrf_style
        ),
        id='cll_persenjabfungth',
        is_open=False
    )
], style=cont_style)

dosentetapinf = html.Div([
    dbc.Row([
        dbc.Col([
                html.H5('Daftar Dosen Tetap Informatika', style=ttlgrf_style),
                dt.DataTable(
                    id='dfdosentetapinf',
                    columns=[
                        {'name': i, 'id': i} for i in dfdosentetapinf.columns
                    ],
                    data=dfdosentetapinf.to_dict('records'),
                    sort_action='native',
                    sort_mode='multi',
                    style_table={'padding': '10px', 'overflowX': 'auto'},
                    style_header={'textAlign': 'center'},
                    style_data={'font-size': '80%', 'textAlign': 'center'},
                    style_cell={'width': 95},
                    page_size=10,
                )
        ], width=12),
    ])
], style={'margin-top': '50px', 'width': '100%'})

dosentetapindustri = html.Div([
    dbc.Row([
        dbc.Col([
                html.H5('Daftar Dosen Industri Praktisi', style=ttlgrf_style),
                dt.DataTable(
                    id='dfdosentetapinf',
                    columns=[
                        {'name': i, 'id': i} for i in dfdosenindustri.columns
                    ],
                    data=dfdosenindustri.to_dict('records'),
                    sort_action='native',
                    sort_mode='multi',
                    style_table={'padding': '10px', 'overflowX': 'auto'},
                    style_header={'textAlign': 'center'},
                    style_data={'font-size': '80%', 'textAlign': 'center'},
                    style_cell={'width': 95},
                    page_size=10,
                )
        ], width=12),
    ])
], style={'margin-top': '50px', 'width': '100%'})
