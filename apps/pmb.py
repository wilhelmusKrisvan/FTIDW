import dash_table as dt
import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from appConfig import app
from urllib.request import urlopen
import model.dao_pmb as data
import json
from datetime import date

with urlopen(
        'https://raw.githubusercontent.com/wilhelmusKrisvan/GEOJSON_IDN/main/IDN_prov.json') as response:
    province = json.load(response)

dfseleksi = data.getSeleksi()
dfmhsasing = data.getMahasiswaAsing()
dfmhssmasmk = data.getJenisSekolahPendaftar()
dfmhsprovdaftar = data.getProvinsiDaftar()
dfmhsprovlolos = data.getProvinsiLolos()
dfmhsprovregis = data.getProvinsiRegis()
tbl_mahasiswaAktif = data.getMahasiswaAktif()
# dfmhsrasio = data.getRasioCalonMahasiswa()
# dfmhsJml = data.getPerkembanganJumlahMaba()
dfmhsPersenNaik = data.getPersentaseKenaikanMaba()

listDropdown = []
for x in range(0, 5):
    counter = x + 1
    tahun = 5
    yearnow = date.today().strftime('%Y')
    listDropdown.append(
        str(int(yearnow) - tahun + x) + '/' + str(int(yearnow) - (tahun - 1) + x))

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
    'padding': '10px',
    'justify-content': 'center',
    'margin-top': '25px'
}

cardgrf_style = {
    'border': '1px solid #fafafa',
    'border-radius': '10px',
    'padding': '10px',
    'box-shadow': '5px 10px 30px #ebedeb'
}

cardtbl_style = {
    'border': '1px solid #fafafa',
    'border-radius': '10px',
    'padding': '20px 10px 60px 10px',
    'box-shadow': '5px 10px 30px #ebedeb'
}

cardoncard_style = {
    'padding': '10px',
}

ttlgrf_style = {
    'textAlign': 'center',
    'padding': '10px',
    'color': 'black'
}

filterLabel_style = {
    'textAlign': 'center',
    'padding': '0px',
    'color': 'black'
}

buttonLink_style = {
    'position': 'fixed',
    'width': '60px',
    'height': '60px',
    'bottom': '40px',
    'right': '40px',
    'background-color': '#2780e3',
    'color': 'white',
    'border-radius': '50px',
    'text-align': 'center',
    'box-shadow': '5px 10px 20px #ebedeb',
    'border': '1px solid #fafafa'
}

button_style = {
    'width': '120px',
    'height': '50px',
    'border-radius': '10px',
    'box-shadow': '5px 10px 20px #ebedeb',
    'border': '1px solid #fafafa',
    'color': 'white',
    'background-color': '#2780e3',
    'right': '0',
    'position': 'absolute',
    'margin': '-50px 25px 10px 10px',
}

mhsseleksi = dbc.Container([
    dbc.Card([
        html.H5('Seleksi Mahasiswa',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.P('Dari', style={'color': 'black'}),
                            dcc.Dropdown(
                                id='Fromdrpdwn_mhsseleksi',
                                options=[{'label': i, 'value': i} for i in listDropdown],
                                value=listDropdown[0],
                                style={'color': 'black'},
                                clearable=False,
                                placeholder='Dari',
                            ),
                        ]),
                    ], width=6),
                    dbc.Col([
                        html.Div([
                            html.P('Sampai', style={'color': 'black'}),
                            dcc.Dropdown(
                                id='Todrpdwn_mhsseleksi',
                                options=[{'label': i, 'value': i} for i in listDropdown],
                                value=listDropdown[len(listDropdown) - 1],
                                style={'color': 'black'},
                                clearable=False,
                                placeholder='Sampai',
                            ),
                        ]),
                    ], width=6),
                ]),
                dcc.Loading([
                    dcc.Graph(id='grf_mhsseleksi'),
                ], type="default"),
                dbc.Button('Lihat Semua Data', id='cll_grfseleksi',
                           n_clicks=0, style=button_style)
            ]),
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_seleksi',
                columns=[{"name": i, "id": i} for i in dfseleksi.columns],
                data=dfseleksi.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                page_size=10,
                export_format='xlsx'
            ), style=cardtbl_style
        ),
        id='cll_tblseleksi',
        is_open=False
    )
], style=cont_style)

mhsAktif = dbc.Container([
    dbc.Card([
        html.H5('Mahasiswa Aktif',
                style=ttlgrf_style),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.P('Dari', style={'color': 'black'}),
                        dcc.Dropdown(
                            id='Fromdrpdwn_mhsAktif',
                            options=[{'label': i, 'value': i} for i in listDropdown],
                            value=listDropdown[0],
                            style={'color': 'black'},
                            clearable=False,
                            placeholder='Dari',
                        ),
                    ]),
                ], width=6),
                dbc.Col([
                    html.Div([
                        html.P('Sampai', style={'color': 'black'}),
                        dcc.Dropdown(
                            id='Todrpdwn_mhsAktif',
                            options=[{'label': i, 'value': i} for i in listDropdown],
                            value=listDropdown[len(listDropdown) - 1],
                            style={'color': 'black'},
                            clearable=False,
                            placeholder='Sampai',
                        ),
                    ]),
                ], width=6),
            ]),
            dcc.Loading([
                dcc.Graph(id='grf_mahasiswaAktif'),
            ], type="default"),
            dbc.Button('Lihat Semua Data', id='cll_grfmhsaktif',
                       n_clicks=0, style=button_style),
        ])
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_mahasiswaAktif',
                columns=[{"name": i, "id": i} for i in tbl_mahasiswaAktif.columns],
                data=tbl_mahasiswaAktif.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                page_size=10,
                export_format='xlsx'
            ), style=cardtbl_style
        ),
        id='cll_tblmahasiswaAktif',
        is_open=False
    )
], style=cont_style)

