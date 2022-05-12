import dash
import pandas as pd
import dash_table as dt
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from appConfig import app, server
from datetime import date
import time
import model.dao_ppp as data

dfdosen = data.getDosen()
dosen = dfdosen['nama'].dropna().unique()

dfjmlppp = data.getJumlahPPP()
# dfjmlpkm = data.getJumlahPKM()
# dfppdosenkpskripsimhs = data.getPPDosenKPSkripsiMhs()
# dfpenelitianmhs = data.getPenelitianMhs()
dfpkmmhs = data.getPKMMhs()

tbl_kerjaPeneliti = data.getKerjasamaPenelitian()
tbl_kerjaPKM = data.getKerjasamaPKM()

# GAJEE
dfpenelitiandana = data.getPenelitianDana()
dfpkmdana = data.getPKMDana()

dfkisitasi3th = data.getKISitasi3th()

dfluaranhkidosen = data.getLuaranHKIDosenperTh()
dfluaranttgudosen = data.getLuaranTTGUDosenperTh()
dfluaranbukudosen = data.getLuaranBukuDosenperTh()

dfpublikasimhs = data.getPublikasiMhs()
dfttguadopsimhs = data.getTTGUMhsDiadopsi()
dfluaranhkimhs = data.getLuaranHKIMhsperTh()

dfratajumlpenelitiandosen = data.getRerataJumlPenelitianDosenperTh()
dfratajumlpublikasidosen = data.getRerataJumlPublikasiDosenperTh()

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

listDropdownTA = []
for x in range(0, 5):
    counter = x + 1
    listDropdownTA.append(
        str(int(date.today().strftime('%Y')) - 5 + x) + '/' + str(int(date.today().strftime('%Y')) - 4 + x))

listDropdownTh = []
for x in range(0, 5):
    counter = x + 1
    listDropdownTh.append(str(int(date.today().strftime('%Y')) - 5 + x))

penSum = dbc.Container([
    dbc.Card([
        html.H5('Jumlah Seluruh Penelitian per Tahun',
                style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Dari :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPenSumStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[1],
                        style={'color': 'black'},
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Sampai :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPenSumEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[4],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ])
        ]),dbc.CardBody([
            dcc.Loading(
                id='loading-1',
                type="default",
                children=dcc.Graph(id='grf_penSum')),
            dbc.Button('Lihat Semua Data', id='cll_grfpenSum', n_clicks=0, style=button_style)
        ], style={'padding': '0px'})
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_PenSum',
        is_open=False
    )
], style=cont_style)

pkmSum = dbc.Container([
    dbc.Card([
        html.H5('Jumlah Seluruh PKM per Tahun',
                style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Dari :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPKMSumStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[1],
                        style={'color': 'black'},
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Sampai :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPKMSumEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[4],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ])
        ]),dbc.CardBody([
            dcc.Loading(
                id='loading-1',
                type="default",
                children=dcc.Graph(id='grf_pkmSum')),
            dbc.Button('Lihat Semua Data', id='cll_grfpkmSum', n_clicks=0, style=button_style)
        ], style={'padding': '0px'})
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_PKMSum',
        is_open=False
    )
], style=cont_style)

penDs = dbc.Container([
    dbc.Card([
        html.H5('Penelitian Dosen',
                style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Nama Dosen :', style={'margin-bottom': '0'}),
                    dcc.Dropdown(
                        id='fltrPenDsNama',
                        options=[{'label': i, 'value': i} for i in dosen],
                        value=dosen[1],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ])
        ]),
        dbc.CardBody([
            dcc.Loading(
                id='loading-1',
                type="default",
                children=dcc.Graph(id='grf_penDs')),
            dbc.Button('Lihat Semua Data', id='cll_grfpenDs', n_clicks=0, style=button_style)
        ], style={'padding': '0px'})
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_PenDs',
        is_open=False
    )
], style=cont_style)

pkmDs = dbc.Container([
    dbc.Card([
        html.H5('PKM Dosen',
                style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Nama Dosen :', style={'margin-bottom': '0'}),
                    dcc.Dropdown(
                        id='fltrPKMDsNama',
                        options=[{'label': i, 'value': i} for i in dosen],
                        value=dosen[1],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ])
        ]),
        dbc.CardBody([
            dcc.Loading(
                id='loading-1',
                type="default",
                children=dcc.Graph(id='grf_pkmDs')),
            dbc.Button('Lihat Semua Data', id='cll_grfpkmDs', n_clicks=0, style=button_style)
        ], style={'padding': '0px'})
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_PKMDs',
        is_open=False
    )
], style=cont_style)

# pppDs = dbc.Container([
#     dbc.Card([
#         html.H5('Penelitian PKM Publikasi Dosen',
#                 style=ttlgrf_style),
#         html.Div([
#             dbc.Row([
#                 dbc.Col([
#                     html.P('Nama Dosen :', style={'margin-bottom': '0'}),
#                     dcc.Dropdown(
#                         id='fltrPPPDsNama',
#                         options=[{'label': i, 'value': i} for i in dosen],
#                         value=dosen[1],
#                         style={'color': 'black'},
#                         clearable=False
#                     )
#                 ]),
#                 dbc.Col([
#                     html.P('Visualisasi :', style={'margin-bottom': '0'}),
#                     dcc.RadioItems(
#                         id='radio_ppp',
#                         options=[{'label': 'Penelitian', 'value': 'pen'},
#                                  {'label': 'PKM', 'value': 'pkm'},
#                                  {'label': 'Publikasi', 'value': 'pub'},
#                                  {'label': 'Luaran Lainnya', 'value': 'luaran'}
#                                  ],
#                         value='pen',
#                         style={'width': '100%', 'padding': '0px', },
#                         className='card-body',
#                         labelStyle={'display': 'block', 'display': 'inline-block',
#                                     'margin-right': '10%', 'margin-top': '5px'}
#                     )
#                 ])
#             ])
#         ]),
#         dbc.CardBody([
#             dcc.Loading(
#                 id='loading-1',
#                 type="default",
#                 children=dcc.Graph(id='grf_pppDosen')),
#             dbc.Button('Lihat Semua Data', id='cll_grfpppDosen', n_clicks=0, style=button_style)
#         ], style={'padding': '0px'})
#     ], style=cardgrf_style),
#     dbc.Collapse(
#         id='cll_PPPDosen',
#         is_open=False
#     )
# ], style=cont_style)
penMhs = dbc.Container([
    dbc.Card([
        html.H5('Penelitian Dosen yang Melibatkan Mahasiswa',
                style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Dari :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPenDMStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[1],
                        style={'color': 'black'},
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Sampai :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPenDMEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[4],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ]),
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.P('Visualisasi :', style={'margin-bottom': '0', 'margin-top': '10px'}),
                        dcc.RadioItems(
                            id='radio_pendm',
                            options=[{'label': 'Jumlah', 'value': 'jumlah'},
                                     {'label': 'Rata-rata', 'value': 'rata'},
                                     {'label': 'Top 10 Partisipan Terbanyak', 'value': 'top'}
                                     ],
                            value='rata',
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
                    children=dcc.Graph(id='grf_PenDM')),
                dbc.Button('Lihat Semua Data', id='cll_grfPenDM', n_clicks=0,
                           style=button_style)
            ], style={'textAlign': 'center'})
        ])
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_PenDM',
        is_open=False
    )
], style=cont_style)

pkmMhs = dbc.Container([
    dbc.Card([
        html.H5('PKM Dosen yang Melibatkan Mahasiswa',
                style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Dari :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPKMDMStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[1],
                        style={'color': 'black'},
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Sampai :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPKMDMEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[4],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ]),
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.P('Visualisasi :', style={'margin-bottom': '0', 'margin-top': '10px'}),
                        dcc.RadioItems(
                            id='radio_pkmdm',
                            options=[{'label': 'Jumlah', 'value': 'jumlah'},
                                     {'label': 'Rata-rata', 'value': 'rata'},
                                     {'label': 'Top 10 Partisipan Terbanyak', 'value': 'top'}
                                     ],
                            value='rata',
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
                    children=dcc.Graph(id='grf_pkmDM')),
                dbc.Button('Lihat Semua Data', id='cll_grfpkmDM', n_clicks=0,
                           style=button_style)
            ], style={'textAlign': 'center'})
        ])
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_PKMDM',
        is_open=False
    )
], style=cont_style)

# pppMhs = dbc.Container([
#     dbc.Card([
#         html.H5('Penelitian PKM Publikasi Dosen & Mahasiswa',
#                 style=ttlgrf_style),
#         html.Div([
#             dbc.Row([
#                 dbc.Col([
#                     html.P('Dari :', style={'marginBottom': 0}),
#                     dcc.Dropdown(
#                         id='fltrPPPDMStart',
#                         options=[{'label': i, 'value': i} for i in listDropdownTh],
#                         value=listDropdownTh[1],
#                         style={'color': 'black'},
#                         clearable=False
#                     )
#                 ]),
#                 dbc.Col([
#                     html.P('Sampai :', style={'marginBottom': 0}),
#                     dcc.Dropdown(
#                         id='fltrPPPDMEnd',
#                         options=[{'label': i, 'value': i} for i in listDropdownTh],
#                         value=listDropdownTh[4],
#                         style={'color': 'black'},
#                         clearable=False
#                     )
#                 ])
#             ]),
#             dcc.Tabs([
#                 dcc.Tab(label='Penelitian Dosen & Mahasiswa', value='telitidosenmhs',
#                         children=[
#                             html.Div([
#                                 dbc.Row([
#                                     dbc.Col([
#                                         html.P('Visualisasi :', style={'margin-bottom': '0','margin-top':'10px'}),
#                                         dcc.RadioItems(
#                                             id='radio_pendm',
#                                             options=[{'label': 'Rerata', 'value': 'rata'},
#                                                      {'label': 'Top 10 Partisipan Terbanyak', 'value': 'top'}
#                                                      ],
#                                             value='rata',
#                                             style={'width': '100%', 'padding': '0px', },
#                                             className='card-body',
#                                             labelStyle={'display': 'block', 'display': 'inline-block',
#                                                         'margin-right': '10%', 'margin-top': '5px'}
#                                         )
#                                     ],style={'padding-left':'5%'})
#                                 ],style={'padding-left':'5%','margin-bottom':'0px'}),
#                                 dcc.Loading(
#                                     id='loading-1',
#                                     type="default",
#                                     children=dcc.Graph(id='grf_telitiDsMhs')),
#                                 dbc.Button('Lihat Semua Data', id='cll_grftelitiDM', n_clicks=0,
#                                            style=button_style)
#                             ],style={'textAlign':'center'})
#                         ], style=tab_style, selected_style=selected_style
#                         ),
#                 dcc.Tab(label='PKM Dosen & Mahasiswa', value='pkmdosenmhs',
#                         children=[
#                             html.Div([
#                                 dbc.Row([
#                                     dbc.Col([
#                                         html.P('Visualisasi :', style={'margin-bottom': '0', 'margin-top': '10px'}),
#                                         dcc.RadioItems(
#                                             id='radio_pkmdm',
#                                             options=[{'label': 'Rerata', 'value': 'rata'},
#                                                      {'label': 'Top 10 Partisipan Terbanyak', 'value': 'top'}
#                                                      ],
#                                             value='rata',
#                                             style={'width': '100%', 'padding': '0px', },
#                                             className='card-body',
#                                             labelStyle={'display': 'block', 'display': 'inline-block',
#                                                         'margin-right': '10%', 'margin-top': '5px'}
#                                         )
#                                     ], style={'padding-left': '5%'})
#                                 ], style={'padding-left': '5%', 'margin-bottom': '0px'}),
#                                 dcc.Loading(
#                                     id='loading-1',
#                                     type="default",
#                                     children=dcc.Graph(id='grf_pkmDsMhs')),
#                                 dbc.Button('Lihat Semua Data', id='cll_grfpkmDM', n_clicks=0,
#                                            style=button_style)
#                             ],style={'textAlign':'center'})
#                         ], style=tab_style, selected_style=selected_style)
#             ], style=tabs_styles, id='tab_pppDM', value='telitidosenmhs')
#         ])
#     ], style=cardgrf_style),
#     dbc.Collapse(
#         id='cll_PPPDM',
#         is_open=False
#     )
# ], style=cont_style)
penMitra = dbc.Container([
    dbc.Card([
        html.H5('Penelitian dengan Mitra',
                style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Dari :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPenMitraStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[0],
                        style={'color': 'black'},
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Sampai :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPenMitraEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[4],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ]),
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.P('Visualisasi :', style={'margin-bottom': '0', 'margin-top': '10px'}),
                        dcc.RadioItems(
                            id='radio_penMitra',
                            options=[{'label': 'Top 10 Mitra (Judul Terbanyak)', 'value': 'top'},
                                     {'label': 'Jenis Mitra', 'value': 'jenis'},
                                     {'label': 'Wilayah Mitra', 'value': 'wilayah'}
                                     ],
                            value='top',
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
                    children=dcc.Graph(id='grf_penMitra')),
                dbc.Button('Lihat Semua Data', id='cll_grfpenMitra', n_clicks=0, style=button_style)
            ], style={'textAlign': 'center'})
        ])
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_penMitra',
        is_open=False
    )
], style=cont_style)

pkmMitra = dbc.Container([
    dbc.Card([
        html.H5('PKM dengan Mitra',
                style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Dari :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPKMMitraStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[0],
                        style={'color': 'black'},
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Sampai :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPKMMitraEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[4],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ]),
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.P('Visualisasi :', style={'margin-bottom': '0', 'margin-top': '10px'}),
                        dcc.RadioItems(
                            id='radio_pkmMitra',
                            options=[{'label': 'Top 10 Mitra (Judul Terbanyak)', 'value': 'top'},
                                     {'label': 'Jenis Mitra', 'value': 'jenis'},
                                     {'label': 'Wilayah Mitra', 'value': 'wilayah'}
                                     ],
                            value='top',
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
                    children=dcc.Graph(id='grf_pkmMitra')),
                dbc.Button('Lihat Semua Data', id='cll_grfpkmMitra', n_clicks=0, style=button_style)
            ], style={'textAlign': 'center'})
        ])
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_pkmMitra',
        is_open=False
    )
], style=cont_style)

