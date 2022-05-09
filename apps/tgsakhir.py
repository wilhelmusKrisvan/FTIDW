import dash
import pandas as pd
import dash_table as dt
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from sqlalchemy import create_engine
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
from appConfig import app
from datetime import date
import model.dao_tgsakhir as data

# con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

dfdosbing = data.getMahasiswaBimbinganSkripsi()
dflulusan = data.getIPK()

dfavgmasa = data.getRateMasaStudi()
dfmasastudilulusan = data.getMasaStudi()

dfkppkm = data.getMahasiswaKPpkm()
dfkpall = data.getMahasiswaKP()

dfjumllulusan = data.getJmlLulusan()
dfjumllulusanot = data.getJumlLulusSkripsiOntime()

dfskripmhs = data.getMhahasiswaSkripsipkm()
dfmitra = data.getMitraKP()
dfmitraSkripsi=data.getMitraSkripsi()
dfttgumhs = data.getTTGU()
dfpersen_mhsLulus = data.getMahasiswaLulus()
dfpersen_mhsLulusAngkt = data.getMahasiswaLulusBandingTotal()

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

cardtbl_style = {
    'border': '1px solid #fafafa',
    'border-radius': '10px',
    'padding': '20px 10px 60px 10px',
    'box-shadow': '5px 10px 30px #ebedeb'
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

listDropdownSem = ['GASAL','GENAP']

listDropdownTA = []
for x in range(0, 5):
    counter = x + 1
    listDropdownTA.append(
        str(int(date.today().strftime('%Y')) - 5 + x) + '/' + str(int(date.today().strftime('%Y')) - 4 + x))

listDropdownTh = []
for x in range(0, 5):
    counter = x + 1
    listDropdownTh.append(str(int(date.today().strftime('%Y')) - 5 + x))

#------------KP------------
kp_prodi = dbc.Container([
    dbc.Card([
        html.H5('KP Prodi Informatika',
                style=ttlgrf_style),
        dbc.Row([
            dbc.Col([
                html.P('Dari :', style={'marginBottom': 0}),
                dcc.Dropdown(
                    id='fltrKPProdStart',
                    options=[{'label': i, 'value': i} for i in listDropdownTA],
                    value=listDropdownTA[0],
                    style={'color': 'black'},
                    clearable=False
                )
            ]),
            dbc.Col([
                html.P('Sampai :', style={'marginBottom': 0}),
                dcc.Dropdown(
                    id='fltrKPProdEnd',
                    options=[{'label': i, 'value': i} for i in listDropdownTA],
                    value=listDropdownTA[3],
                    style={'color': 'black'},
                    clearable=False
                )
            ])
        ], style={'padding': '15px'}),
        dcc.Tabs([
            dcc.Tab(label='All', value='all',
                    children=[
                        html.Div([
                            dcc.Loading(
                                id='loading-1',
                                type="default",
                                children=dcc.Graph(id='grf_kpall')),
                            dbc.Button('Lihat Semua Data', id='cll_grfkpall', n_clicks=0,
                                       style=button_style)
                        ])
                    ], style=tab_style, selected_style=selected_style),
            dcc.Tab(label='PKM Dosen', value='PKMDosen',
                    children=[
                        html.Div([
                            dcc.Loading(
                                id='loading-1',
                                type="default",
                                children=dcc.Graph(id='grf_kppkm')),
                            dbc.Button('Lihat Semua Data', id='cll_grfkppkm', n_clicks=0,
                                       style=button_style),
                        ])
                    ], style=tab_style, selected_style=selected_style)
        ], style=tab_style, id='tab_kpall', value='all'
        )
    ], style=cardgrf_style
    ),
    dbc.Collapse(
        id='cll_tblkp',
        is_open=False
    )
], style=cont_style)

ttguKP = dbc.Container([
    dbc.Card([
        html.H5('Mahasiswa KP yang Memiliki output Teknologi Tepat Guna (TTGU)',
                style=ttlgrf_style),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.P('Dari : ', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrKPTTGUStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                        value=listDropdownTA[0],
                        style={'color': 'black'},
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Sampai : ', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrKPTTGUEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                        value=listDropdownTA[3],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ]),
            dcc.Loading(
                id='loading-1',
                type="default",
                children=dcc.Graph(id='grf_kpttgu')),
            dbc.Button('Lihat Semua Data', id='cll_grfkpttgu', n_clicks=0, style=button_style)
        ])
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_ttgumhs',
                columns=[{"name": i, "id": i} for i in dfttgumhs.columns],
                data=dfttgumhs.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'height': '100%', 'padding': '10px',
                             'overflowY': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                export_format='xlsx',
                page_size=5
            ), style=cardtbl_style
        ),
        id='cll_tblkpttgu',
        is_open=False
    )
], style=cont_style)

#------------SKRIPSI------------
skripsi = dbc.Container([
    dbc.Card([
        html.H5('Skripsi Prodi Informatika', style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Dari : ', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrSkripsiPKMStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                        value=listDropdownTA[0],
                        style={'color': 'black'},
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Sampai : ', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrSkripsiPKMEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                        value=listDropdownTA[3],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ])
        ]),
        dcc.Tabs([
            dcc.Tab(label='All', value='all',
                    children=[
                        html.Div([
                            dcc.Loading(
                                id='loading-1',
                                type="default",
                                children=dcc.Graph(id='grf_skripsipkm')),
                            dbc.Button('Lihat Semua Data', id='cll_grfskripsipkm', n_clicks=0,
                                       style=button_style)
                        ]),
                    ], style=tab_style, selected_style=selected_style),
            dcc.Tab(label='PKM Skripsi Mahasiswa', value='PKMSkripsi',
                    children=[
                        html.Div([
                            dcc.Loading(
                                id='loading-1',
                                type="default",
                                children=dcc.Graph(id='grf_skripsipkmPersen')),
                            dbc.Button('Lihat Semua Data', id='cll_grfskripsipkmPersen', n_clicks=0,
                                       style=button_style)
                        ])
                    ], style=tab_style, selected_style=selected_style)
        ], style=tab_style, id='tab_pkmall', value='all'
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_tblskripsipkm',
        is_open=False
    )
], style=cont_style)
# skripsii = dbc.Container([
#     dbc.Row([
#         dbc.Col(
#             dbc.Card([
#                 html.H5('Mahasiswa Skripsi Terlibat PKM',
#                         style=ttlgrf_style),
#                 dt.DataTable(
#                     id='tbl_skripmhs',
#                     columns=[{"name": i, "id": i} for i in dfskripmhs.columns],
#                     data=dfskripmhs.to_dict('records'),
#                     sort_action='native',
#                     sort_mode='multi',
#                     style_table={'width': '100%', 'height': '100%', 'padding': '10px',
#                                  'overflowY': 'auto', 'margin-top': '25px'},
#                     style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
#                     style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
#                     page_size=5
#                 )
#             ], style=cardgrf_style
#             ),
#         )
#     ], style={'margin-top': '10px'})
# ], style=cont_style)

dosbing = dbc.Container([
    dbc.Card([
        html.H5('3.b. Dosen Pembimbing Tugas Akhir', style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody([
                dbc.Row(
                    dbc.Col([
                        html.Div([
                            html.P('Tahun Ajaran :', style={'marginBottom': 0}),
                            dcc.Dropdown(
                                id='fltrDosbing',
                                options=[{'label': i, 'value': i} for i in listDropdownTA],
                                value=listDropdownTA[0],
                                style={'color': 'black'},
                                clearable=False
                            )
                        ])
                    ])
                ),
                dcc.Loading(
                    id='loading-1',
                    type="default",
                    children=dcc.Graph(id='grf_dosbing')),
                dbc.Button('Lihat Semua Data', id='cll_grfdosbing', n_clicks=0, style=button_style)
            ])
        )
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_dosbing',
                columns=[{"name": i, "id": i} for i in dfdosbing.columns],
                data=dfdosbing.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                page_size=10,
                export_format='xlsx'
            ), style=cardtbl_style
        ),
        id='cll_tbldosbing',
        is_open=False
    )
], style=cont_style)
# dosbingg = dbc.Container([
#     dbc.Card([
#         html.H5('3.b. Dosen Pembimbing Tugas Akhir',
#                 style=ttlgrf_style),
#         dbc.CardLink(
#             dbc.CardBody([
#                 html.P('Tahun Ajaran :', style={'marginBottom': 0}),
#                 dcc.Dropdown(
#                     id='fltrDosbing',
#                     options=[{'label': i, 'value': i} for i in listDropdownTA],
#                     value=listDropdownTA[0],
#                     style={'color': 'black'},
#                     clearable=False
#                 ),
#                 dcc.Graph(id='grf_dosbing')
#             ]),
#             id='cll_grfdosbing',
#             n_clicks=0
#         ),
#     ], style=cardgrf_style),
#     dbc.Collapse(
#         dbc.Card(
#             dt.DataTable(
#                 id='tbl_dosbing',
#                 columns=[{"name": i, "id": i} for i in dfdosbing.columns],
#                 data=dfdosbing.to_dict('records'),
#                 sort_action='native',
#                 sort_mode='multi',
#                 style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
#                 style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
#                 style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
#                 page_size=10,
#                 export_format='xlsx'
#             ), style=cardgrf_style
#         ),
#         id='cll_tbldosbing',
#         is_open=False
#     )
# ], style=cont_style)

#------------YUDISIUM------------