mhsasing = dbc.Container([
    dbc.Card([
        html.H5('Mahasiswa Asing',
                style=ttlgrf_style),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.P('Dari', style={'color': 'black'}),
                    dcc.Dropdown(
                        id='Fromdrpdwn_mhsasing',
                        options=[{'label': i, 'value': i} for i in listDropdown],
                        value=listDropdown[0],
                        style={'color': 'black'},
                        clearable=False,
                        placeholder='Dari',
                    ),
                ]),
            ], width=6),
            dbc.Col([
                html.Div([
                    html.P('Sampai', style={'color': 'black'}),
                    dcc.Dropdown(
                        id='Todrpdwn_mhsasing',
                        options=[{'label': i, 'value': i} for i in listDropdown],
                        value=listDropdown[len(listDropdown) - 1],
                        style={'color': 'black'},
                        clearable=False,
                        placeholder='Sampai',
                    ),
                ]),
            ], width=6),
        ], style={'padding': '15px'}),
        dcc.Tabs([
            dcc.Tab(label='FTI', value='all',
                    children=[
                        dbc.CardBody([
                            dcc.Loading([
                                dcc.Graph(id='grf_mhsasing'),
                            ], type="default"),
                            dbc.Button('Lihat Semua Data', id='cll_grfasing', n_clicks=0, style=button_style),
                        ])
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='INF', value='INF',
                    children=[
                        dbc.CardBody([
                            dcc.Loading([
                                dcc.Graph(id='grf_mhsasingINF'),
                            ], type="default"),
                            dbc.Button('Lihat Semua Data', id='cll_grfasingINF', n_clicks=0, style=button_style),
                        ])
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='SI', value='SI',
                    children=[
                        dbc.CardBody([
                            dcc.Loading([
                                dcc.Graph(id='grf_mhsasingSI'),
                            ], type="default"),
                            dbc.Button('Lihat Semua Data', id='cll_grfasingSI', n_clicks=0, style=button_style),
                        ])
                    ],
                    style=tab_style, selected_style=selected_style)
        ], id='tab_mhsasing', value='all')
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_tblasing',
        is_open=False,
    )
], style=cont_style)

# mhsrasio = dbc.Container([
#     dbc.Card([
#         html.H5('Rasio Daya Tampung : Pendaftar Registrasi Mahasiswa',
#                 style=ttlgrf_style),
#         dbc.CardBody([
#             dbc.Row([
#                 dbc.Col([
#                     html.Div([
#                         html.P('Dari', style={'color': 'black'}),
#                         dcc.Dropdown(
#                             id='Fromdrpdwn_mhsrasio',
#                             options=[{'label': i, 'value': i} for i in listDropdown],
#                             value=listDropdown[0],
#                             style={'color': 'black'},
#                             clearable=False,
#                             placeholder='Dari',
#                         ),
#                     ]),
#                 ], width=6),
#                 dbc.Col([
#                     html.Div([
#                         html.P('Sampai', style={'color': 'black'}),
#                         dcc.Dropdown(
#                             id='Todrpdwn_mhsrasio',
#                             options=[{'label': i, 'value': i} for i in listDropdown],
#                             value=listDropdown[len(listDropdown) - 1],
#                             style={'color': 'black'},
#                             clearable=False,
#                             placeholder='Sampai',
#                         ),
#                     ]),
#                 ], width=6),
#             ]),
#             dcc.Loading([
#                 dcc.Graph(id='grf_mhsrasio'),
#             ], type="default"),
#             dbc.Button('Lihat Semua Data', id='cll_grfrasio', n_clicks=0, style=button_style),
#         ])
#     ], style=cardgrf_style),
#     dbc.Collapse(
#         dbc.Card(
#             dt.DataTable(
#                 id='tbl_mhsrasio',
#                 columns=[{"name": i, "id": i} for i in dfmhsrasio.columns],
#                 data=dfmhsrasio.to_dict('records'),
#                 sort_action='native',
#                 sort_mode='multi',
#                 style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
#                 export_format='xlsx',
#                 style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
#                 style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
#                 style_cell={'width': 70},
#                 page_size=10
#             ), style=cardtbl_style
#         ),
#         id='cll_tblrasio',
#         is_open=False
#     )
# ], style=cont_style)

mhsasmasmk = dbc.Container([
    dbc.Card([
        html.H5('Asal Sekolah Mahasiswa Pendaftar',
                style=ttlgrf_style),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.P('Dari', style={'color': 'black'}),
                        dcc.Dropdown(
                            id='Fromdrpdwn_mhssmasmk',
                            options=[{'label': i, 'value': i} for i in listDropdown],
                            value=listDropdown[0],
                            style={'color': 'black'},
                            clearable=False,
                            placeholder='Dari',
                        ),
                    ]),
                ], width=6),
                dbc.Col([
                    html.Div([
                        html.P('Sampai', style={'color': 'black'}),
                        dcc.Dropdown(
                            id='Todrpdwn_mhssmasmk',
                            options=[{'label': i, 'value': i} for i in listDropdown],
                            value=listDropdown[len(listDropdown) - 1],
                            style={'color': 'black'},
                            clearable=False,
                            placeholder='Sampai',
                        ),
                    ]),
                ], width=6),
            ]),
            dcc.Loading([
                dcc.Graph(id='grf_mhssmasmk'),
            ], type="default"),
            dbc.Button('Lihat Semua Data', id='cll_grfsmasmk', n_clicks=0, style=button_style),
        ])
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_mhssmasmk',
                columns=[{"name": i, "id": i} for i in dfmhssmasmk.columns],
                data=dfmhssmasmk.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                export_format='xlsx',
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 70},
                page_size=10
            ), style=cardtbl_style
        ),
        id='cll_tblsmasmk',
        is_open=False
    )
], style=cont_style)