# kerjasamaPPP = dbc.Container([
#     dbc.Card([
#         html.H5('Kegiatan dengan Mitra',
#                 style=ttlgrf_style),
#         html.Div([
#             dbc.Row([
#                 dbc.Col([
#                     html.P('Dari :', style={'marginBottom': 0}),
#                     dcc.Dropdown(
#                         id='fltrMitraStart',
#                         options=[{'label': i, 'value': i} for i in listDropdownTh],
#                         value=listDropdownTh[0],
#                         style={'color': 'black'},
#                         clearable=False
#                     )
#                 ]),
#                 dbc.Col([
#                     html.P('Sampai :', style={'marginBottom': 0}),
#                     dcc.Dropdown(
#                         id='fltrMitraEnd',
#                         options=[{'label': i, 'value': i} for i in listDropdownTh],
#                         value=listDropdownTh[4],
#                         style={'color': 'black'},
#                         clearable=False
#                     )
#                 ])
#             ]),
#             dcc.Tabs([
#                 dcc.Tab(label='Penelitian', value='kerjaTeliti',
#                         children=[
#                             html.Div([
#                                 dbc.Row([
#                                     dbc.Col([
#                                         html.P('Visualisasi :', style={'margin-bottom': '0', 'margin-top': '10px'}),
#                                         dcc.RadioItems(
#                                             id='radio_penmitra',
#                                             options=[{'label': 'Top 10 Mitra (Judul Terbanyak)', 'value': 'top'},
#                                                      {'label': 'Jenis Mitra', 'value': 'jenis'},
#                                                      {'label': 'Wilayah Mitra', 'value':'wilayah'}
#                                                      ],
#                                             value='top',
#                                             style={'width': '100%', 'padding': '0px', },
#                                             className='card-body',
#                                             labelStyle={'display': 'block', 'display': 'inline-block',
#                                                         'margin-right': '10%', 'margin-top': '5px'}
#                                         )
#                                     ], style={'padding-left': '5%'})
#                                 ], style={'padding-left': '5%', 'margin-bottom': '0px'}),
#                                 dcc.Loading(
#                                     id='loading-1',
#                                     type="default",
#                                     children=dcc.Graph(id='grf_MitraTeliti')),
#                                 dbc.Button('Lihat Semua Data', id='cll_grfMitraTeliti', n_clicks=0, style=button_style)
#                             ],style={'textAlign':'center'})
#                         ],
#                         style=tab_style, selected_style=selected_style),
#                 dcc.Tab(label='PKM', value='kerjaPKM',
#                         children=[
#                             html.Div([
#                                 dbc.Row([
#                                     dbc.Col([
#                                         html.P('Visualisasi :', style={'margin-bottom': '0', 'margin-top': '10px'}),
#                                         dcc.RadioItems(
#                                             id='radio_pkmmitra',
#                                             options=[{'label': 'Top 10 Mitra (Judul Terbanyak)', 'value': 'top'},
#                                                      {'label': 'Jenis Mitra', 'value': 'jenis'},
#                                                      {'label': 'Wilayah Mitra', 'value':'wilayah'}
#                                                      ],
#                                             value='top',
#                                             style={'width': '100%', 'padding': '0px', },
#                                             className='card-body',
#                                             labelStyle={'display': 'block', 'display': 'inline-block',
#                                                         'margin-right': '10%', 'margin-top': '5px'}
#                                         )
#                                     ], style={'padding-left': '5%'})
#                                 ], style={'padding-left': '5%', 'margin-bottom': '0px'}),
#                                 dcc.Loading(
#                                     id='loading-1',
#                                     type="default",
#                                     children=dcc.Graph(id='grf_MitraPKM')),
#                                 dbc.Button('Lihat Semua Data', id='cll_grfMitraPKM', n_clicks=0, style=button_style)
#                             ], style={'textAlign': 'center'})
#                         ], style=tab_style, selected_style=selected_style),
#             ], style=tabs_styles, id='tab_Mitra', value='kerjaTeliti'),
#         ])
#     ], style=cardgrf_style),
#     dbc.Collapse(
#         id='cll_Mitra',
#         is_open=False
#     )
# ], style=cont_style)

# sitasi = dbc.Container([
#     dbc.Card([
#         html.H5('Jumlah Karya Ilmiah yang Disitasi',
#                 style=ttlgrf_style),
#         dbc.CardBody([
#             dbc.Row([
#                 dbc.Col(
#                     html.Div([
#                         dbc.Row([
#                             dbc.Col([
#                                 html.P('Dari :', style={'marginBottom': 0}),
#                                 dcc.Dropdown(
#                                     id='fltrSitasiStart',
#                                     options=[{'label': i, 'value': i} for i in listDropdownTh],
#                                     value=listDropdownTh[0],
#                                     style={'color': 'black'},
#                                     clearable=False
#                                 )
#                             ]),
#                             dbc.Col([
#                                 html.P('Sampai :', style={'marginBottom': 0}),
#                                 dcc.Dropdown(
#                                     id='fltrSitasiEnd',
#                                     options=[{'label': i, 'value': i} for i in listDropdownTh],
#                                     value=listDropdownTh[3],
#                                     style={'color': 'black'},
#                                     clearable=False
#                                 )
#                             ])
#                         ])
#                     ])
#                 ),
#                 dbc.Col([
#                     html.P('Visualisasi :', style={'margin-bottom': '0'}),
#                     dcc.RadioItems(
#                         id='radioSitasi',
#                         options=[{'label': 'Per Tahun', 'value': 'tahun'},
#                                  {'label': 'Dosen Top', 'value': 'topdosen'}
#                                  ],
#                         value='tahun',
#                         style={'width': '100%', 'padding': '0px', },
#                         className='card-body',
#                         labelStyle={'display': 'block', 'display': 'inline-block',
#                                     'margin-right': '10%', 'margin-top': '5px'},
#                     )
#                 ])
#             ]),
#             dcc.Loading(
#                 id='loading-1',
#                 type="default",
#                 children=dcc.Graph(id='grf_sitasi')),
#             dbc.Button('Lihat Semua Data', id='cll_grfsitasi', n_clicks=0, style=button_style),
#         ]),
#     ], style=cardgrf_style),
#     dbc.Collapse(
#         dbc.Card(
#             dt.DataTable(
#                 id='tbl_Sitasi',
#                 columns=[
#                     {'name': i, 'id': i} for i in dfkisitasi3th.columns
#                 ],
#                 data=dfkisitasi3th.to_dict('records'),
#                 sort_action='native',
#                 sort_mode='multi',
#                 style_table={'padding': '10px', 'overflowX': 'auto'},
#                 style_header={'textAlign': 'center'},
#                 style_data={'font-size': '80%', 'textAlign': 'center'},
#                 style_cell={'width': 95},
#                 page_size=10,
#                 export_format='xlsx'
#             ), style=cardtbl_style
#         ),
#         id='cll_tblsitasi',
#         is_open=False
#     )
# ], style=cont_style)

penSitasi = dbc.Container([
    dbc.Card([
        html.H5('Jumlah Penelitian yang Disitasi',
                style=ttlgrf_style),
        dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.P('Dari :', style={'marginBottom': 0}),
                                dcc.Dropdown(
                                    id='fltrPenSitasiStart',
                                    options=[{'label': i, 'value': i} for i in listDropdownTh],
                                    value=listDropdownTh[0],
                                    style={'color': 'black'},
                                    clearable=False
                                )
                            ]),
                            dbc.Col([
                                html.P('Sampai :', style={'marginBottom': 0}),
                                dcc.Dropdown(
                                    id='fltrPenSitasiEnd',
                                    options=[{'label': i, 'value': i} for i in listDropdownTh],
                                    value=listDropdownTh[3],
                                    style={'color': 'black'},
                                    clearable=False
                                )
                            ])
                        ])
                    ])
                ),
                dbc.Col([
                    html.P('Visualisasi :', style={'margin-bottom': '0'}),
                    dcc.RadioItems(
                        id='radioPenSitasi',
                        options=[{'label': 'Sitasi Per Tahun', 'value': 'tahun'},
                                 {'label': 'Dosen Sitasi Terbanyak', 'value': 'topdosen'}
                                 ],
                        value='tahun',
                        style={'width': '100%', 'padding': '0px', },
                        className='card-body',
                        labelStyle={'display': 'block', 'display': 'inline-block',
                                    'margin-right': '10%', 'margin-top': '5px'},
                    )
                ])
            ]),
            dcc.Loading(
                id='loading-1',
                type="default",
                children=dcc.Graph(id='grf_penSitasi')),
            dbc.Button('Lihat Semua Data', id='cll_grfpenSitasi', n_clicks=0, style=button_style),
        ]),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_penSitasi',
                columns=[
                    {'name': i, 'id': i} for i in dfkisitasi3th.columns
                ],
                data=dfkisitasi3th.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'padding': '10px', 'overflowX': 'auto'},
                style_header={'textAlign': 'center'},
                style_data={'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 95},
                page_size=10,
                export_format='xlsx'
            ), style=cardtbl_style
        ),
        id='cll_tblpenSitasi',
        is_open=False
    )
], style=cont_style)

pkmSitasi = dbc.Container([
    dbc.Card([
        html.H5('Jumlah PKM yang Disitasi',
                style=ttlgrf_style),
        dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.P('Dari :', style={'marginBottom': 0}),
                                dcc.Dropdown(
                                    id='fltrPKMSitasiStart',
                                    options=[{'label': i, 'value': i} for i in listDropdownTh],
                                    value=listDropdownTh[0],
                                    style={'color': 'black'},
                                    clearable=False
                                )
                            ]),
                            dbc.Col([
                                html.P('Sampai :', style={'marginBottom': 0}),
                                dcc.Dropdown(
                                    id='fltrPKMSitasiEnd',
                                    options=[{'label': i, 'value': i} for i in listDropdownTh],
                                    value=listDropdownTh[3],
                                    style={'color': 'black'},
                                    clearable=False
                                )
                            ])
                        ])
                    ])
                ),
                dbc.Col([
                    html.P('Visualisasi :', style={'margin-bottom': '0'}),
                    dcc.RadioItems(
                        id='radioPKMSitasi',
                        options=[{'label': 'Sitasi Per Tahun', 'value': 'tahun'},
                                 {'label': 'Dosen Sitasi Terbanyak', 'value': 'topdosen'}
                                 ],
                        value='tahun',
                        style={'width': '100%', 'padding': '0px', },
                        className='card-body',
                        labelStyle={'display': 'block', 'display': 'inline-block',
                                    'margin-right': '10%', 'margin-top': '5px'},
                    )
                ])
            ]),
            dcc.Loading(
                id='loading-1',
                type="default",
                children=dcc.Graph(id='grf_pkmSitasi')),
            dbc.Button('Lihat Semua Data', id='cll_grfpenSitasi', n_clicks=0, style=button_style),
        ]),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_pkmSitasi',
                columns=[
                    {'name': i, 'id': i} for i in dfkisitasi3th.columns
                ],
                data=dfkisitasi3th.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'padding': '10px', 'overflowX': 'auto'},
                style_header={'textAlign': 'center'},
                style_data={'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 95},
                page_size=10,
                export_format='xlsx'
            ), style=cardtbl_style
        ),
        id='cll_tblpkmSitasi',
        is_open=False
    )
], style=cont_style)

# luaranDs = dbc.Container([
#     dbc.Card([
#         html.H5('Luaran PPP Dosen',
#                 style=ttlgrf_style),
#         html.Div([
#             dbc.Row([
#                 dbc.Col([
#                     html.P('Dari :', style={'marginBottom': 0}),
#                     dcc.Dropdown(
#                         id='fltrLuaranStart',
#                         options=[{'label': i, 'value': i} for i in listDropdownTA],
#                         value=listDropdownTA[0],
#                         style={'color': 'black'},
#                         clearable=False
#                     )
#                 ]),
#                 dbc.Col([
#                     html.P('Sampai :', style={'marginBottom': 0}),
#                     dcc.Dropdown(
#                         id='fltrLuaranEnd',
#                         options=[{'label': i, 'value': i} for i in listDropdownTA],
#                         value=listDropdownTA[0],
#                         style={'color': 'black'},
#                         clearable=False
#                     )
#                 ])
#             ]),
#             dcc.Tabs([
#                 dcc.Tab(label='FTI', value='fti',
#                         children=[
#                             html.Div([
#                                 dbc.Row([
#                                     dbc.Col([
#                                         html.P('Visualisasi :', style={'margin-bottom': '0', 'margin-top': '10px'}),
#                                         dcc.RadioItems(
#                                             id='radio_luaranfti',
#                                             options=[{'label': 'Hak Kekayaan Intelektual (HKI)', 'value': 'hki'},
#                                                      {'label': 'Teknologi Tepat Guna (TTGU)', 'value': 'ttgu'},
#                                                      {'label': 'Buku', 'value': 'buku'}
#                                                      ],
#                                             value='hki',
#                                             style={'width': '100%', 'padding': '0px', },
#                                             className='card-body',
#                                             labelStyle={'display': 'block', 'display': 'inline-block',
#                                                         'margin-right': '5%', 'margin-top': '5px'}
#                                         )
#                                     ], style={'padding-left': '5%'})
#                                 ], style={'padding-left': '5%', 'margin-bottom': '0px'}),
#                                 dbc.Spinner([
#                                       dcc.Graph(id='grf_luarandsfti')
#                                 ], size='md', color='info', type='grow'),
#                                 dbc.Button('Lihat Tabel', id='cll_grfluarandsfti', n_clicks=0,
#                                            style=button_style)
#                             ],style={'textAlign':'center'})
#                         ],
#                         style=tab_style, selected_style=selected_style),
#                 dcc.Tab(label='Per Dosen', value='dosen',
#                         children=[
#                             html.Div([
#                                 dbc.Row([
#                                     dbc.Col([
#                                         html.P('Nama Dosen :', style={'margin-bottom': '0', 'margin-top': '10px'}),
#                                         dcc.Dropdown(
#                                             id='fltrLuaranDsNama',
#                                             options=[{'label': i, 'value': i} for i in dosen],
#                                             value=dosen[1],
#                                             style={'color': 'black'},
#                                             clearable=False
#                                         )
#                                     ],width=4),
#                                     dbc.Col([
#                                         html.P('Visualisasi :', style={'margin-bottom': '0', 'margin-top': '10px'}),
#                                         dcc.RadioItems(
#                                             id='radio_luarands',
#                                             options=[{'label': 'Hak Kekayaan Intelektual (HKI)', 'value': 'hki'},
#                                                      {'label': 'Teknologi Tepat Guna (TTGU)', 'value': 'ttgu'},
#                                                      {'label': 'Buku', 'value': 'buku'}
#                                                      ],
#                                             value='hki',
#                                             style={'width': '100%', 'padding': '0px', },
#                                             className='card-body',
#                                             labelStyle={'display': 'block', 'display': 'inline-block',
#                                                         'margin-right': '5%', 'margin-top': '5px'}
#                                         )
#                                     ],width=8, style={'padding-left': '5%'})
#                                 ], style={'padding-left': '5%', 'margin-bottom': '0px'}),
#                                 dbc.Spinner([
#                                       dcc.Graph(id='grf_luarands')
#                                 ], size='md', color='info', type='grow'),
#                                 dbc.Button('Lihat Tabel', id='cll_grfluarands', n_clicks=0,
#                                            style=button_style)
#                             ],style={'justify-content':'center'})
#                         ],
#                         style=tab_style, selected_style=selected_style)
#             ], style=tabs_styles, id='tab_luaranDosen', value='fti'),
#         ]),
#     ], style=cardgrf_style),
#     dbc.Collapse(
#         id='cll_luaranPPPDosen',
#         is_open=False
#     )
# ], style=cont_style)

luaranPenDs = dbc.Container([
    dbc.Card([
        html.H5('Luaran Penelitian Dosen',
                style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Dari :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrLuaranStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                        value=listDropdownTA[0],
                        style={'color': 'black'},
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Sampai :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrLuaranEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                        value=listDropdownTA[2],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ]),
            html.Div([
                dbc.Row(
                    dbc.Col([
                        html.P('Nama Dosen :', style={'margin-bottom': '0'}),
                        dcc.Dropdown(
                            id='fltrHKIDsNama',
                            options=[{'label': i, 'value': i} for i in dosen],
                            value=dosen[1],
                            style={'color': 'black'},
                            clearable=False
                        )
                    ])
                ),
                dcc.Loading(
                    id='loading-1',
                    type="default",
                    children=dcc.Graph(id='grf_hkiDs')),
                dbc.Button('Lihat Semua Data', id='cll_grfhkiDs', n_clicks=0,
                           style=button_style)
            ]),
        ])
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_luaranPenDosen',
        is_open=False
    )
], style=cont_style)

luaranPKMDs = dbc.Container([
    dbc.Card([
        html.H5('Luaran PKM Dosen',
                style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Dari :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrLuaranPKMStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                        value=listDropdownTA[0],
                        style={'color': 'black'},
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Sampai :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrLuaranPKMEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                        value=listDropdownTA[2],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ]),
            html.Div([
                dbc.Row(
                    dbc.Col([
                        html.P('Nama Dosen :', style={'margin-bottom': '0'}),
                        dcc.Dropdown(
                            id='fltrHKIPKMDsNama',
                            options=[{'label': i, 'value': i} for i in dosen],
                            value=dosen[1],
                            style={'color': 'black'},
                            clearable=False
                        )
                    ])
                ),
                dcc.Loading(
                    id='loading-1',
                    type="default",
                    children=dcc.Graph(id='grf_hkiPKMDs')),
                dbc.Button('Lihat Semua Data', id='cll_grfhkiPKMDs', n_clicks=0,
                           style=button_style)
            ]),
        ])
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_luaranPKMDosen',
        is_open=False
    )
], style=cont_style)