persen_mhsLulus = dbc.Container([
    dbc.Card([
        html.H5('Persentase Lulusan',
                style=ttlgrf_style),
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Tepat Waktu per Tahun Ajaran', value='llsontime',
                        children=[
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.P('Dari :', style={'marginBottom': 0}),
                                        dcc.Dropdown(
                                            id='fltrLulusOTStart',
                                            options=[{'label': i, 'value': i} for i in listDropdownTA],
                                            value=listDropdownTA[0],
                                            style={'color': 'black'},
                                            clearable=False
                                        )
                                    ]),
                                    dbc.Col([
                                        html.P('Sampai :', style={'marginBottom': 0}),
                                        dcc.Dropdown(
                                            id='fltrLulusOTEnd',
                                            options=[{'label': i, 'value': i} for i in listDropdownTA],
                                            value=listDropdownTA[3],
                                            style={'color': 'black'},
                                            clearable=False
                                        )
                                    ])
                                ])
                            ]),
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.P('Visualisasi :', style={'margin-bottom': '0', 'margin-top': '10px'}),
                                        dcc.RadioItems(
                                            id='radio_llsnot',
                                            options=[{'label': 'Jumlah', 'value': 'jumlot'},
                                                     {'label': 'Persetase Lulusan OT : Mahasiswa', 'value': 'persenot'}
                                                     ],
                                            value='jumlot',
                                            style={'width': '100%', 'padding': '0px', },
                                            className='card-body',
                                            labelStyle={'display': 'block', 'display': 'inline-block',
                                                        'margin-right': '10%', 'margin-top': '5px'}
                                        )
                                    ], style={'padding-left': '5%'})
                                ], style={'padding-left': '5%', 'margin-bottom': '0px'}),
                                dcc.Loading(
                                    id='loading-1',
                                    type="default",
                                    children=dcc.Graph(id='grf_llsontime')),
                                dbc.Button('Lihat Semua Data', id='cll_grfllsontime', n_clicks=0,
                                            style=button_style)
                            ])
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='per Total Jumlah Mahasiswa', value='llstotal',
                        children=[
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.P('Dari :', style={'marginBottom': 0}),
                                        dcc.Dropdown(
                                            id='fltrLulusTotStart',
                                            options=[{'label': i, 'value': i} for i in listDropdownTh],
                                            value=listDropdownTh[0],
                                            style={'color': 'black'},
                                            clearable=False
                                        )
                                    ]),
                                    dbc.Col([
                                        html.P('Sampai :', style={'marginBottom': 0}),
                                        dcc.Dropdown(
                                            id='fltrLulusTotEnd',
                                            options=[{'label': i, 'value': i} for i in listDropdownTh],
                                            value=listDropdownTh[3],
                                            style={'color': 'black'},
                                            clearable=False
                                        )
                                    ])
                                ])
                            ]),
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.P('Visualisasi :', style={'margin-bottom': '0', 'margin-top': '10px'}),
                                        dcc.RadioItems(
                                            id='radio_llsntot',
                                            options=[{'label': 'Jumlah', 'value': 'jumltot'},
                                                     {'label': 'Persetase Lulusan : Mahasiswa', 'value': 'persentot'}
                                                     ],
                                            value='jumltot',
                                            style={'width': '100%', 'padding': '0px', },
                                            className='card-body',
                                            labelStyle={'display': 'block', 'display': 'inline-block',
                                                        'margin-right': '10%', 'margin-top': '5px'}
                                        )
                                    ], style={'padding-left': '5%'})
                                ], style={'padding-left': '5%', 'margin-bottom': '0px'}),
                                dcc.Loading(
                                    id='loading-1',
                                    type="default",
                                    children=dcc.Graph(id='grf_llstotal')),
                                dbc.Button('Lihat Semua Data', id='cll_grfllstotal', n_clicks=0,
                                            style=button_style),
                            ])
                        ], style=tab_style, selected_style=selected_style)
            ], style=tab_style, id='tab_kppersenlls', value='llsontime'
            )
        ])
    ], style=cardgrf_style
    ),
    dbc.Collapse(
        id='cll_tblpersenlls',
        is_open=False
    )
], style=cont_style)
# persen_mhsLuluss = dbc.Container([
#     dbc.Row([
#         dbc.Col(
#             dbc.Card([
#                 html.H5('Persentase Mahasiswa Lulus Tepat Waktu setiap Tahun Ajaran',
#                         style=ttlgrf_style),
#                 dt.DataTable(
#                     id='tbl_persen_mhsLulus',
#                     columns=[{"name": i, "id": i} for i in dfpersen_mhsLulus.columns],
#                     data=dfpersen_mhsLulus.to_dict('records'),
#                     sort_action='native',
#                     sort_mode='multi',
#                     style_table={'width': '100%', 'height': '100%', 'padding': '10px',
#                                  'overflowY': 'auto', 'margin-top': '25px'},
#                     style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
#                     style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
#                     page_size=5
#                 )
#             ], style=cardgrf_style
#             ),
#         ),
#         dbc.Col([
#             dbc.Card([
#                 html.H5('Persentase Mahasiswa Lulus dibanding Total Jumlah Mahasiswa',
#                         style=ttlgrf_style),
#                 dt.DataTable(
#                     id='tbl_persen_mhsLulusAngkt',
#                     columns=[{"name": i, "id": i} for i in dfpersen_mhsLulusAngkt.columns],
#                     data=dfpersen_mhsLulusAngkt.to_dict('records'),
#                     sort_action='native',
#                     sort_mode='multi',
#                     style_table={'width': '100%', 'height': '100%', 'padding': '10px',
#                                  'overflowY': 'auto', 'margin-top': '25px'},
#                     style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
#                     style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
#                     page_size=3
#                 )
#             ], style=cardgrf_style
#             ),
#         ]),
#     ], style={'margin-top': '10px'})
# ], style=cont_style)

ipk_lulusan = dbc.Container([
    dbc.Card([
        html.H5('8.a. IPK Lulusan',
                style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Dari :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrIPKStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                        value=listDropdownTA[0],
                        style={'color': 'black'},
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Sampai :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrIPKEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                        value=listDropdownTA[3],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ])
        ]),
        html.Div([
            dcc.Loading(
                id='loading-1',
                type="default",
                children=dcc.Graph(id='grf_ipklulusan')),
            dbc.Button('Lihat Semua Data', id='cll_grfipklulusan', n_clicks=0,
                        style=button_style)
        ])
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_lulusan',
                columns=[{"name": i, "id": i} for i in dflulusan.columns],
                data=dflulusan.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                page_size=10,
                export_format='xlsx'
            ), style=cardtbl_style
        ),
        id='cll_tbllulusan',
        is_open=False,
    )
], style=cont_style)

juml_lulusan = dbc.Container([
    dbc.Card([
        html.H5('Jumlah Lulusan', style=ttlgrf_style),
        dbc.CardBody([
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.P('Dari :', style={'marginBottom': 0}),
                        dcc.Dropdown(
                            id='fltrLulusanStart',
                            options=[{'label': i, 'value': i} for i in listDropdownTA],
                            value=listDropdownTA[0],
                            style={'color': 'black'},
                            clearable=False
                        )
                    ]),
                    dbc.Col([
                        html.P('Sampai :', style={'marginBottom': 0}),
                        dcc.Dropdown(
                            id='fltrLulusanEnd',
                            options=[{'label': i, 'value': i} for i in listDropdownTA],
                            value=listDropdownTA[3],
                            style={'color': 'black'},
                            clearable=False
                        )
                    ])
                ])
            ]),
            html.Div([
                dcc.Tabs([
                    dcc.Tab(label='Per Semester Yudisium',value='all',
                            children=[
                                dcc.Loading(
                                    id='loading-1',
                                    type="default",
                                    children=dcc.Graph(id='grf_jmllulusan')),
                                dbc.Button('Lihat Semua Data',id='cll_grflulusanall',n_clicks=0, style=button_style)
                            ], style=tab_style, selected_style=selected_style),
                    dcc.Tab(label='Skripsi Tepat Waktu (3.5 - 4.5 Tahun)', value='ontime',
                            children=[
                                dcc.Loading(
                                    id='loading-1',
                                    type="default",
                                    children=dcc.Graph(id='grf_skripsiontime')),
                                dbc.Button('Lihat Semua Data',id='cll_grflulusanot', n_clicks=0, style=button_style)
                            ], style=tab_style, selected_style=selected_style)
                ], style=tab_style, id='tab_lulusan', value='all')
            ])
        ])
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_tbljumllulusan',
        is_open=False
    )
], style=cont_style)

masa_studi = dbc.Container([
    dbc.Card([
        html.H5('Masa Studi Lulusan', style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Dari :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrMSStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                        value=listDropdownTA[0],
                        style={'color': 'black'},
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Sampai :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrMSEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                        value=listDropdownTA[3],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ])
        ]),
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Masa Studi Lulusan Berdasarkan Kategori per Semester', value='all',
                        children=[
                            dcc.Loading(
                                id='loading-1',
                                type="default",
                                children=dcc.Graph(id='grf_msall')),
                            dbc.Button('Lihat Semua Data', id='cll_grfmasaall', n_clicks=0, style=button_style)
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Rata-rata Masa Studi Lulusan per Tahun Ajaran Yudisium', value='rerata',
                        children=[
                            dcc.Loading(
                                id='loading-1',
                                type="default",
                                children=dcc.Graph(id='grf_msrerata')),
                            dbc.Button('Lihat Semua Data', id='cll_grfmasarerata', n_clicks=0, style=button_style)
                        ], style=tab_style, selected_style=selected_style)
            ], style=tab_style, id='tab_masa', value='all')
        ])
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_tblmasa',
        is_open=False)
], style=cont_style)