mhsprovinsi = dbc.Container([
    dbc.Card([
        html.H5('Lokasi Asal Calon Mahasiswa',
                style=ttlgrf_style),
        html.Div(
            dcc.Tabs([
                dcc.Tab(label='Pendaftar', value='daftar',
                        children=[
                            dbc.Card([
                                dbc.Row([
                                    dbc.Col([
                                        html.Div([
                                            html.P('Dari', style={'color': 'black'}),
                                            dcc.Dropdown(
                                                id='Fromdrpdwn_TAdaftar',
                                                options=[{'label': i, 'value': i} for i in listDropdown],
                                                value=listDropdown[0],
                                                style={'color': 'black'},
                                                clearable=False,
                                                placeholder='Dari',
                                            ),
                                        ], id='visiFrom_TAdaftar'),
                                    ], width=6),
                                    dbc.Col([
                                        html.Div([
                                            html.P('Sampai', style={'color': 'black'}),
                                            dcc.Dropdown(
                                                id='Todrpdwn_TAdaftar',
                                                options=[{'label': i, 'value': i} for i in listDropdown],
                                                value=listDropdown[len(listDropdown) - 1],
                                                style={'color': 'black'},
                                                clearable=False,
                                                placeholder='Sampai',
                                            ),
                                        ], id='visiTo_TAdaftar')
                                    ], width=6),
                                ], style={'margin-bottom': '15px'}),
                                dbc.Row([
                                    dbc.Col([
                                        html.P('Visualisasi: ', style={'color': 'black'}),
                                        dcc.RadioItems(
                                            id='radio_daftar',
                                            options=[{'label': 'Persebaran Wilayah (Maps)', 'value': 'geojson'},
                                                     {'label': 'Jumlah Mahasiswa per Provinsi (Bar Chart)',
                                                      'value': 'bar'}
                                                     ],
                                            value='geojson',
                                            style={'width': '100%', 'padding': '0px', },
                                            className='card-body',
                                            labelStyle={'display': 'block'}
                                        ),
                                    ]),
                                ]),
                                dbc.CardBody([
                                    dcc.Loading([
                                        dcc.Graph(id='grf_mhsprovdaftar'),
                                    ], type="default"),
                                    dbc.Button('Lihat Semua Data', id='cll_grfmhsprovdaftar', n_clicks=0,
                                               style=button_style),
                                ]),
                            ], style={'padding': '10px', 'border': 'white'})
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Lolos Seleksi', value='lolos',
                        children=[
                            dbc.Card([
                                dbc.Row([
                                    dbc.Col([
                                        html.Div([
                                            html.P('Dari', style={'color': 'black'}),
                                            dcc.Dropdown(
                                                id='Fromdrpdwn_TAlolos',
                                                options=[{'label': i, 'value': i} for i in listDropdown],
                                                value=listDropdown[0],
                                                style={'color': 'black'},
                                                clearable=False,
                                                placeholder='Dari',
                                            ),
                                        ], id='visiFrom_TAlolos'),
                                    ], width=6),
                                    dbc.Col([
                                        html.Div([
                                            html.P('Sampai', style={'color': 'black'}),
                                            dcc.Dropdown(
                                                id='Todrpdwn_TAlolos',
                                                options=[{'label': i, 'value': i} for i in listDropdown],
                                                value=listDropdown[len(listDropdown) - 1],
                                                style={'color': 'black'},
                                                clearable=False,
                                                placeholder='Sampai',
                                            ),
                                        ], id='visiTo_TAlolos')
                                    ], width=6),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dcc.RadioItems(
                                            id='radio_lolos',
                                            options=[{'label': 'Persebaran Wilayah', 'value': 'geojson'},
                                                     {'label': 'Jumlah Mahasiswa per Provinsi', 'value': 'bar'}],
                                            value='geojson',
                                            style={'width': '100%', 'padding': '0px', },
                                            className='card-body',
                                            labelStyle={'display': 'block'}
                                        ),
                                    ])
                                ]),
                                dbc.CardBody([
                                    dcc.Loading([
                                        dcc.Graph(id='grf_mhsprovlolos'),
                                    ], type="default"),
                                    dbc.Button('Lihat Semua Data', id='cll_grfmhsprovlolos', n_clicks=0,
                                               style=button_style),
                                ]),
                            ], style={'padding': '10px', 'border': 'white'})
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Registrasi Ulang', value='regis',
                        children=[
                            dbc.Card([
                                dbc.Row([
                                    dbc.Col([
                                        html.Div([
                                            html.P('Dari', style={'color': 'black'}),
                                            dcc.Dropdown(
                                                id='Fromdrpdwn_TAregis',
                                                options=[{'label': i, 'value': i} for i in listDropdown],
                                                value=listDropdown[0],
                                                style={'color': 'black'},
                                                clearable=False,
                                                placeholder='Dari',
                                            ),
                                        ], id='visiFrom_TAregis'),
                                    ], width=6),
                                    dbc.Col([
                                        html.Div([
                                            html.P('Sampai', style={'color': 'black'}),
                                            dcc.Dropdown(
                                                id='Todrpdwn_TAregis',
                                                options=[{'label': i, 'value': i} for i in listDropdown],
                                                value=listDropdown[len(listDropdown) - 1],
                                                style={'color': 'black'},
                                                clearable=False,
                                                placeholder='Sampai',
                                            ),
                                        ], id='visiTo_TAregis')
                                    ], width=6),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dcc.RadioItems(
                                            id='radio_regis',
                                            options=[{'label': 'Persebaran Wilayah', 'value': 'geojson'},
                                                     {'label': 'Jumlah Mahasiswa per Provinsi', 'value': 'bar'}
                                                     ],
                                            value='geojson',
                                            style={'width': '100%', 'padding': '0px'},
                                            className='card-body',
                                            labelStyle={'display': 'block'}
                                        ),
                                    ]),
                                ]),
                                dbc.CardBody([
                                    dcc.Loading([
                                        dcc.Graph(id='grf_mhsprovregis'),
                                    ], type="default"),
                                    dbc.Button('Lihat Semua Data', id='cll_grfmhsprovregis', n_clicks=0,
                                               style=button_style),
                                ]),
                            ], style={'padding': '10px', 'border': 'white'})
                        ], style=tab_style, selected_style=selected_style)
            ], style=tabs_styles, id='tab_mhsprov', value='daftar'
            )
        )
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_tblmhsprov',
        is_open=False
    ),
], style=cont_style)

# mhsKembangJml = dbc.Container([
#     dbc.Card([
#         html.H5('Perkembangan Jumlah Penerimaan Mahasiswa Baru',
#                 style=ttlgrf_style),
#         dbc.CardBody([
#             dbc.Row([
#                 dbc.Col([
#                     html.Div([
#                         html.P('Dari', style={'color': 'black'}),
#                         dcc.Dropdown(
#                             id='Fromdrpdwn_mhsJml',
#                             options=[{'label': i, 'value': i} for i in listDropdown],
#                             value=listDropdown[0],
#                             style={'color': 'black'},
#                             clearable=False,
#                             placeholder='Dari',
#                         ),
#                     ]),
#                 ], width=6),
#                 dbc.Col([
#                     html.Div([
#                         html.P('Sampai', style={'color': 'black'}),
#                         dcc.Dropdown(
#                             id='Todrpdwn_mhsJml',
#                             options=[{'label': i, 'value': i} for i in listDropdown],
#                             value=listDropdown[len(listDropdown) - 1],
#                             style={'color': 'black'},
#                             clearable=False,
#                             placeholder='Sampai',
#                         ),
#                     ]),
#                 ], width=6)
#             ]),
#             dcc.Loading([
#                 dcc.Graph(id='grf_mhsJml'),
#             ], type="default"),
#             dbc.Button('Lihat Semua Data', id='cll_grfJml', n_clicks=0, style=button_style),
#         ])
#     ], style=cardgrf_style),
#     dbc.Collapse(
#         dbc.Card(
#             dt.DataTable(
#                 id='tbl_Jml',
#                 columns=[{"name": i, "id": i} for i in dfmhsJml.columns],
#                 data=dfmhsJml.to_dict('records'),
#                 sort_action='native',
#                 sort_mode='multi',
#                 style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
#                 export_format='xlsx',
#                 style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
#                 style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
#                 style_cell={'width': 70},
#                 page_size=10
#             ), style=cardtbl_style
#         ),
#         id='cll_tblJml',
#         is_open=False
#     )
# ], style=cont_style)