luaranPenMhs = dbc.Container([
    dbc.Card([
        html.H5('Luaran Penelitian Mahasiswa',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Publikasi', value='pubMhs',
                    children=[
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    html.P('Dari :', style={'marginBottom': 0}),
                                    dcc.Dropdown(
                                        id='fltrPubMhsStart',
                                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                                        value=listDropdownTA[0],
                                        style={'color': 'black'},
                                        clearable=False
                                    )
                                ]),
                                dbc.Col([
                                    html.P('Sampai :', style={'marginBottom': 0}),
                                    dcc.Dropdown(
                                        id='fltrPubMhsEnd',
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
                                children=dcc.Graph(id='grf_pubMhs')),
                            dbc.Button('Lihat Semua Data', id='cll_grfpubMhs', n_clicks=0,
                                       style=button_style)
                        ])
                    ], style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Teknologi Tepat Guna (TTGU)', value='ttguMhs',
                    children=[
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    html.P('Dari :', style={'marginBottom': 0}),
                                    dcc.Dropdown(
                                        id='fltrTTGUMhsStart',
                                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                                        value=listDropdownTh[0],
                                        style={'color': 'black'},
                                        clearable=False
                                    )
                                ]),
                                dbc.Col([
                                    html.P('Sampai :', style={'marginBottom': 0}),
                                    dcc.Dropdown(
                                        id='fltrTTGUMhsEnd',
                                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                                        value=listDropdownTh[3],
                                        style={'color': 'black'},
                                        placeholder='Pilih Tahun Akhir',
                                        clearable=False
                                    )
                                ])
                            ])
                        ]),
                        html.Div([
                            dcc.Loading(
                                id='loading-1',
                                type="default",
                                children=dcc.Graph(id='grf_ttguMhs')),
                            dbc.Button('Lihat Semua Data', id='cll_grfttguMhs', n_clicks=0,
                                       style=button_style)
                        ])
                    ], style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Hak Kekayaan Intelektual (HKI)', value='hkiMhs',
                    children=[
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    html.P('Dari :', style={'marginBottom': 0}),
                                    dcc.Dropdown(
                                        id='fltrHKIMhsStart',
                                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                                        value=listDropdownTh[0],
                                        style={'color': 'black'},
                                        clearable=False
                                    )
                                ]),
                                dbc.Col([
                                    html.P('Sampai :', style={'marginBottom': 0}),
                                    dcc.Dropdown(
                                        id='fltrHKIMhsEnd',
                                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                                        value=listDropdownTh[3],
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
                                children=dcc.Graph(id='grf_hkiMhs')),
                            dbc.Button('Lihat Semua Data', id='cll_grfhkiMhs', n_clicks=0,
                                       style=button_style)
                        ])
                    ], style=tab_style, selected_style=selected_style),
        ], style=tabs_styles, id='tab_luaranMhs', value='pubMhs')
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_luaranPPPMhs',
        is_open=False
    )
], style=cont_style)

luaranPKMMhs = dbc.Container([
    dbc.Card([
        html.H5('Luaran PKM Mahasiswa',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Publikasi', value='pubPKMMhs',
                    children=[
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    html.P('Dari :', style={'marginBottom': 0}),
                                    dcc.Dropdown(
                                        id='fltrPubPKMMhsStart',
                                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                                        value=listDropdownTA[0],
                                        style={'color': 'black'},
                                        clearable=False
                                    )
                                ]),
                                dbc.Col([
                                    html.P('Sampai :', style={'marginBottom': 0}),
                                    dcc.Dropdown(
                                        id='fltrPubPKMMhsEnd',
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
                                children=dcc.Graph(id='grf_pubPKMMhs')),
                            dbc.Button('Lihat Semua Data', id='cll_grfpubPKMMhs', n_clicks=0,
                                       style=button_style)
                        ])
                    ], style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Teknologi Tepat Guna (TTGU)', value='ttguPKMMhs',
                    children=[
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    html.P('Dari :', style={'marginBottom': 0}),
                                    dcc.Dropdown(
                                        id='fltrTTGUPKMMhsStart',
                                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                                        value=listDropdownTh[0],
                                        style={'color': 'black'},
                                        clearable=False
                                    )
                                ]),
                                dbc.Col([
                                    html.P('Sampai :', style={'marginBottom': 0}),
                                    dcc.Dropdown(
                                        id='fltrTTGUPKMMhsEnd',
                                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                                        value=listDropdownTh[3],
                                        style={'color': 'black'},
                                        placeholder='Pilih Tahun Akhir',
                                        clearable=False
                                    )
                                ])
                            ])
                        ]),
                        html.Div([
                            dcc.Loading(
                                id='loading-1',
                                type="default",
                                children=dcc.Graph(id='grf_ttguPKMMhs')),
                            dbc.Button('Lihat Semua Data', id='cll_grfttguPKMMhs', n_clicks=0,
                                       style=button_style)
                        ])
                    ], style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Hak Kekayaan Intelektual (HKI)', value='hkiPKMMhs',
                    children=[
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    html.P('Dari :', style={'marginBottom': 0}),
                                    dcc.Dropdown(
                                        id='fltrHKIPKMMhsStart',
                                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                                        value=listDropdownTh[0],
                                        style={'color': 'black'},
                                        clearable=False
                                    )
                                ]),
                                dbc.Col([
                                    html.P('Sampai :', style={'marginBottom': 0}),
                                    dcc.Dropdown(
                                        id='fltrHKIPKMMhsEnd',
                                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                                        value=listDropdownTh[3],
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
                                children=dcc.Graph(id='grf_hkiPKMMhs')),
                            dbc.Button('Lihat Semua Data', id='cll_grfhkiPKMMhs', n_clicks=0,
                                       style=button_style)
                        ])
                    ], style=tab_style, selected_style=selected_style),
        ], style=tabs_styles, id='tab_luaranPKMMhs', value='pubPKMMhs')
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_luaranPKMMhs',
        is_open=False
    )
], style=cont_style)

penRerata = dbc.Container([
    dbc.Card([
        html.H5('Rata-rata Jumlah Penelitian Dosen',
                style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Dari :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPenRerataStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[0],
                        style={'color': 'black'},
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Sampai :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPenRerataEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[3],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ]),
            html.Div([
                dcc.Loading(
                    id='loading-1',
                    type="default",
                    children=dcc.Graph(id='grf_reTelitiDosen')),
                dbc.Button('Lihat Semua Data', id='cll_grfreTelitiDosen', n_clicks=0,
                           style=button_style)
            ])
        ])
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_rerataPen',
        is_open=False
    )
], style=cont_style)

pkmRerata = dbc.Container([
    dbc.Card([
        html.H5('Rata-rata Jumlah PKM Dosen',
                style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Dari :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPKMRerataStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[0],
                        style={'color': 'black'},
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Sampai :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPKMRerataEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[3],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ]),
            html.Div([
                dcc.Loading(
                    id='loading-1',
                    type="default",
                    children=dcc.Graph(id='grf_rePubDosen')),
                dbc.Button('Lihat Semua Data', id='cll_grfrePubDosen', n_clicks=0,
                           style=button_style)
            ])
        ]),
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_rerataPKM',
        is_open=False
    )
], style=cont_style)

penDana = dbc.Container([
    dbc.Card([
        html.H5('Jumlah Penelitian Berdasarkan Sumber Dana per Tahun Ajaran',
                style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Dari :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPenDanaStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[0],
                        style={'color': 'black'},
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Sampai :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPenDanaEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[3],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ]),
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.P('Visualisasi :', style={'margin-bottom': '0'}),
                        dcc.RadioItems(
                            id='radio_penDana',
                            options=[{'label': 'Wilayah', 'value': 'wilayah'},
                                     {'label': 'Sumber Dana', 'value': 'sumber'},
                                     {'label': 'Asal Sumber Dana', 'value': 'asal'}
                                     ],
                            value='wilayah',
                            style={'width': '100%', 'padding': '0px', },
                            className='card-body',
                            labelStyle={'display': 'block', 'display': 'inline-block',
                                        'margin-right': '10%', 'margin-top': '5px'}
                        )
                    ])
                ])
            ], style={'textAlign': 'center'}),
            html.Div([
                dcc.Loading(
                    id='loading-1',
                    type="default",
                    children=dcc.Graph(id='grf_penDana')),
                dbc.Button('Lihat Semua Data', id='cll_grfpenDana', n_clicks=0,
                           style=button_style)
            ])
        ]),
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_penDana',
        is_open=False
    )
], style=cont_style)

pkmDana = dbc.Container([
    dbc.Card([
        html.H5('Jumlah PKM Berdasarkan Sumber Dana per Tahun Ajaran',
                style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Dari :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPKMDanaStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[0],
                        style={'color': 'black'},
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Sampai :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrPKMDanaEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[3],
                        style={'color': 'black'},
                        clearable=False
                    )
                ])
            ]),
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.P('Visualisasi :', style={'margin-bottom': '0'}),
                        dcc.RadioItems(
                            id='radio_pkmDana',
                            options=[{'label': 'Wilayah', 'value': 'wilayah'},
                                     {'label': 'Sumber Dana', 'value': 'sumber'},
                                     {'label': 'Asal Sumber Dana', 'value': 'asal'}
                                     ],
                            value='wilayah',
                            style={'width': '100%', 'padding': '0px', },
                            className='card-body',
                            labelStyle={'display': 'block', 'display': 'inline-block',
                                        'margin-right': '10%', 'margin-top': '5px'}
                        )
                    ])
                ])
            ], style={'textAlign': 'center'}),
            html.Div([
                dcc.Loading(
                    id='loading-1',
                    type="default",
                    children=dcc.Graph(id='grf_pkmDana')),
                dbc.Button('Lihat Semua Data', id='cll_grfpkmDana', n_clicks=0,
                           style=button_style)
            ])
        ]),
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_pkmDana',
        is_open=False
    )
], style=cont_style)