mitra = dbc.Container([
    dbc.Card([
        html.H5('Mitra yang Terlibat KP',style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Semester:', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrMitraKPSem',
                        options=[{'label': i, 'value': i} for i in listDropdownSem],
                        value=listDropdownSem[0],
                        style={'color': 'black'},
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Tahun Ajaran : ', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrMitraKPTA',
                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                        value=listDropdownTA[0],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ])
        ]),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Visualisasi :', style={'margin-bottom': '0', 'margin-top': '10px'}),
                    dcc.RadioItems(
                        id='radio_mitrakp',
                        options=[{'label': 'Top 10 Mitra (KP Terbanyak)', 'value': 'top'},
                                 {'label': 'Jenis Mitra', 'value': 'jenis'},
                                 {'label': 'Wilayah Mitra', 'value': 'wilayah'}
                                 ],
                        value='top',
                        style={'width': '100%', 'padding': '0px', },
                        className='card-body',
                        labelStyle={'display': 'block', 'display': 'inline-block',
                                    'margin-right': '10%', 'margin-top': '5px'}
                    )
                ], style={'padding-left': '5%'}),
            ], style={'padding-left': '5%', 'margin-bottom': '0px'}),
            dcc.Loading(
                id='loading-1',
                type="default",
                children=dcc.Graph(id='grf_mitra')),
            dbc.Button('Lihat Semua Data', id='cll_grfmitra', n_clicks=0,
                       style=button_style)
        ], style={'textAlign': 'center'})
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                    id='tbl_mitra',
                    columns=[{"name": i, "id": i} for i in dfmitra.columns],
                    data=dfmitra.to_dict('records'),
                    sort_action='native',
                    sort_mode='multi',
                    style_table={'width': '100%', 'height': '100%', 'padding': '10px',
                                 'overflowY': 'auto', 'margin-top': '25px'},
                    style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    page_size=5
                ), style=cardgrf_style
        ),
        id='cll_tblmitra',
        is_open=False
    )
], style=cont_style)

mitraSkripsi = dbc.Container([
    dbc.Card([
        html.H5('Mitra yang Terlibat Skripsi',style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Semester:', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrMitraSSem',
                        options=[{'label': i, 'value': i} for i in listDropdownSem],
                        value=listDropdownSem[0],
                        style={'color': 'black'},
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Tahun Ajaran : ', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrMitraSTA',
                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                        value=listDropdownTA[2],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ])
        ]),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Visualisasi :', style={'margin-bottom': '0', 'margin-top': '10px'}),
                    dcc.RadioItems(
                        id='radio_mitraS',
                        options=[{'label': 'Top 10 Mitra (Skripsi Terbanyak)', 'value': 'top'},
                                 {'label': 'Jenis Mitra', 'value': 'jenis'},
                                 {'label': 'Wilayah Mitra', 'value': 'wilayah'}
                                 ],
                        value='top',
                        style={'width': '100%', 'padding': '0px', },
                        className='card-body',
                        labelStyle={'display': 'block', 'display': 'inline-block',
                                    'margin-right': '10%', 'margin-top': '5px'}
                    )
                ], style={'padding-left': '5%'}),
            ], style={'padding-left': '5%', 'margin-bottom': '0px'}),
            dcc.Loading(
                id='loading-1',
                type="default",
                children=dcc.Graph(id='grf_mitraS')),
            dbc.Button('Lihat Semua Data', id='cll_grfmitraS', n_clicks=0,
                       style=button_style)
        ], style={'textAlign': 'center'})
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                    id='tbl_mitra',
                    columns=[{"name": i, "id": i} for i in dfmitraSkripsi.columns],
                    data=dfmitraSkripsi.to_dict('records'),
                    sort_action='native',
                    sort_mode='multi',
                    style_table={'width': '100%', 'height': '100%', 'padding': '10px',
                                 'overflowY': 'auto', 'margin-top': '25px'},
                    style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    page_size=5
                ), style=cardgrf_style
        ),
        id='cll_tblmitraS',
        is_open=False
    )
], style=cont_style)

# mitraa = dbc.Container([
#     dbc.Row([
#         dbc.Col(
#             dbc.Card([
#                 html.H5('Mitra yang Terlibat di setiap Semester berdasarkan Tingkat Wilayah',
#                         style=ttlgrf_style),
#                 dt.DataTable(
#                     id='tbl_mitra',
#                     columns=[{"name": i, "id": i} for i in dfmitra.columns],
#                     data=dfmitra.to_dict('records'),
#                     sort_action='native',
#                     sort_mode='multi',
#                     style_table={'width': '100%', 'height': '100%', 'padding': '10px',
#                                  'overflowY': 'auto', 'margin-top': '25px'},
#                     style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
#                     style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
#                     page_size=5
#                 )
#             ], style=cardgrf_style
#             ),
#         )
#     ], style={'margin-top': '10px'})
# ], style=cont_style)