mhsPersenNaik = dbc.Container([
    dbc.Card([
        html.H5('Persentase Kenaikan Penerimaan Mahasiswa Baru',
                style=ttlgrf_style),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.P('Dari', style={'color': 'black'}),
                        dcc.Dropdown(
                            id='Fromdrpdwn_mhsPersenNaik',
                            options=[{'label': i, 'value': i} for i in listDropdown],
                            value=listDropdown[0],
                            style={'color': 'black'},
                            clearable=False,
                            placeholder='Dari',
                        ),
                    ]),
                ], width=6),
                dbc.Col([
                    html.Div([
                        html.P('Sampai', style={'color': 'black'}),
                        dcc.Dropdown(
                            id='Todrpdwn_mhsPersenNaik',
                            options=[{'label': i, 'value': i} for i in listDropdown],
                            value=listDropdown[len(listDropdown) - 1],
                            style={'color': 'black'},
                            clearable=False,
                            placeholder='Sampai',
                        ),
                    ]),
                ], width=6),
            ]),
            dcc.Loading([
                dcc.Graph(id='grf_mhsPersenNaik'),
            ], type="default"),
            dbc.Button('Lihat Semua Data', id='cll_grfPersenNaik',
                       n_clicks=0, style=button_style),
        ])
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_PersenNaik',
                columns=[{"name": i, "id": i} for i in dfmhsPersenNaik.columns],
                data=dfmhsPersenNaik.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                export_format='xlsx',
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 70},
                page_size=10
            ), style=cardtbl_style
        ),
        id='cll_tblPersenNaik',
        is_open=False
    )
], style=cont_style)

layout = html.Div([
    html.Div(html.H1('Analisis Mahasiswa Baru Prodi Informatika',
                     style={'margin-top': '30px', 'textAlign': 'center'}
                     )
             ),
    html.A(className='name'),
    html.Div([mhsseleksi]),
    html.Div([mhsPersenNaik]),
    html.Div([mhsAktif]),
    html.Div([mhsasing]),
    # html.Div([mhsrasio]),
    html.Div([mhsasmasmk]),
    html.Div([mhsprovinsi], style={'margin-bottom': '50px'}),
    # html.Div([mhsKembangJml]),
    # html.Div([mhsPersenNaik], style={'margin-bottom': '50px'}),
    dbc.Container([
        dcc.Link([
            dbc.Button('^', style=buttonLink_style),
        ], href='#name'),
    ], style={'margin-left': '90%'}),
], style={'justify-content': 'center'})