ppkm = dbc.Container([
    html.Div([
        dcc.Tabs([
            dcc.Tab(label='Penelitian', value='pen',
                    children=[
                        penSum,
                        penDs,
                        penMhs,
                        penMitra,
                        # skripsi/kp
                        penSitasi,
                        penRerata,
                        penDana,
                        luaranPenDs,
                        luaranPenMhs
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='PKM', value='pkm',
                    children=[
                        pkmSum,
                        pkmDs,
                        pkmMhs,
                        pkmMitra,
                        pkmSitasi,
                        pkmRerata,
                        pkmDana,
                        luaranPKMDs,
                        luaranPKMMhs
                    ],
                    style=tab_style, selected_style=selected_style)
        ], style=tabs_styles, value='pen')
    ])
])

layout = html.Div([
    html.Div(html.H1('Penelitian, Pengabdian, Publikasi, dan Luaran',
                     style={'margin-top': '30px', 'textAlign': 'center'}
                     )
             ),
    html.Div([ppkm], style={'margin-bottom': '50px'}),
    dbc.Container([
        dcc.Link([
            dbc.Button('^', style=buttonLink_style),
        ], href='#name'),
    ], style={'margin-left': '90%'})
], style={'justify-content': 'center'})


# FILTER CALLBACK
@app.callback(
    Output('grf_penSum', 'figure'),
    Input('fltrPenSumStart', 'value'),
    Input('fltrPenSumEnd', 'value')
)
def graphPenSum(start, end):
    dfpen = data.getDataFrameFromDBwithParams(f'''
                        select tahun Tahun, count(*) 'Jumlah Penelitian'
                        from fact_penelitian fact
                                 inner join dim_penelitian_pkm dim on dim.id_penelitian_pkm = fact.id_penelitian
                                 inner join br_pp_dosen on fact.id_penelitian = br_pp_dosen.id_penelitian_pkm
                                 inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen and id_prodi = 9
                                 inner join dim_date on dim_date.id_date = dim.id_tanggal_mulai
                        where dim.jenis = 'PENELITIAN'
                          and tahun between %(start)s and %(end)s
                        group by tahun
                        order by tahun
                        ''', {'start':start, 'end':end})
    dfpub = data.getDataFrameFromDBwithParams(f'''
                        select tahun_publikasi as Tahun, count(*) 'Jumlah Publikasi'
                        from fact_publikasi fact
                        inner join dim_publikasi dimpub on fact.id_publikasi = dimpub.id_publikasi
                        inner join br_pub_dosen brpub on fact.id_publikasi = brpub.id_publikasi
                        inner join dim_dosen dimdos on brpub.id_dosen = dimdos.id_dosen and id_prodi = 9
                        inner join dim_penelitian_pkm dpp on dimpub.id_penelitian_pkm = dpp.id_penelitian_pkm
                        inner join br_pp_publikasi bpp on brpub.id_publikasi = bpp.id_publikasi
                        where dpp.jenis='PENELITIAN'
                            and tahun_publikasi between %(start)s and %(end)s
                        group by tahun_publikasi
                        order by tahun_publikasi
                    ''', {'start':start, 'end':end})
    dfluaran = data.getDataFrameFromDBwithParams(f'''
                        select tahun Tahun, count(*) 'Jumlah Luaran Lainnya'
                        from fact_luaran_lainnya fatl
                        inner join dim_luaran_lainnya diml on fatl.id_luaran_lainnya = diml.id_luaran_lainnya
                        inner join br_pp_luaranlainnya brl on fatl.id_luaran_lainnya = brl.id_luaranlainnya
                        inner join br_pp_dosen brpp on brpp.id_penelitian_pkm = brl.id_penelitian_pkm
                        inner join dim_dosen on brpp.id_Dosen = dim_dosen.id_dosen and id_prodi = 9
                        inner join dim_date on dim_date.id_date = diml.id_tanggal_luaran
                        where brl.jenis='PENELITIAN'
                            and tahun between %(start)s and %(end)s
                        group by tahun
                        order by tahun
                    ''', {'start':start, 'end':end})
    figpenSum = px.bar(dfpen, x=dfpen['Tahun'], y=dfpen['Jumlah Penelitian'],color=px.Constant('Penelitian'),
                      labels=dict(x='Tahun', y='Jumlah Penelitian', color='Keterangan'))
    figpenSum.add_bar(x=dfpub['Tahun'], y=dfpub['Jumlah Publikasi'],name='Publikasi Penelitian')
    figpenSum.add_bar(x=dfluaran['Tahun'], y=dfluaran['Jumlah Luaran Lainnya'],name='Luaran Penelitian')
    figpenSum.update_traces(hovertemplate='Tahun : %{x}<br>Jumlah : %{value}')
    return figpenSum

@app.callback(
    Output('grf_pkmSum', 'figure'),
    Input('fltrPKMSumStart', 'value'),
    Input('fltrPKMSumEnd', 'value')
)
def graphPKMSum(start, end):
    dfpkm = data.getDataFrameFromDBwithParams(f'''
                        select tahun Tahun, count(*) 'Jumlah PKM'
                        from fact_pkm fact
                                 inner join dim_penelitian_pkm dim on dim.id_penelitian_pkm = fact.id_pkm
                                 inner join br_pp_dosen on fact.id_pkm = br_pp_dosen.id_penelitian_pkm
                                 inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen and id_prodi = 9
                                 inner join dim_date on dim_date.id_date = dim.id_tanggal_mulai
                        where dim.jenis = 'PKM'
                          and tahun between %(start)s and %(end)s
                        group by tahun
                        order by tahun
                        ''', {'start':start, 'end':end})
    dfpub = data.getDataFrameFromDBwithParams(f'''
                        select tahun_publikasi as Tahun, count(*) 'Jumlah Publikasi'
                        from fact_publikasi fact
                                 inner join dim_publikasi dimpub on fact.id_publikasi = dimpub.id_publikasi
                                 inner join br_pub_dosen brpub on fact.id_publikasi = brpub.id_publikasi
                                 inner join dim_dosen dimdos on brpub.id_dosen = dimdos.id_dosen and id_prodi = 9
                                 inner join dim_penelitian_pkm dpp on dimpub.id_penelitian_pkm = dpp.id_penelitian_pkm
                                 inner join br_pp_publikasi bpp on brpub.id_publikasi = bpp.id_publikasi
                        where dpp.jenis = 'PKM'
                          and tahun_publikasi between %(start)s and %(end)s
                        group by tahun_publikasi
                        order by tahun_publikasi
                    ''', {'start':start, 'end':end})
    dfluaran = data.getDataFrameFromDBwithParams(f'''
                        select tahun Tahun, count(*) 'Jumlah Luaran Lainnya'
                        from fact_luaran_lainnya fatl
                                 inner join dim_luaran_lainnya diml on fatl.id_luaran_lainnya = diml.id_luaran_lainnya
                                 inner join br_pp_luaranlainnya brl on fatl.id_luaran_lainnya = brl.id_luaranlainnya
                                 inner join br_pp_dosen brpp on brpp.id_penelitian_pkm = brl.id_penelitian_pkm
                                 inner join dim_dosen on brpp.id_Dosen = dim_dosen.id_dosen and id_prodi = 9
                                 inner join dim_date on dim_date.id_date = diml.id_tanggal_luaran
                        where brl.jenis='PKM'
                          and tahun between %(start)s and %(end)s
                        group by tahun
                        order by tahun
                    ''', {'start':start, 'end':end})
    figpkmSum = px.bar(dfpkm, x=dfpkm['Tahun'], y=dfpkm['Jumlah PKM'],color=px.Constant('PKM'),
                      labels=dict(x='Tahun', y='Jumlah PKM', color='Keterangan'))
    figpkmSum.add_bar(x=dfpub['Tahun'], y=dfpub['Jumlah Publikasi'],name='Publikasi PKM')
    figpkmSum.add_bar(x=dfluaran['Tahun'], y=dfluaran['Jumlah Luaran Lainnya'],name='Luaran PKM')
    figpkmSum.update_traces(hovertemplate='Tahun : %{x}<br>Jumlah : %{value}')
    return figpkmSum

@app.callback(
    Output('grf_penDs', 'figure'),
    Input('fltrPenDsNama', 'value')
)
def graphPenDosen(namads):
    dfpen = data.getDataFrameFromDBwithParams(f'''
                        select upper(nama) Nama, tahun Tahun, count(*) 'Jumlah Penelitian'
                        from fact_penelitian fact
                        inner join dim_penelitian_pkm dim on dim.id_penelitian_pkm = fact.id_penelitian
                        inner join br_pp_dosen on fact.id_penelitian = br_pp_dosen.id_penelitian_pkm
                        inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen and id_prodi = 9
                        inner join dim_date on dim_date.id_date = dim.id_tanggal_mulai
                        where tahun>=year(now())-5 and nama like %(nama)s
                        group by nama, tahun
                        order by nama, tahun
                        ''', {'nama': namads})
    dfpub = data.getDataFrameFromDBwithParams(f'''
                        select upper(nama) Nama, tahun_publikasi as Tahun, count(*) 'Jumlah Publikasi'
                        from fact_publikasi fact
                        inner join dim_publikasi dimpub on fact.id_publikasi = dimpub.id_publikasi
                        inner join br_pub_dosen brpub on fact.id_publikasi = brpub.id_publikasi
                        inner join dim_dosen dimdos on brpub.id_dosen = dimdos.id_dosen and id_prodi = 9
                        inner join dim_penelitian_pkm dpp on dimpub.id_penelitian_pkm = dpp.id_penelitian_pkm
                        inner join br_pp_publikasi bpp on brpub.id_publikasi = bpp.id_publikasi
                        where dpp.jenis='PENELITIAN'
                               and (tahun_publikasi>=year(now())-5 and nama like %(nama)s)
                        group by nama, tahun_publikasi
                        order by nama, tahun_publikasi
                    ''', {'nama': namads})
    dfluaran = data.getDataFrameFromDBwithParams(f'''
                        select upper(nama) Nama, tahun Tahun, count(*) 'Jumlah Luaran Lainnya'
                        from fact_luaran_lainnya fatl
                        inner join dim_luaran_lainnya diml on fatl.id_luaran_lainnya = diml.id_luaran_lainnya
                        inner join br_pp_luaranlainnya brl on fatl.id_luaran_lainnya = brl.id_luaranlainnya
                        inner join br_pp_dosen brpp on brpp.id_penelitian_pkm = brl.id_penelitian_pkm
                        inner join dim_dosen on brpp.id_Dosen = dim_dosen.id_dosen and id_prodi = 9
                        inner join dim_date on dim_date.id_date = diml.id_tanggal_luaran
                        where brl.jenis='PENELITIAN'
                               and tahun>=year(now())-5 and nama like %(nama)s
                        group by  nama, tahun
                        order by nama, tahun
                    ''', {'nama': namads})
    figpenDs = px.bar(dfpen, x=dfpen['Tahun'], y=dfpen['Jumlah Penelitian'],color=px.Constant('Penelitian'),
                      labels=dict(x='Tahun', y='Jumlah Penelitian', color='Keterangan'))
    figpenDs.add_bar(x=dfpub['Tahun'], y=dfpub['Jumlah Publikasi'],name='Publikasi Penelitian')
    figpenDs.add_bar(x=dfluaran['Tahun'], y=dfluaran['Jumlah Luaran Lainnya'],name='Luaran Penelitian')
    figpenDs.update_traces(hovertemplate='Tahun : %{x}<br>Jumlah : %{value}')
    return figpenDs


@app.callback(
    Output('grf_pkmDs', 'figure'),
    Input('fltrPKMDsNama', 'value')
)
def graphPKMDosen(namads):
    dfpkm = data.getDataFrameFromDBwithParams(f'''
                        select upper(nama) Nama, tahun Tahun, count(*) as 'Jumlah PKM'
                        from fact_pkm fact
                        inner join dim_penelitian_pkm dim on dim.id_penelitian_pkm = fact.id_pkm
                        inner join br_pp_dosen on fact.id_pkm = br_pp_dosen.id_penelitian_pkm
                        inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen and id_prodi = 9
                        inner join dim_date on dim_date.id_date = dim.id_tanggal_mulai
                        where tahun>=year(now())-5 and nama like %(nama)s
                        group by dim_dosen.id_dosen, nama, tahun
                        order by nama, tahun
                    ''', {'nama': namads})
    dfpub = data.getDataFrameFromDBwithParams(f'''
                        select upper(nama) Nama, tahun_publikasi as Tahun, count(*) 'Jumlah Publikasi'
                        from fact_publikasi fact
                        inner join dim_publikasi dimpub on fact.id_publikasi = dimpub.id_publikasi
                        inner join br_pub_dosen brpub on fact.id_publikasi = brpub.id_publikasi
                        inner join dim_dosen dimdos on brpub.id_dosen = dimdos.id_dosen and id_prodi = 9
                        inner join dim_penelitian_pkm dpp on dimpub.id_penelitian_pkm = dpp.id_penelitian_pkm
                        inner join br_pp_publikasi bpp on brpub.id_publikasi = bpp.id_publikasi
                        where dpp.jenis='PKM'
                                and (tahun_publikasi>=year(now())-5 and nama like %(nama)s)
                        group by nama, tahun_publikasi
                        order by nama, tahun_publikasi
                    ''', {'nama': namads})
    dfluaran = data.getDataFrameFromDBwithParams(f'''
                        select upper(nama) Nama, tahun Tahun, count(*) 'Jumlah Luaran Lainnya'
                        from fact_luaran_lainnya fatl
                        inner join dim_luaran_lainnya diml on fatl.id_luaran_lainnya = diml.id_luaran_lainnya
                        inner join br_pp_luaranlainnya brl on fatl.id_luaran_lainnya = brl.id_luaranlainnya
                        inner join br_pp_dosen brpp on brpp.id_penelitian_pkm = brl.id_penelitian_pkm
                        inner join dim_dosen on brpp.id_Dosen = dim_dosen.id_dosen and id_prodi = 9
                        inner join dim_date on dim_date.id_date = diml.id_tanggal_luaran
                        where brl.jenis='PKM'
                               and tahun>=year(now())-5 and nama like %(nama)s
                        group by  nama, tahun
                        order by nama, tahun
                    ''', {'nama': namads})
    figpkm = px.bar(dfpkm, x=dfpkm['Tahun'], y=dfpkm['Jumlah PKM'],color=px.Constant('PKM'),
                      labels=dict(x='Tahun', y='Jumlah PKM', color='Keterangan'))
    figpkm.add_bar(x=dfpub['Tahun'], y=dfpub['Jumlah Publikasi'], name='Publikasi PKM')
    figpkm.add_bar(x=dfluaran['Tahun'], y=dfluaran['Jumlah Luaran Lainnya'], name='Luaran PKM')
    figpkm.update_traces(hovertemplate='Tahun: %{x}<br>Jumlah :%{value}')
    return figpkm

@app.callback(
    Output('grf_PenDM','figure'),
    Input('fltrPenDMStart','value'),
    Input('fltrPenDMEnd','value'),
    Input('radio_pendm','value')
)
def graphPenDM(start, end, radiopendm):
    if radiopendm == 'jumlah' :
        dfjumlpendm = data.getDataFrameFromDBwithParams(f'''
        select tahun Tahun,
               count(distinct id_penelitian) 'Jumlah Penelitian'
        from fact_penelitian fc
            inner join dim_penelitian_pkm dpp on fc.id_tanggal_mulai = dpp.id_tanggal_mulai
            inner join br_pp_mahasiswa bpm on dpp.id_penelitian_pkm = bpm.id_penelitian_pkm
            inner join dim_mahasiswa dm on bpm.id_mahasiswa = dm.id_mahasiswa
            inner join dim_date dd on dd.id_date = dpp.id_tanggal_mulai
        where tahun between %(start)s and %(end)s
        group by tahun
        order by tahun
        ''',{'start':start,'end':end})
        figjumlpendm = px.line(dfjumlpendm, x=dfjumlpendm['Tahun'], y=dfjumlpendm['Jumlah Penelitian'])
        figjumlpendm.update_layout(yaxis_title='Jumlah Penelitian')
        figjumlpendm.update_traces(mode='lines+markers')
        return figjumlpendm
    elif radiopendm == 'rata':
        dfratapendm = data.getDataFrameFromDBwithParams(f'''
            select tahun                           'Tahun',
                   round(avg(jumlah_Dosen))        'Dosen',
                   round(avg(jumlah_mahasiswa))    'Mahasiswa'
            from fact_penelitian fact
                     inner join dim_penelitian_pkm on fact.id_penelitian = dim_penelitian_pkm.id_penelitian_pkm
                     inner join dim_penelitian_pkm dim on dim.id_penelitian_pkm = fact.id_penelitian
                     inner join br_pp_dosen on fact.id_penelitian = br_pp_dosen.id_penelitian_pkm
                     inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen
                     inner join dim_date on dim_date.id_date = dim.id_tanggal_mulai
                     inner join br_pp_mahasiswa on fact.id_penelitian = br_pp_mahasiswa.id_penelitian_pkm
                     inner join dim_mahasiswa on br_pp_mahasiswa.id_mahasiswa = dim_mahasiswa.id_mahasiswa
            where (tahun between %(start)s and %(end)s)
            group by tahun
            order by tahun
        ''',{'start':start,'end':end})
        figratapendm = px.line(dfratapendm, x=dfratapendm['Tahun'], y=dfratapendm.columns[1:3])
        figratapendm.update_layout(yaxis_title='Rerata Jumlah Partisipan', legend_title='Partisipan')
        figratapendm.update_traces(mode='lines+markers')
        return figratapendm
    elif radiopendm == 'top':
        dftop = data.getDataFrameFromDBwithParams(f'''
        select tahun                 'Tahun',
               upper(substring_index(fact.judul_penelitian,' ',5)) 'Judul Penelitian',
               jumlah_Dosen          'Jumlah Dosen',
               jumlah_mahasiswa      'Jumlah Mahasiswa'
        from fact_penelitian fact
                 inner join dim_penelitian_pkm on fact.id_penelitian = dim_penelitian_pkm.id_penelitian_pkm
                 inner join dim_penelitian_pkm dim on dim.id_penelitian_pkm = fact.id_penelitian
                 inner join br_pp_dosen on fact.id_penelitian = br_pp_dosen.id_penelitian_pkm
                 inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen
                 inner join dim_date on dim_date.id_date = dim.id_tanggal_mulai
                 inner join br_pp_mahasiswa on fact.id_penelitian = br_pp_mahasiswa.id_penelitian_pkm
                 inner join dim_mahasiswa on br_pp_mahasiswa.id_mahasiswa = dim_mahasiswa.id_mahasiswa
        where (tahun between %(start)s and %(end)s)
        group by judul_penelitian, jumlah_Dosen, jumlah_mahasiswa, tahun, `Judul Penelitian`
        order by `Jumlah Dosen` desc,`Jumlah Mahasiswa` desc
        limit 10
        ''',{'start':start,'end':end})
        figtop = px.bar(dftop, y=dftop['Judul Penelitian'], x=dftop.columns[2:4])
        figtop.update_layout(barmode='group', yaxis_title='Judul Penelitian', xaxis_title='Jumlah Partisipan', legend_title='Partisipan')
        return figtop

@app.callback(
    Output('grf_pkmDM', 'figure'),
    Input('fltrPKMDMStart', 'value'),
    Input('fltrPKMDMEnd', 'value'),
    Input('radio_pkmdm', 'value')
)
def PKMDM(start, end, radiopkmdm):
    if radiopkmdm == 'jumlah':
        dfjumlpkmdm = data.getDataFrameFromDBwithParams(f'''
        select tahun Tahun,
               count(distinct id_pkm) 'Jumlah PKM'
        from fact_pkm fp
        inner join dim_penelitian_pkm dpp on fp.id_tanggal_mulai = dpp.id_tanggal_mulai
        inner join br_pp_mahasiswa bpm on dpp.id_penelitian_pkm = bpm.id_penelitian_pkm
        inner join dim_mahasiswa dm on bpm.id_mahasiswa = dm.id_mahasiswa
        inner join dim_date dd on dd.id_date = dpp.id_tanggal_mulai
        where tahun between %(start)s and %(end)s
        group by tahun
        order by tahun
        ''',{'start':start,'end':end})
        figjumlpkmdm = px.line(dfjumlpkmdm, x=dfjumlpkmdm['Tahun'], y=dfjumlpkmdm['Jumlah PKM'])
        figjumlpkmdm.update_layout(yaxis_title='Jumlah PKM')
        figjumlpkmdm.update_traces(mode='lines+markers')
        return figjumlpkmdm
    elif radiopkmdm == 'rata':
        dfratapkmdm = data.getDataFrameFromDBwithParams(f'''
        select Tahun,
               round(avg(jumlah_Dosen))     "Dosen",
               round(avg(jumlah_mahasiswa)) "Mahasiswa"
        from fact_pkm fact
                 inner join dim_penelitian_pkm on fact.id_pkm = dim_penelitian_pkm.id_penelitian_pkm
                 inner join br_pp_dosen on fact.id_pkm = br_pp_dosen.id_penelitian_pkm
                 inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen
                 inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
                 inner join br_pp_mahasiswa on fact.id_pkm = br_pp_mahasiswa.id_penelitian_pkm
                 inner join dim_mahasiswa on br_pp_mahasiswa.id_mahasiswa = dim_mahasiswa.id_mahasiswa
        where tahun between %(start)s and %(end)s
        group by tahun
        order by tahun
        ''',{'start':start,'end':end})
        figratapkmdm = px.line(dfratapkmdm, x=dfratapkmdm['Tahun'], y=dfratapkmdm.columns[1:3])
        figratapkmdm.update_layout(yaxis_title='Rerata Jumlah Partisipan', legend_title='Partisipan')
        figratapkmdm.update_traces(mode='lines+markers')
        return figratapkmdm
    elif radiopkmdm == 'top':
        dftoppkm = data.getDataFrameFromDBwithParams(f'''
        select tahun Tahun,
               upper(substring_index(judul_pkm,' ',5))  "Judul PKM",
               jumlah_Dosen                             "Jumlah Dosen",
               jumlah_mahasiswa                         "Jumlah Mahasiswa"
        from fact_pkm fact
                 inner join dim_penelitian_pkm on fact.id_pkm = dim_penelitian_pkm.id_penelitian_pkm
                 inner join br_pp_dosen on fact.id_pkm = br_pp_dosen.id_penelitian_pkm
                 inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen
                 inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
                 inner join br_pp_mahasiswa on fact.id_pkm = br_pp_mahasiswa.id_penelitian_pkm
                 inner join dim_mahasiswa on br_pp_mahasiswa.id_mahasiswa = dim_mahasiswa.id_mahasiswa
        where Tahun between %(start)s and %(end)s
        group by judul_pkm, jumlah_Dosen, jumlah_mahasiswa, tahun, `Judul PKM`
        order by  `Jumlah Dosen` desc,`Jumlah Mahasiswa` desc
        limit 10
        ''',{'start':start, 'end':end})
        figtoppkm = px.bar(dftoppkm, y=dftoppkm['Judul PKM'], x=dftoppkm.columns[2:4])
        figtoppkm.update_layout(barmode='group', yaxis_title='Judul PKM', xaxis_title='Jumlah Partisipan', legend_title='Partisipan')
        return figtoppkm

@app.callback(
    Output('grf_penMitra', 'figure'),
    Input('fltrPenMitraStart', 'value'),
    Input('fltrPenMitraEnd', 'value'),
    Input('radio_penMitra', 'value')
)
def MitraPen(start, end, radiopenmitra):
    if radiopenmitra == 'top':
        dfpenmitra = data.getDataFrameFromDBwithParams(f'''
        select dm.nama_mitra 'Nama Mitra', count(dpp.judul) `Jumlah Penelitian`
        from br_pp_perjanjian bpp
                 inner join dim_penelitian_pkm dpp on bpp.id_penelitian_pkm = dpp.id_penelitian_pkm
                 inner join dim_perjanjian dp on bpp.id_perjanjian = dp.id_perjanjian
                 inner join br_mitra_perjanjian bmp on dp.id_perjanjian = bmp.id_perjanjian
                 inner join dim_mitra dm on bmp.id_mitra = dm.id_mitra
                 inner join dim_date ddselesai on ddselesai.id_date = dpp.id_tanggal_selesai
                 inner join dim_date ddmulai on ddmulai.id_date = dpp.id_tanggal_mulai
        where bpp.jenis = 'Penelitian'
          and ddselesai.tahun between %(start)s and %(end)s
        group by `Nama Mitra`
        order by `Jumlah Penelitian` desc
        limit 10;
        ''',{'start':start,'end':end})
        figpenmitra = px.bar(dfpenmitra, y=dfpenmitra['Nama Mitra'], x=dfpenmitra['Jumlah Penelitian'])
        return figpenmitra
    elif radiopenmitra == 'jenis':
        dfjenis = data.getDataFrameFromDBwithParams(f'''
        select ddselesai.tahun Tahun,
               case
                   when jenis_mitra = 'ORGANISASI' then 'ORGANISASI'
                   when jenis_mitra = 'PEMERINTAH' then 'PEMERINTAH'
                   when jenis_mitra = 'BISNIS' then 'BISNIS'
                   when jenis_mitra = 'GEREJA' then 'GEREJA'
                   when jenis_mitra = 'PENDIDIKAN' then 'PENDIDIKAN'
                   else 'LAINNYA'
                   end as 'Jenis Mitra',
               count(*) 'Jumlah Penelitian'
        from br_pp_perjanjian bpp
                 inner join dim_penelitian_pkm dpp on bpp.id_penelitian_pkm = dpp.id_penelitian_pkm
                 inner join dim_perjanjian dp on bpp.id_perjanjian = dp.id_perjanjian
                 inner join br_mitra_perjanjian bmp on dp.id_perjanjian = bmp.id_perjanjian
                 inner join dim_mitra dm on bmp.id_mitra = dm.id_mitra
                 inner join dim_date ddselesai on ddselesai.id_date = dpp.id_tanggal_selesai
                 inner join dim_date ddmulai on ddmulai.id_date = dpp.id_tanggal_mulai
        where bpp.jenis = 'Penelitian'
            and ddselesai.tahun between %(start)s and %(end)s
        group by ddselesai.tahun, `Jenis Mitra`
        order by Tahun, `Jenis Mitra`
        ''',{'start':start, 'end':end})
        figjenis = px.bar(dfjenis, x=dfjenis['Tahun'], y=dfjenis['Jumlah Penelitian'], color=dfjenis['Jenis Mitra'])
        figjenis.update_layout(barmode='group', yaxis_title='Jumlah Penelitian', xaxis_title='Tahun, Jenis Mitra', legend_title='Mitra')
        return figjenis
    elif radiopenmitra == 'wilayah':
        dfwilayah = data.getDataFrameFromDBwithParams(f'''
        select ddselesai.tahun Tahun,
               case
                   when dm.wilayah = '1' then 'LOKAL'
                   when dm.wilayah = '2' then 'REGIONAL'
                   when dm.wilayah = '3' then 'NASIONAL'
                   when dm.wilayah = '4' then 'INTERNASIONAL'
                   else 'NONE' end as 'Wilayah Mitra',
               count(*)               'Jumlah Penelitian'
        from br_pp_perjanjian bpp
                 inner join dim_penelitian_pkm dpp on bpp.id_penelitian_pkm = dpp.id_penelitian_pkm
                 inner join dim_perjanjian dp on bpp.id_perjanjian = dp.id_perjanjian
                 inner join br_mitra_perjanjian bmp on dp.id_perjanjian = bmp.id_perjanjian
                 inner join dim_mitra dm on bmp.id_mitra = dm.id_mitra
                 inner join dim_date ddselesai on ddselesai.id_date = dpp.id_tanggal_selesai
                 inner join dim_date ddmulai on ddmulai.id_date = dpp.id_tanggal_mulai
        where bpp.jenis = 'Penelitian'
            and ddselesai.tahun between %(start)s and %(end)s
        group by ddselesai.tahun, `Wilayah Mitra`
        order by Tahun, `Wilayah Mitra`
        ''',{'start':start, 'end':end})
        figwilayah = px.bar(dfwilayah, x=dfwilayah['Tahun'], y=dfwilayah['Jumlah Penelitian'], color=dfwilayah['Wilayah Mitra'])
        figwilayah.update_layout(barmode='group', yaxis_title='Jumlah Penelitian', xaxis_title='Tahun, Wilayah Mitra',
                               legend_title='Mitra')
        return figwilayah

@app.callback(
    Output('grf_pkmMitra', 'figure'),
    Input('fltrPKMMitraStart', 'value'),
    Input('fltrPKMMitraEnd', 'value'),
    Input('radio_pkmMitra', 'value')
)
def PKMDM(start, end, radiopkmmitra):
    if radiopkmmitra == 'top':
        dfratapkmdm = data.getDataFrameFromDBwithParams(f'''
        select dm.nama_mitra 'Nama Mitra', count(dpp.judul) `Jumlah PKM`
        from br_pp_perjanjian bpp
                 inner join dim_penelitian_pkm dpp on bpp.id_penelitian_pkm = dpp.id_penelitian_pkm
                 inner join dim_perjanjian dp on bpp.id_perjanjian = dp.id_perjanjian
                 inner join br_mitra_perjanjian bmp on dp.id_perjanjian = bmp.id_perjanjian
                 inner join dim_mitra dm on bmp.id_mitra = dm.id_mitra
                 inner join dim_date ddselesai on ddselesai.id_date = dpp.id_tanggal_selesai
                 inner join dim_date ddmulai on ddmulai.id_date = dpp.id_tanggal_mulai
        where bpp.jenis = 'PKM'
          and ddselesai.tahun between %(start)s and %(end)s
        group by `Nama Mitra`
        order by `Jumlah PKM` desc
        limit 10;
        ''',{'start':start,'end':end})
        figpkmmitra = px.bar(dfratapkmdm, y=dfratapkmdm['Nama Mitra'], x=dfratapkmdm['Jumlah PKM'])
        return figpkmmitra
    elif radiopkmmitra == 'jenis':
        dfjenis = data.getDataFrameFromDBwithParams(f'''
        select ddselesai.tahun Tahun,
               case
                   when jenis_mitra = 'ORGANISASI' then 'ORGANISASI'
                   when jenis_mitra = 'PEMERINTAH' then 'PEMERINTAH'
                   when jenis_mitra = 'BISNIS' then 'BISNIS'
                   when jenis_mitra = 'GEREJA' then 'GEREJA'
                   when jenis_mitra = 'PENDIDIKAN' then 'PENDIDIKAN'
                   else 'LAINNYA'
                   end as 'Jenis Mitra',
               count(*) 'Jumlah PKM'
        from br_pp_perjanjian bpp
                 inner join dim_penelitian_pkm dpp on bpp.id_penelitian_pkm = dpp.id_penelitian_pkm
                 inner join dim_perjanjian dp on bpp.id_perjanjian = dp.id_perjanjian
                 inner join br_mitra_perjanjian bmp on dp.id_perjanjian = bmp.id_perjanjian
                 inner join dim_mitra dm on bmp.id_mitra = dm.id_mitra
                 inner join dim_date ddselesai on ddselesai.id_date = dpp.id_tanggal_selesai
                 inner join dim_date ddmulai on ddmulai.id_date = dpp.id_tanggal_mulai
        where bpp.jenis = 'PKM'
            and ddselesai.tahun between %(start)s and %(end)s
        group by ddselesai.tahun, `Jenis Mitra`
        order by Tahun, `Jenis Mitra`
        ''',{'start':start, 'end':end})
        figjenis = px.bar(dfjenis, x=dfjenis['Tahun'], y=dfjenis['Jumlah PKM'], color=dfjenis['Jenis Mitra'])
        figjenis.update_layout(barmode='group', yaxis_title='Jumlah PKM', xaxis_title='Tahun, Jenis Mitra',
                               legend_title='Mitra')
        return figjenis
    elif radiopkmmitra == 'wilayah':
        dfwilayah = data.getDataFrameFromDBwithParams(f'''
        select ddselesai.tahun Tahun,
               case
                   when dm.wilayah = '1' then 'LOKAL'
                   when dm.wilayah = '2' then 'REGIONAL'
                   when dm.wilayah = '3' then 'NASIONAL'
                   when dm.wilayah = '4' then 'INTERNASIONAL'
                   else 'NONE' end as 'Wilayah Mitra',
               count(*)               'Jumlah PKM'
        from br_pp_perjanjian bpp
                 inner join dim_penelitian_pkm dpp on bpp.id_penelitian_pkm = dpp.id_penelitian_pkm
                 inner join dim_perjanjian dp on bpp.id_perjanjian = dp.id_perjanjian
                 inner join br_mitra_perjanjian bmp on dp.id_perjanjian = bmp.id_perjanjian
                 inner join dim_mitra dm on bmp.id_mitra = dm.id_mitra
                 inner join dim_date ddselesai on ddselesai.id_date = dpp.id_tanggal_selesai
                 inner join dim_date ddmulai on ddmulai.id_date = dpp.id_tanggal_mulai
        where bpp.jenis = 'PKM'
            and ddselesai.tahun between %(start)s and %(end)s
        group by ddselesai.tahun, `Wilayah Mitra`
        order by Tahun, `Wilayah Mitra`
        ''', {'start': start, 'end': end})
        figwilayah = px.bar(dfwilayah, x=dfwilayah['Tahun'], y=dfwilayah['Jumlah PKM'], color=dfwilayah['Wilayah Mitra'])
        figwilayah.update_layout(barmode='group', yaxis_title='Jumlah PKM', xaxis_title='Tahun, Wilayah Mitra',
                               legend_title='Mitra')
        return figwilayah

#luaran Penelitian mahasiswa
@app.callback(
    Output('grf_pubMhs', 'figure'),
    Input('fltrPubMhsStart', 'value'),
    Input('fltrPubMhsEnd', 'value')
)
def graphPubMhs(tglstart, tglend):
    dfPubMhs = data.getDataFrameFromDBwithParams('''
    select tahun_ajaran                    'Tahun Ajaran',
           count(distinct fp.id_publikasi) 'Jumlah Publikasi'
    from br_pub_mahasiswa bpm
             inner join dim_publikasi dp on bpm.id_publikasi = dp.id_penelitian_pkm
             inner join fact_publikasi fp on bpm.id_publikasi = fp.id_penelitian_pkm
             inner join dim_date dd on fp.id_tanggal_publikasi = dd.id_date
             inner join dim_semester ds on ds.kode_semester = concat(tahun, if(bulan >= 7, 2, 1))
             inner join dim_penelitian_pkm dpp on dp.id_penelitian_pkm = dpp.id_penelitian_pkm
    where fp.is_deleted != 1
        and jenis='PENELITIAN'
        and (tahun_ajaran between %(start)s and %(end)s)
    group by tahun_ajaran
    order by tahun_ajaran;
    ''', {'start': tglstart, 'end': tglend})
    figPubMhs = px.line(dfPubMhs, x=dfPubMhs['Tahun Ajaran'], y=dfPubMhs['Jumlah Publikasi'])
    figPubMhs.update_traces(mode='lines+markers')
    return figPubMhs

@app.callback(
    Output('grf_ttguMhs', 'figure'),
    Input('fltrTTGUMhsStart', 'value'),
    Input('fltrTTGUMhsEnd', 'value')
)
def graphPPMhs(tglstart, tglend):
    dfTTGUMhs = data.getDataFrameFromDBwithParams(f'''
    select tahun                                 'Tahun',
           count(distinct dll.id_penelitian_pkm) 'Jumlah Judul'
    from dim_luaran_lainnya dll
             inner join fact_luaran_lainnya fll on dll.id_penelitian_pkm = fll.id_penelitian_pkm
             inner join dim_jenis_luaran djl on dll.id_jenis_luaran = djl.id_jenis_luaran
             inner join br_ll_mahasiswa blm on dll.id_luaran_lainnya = blm.id_luaran_lainnya
             inner join dim_date dd on dd.id_date = dll.id_tanggal_luaran
             inner join dim_penelitian_pkm dpp on dll.id_penelitian_pkm = dpp.id_penelitian_pkm
    where keterangan_jenis_luaran = 'TEKNOLOGI TEPAT GUNA'
        and jenis='PENELITIAN'
      and (tahun between %(start)s and %(end)s)
    group by tahun
    order by tahun;
    ''', {'start': tglstart, 'end': tglend})
    figTTGUMhs = px.line(dfTTGUMhs, x=dfTTGUMhs['Tahun'], y=dfTTGUMhs['Jumlah Judul'])
    figTTGUMhs.update_traces(mode='lines+markers')
    return figTTGUMhs


@app.callback(
    Output('grf_hkiMhs', 'figure'),
    Input('fltrHKIMhsStart', 'value'),
    Input('fltrHKIMhsEnd', 'value')
)
def graphHKIMhs(tglstart, tglend):
    dfHKIMhs = data.getDataFrameFromDBwithParams('''
    select tahun 'Tahun', count(distinct fll.id_luaran_lainnya) 'Jumlah HKI'
    from br_ll_mahasiswa blm
             inner join fact_luaran_lainnya fll on blm.id_luaran_lainnya = fll.id_luaran_lainnya
             inner join dim_luaran_lainnya dll on blm.id_luaran_lainnya = dll.id_luaran_lainnya
             inner join dim_date dd on dd.id_date = fll.id_tanggal_luaran
             inner join dim_penelitian_pkm dpp on dll.id_penelitian_pkm = dpp.id_penelitian_pkm
    where no_haki is not null
      and jenis='PENELITIAN'
      and (tahun between %(start)s and %(end)s)
    group by tahun
    order by tahun;
    ''', {'start': tglstart, 'end': tglend})
    fig = px.line(dfHKIMhs, x=dfHKIMhs['Tahun'], y=dfHKIMhs['Jumlah HKI'])
    fig.update_traces(mode='lines+markers')
    return fig

#luaran pkm mahasiswa
@app.callback(
    Output('grf_pubPKMMhs', 'figure'),
    Input('fltrPubPKMMhsStart', 'value'),
    Input('fltrPubPKMMhsEnd', 'value')
)
def graphPubMhs(tglstart, tglend):
    dfPubMhs = data.getDataFrameFromDBwithParams('''
    select tahun_ajaran                    'Tahun Ajaran',
           count(distinct fp.id_publikasi) 'Jumlah Publikasi'
    from br_pub_mahasiswa bpm
             inner join dim_publikasi dp on bpm.id_publikasi = dp.id_penelitian_pkm
             inner join fact_publikasi fp on bpm.id_publikasi = fp.id_penelitian_pkm
             inner join dim_date dd on fp.id_tanggal_publikasi = dd.id_date
             inner join dim_semester ds on ds.kode_semester = concat(tahun, if(bulan >= 7, 2, 1))
             inner join dim_penelitian_pkm dpp on dp.id_penelitian_pkm = dpp.id_penelitian_pkm
    where fp.is_deleted != 1
        and jenis='PKM'
       and (tahun_ajaran between %(start)s and %(end)s)
    group by tahun_ajaran
    order by tahun_ajaran;
    ''', {'start': tglstart, 'end': tglend})
    figPubMhs = px.line(dfPubMhs, x=dfPubMhs['Tahun Ajaran'], y=dfPubMhs['Jumlah Publikasi'])
    figPubMhs.update_traces(mode='lines+markers')
    return figPubMhs


@app.callback(
    Output('grf_ttguPKMMhs', 'figure'),
    Input('fltrTTGUPKMMhsStart', 'value'),
    Input('fltrTTGUPKMMhsEnd', 'value')
)
def graphPPMhs(tglstart, tglend):
    dfTTGUMhs = data.getDataFrameFromDBwithParams('''
    select tahun                                 'Tahun',
           count(distinct dll.id_penelitian_pkm) 'Jumlah Judul'
    from dim_luaran_lainnya dll
             inner join fact_luaran_lainnya fll on dll.id_penelitian_pkm = fll.id_penelitian_pkm
             inner join dim_jenis_luaran djl on dll.id_jenis_luaran = djl.id_jenis_luaran
             inner join br_ll_mahasiswa blm on dll.id_luaran_lainnya = blm.id_luaran_lainnya
             inner join dim_date dd on dd.id_date = dll.id_tanggal_luaran
             inner join dim_penelitian_pkm dpp on dll.id_penelitian_pkm = dpp.id_penelitian_pkm
    where keterangan_jenis_luaran = 'TEKNOLOGI TEPAT GUNA'
        and jenis='PKM'
      and (tahun between %(start)s and %(end)s)
    group by tahun
    order by tahun;
    ''', {'start': tglstart, 'end': tglend})
    figTTGUMhs = px.line(dfTTGUMhs, x=dfTTGUMhs['Tahun'], y=dfTTGUMhs['Jumlah Judul'])
    figTTGUMhs.update_traces(mode='lines+markers')
    return figTTGUMhs


@app.callback(
    Output('grf_hkiPKMMhs', 'figure'),
    Input('fltrHKIPKMMhsStart', 'value'),
    Input('fltrHKIPKMMhsEnd', 'value')
)
def graphHKIMhs(tglstart, tglend):
    dfHKIMhs = data.getDataFrameFromDBwithParams(f'''
    select tahun 'Tahun', count(distinct fll.id_luaran_lainnya) 'Jumlah Judul'
    from br_ll_mahasiswa blm
             inner join fact_luaran_lainnya fll on blm.id_luaran_lainnya = fll.id_luaran_lainnya
             inner join dim_luaran_lainnya dll on blm.id_luaran_lainnya = dll.id_luaran_lainnya
             inner join dim_date dd on dd.id_date = fll.id_tanggal_luaran
             inner join dim_penelitian_pkm dpp on dll.id_penelitian_pkm = dpp.id_penelitian_pkm
    where no_haki is not null
      and jenis='PKM'
      and (tahun between %(start)s and %(end)s)
    group by tahun
    order by tahun;
    ''', {'start': tglstart, 'end': tglend})
    fig = px.line(dfHKIMhs, x=dfHKIMhs['Tahun'], y=dfHKIMhs['Jumlah Judul'])
    fig.update_traces(mode='lines+markers')
    return fig

@app.callback(
    Output('grf_reTelitiDosen', 'figure'),
    Input('fltrPenRerataStart', 'value'),
    Input('fltrPenRerataEnd', 'value')
)
def graphRerata(tglstart, tglend):
    dfPenDs = data.getDataFrameFromDBwithParams('''
    select pp.tahun Tahun, pp.jumlah 'Jumlah Judul', dosen.jumlah 'Jumlah Dosen', round(pp.jumlah/dosen.jumlah) Rerata
    from (select dd.tahun tahun, count(bpd.id_penelitian_pkm) jumlah
          from br_pp_dosen bpd
                   inner join dim_penelitian_pkm dpp on bpd.id_penelitian_pkm = dpp.id_penelitian_pkm
                   inner join dim_date dd on dpp.id_tanggal_selesai = dd.id_date
          where bpd.jenis = 'Penelitian'
          group by dd.tahun) pp,
         (select dd.tahun tahun, count(distinct bpd.id_dosen) jumlah
          from br_pp_dosen bpd
                inner join dim_penelitian_pkm dpp on bpd.id_penelitian_pkm = dpp.id_penelitian_pkm
                inner join dim_date dd on dpp.id_tanggal_selesai = dd.id_date
                inner join dim_dosen dd2 on bpd.id_dosen=dd2.id_dosen
          where bpd.jenis = 'Penelitian'
          group by dd.tahun)dosen
    where pp.tahun=dosen.tahun and (pp.tahun between %(Start)s and %(End)s)
    group by pp.tahun, pp.jumlah, dosen.jumlah, `Rerata`
    order by pp.tahun;''', {'Start': tglstart, 'End': tglend})
    figPenDs = px.line(dfPenDs, x=dfPenDs['Tahun'], y=dfPenDs['Rerata'], color=px.Constant('Penelitian /Dosen'),
                       labels=dict(x='Tahun', y='Rerata', color='Keterangan'))
    figPenDs.update_traces(mode='lines+markers')
    figPenDs.add_bar(x=dfPenDs['Tahun'], y=dfPenDs['Jumlah Judul'], name='Penelitian')
    return figPenDs

@app.callback(
    Output('grf_rePubDosen', 'figure'),
    Input('fltrPKMRerataStart', 'value'),
    Input('fltrPKMRerataEnd', 'value')
)
def graphRerata(tglstart, tglend):
    dfPubDs = data.getDataFrameFromDBwithParams('''
    select dd.tahun Tahun, count(distinct dp.id_publikasi) 'Jumlah Judul'
    from br_pp_publikasi bpp
             inner join dim_publikasi dp on bpp.id_penelitian_pkm = dp.id_penelitian_pkm
             inner join dim_date dd on dp.tahun_publikasi = dd.tahun
    where dd.tahun and (dd.tahun between %(Start)s and %(End)s)
    group by dd.tahun''', {'Start': tglstart, 'End': tglend})
    figPubDs = px.bar(dfPubDs, x=dfPubDs['Tahun'], y=dfPubDs['Jumlah Judul'],
                       labels=dict(x='Tahun', y='Jumlah Judul', color='Keterangan'))
    figPubDs.update_yaxes(categoryorder='category descending')
    figPubDs.update_layout(barmode='group')
    return figPubDs


# CALLBACK
@app.callback(Output("loading-output-1", "children"), Input("loading-input-1", "value"))
def input_triggers_spinner(value):
    time.sleep(1)
    return value

@app.callback(
    Output('cll_PenSum', 'is_open'),
    Output('cll_PenSum', 'children'),
    Input('cll_grfpenSum', 'n_clicks'),
    [State('cll_PenSum', 'is_open')]
)
def toggle_collapse(pensum, is_open):
    dfpen = data.getDataFrameFromDB('''
                        select tahun Tahun, count(*) 'Jumlah Penelitian'
                        from fact_penelitian fact
                                 inner join dim_penelitian_pkm dim on dim.id_penelitian_pkm = fact.id_penelitian
                                 inner join br_pp_dosen on fact.id_penelitian = br_pp_dosen.id_penelitian_pkm
                                 inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen and id_prodi = 9
                                 inner join dim_date on dim_date.id_date = dim.id_tanggal_mulai
                        where dim.jenis = 'PENELITIAN'
                          and tahun>year(now())-5
                        group by tahun
                        order by tahun desc''')
    dfpub = data.getDataFrameFromDB('''
                        select tahun_publikasi as Tahun, count(*) 'Jumlah Publikasi'
                        from fact_publikasi fact
                        inner join dim_publikasi dimpub on fact.id_publikasi = dimpub.id_publikasi
                        inner join br_pub_dosen brpub on fact.id_publikasi = brpub.id_publikasi
                        inner join dim_dosen dimdos on brpub.id_dosen = dimdos.id_dosen and id_prodi = 9
                        inner join dim_penelitian_pkm dpp on dimpub.id_penelitian_pkm = dpp.id_penelitian_pkm
                        inner join br_pp_publikasi bpp on brpub.id_publikasi = bpp.id_publikasi
                        where dpp.jenis='PENELITIAN'
                            and tahun_publikasi>year(now())-5
                        group by tahun_publikasi
                        order by tahun_publikasi desc''')
    dfluaran = data.getDataFrameFromDB('''
                        select tahun Tahun, count(*) 'Jumlah Luaran Lainnya'
                        from fact_luaran_lainnya fatl
                        inner join dim_luaran_lainnya diml on fatl.id_luaran_lainnya = diml.id_luaran_lainnya
                        inner join br_pp_luaranlainnya brl on fatl.id_luaran_lainnya = brl.id_luaranlainnya
                        inner join br_pp_dosen brpp on brpp.id_penelitian_pkm = brl.id_penelitian_pkm
                        inner join dim_dosen on brpp.id_Dosen = dim_dosen.id_dosen and id_prodi = 9
                        inner join dim_date on dim_date.id_date = diml.id_tanggal_luaran
                        where brl.jenis='PENELITIAN'
                            and tahun>year(now())-5
                        group by tahun
                        order by tahun desc''')
    df = dfpen.merge(dfpub,how='inner').merge(dfluaran,how='inner')
    isiPenDosen = dbc.Card(
        dt.DataTable(
            id='tbl_penSum',
            columns=[
                {'name': i, 'id': i} for i in df.columns
            ],
            data=df.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    if pensum:
        return not is_open, isiPenDosen
    return is_open, None

@app.callback(
    Output('cll_PKMSum', 'is_open'),
    Output('cll_PKMSum', 'children'),
    Input('cll_grfpkmSum', 'n_clicks'),
    [State('cll_PKMSum', 'is_open')]
)
def toggle_collapse(pkmsum, is_open):
    dfpkm = data.getDataFrameFromDB('''
                        select tahun Tahun, count(*) 'Jumlah PKM'
                        from fact_pkm fact
                                 inner join dim_penelitian_pkm dim on dim.id_penelitian_pkm = fact.id_pkm
                                 inner join br_pp_dosen on fact.id_pkm = br_pp_dosen.id_penelitian_pkm
                                 inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen and id_prodi = 9
                                 inner join dim_date on dim_date.id_date = dim.id_tanggal_mulai
                        where dim.jenis = 'PKM'
                          and tahun>year(now())-5
                        group by tahun
                        order by tahun
                        ''')
    dfpub = data.getDataFrameFromDB('''
                        select tahun_publikasi as Tahun, count(*) 'Jumlah Publikasi'
                        from fact_publikasi fact
                                 inner join dim_publikasi dimpub on fact.id_publikasi = dimpub.id_publikasi
                                 inner join br_pub_dosen brpub on fact.id_publikasi = brpub.id_publikasi
                                 inner join dim_dosen dimdos on brpub.id_dosen = dimdos.id_dosen and id_prodi = 9
                                 inner join dim_penelitian_pkm dpp on dimpub.id_penelitian_pkm = dpp.id_penelitian_pkm
                                 inner join br_pp_publikasi bpp on brpub.id_publikasi = bpp.id_publikasi
                        where dpp.jenis = 'PKM'
                          and tahun_publikasi>year(now())-5
                        group by tahun_publikasi
                        order by tahun_publikasi
                    ''')
    dfluaran = data.getDataFrameFromDB('''
                        select tahun Tahun, count(*) 'Jumlah Luaran Lainnya'
                        from fact_luaran_lainnya fatl
                                 inner join dim_luaran_lainnya diml on fatl.id_luaran_lainnya = diml.id_luaran_lainnya
                                 inner join br_pp_luaranlainnya brl on fatl.id_luaran_lainnya = brl.id_luaranlainnya
                                 inner join br_pp_dosen brpp on brpp.id_penelitian_pkm = brl.id_penelitian_pkm
                                 inner join dim_dosen on brpp.id_Dosen = dim_dosen.id_dosen and id_prodi = 9
                                 inner join dim_date on dim_date.id_date = diml.id_tanggal_luaran
                        where brl.jenis='PKM'
                          and tahun>year(now())-5
                        group by tahun
                        order by tahun
                    ''')
    df = dfpkm.merge(dfpub, how='left').merge(dfluaran,how='left')
    isiPKMDosen = dbc.Card(
        dt.DataTable(
            id='tbl_pkmSum',
            columns=[
                {'name': i, 'id': i} for i in df.columns
            ],
            data=df.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    if pkmsum:
        return not is_open, isiPKMDosen
    return is_open, None

@app.callback(
    Output('cll_PenDs', 'is_open'),
    Output('cll_PenDs', 'children'),
    Input('cll_grfpenDs', 'n_clicks'),
    [State('cll_PenDs', 'is_open')]
)
def toggle_collapse(pends, is_open):
    isiPenDosen = dbc.Card(
        dt.DataTable(
            id='tbl_pppDs',
            columns=[
                {'name': i, 'id': i} for i in dfjmlppp.columns
            ],
            data=dfjmlppp.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    if pends:
        return not is_open, isiPenDosen
    return is_open, None

@app.callback(
    Output('cll_PKMDs', 'is_open'),
    Output('cll_PKMDs', 'children'),
    Input('cll_grfpkmDs', 'n_clicks'),
    [State('cll_PKMDs', 'is_open')]
)
def toggle_collapse(pkmds, is_open):
    isiPKMDosen = dbc.Card(
        dt.DataTable(
            id='tbl_pppDs',
            columns=[
                {'name': i, 'id': i} for i in dfjmlppp.columns
            ],
            data=dfjmlppp.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    if pkmds:
        return not is_open, isiPKMDosen
    return is_open, None


@app.callback(
    Output('cll_PPPDM', 'is_open'),
    Output('cll_PPPDM', 'children'),
    [Input('cll_grfpkmDM', 'n_clicks'),
     Input('cll_grftelitiDM', 'n_clicks'),
     Input('tab_pppDM', 'value')],
    [State('cll_PPPDM', 'is_open')]
)
def toggle_collapse(pkmds, dsmhs, ppp, is_open):
    isiPKMDosen = dbc.Card(
        dt.DataTable(
            id='tbl_pkmDosenMhs',
            columns=[
                {'name': i, 'id': i} for i in dfpkmmhs.columns
            ],
            data=dfpkmmhs.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    isiTelitiDosen = dbc.Card(
        dt.DataTable(
            id='tbl_telitiDosenMhs',
            # columns=[
            #     {'name': i, 'id': i} for i in dfpenelitianmhs.columns
            # ],
            # data=dfpenelitianmhs.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    if pkmds and ppp == 'pkmdosenmhs':
        return not is_open, isiPKMDosen
    if dsmhs and ppp == 'telitidosenmhs':
        return not is_open, isiTelitiDosen
    return is_open, None


@app.callback(
    Output('cll_Mitra', 'is_open'),
    Output('cll_Mitra', 'children'),
    [Input('cll_grfMitraTeliti', 'n_clicks'),
     Input('cll_grfMitraPKM', 'n_clicks'),
     Input('tab_Mitra', 'value')],
    [State('cll_Mitra', 'is_open')]
)
def toggle_collapse(mitrapen, mitrapkm, mitra, is_open):
    isiMitraTeliti = dbc.Card(
        dt.DataTable(
            id='tbl_kerjaTeliti',
            columns=[
                {'name': i, 'id': i} for i in tbl_kerjaPeneliti.columns
            ],
            data=tbl_kerjaPeneliti.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    isiMitraPKM = dbc.Card(
        dt.DataTable(
            id='tbl_kerjaPKM',
            columns=[
                {'name': i, 'id': i} for i in tbl_kerjaPKM.columns
            ],
            data=tbl_kerjaPKM.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    if mitrapen and mitra == 'kerjaTeliti':
        return not is_open, isiMitraTeliti
    if mitrapkm and mitra == 'kerjaPKM':
        return not is_open, isiMitraPKM
    return is_open, None

# @app.callback(
#     Output("cll_tblsitasi", "is_open"),
#     [Input("cll_grfsitasi", "n_clicks")],
#     [State("cll_tblsitasi", "is_open")])
# def toggle_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open

@app.callback(
    Output("cll_tblpenSitasi", "is_open"),
    [Input("grf_penSitasi", "n_clicks")],
    [State("cll_tblpenSitasi", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("cll_tblpkmSitasi", "is_open"),
    [Input("grf_penSitasi", "n_clicks")],
    [State("cll_tblpkmSitasi", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

#LuaranDosen
##TABEL INI
@app.callback(
    Output('cll_luaranPenDosen', 'is_open'),
    Output('cll_luaranPenDosen', 'children'),
    [Input('cll_grfhkiDs', 'n_clicks'),
     Input('cll_grfttguDs', 'n_clicks'),
     Input('cll_grfbukuDs', 'n_clicks'),
     Input('tab_luaranDosen', 'value')],
    [State('cll_luaranPenDosen', 'is_open')]
)
def toggle_collapse(nhkids, nttguds, nbukuds, luarands, is_open):
    isiHKIDosen = dbc.Card(
        dt.DataTable(
            id='tbl_HKIDosen',
            columns=[
                {'name': i, 'id': i} for i in dfluaranhkidosen.columns
            ],
            data=dfluaranhkidosen.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    isiTTGUDosen = dbc.Card(
        dt.DataTable(
            id='tbl_TTGUDosen',
            columns=[
                {'name': i, 'id': i} for i in dfluaranttgudosen.columns
            ],
            data=dfluaranttgudosen.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    isiBukuDosen = dbc.Card(
        dt.DataTable(
            id='tbl_BukuDosen',
            columns=[
                {'name': i, 'id': i} for i in dfluaranbukudosen.columns
            ],
            data=dfluaranbukudosen.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    if nhkids and luarands == 'HKIDosen':
        return not is_open, isiHKIDosen
    if nttguds and luarands == 'TTGUDosen':
        return not is_open, isiTTGUDosen
    if nbukuds and luarands == 'BukuDosen':
        return not is_open, isiBukuDosen
    return is_open, None


@app.callback(
    Output('cll_luaranPPPMhs', 'is_open'),
    Output('cll_luaranPPPMhs', 'children'),
    [Input('cll_grfpubMhs', 'n_clicks'),
     Input('cll_grfttguMhs', 'n_clicks'),
     Input('cll_grfhkiMhs', 'n_clicks'),
     Input('tab_luaranMhs', 'value')],
    [State('cll_luaranPPPMhs', 'is_open')]
)
def toggle_collapse(npub, nttgu, nhki, luaran, is_open):
    isiPublikasiMhs = dbc.Card(
        dt.DataTable(
            id='tbl_pubMhs',
            columns=[
                {'name': i, 'id': i} for i in dfpublikasimhs.columns
            ],
            data=dfpublikasimhs.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    isiTTGUMhs = dbc.Card(
        dt.DataTable(
            id='tbl_ttguMhs',
            columns=[
                {'name': i, 'id': i} for i in dfttguadopsimhs.columns
            ],
            data=dfttguadopsimhs.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    isiHKIMhs = dbc.Card(
        dt.DataTable(
            id='tbl_HKIMhs',
            columns=[
                {'name': i, 'id': i} for i in dfluaranhkimhs.columns
            ],
            data=dfluaranhkimhs.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    if npub and luaran == 'pubMhs':
        return not is_open, isiPublikasiMhs
    if nttgu and luaran == 'ttguMhs':
        return not is_open, isiTTGUMhs
    if nhki and luaran == 'hkiMhs':
        return not is_open, isiHKIMhs
    return is_open, None


@app.callback(
    Output('cll_rerataPPP', 'is_open'),
    Output('cll_rerataPPP', 'children'),
    [Input('cll_grfreTelitiDosen', 'n_clicks'),
     Input('cll_grfrePubDosen', 'n_clicks'),
     Input('tab_rerataPPP', 'value')],
    [State('cll_rerataPPP', 'is_open')])
def toggle_collapse(nneliti, npub, ppp, is_open):
    isiPenelitian = dbc.Card(
        dt.DataTable(
            id='tbl_reTelitiDosen',
            columns=[
                {'name': i, 'id': i} for i in dfratajumlpenelitiandosen.columns
            ],
            data=dfratajumlpenelitiandosen.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    ),
    isiPublikasi = dbc.Card(
        dt.DataTable(
            id='rePubDosen',
            columns=[
                {'name': i, 'id': i} for i in dfratajumlpublikasidosen.columns
            ],
            data=dfratajumlpublikasidosen.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    ),
    if nneliti and ppp == 'reTelitiDosen':
        return not is_open, isiPenelitian
    if npub and ppp == 'rePubDosen':
        return not is_open, isiPublikasi
    return is_open, None

# GRAPH CALLBACK
@app.callback(
    Output('grf_penSitasi', 'figure'),
    Input('fltrPenSitasiStart', 'value'),
    Input('fltrPenSitasiEnd', 'value'),
    Input('radioPenSitasi', 'value')
)
def graphPenSitasi(valueFrom, valueTo, radioValue):
    if radioValue == 'tahun':
        dfperth = data.getDataFrameFromDBwithParams(f'''
            select tahun_sitasi                'Tahun Sitasi',
                   sum(distinct jumlah_sitasi) 'Jumlah Sitasi'
            from fact_publikasi_sitasi fps
                inner join dim_publikasi dp on fps.id_publikasi = dp.id_publikasi
                inner join dim_penelitian_pkm dpp on dp.id_penelitian_pkm = dpp.id_penelitian_pkm
            where jenis='PENELITIAN'
                  and tahun_sitasi between %(start)s and %(end)s
            group by tahun_sitasi
            order by tahun_sitasi;
        ''', {'start': valueFrom, 'end': valueTo})
        figperth = px.bar(dfperth, x=dfperth['Tahun Sitasi'], y=dfperth['Jumlah Sitasi'], color=dfperth['Tahun Sitasi'])
        return figperth
    elif radioValue == 'topdosen':
        dftopdosen = data.getDataFrameFromDBwithParams(f'''
        select sub.`Tahun Sitasi`, `Nama Dosen`, `Jumlah Sitasi`
        from (select tahun_sitasi                                                                 'Tahun Sitasi',
                     dd.nama                                                                      'Nama Dosen',
                     sum(jumlah_sitasi)                                                           'Jumlah Sitasi',
                     row_number() over (partition by tahun_sitasi order by jumlah_sitasi desc) as row
              from fact_publikasi_sitasi fps
                       inner join dim_publikasi dp on fps.id_publikasi = dp.id_publikasi
                       inner join dim_penelitian_pkm dpp on dp.id_penelitian_pkm = dpp.id_penelitian_pkm
                       inner join br_pub_dosen bpd on dp.id_publikasi = bpd.id_publikasi
                       inner join dim_dosen dd on bpd.id_dosen = dd.id_dosen
              where dd.id_prodi = 9
                    and jenis='PENELITIAN'
                    and tahun_sitasi between %(start)s and %(end)s
              group by dd.nama, tahun_sitasi) sub
        where row <= 1
        order by `Tahun Sitasi`;
        ''', {'start': valueFrom, 'end': valueTo})
        figtopds = px.bar(dftopdosen, x=dftopdosen['Tahun Sitasi'], y=dftopdosen['Jumlah Sitasi'], color=dftopdosen['Nama Dosen'])
        return figtopds

@app.callback(
    Output('grf_pkmSitasi', 'figure'),
    Input('fltrPKMSitasiStart', 'value'),
    Input('fltrPKMSitasiEnd', 'value'),
    Input('radioPKMSitasi', 'value')
)
def graphPKMSitasi(valueFrom, valueTo, radioValue):
    if radioValue == 'tahun':
        dfperth = data.getDataFrameFromDBwithParams(f'''
            select tahun_sitasi                'Tahun Sitasi',
                   sum(distinct jumlah_sitasi) 'Jumlah Sitasi'
            from fact_publikasi_sitasi fps
                inner join dim_publikasi dp on fps.id_publikasi = dp.id_publikasi
                inner join dim_penelitian_pkm dpp on dp.id_penelitian_pkm = dpp.id_penelitian_pkm
            where jenis='PKM'
                  and tahun_sitasi between %(start)s and %(end)s
            group by tahun_sitasi
            order by tahun_sitasi;
        ''', {'start': valueFrom, 'end': valueTo})
        figperth = px.bar(dfperth, x=dfperth['Tahun Sitasi'], y=dfperth['Jumlah Sitasi'], color=dfperth['Tahun Sitasi'])
        return figperth
    elif radioValue == 'topdosen':
        dftopdosen = data.getDataFrameFromDBwithParams(f'''
        select sub.`Tahun Sitasi`, `Nama Dosen`, `Jumlah Sitasi`
        from (select tahun_sitasi                                                                 'Tahun Sitasi',
                     dd.nama                                                                      'Nama Dosen',
                     sum(jumlah_sitasi)                                                           'Jumlah Sitasi',
                     row_number() over (partition by tahun_sitasi order by jumlah_sitasi desc) as row
              from fact_publikasi_sitasi fps
                       inner join dim_publikasi dp on fps.id_publikasi = dp.id_publikasi
                       inner join dim_penelitian_pkm dpp on dp.id_penelitian_pkm = dpp.id_penelitian_pkm
                       inner join br_pub_dosen bpd on dp.id_publikasi = bpd.id_publikasi
                       inner join dim_dosen dd on bpd.id_dosen = dd.id_dosen
              where dd.id_prodi = 9
                    and jenis='PKM'
                    and tahun_sitasi between %(start)s and %(end)s
              group by dd.nama, tahun_sitasi) sub
        where row <= 1
        order by `Tahun Sitasi`;
        ''', {'start': valueFrom, 'end': valueTo})
        figtopds = px.bar(dftopdosen, x=dftopdosen['Tahun Sitasi'], y=dftopdosen['Jumlah Sitasi'], color=dftopdosen['Nama Dosen'])
        return figtopds

#luaran penelitian
@app.callback(
    Output('grf_hkiDs', 'figure'),
    Input('fltrLuaranStart', 'value'),
    Input('fltrLuaranEnd', 'value'),
    Input('fltrHKIDsNama', 'value')
)
def grafPubPenDs(start, end, namads):
    dfhki = data.getDataFrameFromDBwithParams(f'''
    select  tahun Tahun, nama 'Nama Dosen',
            count(dpp.id_penelitian_pkm) 'Jumlah HKI' 
    from dim_penelitian_pkm dpp
    inner join br_pp_luaranlainnya bpl on dpp.id_penelitian_pkm = bpl.id_penelitian_pkm
    inner join br_pp_dosen bpd on bpl.id_penelitian_pkm = bpd.id_penelitian_pkm
    inner join dim_dosen dd on bpd.id_dosen = dd.id_dosen
    INNER JOIN dim_date dt on dpp.id_tanggal_selesai = dt.id_date
    where jenis_luaran like 'HAK ATAS KEKAYAAN INTELEKTUAL' 
        and nama like %(nama)s
        and tahun between %(start)s and %(end)s
    group by tahun, nama,jenis_luaran
    order by tahun
    ''',{'start':start, 'end':end, 'nama':namads})
    dfttgu = data.getDataFrameFromDBwithParams(f'''
        select  tahun 'Tahun', 
                nama 'Nama Dosen',
                count(dpp.id_penelitian_pkm) 'Jumlah TTGU' 
        from dim_penelitian_pkm dpp
        inner join br_pp_luaranlainnya bpl on dpp.id_penelitian_pkm = bpl.id_penelitian_pkm
        inner join br_pp_dosen bpd on bpl.id_penelitian_pkm = bpd.id_penelitian_pkm
        inner join dim_dosen dd on bpd.id_dosen = dd.id_dosen
        INNER JOIN dim_date dt on dpp.id_tanggal_selesai = dt.id_date
        where jenis_luaran like 'TEKNOLOGI TEPAT GUNA' 
            and nama like %(nama)s
            and tahun between %(start)s and %(end)s
        group by tahun, nama,jenis_luaran
        order by tahun
        ''', {'start': start, 'end': end, 'nama': namads})
    dfbuku = data.getDataFrameFromDBwithParams(f'''
        select  tahun Tahun, 
                nama 'Nama Dosen',
                count(dpp.id_penelitian_pkm) 'Jumlah Buku'
        from dim_penelitian_pkm dpp
        inner join br_pp_luaranlainnya bpl on dpp.id_penelitian_pkm = bpl.id_penelitian_pkm
        inner join br_pp_dosen bpd on bpl.id_penelitian_pkm = bpd.id_penelitian_pkm
        inner join dim_dosen dd on bpd.id_dosen = dd.id_dosen
        INNER JOIN dim_date dt on dpp.id_tanggal_selesai = dt.id_date
        where not(jenis_luaran like 'HAK ATAS KEKAYAAN INTELEKTUAL' or jenis_luaran like 'TEKNOLOGI TEPAT GUNA') 
            and nama like %(nama)s
            and tahun between %(start)s and %(end)s
        group by tahun, nama, jenis_luaran
        order by tahun
        ''', {'start': start, 'end': end, 'nama': namads})
    fig = px.bar(dfhki, x=dfhki['Tahun'], y=dfhki['Jumlah HKI'],color=px.Constant('Hak Kekayaan Intelektual'),
                      labels=dict(x='Tahun', y='Jumlah HKI', color='Keterangan'))
    fig.add_bar(x=dfttgu['Tahun'], y=dfttgu['Jumlah TTGU'],name='Teknologi Tepat Guna')
    fig.add_bar(x=dfbuku['Tahun'], y=dfbuku['Jumlah Buku'],name='Buku')
    fig.update_traces(hovertemplate='Tahun : %{x}<br>Jumlah : %{value}')
    return fig

#luaran PKM
@app.callback(
    Output('grf_hkiPKMDs', 'figure'),
    Input('fltrLuaranPKMStart', 'value'),
    Input('fltrLuaranPKMEnd', 'value'),
    Input('fltrHKIPKMDsNama', 'value')
)
def grafPubPKMDs(start, end, namads):
    dfhki = data.getDataFrameFromDBwithParams(f'''
    select tahun                        Tahun,
           nama                         'Nama Dosen',
           count(dpp.id_penelitian_pkm) 'Jumlah HKI'
    from dim_penelitian_pkm dpp
             inner join br_pp_luaranlainnya bpl on dpp.id_penelitian_pkm = bpl.id_penelitian_pkm
             inner join br_pp_dosen bpd on bpl.id_penelitian_pkm = bpd.id_penelitian_pkm
             inner join dim_dosen dd on bpd.id_dosen = dd.id_dosen
             INNER JOIN dim_date dt on dpp.id_tanggal_selesai = dt.id_date
    where jenis_luaran like 'HAK ATAS KEKAYAAN INTELEKTUAL' and dpp.jenis='PKM'
       and nama like %(nama)s
       and tahun between %(start)s and %(end)s
    group by tahun, nama, jenis_luaran
    order by tahun
    ''',{'start':start, 'end':end, 'nama':namads})
    dfttgu = data.getDataFrameFromDBwithParams(f'''
        select tahun                        'Tahun',
               nama                         'Nama Dosen',
               count(dpp.id_penelitian_pkm) 'Jumlah TTGU'
        from dim_penelitian_pkm dpp
                 inner join br_pp_luaranlainnya bpl on dpp.id_penelitian_pkm = bpl.id_penelitian_pkm
                 inner join br_pp_dosen bpd on bpl.id_penelitian_pkm = bpd.id_penelitian_pkm
                 inner join dim_dosen dd on bpd.id_dosen = dd.id_dosen
                 INNER JOIN dim_date dt on dpp.id_tanggal_selesai = dt.id_date
        where jenis_luaran like 'TEKNOLOGI TEPAT GUNA' and dpp.jenis='PKM'
          and nama like %(nama)s
                and tahun between %(start)s and %(end)s
        group by tahun, nama, jenis_luaran
        order by tahun
        ''', {'start': start, 'end': end, 'nama': namads})
    dfbuku = data.getDataFrameFromDBwithParams(f'''
        select tahun                        Tahun,
               nama                         'Nama Dosen',
               count(dpp.id_penelitian_pkm) 'Jumlah Buku'
        from dim_penelitian_pkm dpp
                 inner join br_pp_luaranlainnya bpl on dpp.id_penelitian_pkm = bpl.id_penelitian_pkm
                 inner join br_pp_dosen bpd on bpl.id_penelitian_pkm = bpd.id_penelitian_pkm
                 inner join dim_dosen dd on bpd.id_dosen = dd.id_dosen
                 INNER JOIN dim_date dt on dpp.id_tanggal_selesai = dt.id_date
        where not (jenis_luaran like 'HAK ATAS KEKAYAAN INTELEKTUAL' or jenis_luaran like 'TEKNOLOGI TEPAT GUNA')
            and dpp.jenis='PKM'
            and nama like %(nama)s
            and tahun between %(start)s and %(end)s
        group by tahun, nama, jenis_luaran
        order by tahun
        ''', {'start': start, 'end': end, 'nama': namads})
    fig = px.bar(dfhki, x=dfhki['Tahun'], y=dfhki['Jumlah HKI'],color=px.Constant('Hak Kekayaan Intelektual'),
                      labels=dict(x='Tahun', y='Jumlah HKI', color='Keterangan'))
    fig.add_bar(x=dfttgu['Tahun'], y=dfttgu['Jumlah TTGU'],name='Teknologi Tepat Guna')
    fig.add_bar(x=dfbuku['Tahun'], y=dfbuku['Jumlah Buku'],name='Buku')
    fig.update_traces(hovertemplate='Tahun : %{x}<br>Jumlah : %{value}')
    return fig

#penelitian dana
@app.callback(
    Output('grf_penDana', 'figure'),
    Input('fltrPenDanaStart', 'value'),
    Input('fltrPenDanaEnd', 'value'),
    Input('radio_penDana', 'value')
)
def MitraPen(start, end, radiopendana):
    if radiopendana == 'wilayah':
        dfwil = data.getDataFrameFromDBwithParams(f'''
        select Tahun,
               dim_penelitian_pkm.wilayah_nama "Nama Wilayah",
               count(*) 'Jumlah Penelitian'
        from fact_penelitian fact
            inner join dim_penelitian_pkm on fact.id_penelitian = dim_penelitian_pkm.id_penelitian_pkm
            inner join br_pp_dana on dim_penelitian_pkm.id_penelitian_pkm = br_pp_dana.id_penelitian_pkm
            inner join dim_sumber_dana on br_pp_dana.id_sumber_dana = dim_sumber_dana.id_sumber_dana
            inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
        where tahun between %(start)s and %(end)s
        group by `Nama Wilayah`,tahun
        order by tahun
        ''',{'start':start,'end':end})
        figwil = px.bar(dfwil, x=dfwil['Tahun'], y=dfwil['Jumlah Penelitian'], color=dfwil['Nama Wilayah'])
        figwil.update_layout(yaxis_title='Jumlah Penelitian', xaxis_title='Tahun, Nama Wilayah',
                                legend_title='Nama Wilayah')
        return figwil
    elif radiopendana == 'sumber':
        dfsumber = data.getDataFrameFromDBwithParams(f'''
        select Tahun,
               dim_sumber_dana.jenis_sumber_dana "Sumber Dana",
               count(*) 'Jumlah Penelitian'
        from fact_penelitian fact
            inner join dim_penelitian_pkm on fact.id_penelitian = dim_penelitian_pkm.id_penelitian_pkm
            inner join br_pp_dana on dim_penelitian_pkm.id_penelitian_pkm = br_pp_dana.id_penelitian_pkm
            inner join dim_sumber_dana on br_pp_dana.id_sumber_dana = dim_sumber_dana.id_sumber_dana
            inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
        where tahun between %(start)s and %(end)s
        group by `Sumber Dana`,tahun
        order by tahun
        ''',{'start':start, 'end':end})
        figsumber = px.bar(dfsumber, x=dfsumber['Tahun'], y=dfsumber['Jumlah Penelitian'], color=dfsumber['Sumber Dana'])
        figsumber.update_layout(yaxis_title='Jumlah Penelitian', xaxis_title='Tahun, Sumber Dana',
                                legend_title='Sumber Dana')
        return figsumber
    elif radiopendana == 'asal':
        dfasal = data.getDataFrameFromDBwithParams(f'''
        select Tahun,
               dim_sumber_dana.status "Asal Sumber Dana",
               count(*) 'Jumlah Penelitan'
        from fact_penelitian fact
            inner join dim_penelitian_pkm on fact.id_penelitian = dim_penelitian_pkm.id_penelitian_pkm
            inner join br_pp_dana on dim_penelitian_pkm.id_penelitian_pkm = br_pp_dana.id_penelitian_pkm
            inner join dim_sumber_dana on br_pp_dana.id_sumber_dana = dim_sumber_dana.id_sumber_dana
            inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
        where tahun between %(start)s and %(end)s
        group by `Asal Sumber Dana`,tahun
        order by tahun
        ''',{'start':start, 'end':end})
        figasal = px.bar(dfasal, x=dfasal['Tahun'], y=dfasal['Jumlah Penelitian'], color=dfasal['Asal Sumber Dana'])
        figasal.update_layout(yaxis_title='Jumlah Penelitian', xaxis_title='Tahun, Asal Sumber Dana',
                              legend_title='Asal Sumber Dana')
        return figasal

@app.callback(
    Output('grf_pkmDana', 'figure'),
    Input('fltrPKMDanaStart', 'value'),
    Input('fltrPKMDanaEnd', 'value'),
    Input('radio_pkmDana', 'value')
)
def MitraPen(start, end, radiopkmdana):
    if radiopkmdana == 'wilayah':
        dfwil = data.getDataFrameFromDBwithParams(f'''
        select Tahun,
               dim_penelitian_pkm.wilayah_nama "Nama Wilayah",
               count(*) 'Jumlah PKM'
        from fact_pkm fact
        inner join dim_penelitian_pkm on fact.id_pkm = dim_penelitian_pkm.id_penelitian_pkm
        inner join br_pp_dana on dim_penelitian_pkm.id_penelitian_pkm = br_pp_dana.id_penelitian_pkm
        inner join dim_sumber_dana on br_pp_dana.id_sumber_dana = dim_sumber_dana.id_sumber_dana
        inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
        group by Tahun, `Nama Wilayah`
        order by tahun
        ''',{'start':start,'end':end})
        figwil = px.bar(dfwil, x=dfwil['Tahun'], y=dfwil['Jumlah PKM'], color=dfwil['Nama Wilayah'])
        figwil.update_layout(yaxis_title='Jumlah PKM', xaxis_title='Tahun, Nama Wilayah',
                                legend_title='Nama Wilayah')
        return figwil
    elif radiopkmdana == 'sumber':
        dfsumber = data.getDataFrameFromDBwithParams(f'''
        select Tahun,
               dim_sumber_dana.jenis_sumber_dana "Sumber Dana",
               count(*) 'Jumlah PKM'
        from fact_pkm fact
        inner join dim_penelitian_pkm on fact.id_pkm = dim_penelitian_pkm.id_penelitian_pkm
        inner join br_pp_dana on dim_penelitian_pkm.id_penelitian_pkm = br_pp_dana.id_penelitian_pkm
        inner join dim_sumber_dana on br_pp_dana.id_sumber_dana = dim_sumber_dana.id_sumber_dana
        inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
        group by Tahun, `Sumber Dana`
        order by tahun
        ''',{'start':start, 'end':end})
        figsumber = px.bar(dfsumber, x=dfsumber['Tahun'], y=dfsumber['Jumlah PKM'], color=dfsumber['Sumber Dana'])
        figsumber.update_layout(yaxis_title='Jumlah PKM', xaxis_title='Tahun, Sumber Dana',
                                legend_title='Sumber Dana')
        return figsumber
    elif radiopkmdana == 'asal':
        dfasal = data.getDataFrameFromDBwithParams(f'''
        select Tahun,
               dim_sumber_dana.status "Asal Sumber Dana",
               count(*) 'Jumlah PKM'
        from fact_pkm fact
        inner join dim_penelitian_pkm on fact.id_pkm = dim_penelitian_pkm.id_penelitian_pkm
        inner join br_pp_dana on dim_penelitian_pkm.id_penelitian_pkm = br_pp_dana.id_penelitian_pkm
        inner join dim_sumber_dana on br_pp_dana.id_sumber_dana = dim_sumber_dana.id_sumber_dana
        inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
        group by Tahun, `Asal Sumber Dana`
        order by tahun
        ''',{'start':start, 'end':end})
        figasal = px.bar(dfasal, x=dfasal['Tahun'], y=dfasal['Jumlah PKM'], color=dfasal['Asal Sumber Dana'])
        figasal.update_layout(yaxis_title='Jumlah PKM', xaxis_title='Tahun, Asal Sumber Dana',
                              legend_title='Asal Sumber Dana')
        return figasal

@app.callback(
    Output('cll_rerataPen', 'is_open'),
    Output('cll_rerataPen', 'children'),
    Input('cll_grfreTelitiDosen', 'n_clicks'),
    [State('cll_rerataPen', 'is_open')]
)
def toggle_collapse(rtPen, is_open):
    df = data.getDataFrameFromDB('''
        select pp.tahun Tahun, pp.jumlah 'Jumlah Judul', dosen.jumlah 'Jumlah Dosen', round(pp.jumlah/dosen.jumlah) Rerata
        from (select dd.tahun tahun, count(bpd.id_penelitian_pkm) jumlah
              from br_pp_dosen bpd
                       inner join dim_penelitian_pkm dpp on bpd.id_penelitian_pkm = dpp.id_penelitian_pkm
                       inner join dim_date dd on dpp.id_tanggal_selesai = dd.id_date
              where bpd.jenis = 'Penelitian'
              group by dd.tahun) pp,
             (select dd.tahun tahun, count(distinct bpd.id_dosen) jumlah
              from br_pp_dosen bpd
                    inner join dim_penelitian_pkm dpp on bpd.id_penelitian_pkm = dpp.id_penelitian_pkm
                    inner join dim_date dd on dpp.id_tanggal_selesai = dd.id_date
                    inner join dim_dosen dd2 on bpd.id_dosen=dd2.id_dosen
              where bpd.jenis = 'Penelitian'
              group by dd.tahun)dosen
        where pp.tahun=dosen.tahun and (pp.tahun>year(now())-6)
        group by pp.tahun, pp.jumlah, dosen.jumlah, `Rerata`
        order by pp.tahun desc ;''')
    isi = dbc.Card(
        dt.DataTable(
            id='tbl_penDM',
            columns=[
                {'name': i, 'id': i} for i in df.columns
            ],
            data=df.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    if rtPen:
        return not is_open, isi
    return is_open, None

@app.callback(
    Output('cll_rerataPKM', 'is_open'),
    Output('cll_rerataPKM', 'children'),
    Input('cll_grfrePubDosen', 'n_clicks'),
    [State('cll_rerataPKM', 'is_open')]
)
def toggle_collapse(rtPKM, is_open):
    df = data.getDataFrameFromDB('''
    select dd.tahun Tahun, count(distinct dp.id_publikasi) 'Jumlah Judul'
    from br_pp_publikasi bpp
             inner join dim_publikasi dp on bpp.id_penelitian_pkm = dp.id_penelitian_pkm
             inner join dim_date dd on dp.tahun_publikasi = dd.tahun
    where dd.tahun and (dd.tahun>year(now())-6)
    group by dd.tahun''')
    isi = dbc.Card(
        dt.DataTable(
            id='tbl_penDM',
            columns=[
                {'name': i, 'id': i} for i in df.columns
            ],
            data=df.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    if rtPKM:
        return not is_open, isi
    return is_open, None

#sini
@app.callback(
    Output('cll_penDana', 'is_open'),
    Output('cll_penDana', 'children'),
    Input('cll_grfpenDana', 'n_clicks'),
    [State('cll_penDana', 'is_open')]
)
def toggle_collapse(penmitra, is_open):
    df = data.getDataFrameFromDB('''
    select Tahun,
           judul_penelitian as "Judul Penelitan",
           dim_penelitian_pkm.wilayah_nama "Nama Wilayah",
           dim_sumber_dana.jenis_sumber_dana "Sumber Dana",
           dim_sumber_dana.status "Asal Sumber Dana",
           br_pp_dana.besaran_dana "Jumlah Dana"
    from fact_penelitian fact
        inner join dim_penelitian_pkm on fact.id_penelitian = dim_penelitian_pkm.id_penelitian_pkm
        inner join br_pp_dana on dim_penelitian_pkm.id_penelitian_pkm = br_pp_dana.id_penelitian_pkm
        inner join dim_sumber_dana on br_pp_dana.id_sumber_dana = dim_sumber_dana.id_sumber_dana
        inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
    where tahun>=year(now())-5
    order by tahun, judul_penelitian''')
    isi = dbc.Card(
        dt.DataTable(
            id='tbl_penMitra',
            columns=[
                {'name': i, 'id': i} for i in df.columns
            ],
            data=df.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    if penmitra:
        return not is_open, isi
    return is_open, None

@app.callback(
    Output('cll_pkmDana', 'is_open'),
    Output('cll_pkmDana', 'children'),
    Input('cll_grfpkmDana', 'n_clicks'),
    [State('cll_pkmDana', 'is_open')]
)
def toggle_collapse(pkmdana, is_open):
    df = data.getDataFrameFromDB('''
    select Tahun,
           judul as "Judul Penelitan",
           dim_penelitian_pkm.wilayah_nama "Nama Wilayah",
           dim_sumber_dana.jenis_sumber_dana "Sumber Dana",
           dim_sumber_dana.status "Asal Sumber Dana",
           br_pp_dana.besaran_dana "Jumlah Dana"
    from fact_pkm fact
        inner join dim_penelitian_pkm on fact.id_pkm = dim_penelitian_pkm.id_penelitian_pkm
        inner join br_pp_dana on dim_penelitian_pkm.id_penelitian_pkm = br_pp_dana.id_penelitian_pkm
        inner join dim_sumber_dana on br_pp_dana.id_sumber_dana = dim_sumber_dana.id_sumber_dana
        inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
    where tahun>=year(now())-5
    order by tahun, judul''')
    isi = dbc.Card(
        dt.DataTable(
            id='tbl_pkmMitra',
            columns=[
                {'name': i, 'id': i} for i in df.columns
            ],
            data=df.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    if pkmdana:
        return not is_open, isi
    return is_open, None