#------------ALL------------
tgsakhir = dbc.Container([
    html.Div([
        dcc.Tabs([
            dcc.Tab(label='Kerja Praktik', value='kp',
                    children=[
                        kp_prodi,
                        ttguKP,
                        mitra
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Skripsi', value='skripsi',
                    children=[
                        skripsi,
                        dosbing,
                        mitraSkripsi
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Yudisium', value='yudisium',
                    children=[
                        juml_lulusan,
                        persen_mhsLulus,
                        ipk_lulusan,
                        masa_studi,
                    ],
                    style=tab_style, selected_style=selected_style)
        ], style=tabs_styles, value='kp')
    ])
])

layout = html.Div([
    html.Div(
        html.H1('Analisis KP, Skripsi, Yudisium',
                style={'margin-top': '30px', 'textAlign': 'center'}
                )
    ),
    html.Div([tgsakhir]),
    dbc.Container([
            dcc.Link([
                dbc.Button('^', style=buttonLink_style),
            ], href='#name'),
        ], style={'margin-left': '90%'})
], style={'justify-content': 'center'})


#CALLBACK
#------------KP------------
@app.callback(
    Output('cll_tblkp', 'is_open'),
    Output('cll_tblkp', 'children'),
    [Input("cll_grfkpall", "n_clicks"),
     Input("cll_grfkppkm", "n_clicks"),
     Input("tab_kpall", "value")],
    [State("cll_tblkp", "is_open")])
def toggle_collapse(nall, npkm, kp, is_open):
    dfkp = data.getDataFrameFromDB('''
    select concat(ds.tahun_ajaran,' ',ds.semester_nama) 'Semester',
           count(*) as 'Jumlah KP'
    from fact_kp fk
             inner join dim_semester ds on ds.id_semester = fk.id_semester
             inner join dim_mahasiswa dm on dm.id_mahasiswa = fk.id_mahasiswa AND dm.id_prodi = 9
    where ds.tahun_ajaran between concat(year(now()) - 5, '/', year(now()) - 4) and concat(year(now()), '/', year(now()) + 1)
    group by Semester
    order by `Semester` asc''')
    dfppkm = data.getDataFrameFromDB('''
    select concat(dim_semester.tahun_ajaran, ' ', dim_semester.semester_nama) 'Semester',
           count(*)        as                                                 'Jumlah KP Terlibat PPKM'
    from fact_kp
             inner join dim_semester on dim_semester.id_semester = fact_kp.id_semester
             inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa = fact_kp.id_mahasiswa AND dim_mahasiswa.id_prodi = 9
    where fact_kp.is_pen_pkm = 1
      and dim_semester.tahun_ajaran between concat(year(now()) - 5, '/', year(now()) - 4) and concat(year(now()), '/', year(now()) + 1)
    group by Semester
    order by `Semester` asc
    ''')
    dfnon = data.getDataFrameFromDB('''
    select concat(dim_semester.tahun_ajaran, ' ', dim_semester.semester_nama) 'Semester',
           count(*)              as                                           'Jumlah KP Tidak Terlibat PPKM'
    from fact_kp
             inner join dim_semester on dim_semester.id_semester = fact_kp.id_semester
             inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa = fact_kp.id_mahasiswa AND dim_mahasiswa.id_prodi = 9
    where fact_kp.is_pen_pkm != 1
      and dim_semester.tahun_ajaran between concat(year(now()) - 5, '/', year(now()) - 4) and concat(year(now()), '/', year(now()) + 1)
    group by Semester
    order by `Semester` asc
    ''')
    df = pd.concat([dfkp, dfppkm, dfnon], axis=1)
    dfPersenPKM = data.getDataFrameFromDB('''
                select ak.Semester,
                       round((`Jumlah KP`/`Jumlah Mahasiswa Aktif`)*100, 2) 'Persen Keterlibatan Mahasiswa KP'
                from
                (select concat(ds.tahun_ajaran, ' ', ds.semester_nama) 'Semester',
                       count(*) as                                     'Jumlah KP'
                from fact_kp fk
                         inner join dim_semester ds on ds.id_semester = fk.id_semester
                         inner join dim_mahasiswa dm on dm.id_mahasiswa = fk.id_mahasiswa AND dm.id_prodi = 9
                where fk.is_pen_pkm = 1
                   and ds.tahun_ajaran between concat(year(now()) - 5, '/', year(now()) - 4) and concat(year(now()), '/', year(now()) + 1)
                group by Semester
                  ) pkm,
                (select concat(ds.tahun_ajaran,' ',ds.semester_nama) 'Semester',
                       count(*) as      'Jumlah Mahasiswa Aktif'
                from fact_mahasiswa_status fms
                         inner join dim_mahasiswa dmhs on fms.id_mahasiswa = dmhs.id_mahasiswa
                         inner join dim_semester ds on ds.id_semester = fms.id_semester
                where fms.status = 'AK'
                   and ds.tahun_ajaran between concat(year(now()) - 5, '/', year(now()) - 4) and concat(year(now()), '/', year(now()) + 1)
                group by Semester) ak
                where pkm.Semester=ak.Semester
                order by ak.Semester
            ''')
    isiAll = dbc.Card(
        dt.DataTable(
            id='tbl_kpall',
            # columns=[{"name": i, "id": i} for i in dfkpall.columns],
            columns=[{"name": i, "id": i} for i in df.columns],
            data=dfkpall.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    ),
    isiPKM = dbc.Card(
        dt.DataTable(
            id='tbl_kppkm',
            # columns=[{"name": i, "id": i} for i in dfkppkm.columns],
            columns=[{"name": i, "id": i} for i in dfPersenPKM.columns],
            data=dfkppkm.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    ),
    if nall and kp == 'all':
        return not is_open, isiAll
    if npkm and kp == 'PKMDosen':
        return not is_open, isiPKM
    return is_open, None


@app.callback(
    Output('grf_kpall', 'figure'),
    Output('grf_kppkm', 'figure'),
    Input('fltrKPProdStart', 'value'),
    Input('fltrKPProdEnd', 'value')
)
def graphKPProdi(thstart, thend):
    dfAll = data.getDataFrameFromDBwithParams('''
    select  concat(dim_semester.tahun_ajaran,' ',dim_semester.semester_nama)'Semester', 
            count(*) as 'Jumlah KP' 
    from fact_kp
    inner join dim_semester on dim_semester.id_semester = fact_kp.id_semester
    inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa = fact_kp.id_mahasiswa AND dim_mahasiswa.id_prodi = 9
    where dim_semester.tahun_ajaran between %(start)s and %(end)s
    group by dim_semester.tahun_ajaran, dim_semester.semester_nama, Semester
    order by  Semester 
    ''', {'start': thstart, 'end': thend})
    dfPKM = data.getDataFrameFromDBwithParams('''
    select concat(dim_semester.tahun_ajaran,' ',dim_semester.semester_nama) 'Semester',
           count(*) as 'Jumlah KP',
           'Terlibat PPKM' as Keterangan
    from fact_kp
             inner join dim_semester on dim_semester.id_semester = fact_kp.id_semester
             inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa = fact_kp.id_mahasiswa AND dim_mahasiswa.id_prodi = 9
    where fact_kp.is_pen_pkm = 1 and dim_semester.tahun_ajaran between %(start)s and %(end)s
    group by dim_semester.tahun_ajaran, dim_semester.semester_nama, Semester
    union all
    select concat(dim_semester.tahun_ajaran,' ',dim_semester.semester_nama) 'Semester',
           count(*) as 'Jumlah KP',
           'Tidak Terlibat PPKM' as Keterangan
    from fact_kp
             inner join dim_semester on dim_semester.id_semester = fact_kp.id_semester
             inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa = fact_kp.id_mahasiswa AND dim_mahasiswa.id_prodi = 9
    where fact_kp.is_pen_pkm != 1 and dim_semester.tahun_ajaran between %(start)s and %(end)s
    group by dim_semester.tahun_ajaran, dim_semester.semester_nama, Semester
    order by Semester''', {'start': thstart, 'end': thend})
    # dfTotal= dfPKM.loc[(dfPKM['Keterangan']=='Tidak Terlibat PPKM'),('Jumlah KP')].agg({'Jumlah KP': np.sum})
    figAll = px.bar(dfPKM, y=dfPKM['Jumlah KP'], x=dfPKM['Semester'], color=dfPKM['Keterangan'])
    figAll.add_scatter(
        x=dfAll['Semester'],y=dfAll['Jumlah KP'],
        showlegend=False, mode='text',
        text=dfAll['Jumlah KP'],textposition="top center"
    )
    dfPersenPKM = data.getDataFrameFromDBwithParams('''
        select ak.Semester,
               round((`Jumlah KP`/`Jumlah Mahasiswa Aktif`)*100, 2) 'Persen Keterlibatan Mahasiswa KP'
        from
        (select concat(ds.tahun_ajaran, ' ', ds.semester_nama) 'Semester',
               count(*) as                                     'Jumlah KP'
        from fact_kp fk
                 inner join dim_semester ds on ds.id_semester = fk.id_semester
                 inner join dim_mahasiswa dm on dm.id_mahasiswa = fk.id_mahasiswa AND dm.id_prodi = 9
        where fk.is_pen_pkm = 1
           and ds.tahun_ajaran between %(start)s and %(end)s
        group by Semester
          ) pkm,
        (select concat(ds.tahun_ajaran,' ',ds.semester_nama) 'Semester',
               count(*) as      'Jumlah Mahasiswa Aktif'
        from fact_mahasiswa_status fms
                 inner join dim_mahasiswa dmhs on fms.id_mahasiswa = dmhs.id_mahasiswa
                 inner join dim_semester ds on ds.id_semester = fms.id_semester
        where fms.status = 'AK'
           and ds.tahun_ajaran between %(start)s and %(end)s
        group by Semester) ak
        where pkm.Semester=ak.Semester
        order by ak.Semester
    ''', {'start': thstart, 'end': thend})
    figPersenPKM = px.line(dfPersenPKM, x=dfPersenPKM['Semester'], y=dfPersenPKM['Persen Keterlibatan Mahasiswa KP'])
    figPersenPKM.add_hrect( y0=2.50 if dfPersenPKM['Persen Keterlibatan Mahasiswa KP'].max()<2.50 else dfPersenPKM['Persen Keterlibatan Mahasiswa KP'].max()+1,
                            y1=dfPersenPKM['Persen Keterlibatan Mahasiswa KP'].max()+1 if dfPersenPKM['Persen Keterlibatan Mahasiswa KP'].max()>2.50 else 2.50+1,
                            fillcolor="green", opacity=0.15, line_width=0)
    figPersenPKM.add_hrect( y0=0, y1=2.50,
                            fillcolor="yellow", opacity=0.15, line_width=0)
    figPersenPKM.add_hrect(y0=0, y1=-1,
                           fillcolor="red", opacity=0.15, line_width=0)
    fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                     font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                     yshift=10)
    if (len(dfPKM['Semester']) != 0 and len(dfAll['Semester']) != 0 and len(dfPersenPKM['Semester']) != 0):
        return figAll, figPersenPKM
    elif(len(dfPKM['Semester']) != 0 and len(dfAll['Semester']) == 0 and len(dfPersenPKM['Semester']) != 0):
        return fig, figPersenPKM
    elif (len(dfPKM['Semester']) == 0 and len(dfAll['Semester']) != 0 and len(dfPersenPKM['Semester']) == 0):
        return figAll, fig
    else:
        return fig,fig

@app.callback(
    Output("cll_tblkpttgu", "is_open"),
    [Input("cll_grfkpttgu", "n_clicks")],
    [State("cll_tblkpttgu", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output('grf_kpttgu','figure'),
    Input('fltrKPTTGUStart','value'),
    Input('fltrKPTTGUEnd','value')
)
def graphMhsKPTTGU(start,end):
    df =  data.getDataFrameFromDBwithParams('''
    select tahun_ajaran 'Tahun Ajaran',semester_nama Semester, count(distinct id_mahasiswa) as 'Jumlah Mahasiswa'
    from fact_kp fk
    inner join dim_semester ds on fk.id_semester = ds.id_semester
    where is_pen_pkm='1' and (tahun_ajaran between %(start)s and %(end)s)
    group by tahun_ajaran, semester_nama
    order by tahun_ajaran, semester_nama
    ''',{'start':start,'end':end})
    if (len(df['Semester']) != 0):
        fig = px.bar(df, y=df['Jumlah Mahasiswa'], x=df['Tahun Ajaran'], color=df['Semester'], barmode='group')
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig

#------------SKRIPSI------------
@app.callback(
    Output("cll_tbldosbing", "is_open"),
    [Input("cll_grfdosbing", "n_clicks")],
    [State("cll_tbldosbing", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("cll_tblskripsipkm", "is_open"),
    Output('cll_tblskripsipkm', 'children'),
    [Input("cll_grfskripsipkm", "n_clicks"),
     Input("cll_grfskripsipkmPersen", "n_clicks")],
    [State("cll_tblskripsipkm", "is_open")])
def toggle_collapse(n,nPersen, is_open):
    isiPKM=dbc.Card(
        dt.DataTable(
            id='tbl_skripmhs',
            columns=[{"name": i, "id": i} for i in dfskripmhs.columns],
            data=dfskripmhs.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'height': '100%', 'padding': '10px',
                         'overflowY': 'auto', 'margin-top': '25px'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            export_format='xlsx',
            page_size=5
        ), style=cardtbl_style
    ),
    if n:
        return not is_open
    elif nPersen:
        return not is_open
    return is_open

@app.callback(
    Output('grf_skripsipkm','figure'),
    Output('grf_skripsipkmPersen', 'figure'),
    Input('fltrSkripsiPKMStart','value'),
    Input('fltrSkripsiPKMEnd','value')
)
def graphSkripsiPKM(start,end):
    dftotal = data.getDataFrameFromDBwithParams(f'''
        select concat(tahun_ajaran, ' ', semester_nama) Semester,
               count(distinct fs.id_mahasiswa) as       'Jumlah Mahasiswa'
        from fact_skripsi fs
                 inner join dim_semester ds on fs.id_semester = ds.id_semester
        where tahun_ajaran between %(start)s and %(end)s
        group by Semester
        order by Semester asc
    ''', {'start': start, 'end': end})
    df = data.getDataFrameFromDBwithParams(f'''
        select nonpkm.Semester Semester,
               ifnull(pkm.`Jumlah Mahasiswa`,0) 'Mahasiswa PPKM',
               nonpkm.`Jumlah Mahasiswa` 'Mahasiswa NonPPKM'
        from
        (select concat(tahun_ajaran, ' ', semester_nama) Semester,
               count(distinct fs.id_mahasiswa) as       'Jumlah Mahasiswa',
               'Terlibat PPKM' as Keterangan
        from fact_skripsi fs
                 inner join dim_semester ds on fs.id_semester = ds.id_semester
                 inner join br_pp_skripsi bps on fs.id_mahasiswa = bps.id_mahasiswa
        where tahun_ajaran between %(start)s and %(end)s
        group by Semester) pkm
            right join
        (select concat(tahun_ajaran, ' ', semester_nama) Semester,
               count(distinct fs.id_mahasiswa) as       'Jumlah Mahasiswa',
               'Tidak Terlibat PPKM' as Keterangan
        from fact_skripsi fs
                 inner join dim_semester ds on fs.id_semester = ds.id_semester
                 left join br_pp_skripsi bps on fs.id_mahasiswa = bps.id_mahasiswa
        where bps.id_mahasiswa is null 
          and tahun_ajaran between %(start)s and %(end)s
        group by Semester) nonpkm
        on pkm.Semester=nonpkm.Semester
        order by nonpkm.Semester asc
        ''', {'start': start, 'end': end})
    figAll = px.bar(df, y=df['Mahasiswa PPKM'], x=df['Semester'], color=px.Constant('Mahasiswa PPKM'),
                 labels=dict(x="Semester", y="Jumlah Mahasiswa PPKM", color="Jenis Mahasiswa"))
    figAll.add_bar(y=df['Mahasiswa NonPPKM'], x=df['Semester'], name='Mahasiswa NonPPKM')
    figAll.update_traces(hovertemplate="<br> Jumlah Mahasiswa=%{y} </br> Semester= %{x}")
    figAll.add_scatter(x=dftotal['Semester'], y=dftotal['Jumlah Mahasiswa'],
                    showlegend=False, mode='text',
                    text=dftotal['Jumlah Mahasiswa'], textposition="top center")
    dfpersen = data.getDataFrameFromDBwithParams(f'''
    select skripsi.Semester,
           round((`Jumlah Mahasiswa Skripsi PKM` / `Jumlah Mahasiswa Skripsi`) * 100, 2) 'Persen Keterlibatan Mahasiswa Skripsi'
    from (select concat(ds.tahun_ajaran, ' ', ds.semester_nama) 'Semester',
                 count(*) as                                    'Jumlah Mahasiswa Skripsi PKM'
          from fact_skripsi fs
                   inner join dim_semester ds on ds.id_semester = fs.id_semester
                   inner join dim_mahasiswa dm on dm.id_mahasiswa = fs.id_mahasiswa AND dm.id_prodi = 9
          where fs.is_pen_pkm = 1
             and ds.tahun_ajaran between %(start)s and %(end)s
          group by Semester
         ) pkm,
         (select concat(ds.tahun_ajaran, ' ', ds.semester_nama) 'Semester',
                 count(*) as                                    'Jumlah Mahasiswa Skripsi'
          from fact_skripsi fs
                   inner join dim_semester ds on ds.id_semester = fs.id_semester
                   inner join dim_mahasiswa dm on dm.id_mahasiswa = fs.id_mahasiswa AND dm.id_prodi = 9
           where ds.tahun_ajaran between %(start)s and %(end)s
          group by Semester) skripsi
    where pkm.Semester = skripsi.Semester
    order by skripsi.Semester
    ''', {'start': start, 'end': end})
    figPersen = px.line(dfpersen, x=dfpersen['Semester'], y=dfpersen['Persen Keterlibatan Mahasiswa Skripsi'])
    figPersen.add_hrect( y0=10,
                         y1=dfpersen['Persen Keterlibatan Mahasiswa Skripsi'].max()+1 if dfpersen['Persen Keterlibatan Mahasiswa Skripsi'].max()>10 else 10+1,
                        fillcolor="green", opacity=0.25, line_width=0)
    figPersen.add_hrect( y0=0, y1=10,
                            fillcolor="yellow", opacity=0.15, line_width=0)
    figPersen.add_hrect(y0=-1, y1=0,
                           fillcolor="red", opacity=0.15, line_width=0)
    fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                     font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                     yshift=10)
    if (len(df['Semester']) != 0 and len(dftotal['Semester']) != 0 and len(dfpersen['Semester']) != 0):
        return figAll, figPersen
    elif (len(df['Semester']) != 0 and len(dftotal['Semester']) == 0 and len(dfpersen['Semester']) != 0):
        return fig, figPersen
    elif (len(df['Semester']) == 0 and len(dftotal['Semester']) != 0 and len(dfpersen['Semester']) == 0):
        return figAll, fig
    else:
        return fig, fig

@app.callback(
    Output('grf_dosbing', 'figure'),
    Input('fltrDosbing', 'value'),
)
def graphDosbing(value):
    df = data.getDataFrameFromDBwithParams('''
    select tahun_ajaran 'Tahun Ajaran',
           semester_nama 'Semester',
           count(id_mahasiswa) 'Jumlah Mahasiswa',
           nama 'Nama Dosen'
    from fact_skripsi fs
    inner join dim_dosen dd on fs.id_dosen_pembimbing1=dd.id_dosen
    inner join dim_semester ds on fs.id_semester = ds.id_semester
    where tahun_ajaran=%(tahun_ajaran)s
    group by tahun_ajaran,semester_nama,nama
    order by `Jumlah Mahasiswa` desc , semester_nama''', {'tahun_ajaran': value})
    if (len(df['Semester']) != 0):
        fig = px.bar(df, y=df['Nama Dosen'], x=df['Jumlah Mahasiswa'], color=df['Semester'], barmode='group')
        fig.add_vrect(x0=0, x1=6,
                      fillcolor="green", opacity=0.15, line_width=0)
        fig.add_vrect(x0=6, x1=10,
                      fillcolor="yellow", opacity=0.15, line_width=0)
        fig.add_vrect(x0=10, x1=df['Jumlah Mahasiswa'].max()+3,
                      fillcolor="red", opacity=0.15, line_width=0)
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig

#------------YUDISIUM------------
@app.callback(
    Output('cll_tblpersenlls', 'is_open'),
    Output('cll_tblpersenlls', 'children'),
    [Input("cll_grfllsontime", "n_clicks"),
     Input("cll_grfllstotal", "n_clicks"),
     Input("tab_kppersenlls", "value")],
    [State("cll_tblpersenlls", "is_open")])
def toggle_collapse(ontime, total, persen, is_open):
    isiOntime = dbc.Card(
        dt.DataTable(
            id='tbl_persen_mhsLulus',
            columns=[{"name": i, "id": i} for i in dfpersen_mhsLulus.columns],
            data=dfpersen_mhsLulus.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'height': '100%', 'padding': '10px',
                         'overflowY': 'auto', 'margin-top': '25px'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            export_format='xlsx',
            page_size=5
        ), style=cardtbl_style
    ),
    isiTotal = dbc.Card(
        dt.DataTable(
            id='tbl_persen_mhsLulusAngkt',
            columns=[{"name": i, "id": i} for i in dfpersen_mhsLulusAngkt.columns],
            data=dfpersen_mhsLulusAngkt.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'height': '100%', 'padding': '10px',
                         'overflowY': 'auto', 'margin-top': '25px'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            export_format='xlsx',
            page_size=3
        ), style=cardtbl_style
    ),
    if ontime and persen == 'llsontime':
        return not is_open, isiOntime
    if total and persen == 'llstotal':
        return not is_open, isiTotal
    return is_open, None


@app.callback(
    Output('grf_llsontime', 'figure'),
    Input('fltrLulusOTStart', 'value'),
    Input('fltrLulusOTEnd', 'value'),
    Input('radio_llsnot','value')
)
def graphPersenMHSLulusOT(start, end, radio):
    if radio=='jumlot':
        dfOnTimeLlsn= data.getDataFrameFromDBwithParams(f'''
            select tahun_ajaran              'Tahun Ajaran',
                   lls.tahun_angkatan        'Tahun Angkatan',
                   lls.jml as                'Jumlah Lulusan',
                   mhs.jml as                'Jumlah Mahasiswa',
                   (lls.jml / mhs.jml) * 100 'Persentase'
            from (select count(dm.id_mahasiswa) jml, tahun_ajaran_yudisium, semester_nama, tahun_angkatan
                  from fact_yudisium fy
                           inner join dim_mahasiswa dm on fy.id_mahasiswa = dm.id_mahasiswa
                           inner join dim_semester_yudisium dsy on fy.id_semester_yudisium = dsy.id_semester_yudisium
                  where convert(substr(tahun_ajaran, 6, 4), int) - 4 = convert(tahun_angkatan, int)
                    and semester_nama = 'GENAP'
                  group by tahun_ajaran_yudisium, tahun_angkatan, semester_nama
                  order by tahun_ajaran_yudisium desc, semester_nama desc) lls,
                 (select ds.tahun_ajaran,
                         dm.tahun_angkatan,
                         count(distinct dm.id_mahasiswa) jml
                  from fact_mahasiswa_status ms
                           inner join dim_mahasiswa dm on ms.id_mahasiswa = dm.id_mahasiswa
                           inner join dim_semester ds on ms.id_semester = ds.id_semester
                  where kode_semester >= '20161'
                    and (status = 'AK' or status = 'UD' or status = 'CS')
                  group by tahun_ajaran, tahun_angkatan
                  order by tahun_ajaran desc) mhs
            where mhs.tahun_ajaran = lls.tahun_ajaran_yudisium
              and mhs.tahun_angkatan = lls.tahun_angkatan
              and tahun_ajaran between %(start)s and %(end)s
            order by tahun_ajaran asc;
            ''', {'start': start, 'end': end})
        if (len(dfOnTimeLlsn['Tahun Ajaran']) != 0):
            figOnTime = px.bar(dfOnTimeLlsn, y=dfOnTimeLlsn.columns[2:4], x=dfOnTimeLlsn['Tahun Ajaran'],
                               barmode='group')
            return figOnTime
        else:
            fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                             font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                             yshift=10)
            return fig
    elif radio=='persenot':
        dfPersenOTLulusan = data.getDataFrameFromDBwithParams(f'''
        select tahun_ajaran                     'Tahun Ajaran',
                   (lls.jml / mhs.jml) * 100    'Persentase'
            from (select count(dm.id_mahasiswa) jml, tahun_ajaran_yudisium, semester_nama, tahun_angkatan
                  from fact_yudisium fy
                           inner join dim_mahasiswa dm on fy.id_mahasiswa = dm.id_mahasiswa
                           inner join dim_semester_yudisium dsy on fy.id_semester_yudisium = dsy.id_semester_yudisium
                  where convert(substr(tahun_ajaran, 6, 4), int) - 4 = convert(tahun_angkatan, int)
                    and semester_nama = 'GENAP'
                  group by tahun_ajaran_yudisium, tahun_angkatan, semester_nama
                  order by tahun_ajaran_yudisium desc, semester_nama desc) lls,
                 (select ds.tahun_ajaran,
                         dm.tahun_angkatan,
                         count(distinct dm.id_mahasiswa) jml
                  from fact_mahasiswa_status ms
                           inner join dim_mahasiswa dm on ms.id_mahasiswa = dm.id_mahasiswa
                           inner join dim_semester ds on ms.id_semester = ds.id_semester
                  where kode_semester >= '20161'
                    and (status = 'AK' or status = 'UD' or status = 'CS')
                  group by tahun_ajaran, tahun_angkatan
                  order by tahun_ajaran desc) mhs
            where mhs.tahun_ajaran = lls.tahun_ajaran_yudisium
              and mhs.tahun_angkatan = lls.tahun_angkatan
              and tahun_ajaran between %(start)s and %(end)s
            order by tahun_ajaran asc;
        ''',{'start': start, 'end': end})
        if (len(dfPersenOTLulusan['Tahun Ajaran']) != 0):
            figPersenOT = px.line(dfPersenOTLulusan, y=dfPersenOTLulusan['Persentase'],
                                  x=dfPersenOTLulusan['Tahun Ajaran'])
            return figPersenOT
        else:
            fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                             font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                             yshift=10)
            return fig


@app.callback(
    Output('grf_llstotal', 'figure'),
    Input('fltrLulusTotStart', 'value'),
    Input('fltrLulusTotEnd', 'value'),
    Input('radio_llsntot','value')
)
def graphPersenMHSLulusOT(start, end, radio):
    if radio == 'jumltot':
        dftot = data.getDataFrameFromDBwithParams(f'''
        select lulus.tahun_angkatan                'Angkatan',
               lulus.jumlah                        'Jumlah Lulusan',
               total.jumlah                        'Total Mahasiswa',
               (lulus.jumlah / total.jumlah) * 100 "Persentase"
        from (
                 select tahun_angkatan, count(distinct fy.id_mahasiswa) 'jumlah'
                 from fact_yudisium fy
                          inner join dim_mahasiswa dm on dm.id_mahasiswa = fy.id_mahasiswa
                          inner join dim_semester_yudisium dsy on fy.id_semester_yudisium = dsy.id_semester_yudisium
                 group by tahun_angkatan
             ) lulus,
             (
                 select tahun_angkatan, count(distinct id_mahasiswa) 'jumlah'
                 from dim_mahasiswa dm
                 group by tahun_angkatan
             ) total
        where lulus.tahun_angkatan = total.tahun_angkatan 
        order by lulus.tahun_angkatan desc;
        ''',{'start':start, 'end':end})
        if (len(dftot['Angkatan']) != 0):
            figtot = px.bar(dftot, y=dftot.columns[2:4], x=dftot['Angkatan'])
            return figtot
        else:
            fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                             font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                             yshift=10)
            return fig
    elif radio == 'persentot':
        dftotpersen = data.getDataFrameFromDBwithParams(f'''
        select lulus.tahun_angkatan                'Angkatan',
               (lulus.jumlah / total.jumlah) * 100 'Persentase'
        from (
                 select tahun_angkatan, count(distinct fy.id_mahasiswa) 'jumlah'
                 from fact_yudisium fy
                          inner join dim_mahasiswa dm on dm.id_mahasiswa = fy.id_mahasiswa
                          inner join dim_semester_yudisium dsy on fy.id_semester_yudisium = dsy.id_semester_yudisium
                 group by tahun_angkatan
             ) lulus,
             (
                 select tahun_angkatan, count(distinct id_mahasiswa) 'jumlah'
                 from dim_mahasiswa dm
                 group by tahun_angkatan
             ) total
        where lulus.tahun_angkatan = total.tahun_angkatan
            and lulus.tahun_angkatan between %(start)s and %(end)s
        order by lulus.tahun_angkatan desc;
        ''',{'start':start, 'end':end})
        if (len(dftotpersen['Angkatan']) != 0):
            figtotpersen = px.line(dftotpersen, y=dftotpersen['Persentase'], x=dftotpersen['Angkatan'])
            return figtotpersen
        else:
            fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                             font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                             yshift=10)
            return fig


@app.callback(
    Output("cll_tbllulusan", "is_open"),
    [Input("cll_grfipklulusan", "n_clicks")],
    [State("cll_tbllulusan", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output('grf_ipklulusan', 'figure'),
    Input('fltrIPKStart', 'value'),
    Input('fltrIPKEnd', 'value')
)
def graphIPKLulusan(thstart, thend):
    dfavg = data.getDataFrameFromDBwithParams('''
    select avg(ipk) as 'Rata-rata IPK' ,  tahun_ajaran_yudisium as 'Tahun Ajaran Yudisium'
    from fact_yudisium
    where tahun_ajaran_yudisium between %(start)s and %(end)s
    group by tahun_ajaran_yudisium
    order by tahun_ajaran_yudisium;''', {'start': thstart, 'end': thend})
    dfmax = data.getDataFrameFromDBwithParams('''
    select max(ipk) as 'IPK' ,  tahun_ajaran_yudisium as 'Tahun Ajaran Yudisium'
    from fact_yudisium
    where tahun_ajaran_yudisium between %(start)s and %(end)s
    group by tahun_ajaran_yudisium
    order by tahun_ajaran_yudisium;''', {'start': thstart, 'end': thend})
    dfmin = data.getDataFrameFromDBwithParams('''
    select min(ipk) as 'IPK' ,  tahun_ajaran_yudisium as 'Tahun Ajaran Yudisium'
    from fact_yudisium
    where tahun_ajaran_yudisium between %(start)s and %(end)s
    group by tahun_ajaran_yudisium
    order by tahun_ajaran_yudisium;''', {'start': thstart, 'end': thend})
    if (len(dfavg['Tahun Ajaran Yudisium']) != 0):
        fig = px.bar(dfavg, y=dfavg['Rata-rata IPK'], x=dfavg['Tahun Ajaran Yudisium'],
                     color=px.Constant('Rata-rata IPK'),
                     labels=dict(x="Tahun Ajaran Yudisium", color="Keterangan"))
        fig.add_scatter(y=dfmax['IPK'], x=dfmax['Tahun Ajaran Yudisium'], name='IPK Tertinggi',
                        hovertemplate="IPK Tertinggi <br>IPK=%{y} </br> Tahun Ajaran= %{x}")
        fig.add_scatter(y=dfmin['IPK'], x=dfmin['Tahun Ajaran Yudisium'], name='IPK Terendah',
                        hovertemplate="IPK Terendah <br>IPK=%{y} </br> Tahun Ajaran= %{x}")
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


@app.callback(
    Output('cll_tbljumllulusan', 'is_open'),
    Output('cll_tbljumllulusan', 'children'),
    [Input("cll_grflulusanall", "n_clicks"),
     Input("cll_grflulusanot", "n_clicks"),
     Input("tab_lulusan", "value")],
    [State("cll_tbljumllulusan", "is_open")])
def toggle_collapse(all, ot, llsn, is_open):
    isiAll = dbc.Card(
        dt.DataTable(
            id='tbl_lulusanall',
            columns=[{"name": i, "id": i} for i in dfjumllulusan.columns],
            data=dfjumllulusan.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    ),
    isiOnTime = dbc.Card(
        dt.DataTable(
            id='tbl_lulusanot',
            columns=[{"name": i, "id": i} for i in dfjumllulusanot.columns],
            data=dfjumllulusanot.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    ),
    if all and llsn == 'all':
        return not is_open, isiAll
    if ot and llsn == 'ot':
        return not is_open, isiOnTime
    return is_open, None


@app.callback(
    Output('grf_jmllulusan', 'figure'),
    Input('fltrLulusanStart', 'value'),
    Input('fltrLulusanEnd', 'value')
)
def graphJLulusan(thstart, thend):
    df = data.getDataFrameFromDBwithParams('''
    select  concat(tahun_ajaran_yudisium,' ',semester_yudisium) Semester, 
            count(*) as 'Jumlah Mahasiswa Yudisium'
    from fact_yudisium fy
    inner join dim_semester_yudisium dsy on fy.id_semester_yudisium = dsy.id_semester_yudisium
    where tahun_ajaran_yudisium between %(start)s and %(end)s
    group by kode_semester, Semester
    order by kode_semester asc, Semester''', {'start': thstart, 'end': thend})
    if (len(df['Semester']) != 0):
        fig = px.bar(df, y=df['Jumlah Mahasiswa Yudisium'], x=df['Semester'], labels=dict(x="Tahun Ajaran", y="Jumlah"))
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False, yshift=10)
        return fig

@app.callback(
    Output('grf_skripsiontime', 'figure'),
    Input('fltrLulusanStart', 'value'),
    Input('fltrLulusanEnd', 'value')
)
def graphJLulusanOT(thstart, thend):
    df = data.getDataFrameFromDBwithParams('''
    select concat(tahun_ajaran_yudisium, ' ', semester_yudisium) Semester,
           count(id_mahasiswa)                                   'Jumlah Mahasiswa',
           'Tepat Waktu' as                                      Keterangan
    from fact_yudisium fy
             inner join dim_semester ds on fy.id_semester_yudisium = ds.id_semester
    where (masa_studi_dalam_bulan >= 42 and masa_studi_dalam_bulan <= 54)
      and tahun_ajaran_yudisium between %(start)s and %(end)s
    group by Semester, kode_semester
    union all
    select concat(tahun_ajaran_yudisium, ' ', semester_yudisium) Semester,
           count(*) as                                           'Jumlah Mahasiswa',
           'Tidak Tepat Waktu'  as                               Keterangan
    from fact_yudisium fy
             inner join dim_semester_yudisium dsy on fy.id_semester_yudisium = dsy.id_semester_yudisium
    where not(masa_studi_dalam_bulan >= 42 and masa_studi_dalam_bulan <= 54) 
        and tahun_ajaran_yudisium between %(start)s and %(end)s
    group by kode_semester, Semester
    order by Semester;''', {'start': thstart, 'end': thend})
    if (len(df['Semester']) != 0):
        fig = px.bar(df, y=df['Jumlah Mahasiswa'], x=df['Semester'], color=df['Keterangan'])
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig

@app.callback(
    Output("cll_tblallmasa", "is_open"),
    [Input("cll_tblavgmasa", "n_clicks")],
    [State("cll_tblallmasa", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output('cll_tblmasa', 'is_open'),
    Output('cll_tblmasa', 'children'),
    [Input("cll_grfmasaall", "n_clicks"),
     Input("cll_grfmasarerata", "n_clicks"),
     Input("tab_masa", "value")],
    [State("cll_tblmasa", "is_open")])
def toggle_collapse(all, rerata, masa, is_open):
    isiAll = dbc.Card(
        dt.DataTable(
            id='tbl_avgmasa',
            columns=[{"name": i, "id": i} for i in dfavgmasa.columns],
            data=dfavgmasa.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            page_size=5
        ), style=cardgrf_style
    ),
    isiRerata = dbc.Card(
        dt.DataTable(
            id='tbl_allmasa',
            columns=[{"name": i, "id": i} for i in dfmasastudilulusan.columns],
            data=dfmasastudilulusan.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'height': '100%', 'padding': '10px',
                         'overflowY': 'auto', 'margin-top': '25px'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            page_size=5
        ), style=cardgrf_style
    ),
    if all and masa == 'rerata':
        return not is_open, isiAll
    if rerata and masa == 'all':
        return not is_open, isiRerata
    return is_open, None

@app.callback(
    Output('grf_msall', 'figure'),
    Input('fltrMSStart', 'value'),
    Input('fltrMSEnd', 'value')
)
def graphMSLulusan(start, end):
    df = data.getDataFrameFromDBwithParams('''
    select *
    from (select concat(dim_mahasiswa.tahun_angkatan, '/',
                        cast(dim_mahasiswa.tahun_angkatan + 1 as char(4)))                                      as 'Tahun Ajaran Masuk',
                 SUM(case when masa_studi_dalam_bulan < 36 then 1 else 0 end)                                   as '< 3 Tahun',
                 SUM(case
                         when masa_studi_dalam_bulan >= 36 AND masa_studi_dalam_bulan < 42 then 1
                         else 0 end)                                                                            as '3 - 3.5 Tahun',
                 SUM(case
                         when masa_studi_dalam_bulan >= 42 AND masa_studi_dalam_bulan < 54 then 1
                         else 0 end)                                                                            as '3.5 - 4.5 Tahun',
                 SUM(case
                         when masa_studi_dalam_bulan >= 54 AND masa_studi_dalam_bulan <= 84 then 1
                         else 0 end)                                                                            as '4.5 - 7 Tahun',
                 SUM(case when masa_studi_dalam_bulan >= 85 then 1 else 0 end)                                  as '> 7 tahun'
          from fact_yudisium
                   inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa = fact_yudisium.id_mahasiswa
          group by `Tahun Ajaran Masuk`
          order by `Tahun Ajaran Masuk`) lulusan
             left join (
        select count(id_mahasiswa) 'Jumlah Mahasiswa', tahun_ajaran 'Tahun Ajaran'
        from fact_pmb
                 inner join dim_semester on dim_semester.id_semester = fact_pmb.id_semester AND id_prodi_diterima = 9
        group by tahun_ajaran
        order by tahun_ajaran desc
    ) mhsditerima on mhsditerima.`Tahun Ajaran` = `Tahun Ajaran Masuk`
    order by `Tahun Ajaran Masuk` asc
    ''', {'start': start, 'end': end})
    if (len(df['Tahun Ajaran Masuk']) != 0):
        fig = px.bar(df, x=df['Tahun Ajaran Masuk'], y=df.columns[1:6])
        fig.update_layout(xaxis_title="Tahun Ajaran Masuk",
                          yaxis_title="Jumlah Lulusan",
                          legend_title_text="Kategori Masa Studi")
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig

@app.callback(
    Output('grf_msrerata', 'figure'),
    Input('fltrMSStart', 'value'),
    Input('fltrMSEnd', 'value')
)
def graphMSLulusan(start, end):
    df = data.getDataFrameFromDBwithParams('''
    select tahun_ajaran_yudisium 'Tahun Ajaran Yudisium',
           round(avg(masa_studi_dalam_bulan),0) as 'Rata-rata Masa Studi (Bulanan)'
    from fact_yudisium
    where tahun_ajaran_yudisium between %(start)s and %(end)s
    group by tahun_ajaran_yudisium
    order by tahun_ajaran_yudisium asc 
    ''', {'start': start, 'end': end})
    if (len(df['Rata-rata Masa Studi (Bulanan)']) != 0):
        fig = px.bar(df, y=df['Rata-rata Masa Studi (Bulanan)'], x=df['Tahun Ajaran Yudisium'], color=px.Constant('Rata-rata Masa Studi (Bulanan)'),
                     labels=dict(color="Keterangan"))
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig

@app.callback(
    Output("cll_tblmitra", "is_open"),
    [Input("cll_grfmitra", "n_clicks")],
    [State("cll_tblmitra", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output('grf_mitra', 'figure'),
    Input('fltrMitraKPSem', 'value'),
    Input('fltrMitraKPTA', 'value'),
    Input('radio_mitrakp', 'value')
)
def PKMDM(sem, ta, radiomitrakp):
    dftotal = data.getDataFrameFromDBwithParams(f'''
    select  concat(semester_nama,' ',tahun_ajaran) Semester,
            count(id_kp) 'Jumlah KP'
    from fact_kp fk
        inner join dim_semester ds on fk.id_semester = ds.id_semester
        inner join dim_mitra dm on fk.id_mitra = dm.id_mitra
    where tahun_ajaran=%(ta)s and semester_nama=%(sem)s
    group by kode_semester, Semester
    order by kode_semester desc, Semester
    ''',{'sem':sem,'ta':ta})
    if radiomitrakp == 'top':
        dfsumkp = data.getDataFrameFromDBwithParams(f'''
        select nama_mitra 'Nama Mitra', count(id_kp) Jumlah
        from fact_kp fk
            inner join dim_semester ds on fk.id_semester = ds.id_semester
            inner join dim_mitra dm on fk.id_mitra = dm.id_mitra
        where tahun_ajaran=%(ta)s and semester_nama=%(sem)s
        group by nama_mitra
        order by Jumlah desc
        limit 10;
        ''',{'sem':sem,'ta':ta})
        if (len(dfsumkp['Jumlah']) != 0):
            figkpsummitra = px.bar(dfsumkp, y=dfsumkp['Nama Mitra'], x=dfsumkp['Jumlah'])
            return figkpsummitra
        else:
            figkpsummitra = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                             font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                             yshift=10)
            return figkpsummitra
    elif radiomitrakp == 'jenis':
        dfjeniskp = data.getDataFrameFromDBwithParams(f'''
        select concat(semester_nama,' ',tahun_ajaran) Semester,
               case
                   when jenis_mitra = 'ORGANISASI' then 'ORGANISASI'
                   when jenis_mitra = 'PEMERINTAH' then 'PEMERINTAH'
                   when jenis_mitra = 'BISNIS' then 'BISNIS'
                   when jenis_mitra = 'GEREJA' then 'GEREJA'
                   when jenis_mitra = 'PENDIDIKAN' then 'PENDIDIKAN'
                   else 'LAINNYA'
                   end as      'Jenis Mitra',
               count(id_kp)    'Jumlah KP'
        from fact_kp fk
            inner join dim_semester ds on fk.id_semester = ds.id_semester
            inner join dim_mitra dm on fk.id_mitra = dm.id_mitra
        where tahun_ajaran=%(ta)s and semester_nama=%(sem)s
        group by semester_nama, `Jenis Mitra`, Semester
        order by semester_nama desc, `Jenis Mitra`, Semester;
        ''',{'sem':sem,'ta':ta})
        if (len(dfjeniskp['Semester']) != 0):
            figjenis = px.bar(dfjeniskp, x=dfjeniskp['Semester'], y=dfjeniskp['Jumlah KP'], color=dfjeniskp['Jenis Mitra'])
            figjenis.update_layout(yaxis_title='Jumlah KP', xaxis_title='Tahun, Jenis Mitra', legend_title='Mitra')
            figjenis.add_scatter(
                                    x=dftotal['Semester'],y=dftotal['Jumlah KP'],
                                    showlegend=False, mode='text',
                                    text=dftotal['Jumlah KP'],textposition="top center"
                                )
            return figjenis
        else:
            figjenis = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                             font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                             yshift=10)
            return figjenis
    elif radiomitrakp == 'wilayah':
        dfkpwilayah = data.getDataFrameFromDBwithParams(f'''
        select concat(semester_nama,' ',tahun_ajaran) Semester,
               case
                   when dm.wilayah = '1' then 'LOKAL'
                   when dm.wilayah = '2' then 'REGIONAL'
                   when dm.wilayah = '3' then 'NASIONAL'
                   when dm.wilayah = '4' then 'INTERNASIONAL'
                   else 'NONE' end as 'Wilayah Mitra',
               count(id_kp) 'Jumlah KP'
        from fact_kp fk
            inner join dim_semester ds on fk.id_semester = ds.id_semester
            inner join dim_mitra dm on fk.id_mitra = dm.id_mitra
        where tahun_ajaran=%(ta)s and semester_nama=%(sem)s
        group by kode_semester,`Wilayah Mitra`,Semester
        order by kode_semester desc,`Wilayah Mitra`,Semester
        ''', {'sem':sem,'ta':ta})
        if (len(dfkpwilayah['Semester']) != 0):
            figwilayah = px.bar(dfkpwilayah, x=dfkpwilayah['Semester'], y=dfkpwilayah['Jumlah KP'],
                                color=dfkpwilayah['Wilayah Mitra'])
            figwilayah.update_layout(yaxis_title='Jumlah KP', xaxis_title='Semester, Wilayah Mitra',
                                     legend_title='Mitra')
            figwilayah.add_scatter(
                                    x=dftotal['Semester'],y=dftotal['Jumlah KP'],
                                    showlegend=False, mode='text',
                                    text=dftotal['Jumlah KP'],textposition="top center"
                                )
            return figwilayah
        else:
            figwilayah = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                             font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                             yshift=10)
            return figwilayah

@app.callback(
    Output('grf_mitraS', 'figure'),
    Input('fltrMitraSSem', 'value'),
    Input('fltrMitraSTA', 'value'),
    Input('radio_mitraS', 'value')
)
def PKMDM(sem, ta, radiomitrakp):
    if radiomitrakp == 'top':
        dfsumkp = data.getDataFrameFromDBwithParams(f'''
        select nama_mitra 'Nama Mitra', count(id_skripsi) Jumlah
        from fact_skripsi fs
            inner join dim_semester ds on fs.id_semester = ds.id_semester
            inner join br_pp_skripsi bps on fs.id_mahasiswa = bps.id_mahasiswa
            inner join br_pp_mitra bpm on bps.id_penelitian_pkm = bpm.id_penelitian_pkm
            inner join dim_mitra dm on bpm.id_mitra = dm.id_mitra
        where tahun_ajaran=%(ta)s and semester_nama=%(sem)s
        group by nama_mitra
        order by Jumlah desc
        limit 10;
        ''',{'ta':ta,'sem':sem})
        if (len(dfsumkp['Jumlah']) != 0):
            figkpsummitra = px.bar(dfsumkp, y=dfsumkp['Nama Mitra'], x=dfsumkp['Jumlah'])
            figkpsummitra.update_xaxes(categoryorder='category descending')
            return figkpsummitra
        else:
            figkpsummitra = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                             font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                             yshift=10)
            return figkpsummitra
    elif radiomitrakp == 'jenis':
        dfjeniskp = data.getDataFrameFromDBwithParams(f'''
        select concat(semester_nama,' ',tahun_ajaran) Semester,
               case
                   when jenis_mitra = 'ORGANISASI' then 'ORGANISASI'
                   when jenis_mitra = 'PEMERINTAH' then 'PEMERINTAH'
                   when jenis_mitra = 'BISNIS' then 'BISNIS'
                   when jenis_mitra = 'GEREJA' then 'GEREJA'
                   when jenis_mitra = 'PENDIDIKAN' then 'PENDIDIKAN'
                   else 'LAINNYA'
                   end as      'Jenis Mitra',
               count(id_skripsi)    'Jumlah Skripsi'
        from fact_skripsi fs
            inner join dim_semester ds on fs.id_semester = ds.id_semester
            inner join br_pp_skripsi bps on fs.id_mahasiswa = bps.id_mahasiswa
            inner join br_pp_mitra bpm on bps.id_penelitian_pkm = bpm.id_penelitian_pkm
            inner join dim_mitra dm on bpm.id_mitra = dm.id_mitra
#         where tahun_ajaran=%(ta)s and semester_nama=%(sem)s
        group by semester_nama, `Jenis Mitra`, Semester
        order by semester_nama desc, `Jenis Mitra`, Semester;
        ''',{'ta':ta,'sem':sem})
        if (len(dfjeniskp['Semester']) != 0):
            figjenis = px.bar(dfjeniskp, x=dfjeniskp['Semester'], y=dfjeniskp['Jumlah Skripsi'],
                              color=dfjeniskp['Jenis Mitra'])
            figjenis.update_layout(barmode='group', yaxis_title='Jumlah Skripsi', xaxis_title='Tahun, Jenis Mitra',
                                   legend_title='Mitra')
            return figjenis
        else:
            figjenis = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                             font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                             yshift=10)
            return figjenis
    elif radiomitrakp == 'wilayah':
        dfkpwilayah = data.getDataFrameFromDBwithParams(f'''
        select concat(semester_nama,' ',tahun_ajaran) Semester,
               case
                   when dm.wilayah = '1' then 'LOKAL'
                   when dm.wilayah = '2' then 'REGIONAL'
                   when dm.wilayah = '3' then 'NASIONAL'
                   when dm.wilayah = '4' then 'INTERNASIONAL'
                   else 'NONE' end as 'Wilayah Mitra',
               count(id_skripsi) 'Jumlah Skripsi'
        from fact_skripsi fs
            inner join dim_semester ds on fs.id_semester = ds.id_semester
            inner join br_pp_skripsi bps on fs.id_mahasiswa = bps.id_mahasiswa
            inner join br_pp_mitra bpm on bps.id_penelitian_pkm = bpm.id_penelitian_pkm
            inner join dim_mitra dm on bpm.id_mitra = dm.id_mitra
        where tahun_ajaran=%(ta)s and semester_nama=%(sem)s
        group by semester_nama, `Wilayah Mitra`, Semester
        order by semester_nama desc, `Wilayah Mitra`, Semester;
        ''', {'ta':ta,'sem':sem})
        if (len(dfkpwilayah['Semester']) != 0):
            figwilayah = px.bar(dfkpwilayah, x=dfkpwilayah['Semester'], y=dfkpwilayah['Jumlah Skripsi'],
                                color=dfkpwilayah['Wilayah Mitra'])
            figwilayah.update_layout(yaxis_title='Jumlah Skripsi', xaxis_title='Tahun, Wilayah Mitra',
                                     legend_title='Mitra')
            return figwilayah
        else:
            figwilayah = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                             font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                             yshift=10)
            return figwilayah