# CONTROL COLLAPSE
@app.callback(
    Output("cll_tblseleksi", "is_open"),
    [Input("cll_grfseleksi", "n_clicks")],
    [State("cll_tblseleksi", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tblasing", "is_open"),
    Output("cll_tblasing", "children"),
    [Input("cll_grfasing", "n_clicks"),
     Input("cll_grfasingINF", "n_clicks"),
     Input("cll_grfasingSI", "n_clicks"),
     Input('tab_mhsasing', 'value')],
    [State("cll_tblasing", "is_open")])
def toggle_collapse(nall, ninf, nsi, mhs, is_open):
    isiMhsAsing = dbc.Card(
        dt.DataTable(
            id='tbl_mhsasing',
            columns=[{"name": i, "id": i} for i in dfmhsasing.columns],
            data=dfmhsasing.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            export_format='xlsx',
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 70},
            page_size=10
        ), style=cardtbl_style
    )
    if nall and mhs == 'all':
        return not is_open, isiMhsAsing
    if ninf and mhs == 'INF':
        return not is_open, isiMhsAsing
    if nsi and mhs == 'SI':
        return not is_open, isiMhsAsing
    return is_open, None


@app.callback(
    Output("cll_tblrasio", "is_open"),
    [Input("cll_grfrasio", "n_clicks")],
    [State("cll_tblrasio", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tblsmasmk", "is_open"),
    [Input("cll_grfsmasmk", "n_clicks")],
    [State("cll_tblsmasmk", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tblmhsprov", "is_open"),
    Output("cll_tblmhsprov", "children"),
    [Input("cll_grfmhsprovdaftar", "n_clicks"),
     Input("cll_grfmhsprovlolos", "n_clicks"),
     Input("cll_grfmhsprovregis", "n_clicks"),
     Input("tab_mhsprov", "value")],
    [State("cll_tblmhsprov", "is_open")])
def toggle_collapse(ndaftar, nlolos, nregis, prov, is_open):
    isiDaftar = dbc.Card(
        dt.DataTable(
            id='tbl_mhsprovdaftar',
            columns=[{"name": i, "id": i} for i in dfmhsprovdaftar.columns],
            data=dfmhsprovdaftar.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            export_format='xlsx',
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 70},
            page_size=10
        ), style=cardtbl_style
    ),
    isiLolos = dbc.Card(
        dt.DataTable(
            id='tbl_mhsprovlolos',
            columns=[{"name": i, "id": i} for i in dfmhsprovlolos.columns],
            data=dfmhsprovlolos.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            export_format='xlsx',
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 70},
            page_size=10
        ), style=cardtbl_style
    ),
    isiRegis = dbc.Card(
        dt.DataTable(
            id='tbl_mhsprovregis',
            columns=[{"name": i, "id": i} for i in dfmhsprovregis.columns],
            data=dfmhsprovregis.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            export_format='xlsx',
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 70},
            page_size=10
        ), style=cardtbl_style
    ),
    if ndaftar and prov == 'daftar':
        return not is_open, isiDaftar
    if nlolos and prov == 'lolos':
        return not is_open, isiLolos
    if nregis and prov == 'regis':
        return not is_open, isiRegis
    return is_open, None


@app.callback(
    Output("cll_tblJml", "is_open"),
    [Input("cll_grfJml", "n_clicks")],
    [State("cll_tblJml", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tblPersenNaik", "is_open"),
    [Input("cll_grfPersenNaik", "n_clicks")],
    [State("cll_tblPersenNaik", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# SHOW GRAPHIC ANALYSIS
@app.callback(
    Output('grf_mhsseleksi', 'figure'),
    Input('Fromdrpdwn_mhsseleksi', 'value'),
    Input('Todrpdwn_mhsseleksi', 'value'),
)
def graphSeleksi(valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''select 
dataMahasiswa.tahun_aka as 'Tahun Ajaran', dy_tampung as 'Daya Tampung',jml_pendaftar as 'Pendaftar', 
lolos as 'Lolos Seleksi', registrasi as 'Registrasi',baru as 'Baru Reguler', Barutransfer as 'Baru Transfer', 
aktif.jmlaktif as 'Aktif Reguler', 0 as 'Aktif Transfer' from (
    select dataPendaftar.*, count(id_tanggal_lolos_seleksi) as lolos, count(id_tanggal_registrasi) as registrasi,count(id_mahasiswa) as baru,  
    0 as Barutransfer
    from(
    select dy.id_semester, tahun_ajaran as tahun_aka, dy.jumlah as dy_tampung, count(fpmbDaftar.id_pmb)  as jml_pendaftar 
    from dim_daya_tampung dy
    inner join dim_semester smstr on dy.id_semester = smstr.id_semester
    inner join dim_prodi prodi on prodi.id_prodi = dy.id_prodi
    left join fact_pmb fpmbDaftar on dy.id_semester = fpmbDaftar.id_semester and (fpmbDaftar.id_prodi_pilihan_1 || fpmbDaftar.id_prodi_pilihan_3 || fpmbDaftar.id_prodi_pilihan_3 = 9)
    where kode_prodi = '71' and dy.id_semester <= (select id_semester from dim_semester where tahun_ajaran=concat(year(now())-1,'/',year(now())) limit 1)
    group 
    by tahun_aka, dy_tampung, dy.id_semester
    ) dataPendaftar
    left join fact_pmb fpmbLolos on dataPendaftar.id_semester = fpmbLolos.id_semester and fpmbLolos.id_prodi_diterima = 9
    group by id_semester, tahun_aka,dy_tampung, jml_pendaftar
    order by id_semester asc
)dataMahasiswa
left join (
select count(*) as jmlaktif, tahun_ajaran from fact_mahasiswa_status
left join dim_semester on fact_mahasiswa_status.id_semester = dim_semester.id_semester
where status = 'AK' 
group by tahun_ajaran
)aktif on aktif.tahun_ajaran = tahun_aka
where tahun_ajaran between 
%(From)s and %(To)s''', {'From': valueFrom, 'To': valueTo})
    if (len(df['Daya Tampung']) != 0):
        fig = px.bar(df, x=df['Tahun Ajaran'], y=df['Daya Tampung'], color=px.Constant('Daya Tampung'),
                     labels=dict(x="Tahun Ajaran", y="Jumlah", color="Jenis Pendaftar"))
        fig.add_scatter(x=df['Tahun Ajaran'], y=df['Pendaftar'], name='Pendaftar',
                        hovertemplate="Jenis Pendaftar=Pendaftar <br>Jumlah=%{y} </br> Tahun Ajaran= %{x}")
        fig.add_scatter(x=df['Tahun Ajaran'], y=df['Lolos Seleksi'], name='Lolos Seleksi',
                        line=dict(color='rgb(225, 210, 0)'),
                        hovertemplate="Jenis Pendaftar=Lolos Seleksi <br>Jumlah=%{y} </br> Tahun Ajaran= %{x}")
        fig.add_scatter(x=df['Tahun Ajaran'], y=df['Registrasi'], name='Registrasi',
                        line=dict(color='green'),
                        hovertemplate="Jenis Pendaftar=Registrasi <br>Jumlah=%{y} </br> Tahun Ajaran= %{x}")
        # fig.add_scatter(x=df['Tahun Ajaran'], y=df['Baru Reguler'], name='Baru Reguler',
        #                 line=dict(color='rgb(0, 143, 245)'),
        #                 hovertemplate="Jenis Pendaftar=Baru Reguler <br>Jumlah=%{y} </br> Tahun Ajaran= %{x}")
        # fig.add_scatter(x=df['Tahun Ajaran'], y=df['Baru Transfer'], name='Baru Transfer',
        #                 line=dict(color='rgb(35, 68, 145)'),
        #                 hovertemplate="Jenis Pendaftar=Baru Transfer <br>Jumlah=%{y} </br> Tahun Ajaran= %{x}")
        # fig.add_scatter(x=df['Tahun Ajaran'], y=df['Aktif Reguler'], name='Aktif Reguler',
        #                 line=dict(color='rgb(54, 235, 54)'),
        #                 hovertemplate="Jenis Pendaftar=Aktif Reguler <br>Jumlah=%{y} </br> Tahun Ajaran= %{x}")
        # fig.add_scatter(x=df['Tahun Ajaran'], y=df['Aktif Transfer'], name='Aktif Transfer',
        #                 line=dict(color='rgb(35, 145, 35)'),
        #                 hovertemplate="Jenis Pendaftar=Aktif Transfer <br>Jumlah=%{y} </br> Tahun Ajaran= %{x}")
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


@app.callback(
    Output("grf_mahasiswaAktif", 'figure'),
    Input('Fromdrpdwn_mhsAktif', 'value'),
    Input('Todrpdwn_mhsAktif', 'value'),
)
def FillAktif(valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''select ds.tahun_ajaran 'Tahun Ajaran', ds.semester_nama Semester, 
    count(*) as 'Jumlah Mahasiswa Aktif' from fact_mahasiswa_status fms
inner join dim_semester ds on ds.id_semester = fms.id_semester
where fms.status = 'AK' and ds.tahun_ajaran between %(From)s and %(To)s
group by ds.tahun_ajaran, ds.semester_nama
order by ds.tahun_ajaran, ds.semester_nama
''', {'From': valueFrom, 'To': valueTo})
    if (len(df['Tahun Ajaran']) != 0):
        fig = px.bar(df, x=df['Tahun Ajaran'], y=df['Jumlah Mahasiswa Aktif'], color=df['Semester'])
        fig.update_layout(barmode='group')
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


@app.callback(
    Output('grf_mhsasing', 'figure'),
    Input('Fromdrpdwn_mhsasing', 'value'),
    Input('Todrpdwn_mhsasing', 'value'),
)
def graphMhsAsing(valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''select tahun_semster as "Tahun Semester", Jumlah, parttime,(Jumlah - parttime) as fulltime
from (
select concat(cast(tahun_angkatan-1 as char(4)),'/',tahun_angkatan) as tahun_semster, count(*) as Jumlah,
SUM(if(substr(nim,3,3)= 'ASG', 1, 0)) AS parttime
from dim_mahasiswa
inner join dim_prodi on dim_mahasiswa.id_prodi = dim_prodi.id_prodi AND (dim_prodi.id_prodi = 9||10)
where warga_negara = 'WNA'
group by tahun_semster, tahun_angkatan
) data
inner join dim_semester on dim_semester.tahun_ajaran = data.tahun_semster AND semester = 1 
where tahun_ajaran between 
%(From)s and %(To)s
order by tahun_semster asc''', {'From': valueFrom, 'To': valueTo})
    if (len(df['Tahun Semester']) != 0):
        fig = px.bar(df, x=df['Tahun Semester'], y=df['Jumlah'], color=px.Constant('Jumlah Total'),
                     labels=dict(x="Tahun Semester", y="Jumlah", color="Jenis Mahasiswa"))
        fig.add_scatter(x=df['Tahun Semester'], y=df['fulltime'], name='Full Time',
                        hovertemplate="Jenis Pendaftar=Full Time <br>Jumlah=%{y} </br> Tahun Semester= %{x}")
        fig.add_scatter(x=df['Tahun Semester'], y=df['parttime'], name='Part Time',
                        hovertemplate="Jenis Pendaftar=Part Time <br>Jumlah=%{y} </br> Tahun Semester= %{x}")
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


@app.callback(
    Output('grf_mhsasingINF', 'figure'),
    Input('Fromdrpdwn_mhsasing', 'value'),
    Input('Todrpdwn_mhsasing', 'value'),
)
def graphMhsAsingINF(valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''select data.nama_prodi,tahun_semster as "Tahun Semester", Jumlah, parttime, (jumlah - parttime) as fulltime
from (
select dim_prodi.nama_prodi, concat(cast(tahun_angkatan-1 as char(4)),'/',tahun_angkatan) as tahun_semster, 
count(*) as jumlah,
SUM(if(substr(nim,3,3)= 'ASG', 1, 0)) AS parttime
from dim_mahasiswa
inner join dim_prodi on dim_mahasiswa.id_prodi = dim_prodi.id_prodi AND (dim_prodi.id_prodi = 9)
where warga_negara = 'WNA'
group by dim_prodi.nama_prodi,tahun_semster, tahun_angkatan
) data
inner join dim_semester on dim_semester.tahun_ajaran = data.tahun_semster
where tahun_ajaran between 
%(From)s and %(To)s
order by nama_prodi, tahun_semster asc''', {'From': valueFrom, 'To': valueTo})
    if (len(df['Tahun Semester']) != 0):
        fig = px.bar(df, x=df['Tahun Semester'], y=df['Jumlah'], color=px.Constant('Jumlah Total'),
                     labels=dict(x="Tahun Semester", y="Jumlah", color="Jenis Mahasiswa"))
        fig.add_scatter(x=df['Tahun Semester'], y=df['fulltime'], name='Full Time',
                        hovertemplate="Jenis Pendaftar=Full Time <br>Jumlah=%{y} </br> Tahun Semester= %{x}")
        fig.add_scatter(x=df['Tahun Semester'], y=df['parttime'], name='Part Time',
                        hovertemplate="Jenis Pendaftar=Part Time <br>Jumlah=%{y} </br> Tahun Semester= %{x}")
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


@app.callback(
    Output('grf_mhsasingSI', 'figure'),
    Input('Fromdrpdwn_mhsasing', 'value'),
    Input('Todrpdwn_mhsasing', 'value'),
)
def graphMhsAsingSI(valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''select data.nama_prodi,tahun_semster as "Tahun Semester", Jumlah, parttime, (jumlah - parttime) as fulltime
from (
select dim_prodi.nama_prodi, concat(cast(tahun_angkatan-1 as char(4)),'/',tahun_angkatan) as tahun_semster, count(*) as jumlah,
SUM(if(substr(nim,3,3)= 'ASG', 1, 0)) AS parttime
from dim_mahasiswa
inner join dim_prodi on dim_mahasiswa.id_prodi = dim_prodi.id_prodi AND (dim_prodi.id_prodi = 10)
where warga_negara = 'WNA'
group by dim_prodi.nama_prodi,tahun_semster, tahun_angkatan
) data
inner join dim_semester on dim_semester.tahun_ajaran = data.tahun_semster AND semester = 1
where tahun_ajaran between 
%(From)s and %(To)s
order by nama_prodi, tahun_semster asc''', {'From': valueFrom, 'To': valueTo})
    if (len(df['Tahun Semester']) != 0):
        fig = px.bar(df, x=df['Tahun Semester'], y=df['Jumlah'], color=px.Constant('Jumlah Total'),
                     labels=dict(x="Tahun Semester", y="Jumlah", color="Jenis Mahasiswa"))
        fig.add_scatter(x=df['Tahun Semester'], y=df['fulltime'], name='Full Time',
                        hovertemplate="Jenis Pendaftar=Full Time <br>Jumlah=%{y} </br> Tahun Semester= %{x}")
        fig.add_scatter(x=df['Tahun Semester'], y=df['parttime'], name='Part Time',
                        hovertemplate="Jenis Pendaftar=Part Time <br>Jumlah=%{y} </br> Tahun Semester= %{x}")
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


# @app.callback(
#     Output('grf_mhsrasio', 'figure'),
#     Input('Fromdrpdwn_mhsrasio', 'value'),
#     Input('Todrpdwn_mhsrasio', 'value'),
# )
# def graphRasioDTPR(valueFrom, valueTo):
#     df_dayaTampung = data.getDataFrameFromDBwithParams('''select ds.tahun_ajaran as 'Tahun Ajaran', ddt.jumlah as "Jumlah Daya Tampung" from dim_daya_tampung ddt
# inner join dim_semester ds on ddt.id_semester = ds.id_semester
# where id_prodi = 9 and ds.tahun_ajaran between
# %(From)s and %(To)s''', {'From': valueFrom, 'To': valueTo})
#     df_pendaftarRegistrasi = data.getDataFrameFromDBwithParams('''select ds.tahun_ajaran as 'Tahun Ajaran', count(*)  as 'Jumlah Pendaftar'  from fact_pmb fpmb
# inner join  dim_semester ds on fpmb.id_semester = ds.id_semester
# where fpmb.id_tanggal_registrasi is not null and fpmb.id_prodi_diterima = 9
# and ds.tahun_ajaran between
# %(From)s and %(To)s
# group by ds.tahun_ajaran
# order by ds.tahun_ajaran''', {'From': valueFrom, 'To': valueTo})
#     df_lolosSeleksi = data.getDataFrameFromDBwithParams('''select ds.tahun_ajaran as 'Tahun Ajaran', count(*)  as 'Jumlah Pendaftar' from fact_pmb fpmb
# inner join  dim_semester ds on fpmb.id_semester = ds.id_semester
# where fpmb.id_tanggal_lolos_seleksi is not null and fpmb.id_prodi_diterima = 9
# and ds.tahun_ajaran between
# %(From)s and %(To)s
# group by ds.tahun_ajaran
# order by ds.tahun_ajaran''', {'From': valueFrom, 'To': valueTo})
#     df_pendaftar = data.getDataFrameFromDBwithParams('''select ds.tahun_ajaran as 'Tahun Ajaran', count(*)  as 'Jumlah Pendaftar'  from fact_pmb fpmb
# inner join  dim_semester ds on fpmb.id_semester = ds.id_semester
# where ds.tahun_ajaran between
# %(From)s and %(To)s
# group by ds.tahun_ajaran
# order by ds.tahun_ajaran''', {'From': valueFrom, 'To': valueTo})
#     if (len(df_dayaTampung['Tahun Ajaran']) != 0 and len(df_pendaftarRegistrasi['Tahun Ajaran']) != 0 and len(
#             df_lolosSeleksi['Tahun Ajaran']) != 0 and len(df_pendaftar['Tahun Ajaran']) != 0):
#         fig = px.bar(df_dayaTampung, x=df_dayaTampung['Tahun Ajaran'], y=df_dayaTampung['Jumlah Daya Tampung'],
#                      color=px.Constant('Daya Tampung'),
#                      labels=dict(x="Tahun Ajaran", y="Jumlah", color="Jenis Pendaftar"))
#         fig.add_scatter(x=df_pendaftarRegistrasi['Tahun Ajaran'], y=df_pendaftarRegistrasi['Jumlah Pendaftar'],
#                         name='Teregistrasi',
#                         hovertemplate="Jenis Pendaftar=Teregistrasi <br>Jumlah=%{y} </br> Tahun Akdemik= %{x}")
#         fig.add_scatter(x=df_lolosSeleksi['Tahun Ajaran'], y=df_lolosSeleksi['Jumlah Pendaftar'], name='Lolos Seleksi',
#                         hovertemplate="Jenis Pendaftar=Lolos Seleksi <br>Jumlah=%{y} </br> Tahun Akdemik= %{x}")
#         fig.add_scatter(x=df_pendaftar['Tahun Ajaran'], y=df_pendaftar['Jumlah Pendaftar'], name='Pendaftar',
#                         hovertemplate="Jenis Pendaftar=Pendaftar <br>Jumlah=%{y} </br> Tahun Akdemik= %{x}")
#         return fig
#     else:
#         fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
#                                          font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
#                                          yshift=10)
#         return fig


@app.callback(
    Output('grf_mhssmasmk', 'figure'),
    Input('Fromdrpdwn_mhssmasmk', 'value'),
    Input('Todrpdwn_mhssmasmk', 'value')
)
def graphAsalSekolah(valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''select
       (case
           when tipe_sekolah_asal=1 then "NEGERI"
           WHEN tipe_sekolah_asal=2 THEN "SWASTA"
           when tipe_sekolah_asal=3 then "N/A"
       END)
           as 'Tipe Sekolah Asal', ds.tahun_ajaran as 'Tahun Ajaran', count(kode_pendaftar) AS 'Jumlah Pendaftar'
from fact_pmb
inner join dim_semester ds on fact_pmb.id_semester = ds.id_semester
where fact_pmb.id_prodi_diterima = 9 and fact_pmb.id_tanggal_registrasi is not null
and ds.tahun_ajaran between 
%(From)s and %(To)s
group by ds.tahun_ajaran,'Tipe Sekolah Asal'
order by ds.tahun_ajaran''', {'From': valueFrom, 'To': valueTo})
    fig = px.bar(df, x=df['Tahun Ajaran'], y=df['Jumlah Pendaftar'], color=df['Tipe Sekolah Asal'])
    fig.update_layout(barmode='group')
    return fig


@app.callback(
    Output('grf_mhsprovdaftar', 'figure'),
    Output('visiFrom_TAdaftar', 'hidden'),
    Output('visiTo_TAdaftar', 'hidden'),
    Input('Fromdrpdwn_TAdaftar', 'value'),
    Input('Todrpdwn_TAdaftar', 'value'),
    Input('radio_daftar', 'value')
)
def graphProvinceDaftar(valueFrom, valueTo, valueRadio):
    dfJson = data.getDataFrameFromDBwithParams('''select sum(pendaftar) AS 'Jumlah Pendaftar', 
    hitungan.provinsi 'Provinsi' from(select
    dl.provinsi as 'Provinsi', ds.tahun_ajaran as 'Tahun Ajaran', count(kode_pendaftar) pendaftar
from fact_pmb
inner join dim_semester ds on fact_pmb.id_semester = ds.id_semester
inner join dim_lokasi dl ON fact_pmb.id_lokasi_rumah = dl.id_lokasi
where ds.tahun_ajaran between %(From)s and %(To)s
group by ds.tahun_ajaran, dl.provinsi) hitungan
group by provinsi
order by provinsi''', {'From': valueFrom, 'To': valueTo})
    if valueRadio == 'bar':
        if (len(dfmhsprovdaftar['Tahun Ajaran']) != 0):
            bardaftar = px.bar(dfmhsprovdaftar, x=dfmhsprovdaftar['Provinsi'], y=dfmhsprovdaftar['Jumlah Pendaftar'],
                               color=dfmhsprovdaftar['Tahun Ajaran'], barmode='group')
            bardaftar.update_layout(xaxis=go.layout.XAxis(tickangle=45))
            return bardaftar, True, True
        else:
            fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                             font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                             yshift=10)
            return fig, True, True
    else:
        if (len(dfJson['Jumlah Pendaftar']) != 0):
            jsondaftar = px.choropleth_mapbox(dfJson, geojson=province, locations="Provinsi",
                                              color_continuous_scale="Viridis",
                                              featureidkey="properties.Propinsi",
                                              center={"lat": -0.47399, "lon": 113.29266}, zoom=3.25,
                                              mapbox_style="carto-positron",
                                              color='Jumlah Pendaftar')
            return jsondaftar, False, False
        else:
            fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                             font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                             yshift=10)
            return fig, False, False


@app.callback(
    Output('grf_mhsprovlolos', 'figure'),
    Output('visiFrom_TAlolos', 'hidden'),
    Output('visiTo_TAlolos', 'hidden'),
    Input('Fromdrpdwn_TAlolos', 'value'),
    Input('Todrpdwn_TAlolos', 'value'),
    Input('radio_lolos', 'value')
)
def graphProvinceLolos(valueFrom, valueTo, valueRadio):
    dfJson = data.getDataFrameFromDBwithParams('''
    select sum(pendaftar) AS 'Pendaftar Lolos Seleksi', 
    hitungan.provinsi 'Provinsi' from(
    select dl.provinsi as 'Provinsi', ds.tahun_ajaran as 'Tahun Ajaran', count(kode_pendaftar) pendaftar
from fact_pmb
inner join dim_semester ds on fact_pmb.id_semester = ds.id_semester
inner join dim_lokasi dl ON fact_pmb.id_lokasi_rumah = dl.id_lokasi
where fact_pmb.id_tanggal_lolos_seleksi is not null and fact_pmb.id_prodi_diterima = 9
and ds.tahun_ajaran between %(From)s and %(To)s
group by ds.tahun_ajaran, dl.provinsi) hitungan
group by provinsi
order by provinsi''', {'From': valueFrom, 'To': valueTo})
    if valueRadio == 'bar':
        if (len(dfmhsprovlolos['Tahun Ajaran']) != 0):
            barlolos = px.bar(dfmhsprovlolos, x=dfmhsprovlolos['Provinsi'], y=dfmhsprovlolos['Pendaftar Lolos Seleksi'],
                              color=dfmhsprovlolos['Tahun Ajaran'], barmode='group')
            barlolos.update_layout(xaxis=go.layout.XAxis(tickangle=45))
            return barlolos, True, True
        else:
            fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                             font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                             yshift=10)
            return fig, True, True
    else:
        if (len(dfJson['Pendaftar Lolos Seleksi']) != 0):
            jsonlolos = px.choropleth_mapbox(dfJson, geojson=province, locations="Provinsi",
                                             color_continuous_scale="Viridis",
                                             featureidkey="properties.Propinsi",
                                             center={"lat": -0.47399, "lon": 113.29266}, zoom=3.25,
                                             mapbox_style="carto-positron",
                                             color='Pendaftar Lolos Seleksi')
            return jsonlolos, False, False
        else:
            fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                             font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                             yshift=10)
            return fig, False, False


@app.callback(
    Output('grf_mhsprovregis', 'figure'),
    Output('visiFrom_TAregis', 'hidden'),
    Output('visiTo_TAregis', 'hidden'),
    Input('Fromdrpdwn_TAregis', 'value'),
    Input('Todrpdwn_TAregis', 'value'),
    Input('radio_regis', 'value')
)
def graphProvinceRegis(valueFrom, valueTo, valueRadio):
    dfJson = data.getDataFrameFromDBwithParams('''
    select sum(pendaftar) AS 'Pendaftar Registrasi Ulang', 
    hitungan.provinsi 'Provinsi' from(select
    dl.provinsi as 'Provinsi', ds.tahun_ajaran, count(kode_pendaftar) pendaftar
from fact_pmb
inner join dim_semester ds on fact_pmb.id_semester = ds.id_semester
inner join dim_lokasi dl ON fact_pmb.id_lokasi_rumah = dl.id_lokasi
where fact_pmb.id_prodi_diterima = 9 and fact_pmb.id_tanggal_registrasi is not null
and ds.tahun_ajaran between %(From)s and %(To)s
group by ds.tahun_ajaran, dl.provinsi) hitungan
group by provinsi
order by provinsi''', {'From': valueFrom, 'To': valueTo})
    if valueRadio == 'bar':
        if (len(dfmhsprovregis['Tahun Ajaran']) != 0):
            barregis = px.bar(dfmhsprovregis, x=dfmhsprovregis['Provinsi'],
                              y=dfmhsprovregis['Pendaftar Registrasi Ulang'],
                              color=dfmhsprovregis['Tahun Ajaran'], barmode='group')
            barregis.update_layout(xaxis=go.layout.XAxis(tickangle=45))
            return barregis, True, True
        else:
            fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                             font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                             yshift=10)
            return fig, True, True
    else:
        if (len(dfJson['Pendaftar Registrasi Ulang']) != 0):
            jsonregis = px.choropleth_mapbox(dfJson, geojson=province, locations="Provinsi",
                                             color_continuous_scale="Viridis",
                                             featureidkey="properties.Propinsi",
                                             center={"lat": -0.789275, "lon": 113.921327}, zoom=3.25,
                                             mapbox_style="carto-positron",
                                             color='Pendaftar Registrasi Ulang')
            return jsonregis, False, False
        else:
            fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                             font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                             yshift=10)
            return fig, False, False


# @app.callback(
#     Output('grf_mhsJml', 'figure'),
#     Input('Fromdrpdwn_mhsJml', 'value'),
#     Input('Todrpdwn_mhsJml', 'value')
# )
# def graphPerkembanganJumlahMaba(valueFrom, valueTo):
#     df = data.getDataFrameFromDBwithParams(
#         '''select tahun_ajaran "Tahun Ajaran",
#         count(distinct fp.id_mahasiswa) Jumlah
#         from fact_pmb fp
#         inner join dim_date dd on dd.id_date = fp.id_tanggal_registrasi
#         inner join dim_semester ds on ds.kode_semester = concat(tahun, if(bulan >= 7, 2, 1))
#         inner join dim_mahasiswa dm on fp.id_mahasiswa = dm.id_mahasiswa
#         where nim like %(TI)s and ds.tahun_ajaran between %(From)s and %(To)s
#         group by tahun_ajaran
#         order by tahun_ajaran''', {'From': valueFrom, 'To': valueTo, 'TI': '71%'})
#     if (len(df['Tahun Ajaran']) != 0):
#         fig = px.line(df, x=df['Tahun Ajaran'], y=df['Jumlah'], )
#         fig.update_traces(mode='lines+markers')
#         return fig
#     else:
#         fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
#                                          font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
#                                          yshift=10)
#         return fig


@app.callback(
    Output('grf_mhsPersenNaik', 'figure'),
    Input('Fromdrpdwn_mhsPersenNaik', 'value'),
    Input('Todrpdwn_mhsPersenNaik', 'value')
)
def graphPersentaseKenaikanMaba(valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''select tahun_ajaran as 'Tahun Ajaran',
       if(@last_entry = 0, 0, format(((entry-@last_entry)/@last_entry)*100,2)) as 'Persentase Pertumbuhan',
        @last_entry := entry 'Jumlah'
from
      (select @last_entry := 0) x,
      (select tahun_ajaran, count(distinct fp.id_mahasiswa) entry
       from   fact_pmb fp
         inner join dim_date dd on dd.id_date = fp.id_tanggal_registrasi
         inner join dim_semester ds on ds.kode_semester = concat(tahun, if(bulan >= 7, 2, 1))
         inner join dim_mahasiswa dm on fp.id_mahasiswa = dm.id_mahasiswa
         where id_tanggal_registrasi is not null and ds.tahun_ajaran between %(From)s and %(To)s
       group by tahun_ajaran) y
order by tahun_ajaran''', {'From': valueFrom, 'To': valueTo})
    if (len(df['Tahun Ajaran']) != 0):
        fig = px.line(df, x=df['Tahun Ajaran'], y=df['Persentase Pertumbuhan'].apply(pd.to_numeric))
        fig.update_layout(yaxis_title="Persentase Pertumbuhan (%)")
        fig.update_traces(mode='lines+markers')
        fig.update_yaxes(categoryorder='category ascending')
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig
