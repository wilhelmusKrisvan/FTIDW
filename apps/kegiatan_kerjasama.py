import dash
import pandas as pd
import dash_table as dt
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from appConfig import app, server
import model.dao_kegiatankerjasama as data
import plotly.graph_objs as go

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

# Kegiatan Dosen
dfrekognisiDosen = data.getPrestasiRekognisiDosen()
dfkegiatandosen = data.getKegiatanDosen()
dfKegiatanKerjasama = data.getKegiatanKerjasama()
# Prestasi Mahasiswa
dfprestasiakademik = data.getPrestasiAkademik()
dfprestasinonakademik = data.getPrestasiNonAkademik()
# Kulum
dfKulum = data.getKegKulUmMOU()
dfTableKulum = data.getTableKegKulUmMOU()
dfJumlahMhsKuliahUmum = data.getRawJumlahMhsKuliahUmum()

dfrerataKulum = data.getRerataJumlPesertaKulUm()
dfRekognisiDosenGraf = data.getRekognisiDosen()

dfTahunRekognisiDosen = data.getListTahunKegRekognisiDosen()
listTahunRekognisiDosen = dfTahunRekognisiDosen['tahun']

dfTahunKegDosen = data.getListTahunKegDosen()
listTahunKegDosen = dfTahunKegDosen['tahun']

dfTahunPrestasiAkademik = data.getListTahunPrestasiAkademik()
listTahunPrestasiAkademik = dfTahunPrestasiAkademik['tahun']

dfTahunPrestasiNonAkademik = data.getListTahunPrestasiNonAkademik()
listTahunPrestasiNonAkademik = dfTahunPrestasiNonAkademik['tahun']

dfTahunKulumMOU = data.getListTahunKulumMOU()
listTahunKulumMOU = dfTahunKulumMOU['tahun']

dfTahunTipeKegiatan = data.getListTahunTipeKegiatan()
listTahunTipeKegiatan = dfTahunTipeKegiatan['Tahun']



# dfkerjasama = data.getKerjasama()
# dfkerjasamakegiatan = data.getKerjasamaKegiatan()
# dfkerjasamakp = data.getKerjasamaKP()
# dfkerjasamapp = data.getKerjasamaPP()

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

card_style = {
    'border': '1px solid #fafafa',
    'border-radius': '10px',
    'margin-top': '10px',
    'padding': '10px',
    'justify-content': 'center',
    'width': '100%',
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
}

button_style = {
    'width': '160px',
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


kegiatan_dosen = dbc.Container([
    dbc.Card([
        dcc.Tabs([
            dcc.Tab(label='Kegiatan Rekognisi Dosen', value='rekognisiDosen',
                    children=[
                        dbc.Container([
                            dbc.Card([
                                dbc.Row([
                                            dbc.Col([
                                                html.Br(),
                                                html.H6('Wilayah :'),
                                                dcc.Dropdown(
                                                    id='drpdwn_kegRekoginisiDosen',
                                                    options=[{'label': 'Regional', 'value': '1'},
                                                             {'label': 'Nasional', 'value': '2'},
                                                             {'label': 'Asean', 'value': '3'},
                                                             {'label': 'Internasional', 'value': '4'}
                                                             ],
                                                    value='2',
                                                    style={'color': 'black'},
                                                    clearable=False,
                                                ),
                                            ], ),
                                            dbc.Col([
                                                html.Br(),
                                                html.H6('Dari :'),
                                                dcc.Dropdown(
                                                    id='drpdwn_FromTahunkegRekoginisiDosen',
                                                    options=[{'label': i, 'value': i} for i in listTahunRekognisiDosen],
                                                    value='2015',
                                                    style={'color': 'black'},
                                                    clearable=False,
                                                ),
                                            ], ),
                                            dbc.Col([
                                                html.Br(),
                                                html.H6('Sampai :'),
                                                dcc.Dropdown(
                                                    id='drpdwn_ToTahunkegRekoginisiDosen',
                                                    options=[{'label': i, 'value': i} for i in listTahunRekognisiDosen],
                                                    value='2020',
                                                    style={'color': 'black'},
                                                    clearable=False,
                                                ),
                                            ], ),
                                        ]),
                                dbc.CardLink(
                                    dbc.CardBody([
                                        dcc.Loading(
                                            id='loading-1',
                                            type="default",
                                            children=dcc.Graph(id='grf_rekognisiDosen', )
                                        ),
                                        dbc.Button('Lihat Semua Data',
                                                   id='cll_grfrekognisidosen',
                                                   n_clicks=0,
                                                   style=button_style)
                                    ]),
                                    id='cll_grfrekognisidosen',
                                    n_clicks=0
                                ),
                            ], style=cardgrf_style),
                            dbc.Collapse(
                                dbc.Card(
                                    dt.DataTable(
                                        id='tbl_rekognisiDosen',
                                        columns=[
                                            {'name': i, 'id': i} for i in dfrekognisiDosen.columns
                                        ],
                                        data=dfrekognisiDosen.to_dict('records'),
                                        sort_action='native',
                                        sort_mode='multi',
                                        style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto',
                                                     'margin-top': '25px'},
                                        style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                                        style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                                        style_cell={'width': 95},
                                        page_size=10,
                                        export_format='xlsx'
                                    ),
                                ),
                                id='cll_tblrekognisidosen',
                                is_open=False
                            ),

                        ], style=cont_style),

                    ],
                    style=tab_style, selected_style=selected_style),

            dcc.Tab(label='Jumlah Kegiatan Dosen Tiap Tahun', value='kegDosen',
                    children=[
                        dbc.Container([
                            dbc.Col([
                                html.Br(),
                                html.H6('Tahun :'),
                                dcc.Dropdown(
                                    id='drpdwn_kegDosen',
                                    options=[{'label': i, 'value': i} for i in listTahunKegDosen],
                                    value='2020',
                                    style={'color': 'black'},
                                    clearable=False,
                                ),
                            ],),
                            dbc.CardLink([
                                dcc.Loading(
                                    id='loading-1',
                                    type="default",
                                    children=dcc.Graph(id='grf_kegDosen'),
                                ),
                                dbc.Button('Lihat Semua Data',
                                           id='cll_grfkegDosen',
                                           n_clicks=0,
                                           style=button_style)
                            ], id='cll_grfkegDosen',
                                n_clicks=0),
                            dbc.Collapse(
                                dbc.Card(
                                    dt.DataTable(
                                        id='tbl_kegiatanDosen',
                                        columns=[
                                            {'name': i, 'id': i} for i in dfkegiatandosen.columns
                                        ],
                                        data=dfkegiatandosen.to_dict('records'),
                                        sort_action='native',
                                        sort_mode='multi',
                                        style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto',
                                                     'margin-top': '25px'},
                                        style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                                        style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                                        style_cell={'width': 95},
                                        page_size=10,
                                        export_format='xlsx'
                                    ), style=cardtbl_style
                                ),style=cardgrf_style,
                                id='cll_tblkegiatandosen',
                                is_open=False
                            )
                        ]),
                    ],
                    style=tab_style, selected_style=selected_style),
        ], style=tabs_styles, id='tab_kegDosen', value='rekognisiDosen'),
    ], style=cardgrf_style),

], style=cont_style)

kegiatanMahasiswa = dbc.Container([
    dbc.Card([
        dcc.Tabs([
            dcc.Tab(label='Prestasi Akademik Mahasiswa', value='prestasiMhs',
                    children=[
                        dbc.Row([
                                        dbc.Col([
                                            html.Br(),
                                            html.H6('Wilayah :'),
                                            dcc.Dropdown(
                                                id='drpdwn_prestasiAkademikMahasiswa',
                                                options=[{'label': 'Lokal', 'value': 'LOKAL'},
                                                         {'label': 'Regional', 'value': 'REGIONAL'},
                                                         {'label': 'Nasional', 'value': 'NASIONAL'},
                                                         {'label': 'Internasional', 'value': 'INTERNASIONAL'}
                                                         ],
                                                value='LOKAL',
                                                style={'color': 'black'},
                                                clearable=False,
                                            ),
                                        ], ),
                                        dbc.Col([
                                            html.Br(),
                                            html.H6('Dari :'),
                                            dcc.Dropdown(
                                                id='drpdwn_FromPrestasiAkademikMahasiswa',
                                                options=[{'label': i, 'value': i} for i in listTahunPrestasiAkademik],
                                                value='2013',
                                                style={'color': 'black'},
                                                clearable=False,
                                            ),
                                        ], ),
                                        dbc.Col([
                                            html.Br(),
                                            html.H6('Sampai :'),
                                            dcc.Dropdown(
                                                id='drpdwn_ToPrestasiAkademikMahasiswa',
                                                options=[{'label': i, 'value': i} for i in listTahunPrestasiAkademik],
                                                value='2017',
                                                style={'color': 'black'},
                                                clearable=False,
                                            ),
                                        ], ),
                                    ]),
                        dbc.CardLink([
                            dcc.Graph(id='grf_prestasiakademik'),
                            dbc.Button('Lihat Semua Data',
                                       id='cll_grfprestasiakademik',
                                       n_clicks=0,
                                       style=button_style)
                        ], id='cll_grfprestasiakademik',
                            n_clicks=0
                        ),
                        dbc.Collapse(
                            dbc.Card(
                                dt.DataTable(
                                    id='tbl_prestasiMhs',
                                    columns=[
                                        {'name': i, 'id': i} for i in dfprestasiakademik.columns
                                    ],
                                    data=dfprestasiakademik.to_dict('records'),
                                    sort_action='native',
                                    sort_mode='multi',
                                    style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto',
                                                 'margin-top': '25px'},
                                    style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                                    style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                                    style_cell={'width': 95},
                                    page_size=10,
                                    export_format='xlsx'
                                )
                            ),
                            id='cll_tblprestasiakademikmhs',
                            is_open=False
                        ),
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Prestasi Non Akademik Mahasiswa', value='NonprestasiMhs',
                    children=[
                        dbc.Row([
                                dbc.Col([
                                    html.Br(),
                                    html.H6('Wilayah :'),
                                    dcc.Dropdown(
                                        id='drpdwn_prestasiNonAkademikMahasiswa',
                                        options=[{'label': 'Lokal', 'value': 'LOKAL'},
                                                 {'label': 'Regional', 'value': 'REGIONAL'},
                                                 {'label': 'Nasional', 'value': 'NASIONAL'},
                                                 {'label': 'Internasional', 'value': 'INTERNASIONAL'}
                                                 ],
                                        value='LOKAL',
                                        style={'color': 'black'},
                                        clearable=False,
                                    ),
                                ]),
                                dbc.Col([
                                    html.Br(),
                                    html.H6('Dari :'),
                                    dcc.Dropdown(
                                        id='drpdwn_FromPrestasiNonAkademikMahasiswa',
                                        options=[{'label': i, 'value': i} for i in listTahunPrestasiNonAkademik],
                                        value='2012',
                                        style={'color': 'black'},
                                        clearable=False,
                                    ),
                                ]),
                                dbc.Col([
                                    html.Br(),
                                    html.H6('Sampai :'),
                                    dcc.Dropdown(
                                        id='drpdwn_ToPrestasiNonAkademikMahasiswa',
                                        options=[{'label': i, 'value': i} for i in listTahunPrestasiNonAkademik],
                                        value='2018',
                                        style={'color': 'black'},
                                        clearable=False,
                                    ),
                                ]),
                            ]),
                        dbc.CardLink([
                            dcc.Graph(id='grf_prestasinonakademik'),
                            dbc.Button('Lihat Semua Data',
                                       id='cll_grfprestasinonakademik',
                                       n_clicks=0,
                                       style=button_style)
                        ],id='cll_grfprestasinonakademik',
                            n_clicks=0
                        ),
                        dbc.Collapse(
                            dbc.Card(
                                dt.DataTable(
                                    id='tbl_NonprestasiMhs',
                                    columns=[
                                        {'name': i, 'id': i} for i in dfprestasinonakademik.columns
                                    ],
                                    data=dfprestasinonakademik.to_dict('records'),
                                    sort_action='native',
                                    sort_mode='multi',
                                    style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto',
                                                 'margin-top': '25px'},
                                    style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                                    style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                                    style_cell={'width': 95},
                                    page_size=10,
                                    export_format='xlsx'
                                )
                            ),
                            id='cll_tblprestasinonakademikmhs',
                            is_open=False
                        ),
                    ],
                    style=tab_style, selected_style=selected_style),
        ], style=tabs_styles, value='prestasiMhs'),
    ], style=cardgrf_style)
], style=cont_style)

kerjasama = dbc.Container([
    dbc.Card([
        html.H5('Jumlah Kegiatan Berdasarkan Tipe Kerjasama',
                style=ttlgrf_style),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.H6('Dari :'),
                dcc.Dropdown(
                    id='drpdwn_FromTipeKegiatan',
                    options=[{'label': i, 'value': i} for i in listTahunTipeKegiatan],
                    value='2015',
                    style={'color': 'black'},
                    clearable=False,
                ),
            ], ),
            dbc.Col([
                html.Br(),
                html.H6('Sampai :'),
                dcc.Dropdown(
                    id='drpdwn_ToTipeKegiatan',
                    options=[{'label': i, 'value': i} for i in listTahunTipeKegiatan],
                    value='2023',
                    style={'color': 'black'},
                    clearable=False,
                ),
            ], ),
        ]),
        dbc.CardLink([
            dcc.Graph(id='grf_tipeKerjasama'),
            dbc.Button('Lihat Semua Data',
                       id='cll_grfKegiatanKerjasama',
                       n_clicks=0,
                       style=button_style)
        ], id='cll_grfKegiatanKerjasama', n_clicks=0),
        dbc.Collapse(
            dbc.Card(
                dt.DataTable(
                    id='tbl_kegiatanKerjasama',
                    columns=[
                        {'name': i, 'id': i} for i in dfKegiatanKerjasama.columns
                    ],
                    data=dfKegiatanKerjasama.to_dict('records'),
                    sort_action='native',
                    sort_mode='multi',
                    style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto',
                                 'margin-top': '25px'},
                    style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    style_cell={'width': 95},
                    page_size=10,
                    export_format='xlsx'
                ), style=cardtbl_style
            ),
            id='cll_tblKegiatanKerjasama',
            is_open=False
        )
    ], style=cardgrf_style),
    html.Br(),
    dbc.Card([
        dcc.Tabs([
            dcc.Tab(label='Jumlah Kegiatan Kuliah Umum Yang Mempunyai MoU atau Kerja Sama', value='Kulum',
                    children=[
                        dbc.Row([
                            dbc.Col([
                                html.Br(),
                                html.H6('Dari :'),
                                dcc.Dropdown(
                                    id='drpdwn_FromKulumMOU',
                                    options=[{'label': i, 'value': i} for i in listTahunKulumMOU],
                                    value='2016',
                                    style={'color': 'black'},
                                    clearable=False,
                                ),
                            ], ),
                            dbc.Col([
                                html.Br(),
                                html.H6('Sampai :'),
                                dcc.Dropdown(
                                    id='drpdwn_ToKulumMOU',
                                    options=[{'label': i, 'value': i} for i in listTahunKulumMOU],
                                    value='2019',
                                    style={'color': 'black'},
                                    clearable=False,
                                ),
                            ], ),
                        ]),
                        dbc.CardLink([
                            dcc.Graph(id='grf_Kulum'),
                            dbc.Button('Lihat Semua Data',
                                       id='cll_grfKulum',
                                       n_clicks=0,
                                       style=button_style)
                        ], id='cll_grfKulum',
                            n_clicks=0),
                        dbc.Collapse(
                            dbc.Card(
                                dt.DataTable(
                                    id='tbl_kulummou',
                                    columns=[
                                        {'name': i, 'id': i} for i in dfTableKulum.columns
                                    ],
                                    data=dfTableKulum.to_dict('records'),
                                    sort_action='native',
                                    sort_mode='multi',
                                    style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto',
                                                 'margin-top': '25px'},
                                    style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                                    style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                                    style_cell={'width': 95},
                                    page_size=10,
                                    export_format='xlsx'
                                ), style=cardtbl_style
                            ),
                            id='cll_tblkulummou',
                            is_open=False
                        )
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Jumlah Peserta Kegiatan Kuliah Umum Yang Mempunyai MoU atau Kerja Sama', value='pesertaKulum',
                    children=[
                        dbc.Col([
                            html.Br(),
                            html.H6('Tahun :'),
                            dcc.Dropdown(
                                id='drpdwn_pesertaKulum',
                                options=[
                                    {'label': '2021', 'value': '2021'},
                                    {'label': '2020', 'value': '2020'},
                                    {'label': '2019', 'value': '2019'},
                                    {'label': '2018', 'value': '2018'},
                                    {'label': '2017', 'value': '2017'}, ],
                                value='2019',
                                style={'color': 'black'},
                                clearable=False,
                            ),
                        ]),
                        dbc.CardLink([
                            dcc.Graph(id='grf_pesertaKulum'),
                            dbc.Button('Lihat Semua Data',
                                       id='cll_grfpesertaKulum',
                                       n_clicks=0,
                                       style=button_style)
                        ], id='cll_grfpesertaKulum',
                            n_clicks=0),
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Rata-rata Peserta Kegiatan Kuliah Umum Yang Mempunyai MoU atau Kerja Sama',
                    value='rerataPesertaKulum',
                    children=[
                        dbc.CardLink(
                            dbc.CardBody([
                                dcc.Loading(
                                    id='loading-2',
                                    type="default",
                                    children=dcc.Graph(id='grf_reratamhskulum'),
                                ),
                                # dbc.Button('Lihat Semua Data',
                                #            id='cll_grf_persentasimhsmbkm',
                                #            n_clicks=0,
                                #            style=button_style)
                            ]),
                            id='cll_grf_reratamhskulum',
                            n_clicks=0
                        ),
                    ],
                    style=tab_style, selected_style=selected_style),
        ], style=tabs_styles, id='tab_Kegkulum', value='Kulum'),
    ], style=cardgrf_style),


    dbc.Collapse(
        id='cll_Kegkulum',
        is_open=False
    )
], style=cont_style)

layout = dbc.Container([
    html.Div([
        html.Div(html.H1('Kegiatan',
                         style={'margin-top': '30px', 'textAlign': 'center'}
                         )
                 ),
        html.Br(),
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Mahasiswa', value='mahasiswa',
                        children=[
                            html.Div([kegiatanMahasiswa]),
                        ],
                        style=tab_style, selected_style=selected_style
                        ),
                dcc.Tab(label='Dosen', value='dosen',
                        children=[
                            html.Div([kegiatan_dosen]),
                        ],
                        style=tab_style, selected_style=selected_style
                        ),
                dcc.Tab(label='Mitra', value='mitra',
                        children=[
                            html.Div([kerjasama], style={'margin-bottom': '50px'}),
                        ],
                        style=tab_style, selected_style=selected_style
                        ),
            ], style=tabs_styles, value='mahasiswa'),
        ]),
        #html.Div([kegiatan_dosen]),
        #html.Div([kegiatanMahasiswa]),
        #html.Div([kerjasama], style={'margin-bottom': '50px'}),
        dbc.Container([
            dcc.Link([
                dbc.Button('^', style=buttonLink_style),
            ], href='#name'),
        ], style={'margin-left': '90%'}),
    ], style={'justify-content': 'center'})
], style=cont_style)


# CONTROL COLLAPSE
@app.callback(
    Output("cll_tblrekognisidosen", "is_open"),
    [Input("cll_grfrekognisidosen", "n_clicks")],
    [State("cll_tblrekognisidosen", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("cll_tblkegiatandosen", "is_open"),
    [Input("cll_grfkegDosen", "n_clicks")],
    [State("cll_tblkegiatandosen", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tblprestasiakademikmhs", "is_open"),
    [Input("cll_grfprestasiakademik", "n_clicks")],
    [State("cll_tblprestasiakademikmhs", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("cll_tblKegiatanKerjasama", "is_open"),
    [Input("cll_grfKegiatanKerjasama", "n_clicks")],
    [State("cll_tblKegiatanKerjasama", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
######################
@app.callback(
    Output("cll_tblprestasinonakademikmhs", "is_open"),
    [Input("cll_grfprestasinonakademik", "n_clicks")],
    [State("cll_tblprestasinonakademikmhs", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_Kegkulum", "is_open"),
    Output("cll_Kegkulum", "children"),
    [Input("cll_grfpesertaKulum", "n_clicks"),
     Input("tab_Kegkulum", "value")],
    [State("cll_Kegkulum", "is_open")])
def toggle_collapse(npesertaKulum, tab_peserta, is_open):
    isipesertaKulum = dt.DataTable(
        id='tbl_pesertaKulum',
        columns=[
            {'name': i, 'id': i} for i in dfrerataKulum.columns
        ],
        data=dfrerataKulum.to_dict('records'),
        sort_action='native',
        sort_mode='multi',
        style_table={'padding': '10px', 'overflowX': 'auto'},
        style_header={'textAlign': 'center'},
        style_data={'font-size': '80%', 'textAlign': 'center'},
        style_cell={'width': 95},
        page_size=10,
        export_format='xlsx'
    )
    if npesertaKulum and tab_peserta == 'pesertaKulum':
        return not is_open, isipesertaKulum
    return is_open, None

@app.callback(
    Output("cll_tblkulummou", "is_open"),
    [Input("cll_grfKulum", "n_clicks")],
    [State("cll_tblkulummou", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# APPS
@app.callback(
    Output('grf_kegDosen', 'figure'),
    Input('grf_kegDosen', 'id'),
    Input('drpdwn_kegDosen', 'value')
)
def graphKegDosen(id, waktu):
    df = data.getDataFrameFromDBwithParams('''
    select tahun as 'Tahun', nama as 'Nama Dosen',count(fkd.id_dosen) 'Jumlah Kegiatan' from fact_kegiatan_dosen fkd
inner join dim_kegiatan dk on fkd.id_kegiatan = dk.id_kegiatan
inner join dim_date dd on dd.id_date=dk.id_tanggal_mulai
inner join dim_dosen d on fkd.id_dosen = d.id_dosen
where tahun = %(tahun)s and d.id_prodi = 9
group by tahun,nama
order by `Jumlah Kegiatan` asc
    ''', {'tahun': waktu})
    fig = px.bar(df, y=df['Nama Dosen'], x=df['Jumlah Kegiatan'],orientation='h',text_auto=True)
    fig.update_layout(
        yaxis=dict(tickvals=df['Nama Dosen'].unique())
    )
    fig.update_layout()
    return fig


@app.callback(
    Output('grf_Kulum', 'figure'),
    Input('grf_Kulum', 'id'),
    Input('drpdwn_FromKulumMOU', 'value'),
    Input('drpdwn_ToKulumMOU', 'value')
)
def graphKulum(id,valueFrom, valueTo):
    #df = dfKulum
    df = data.getDataFrameFromDBwithParams('''
            select ddselesai.tahun as 'Tahun', count(dim_kegiatan.nama_kegiatan) as 'Jumlah Kegiatan'
        from dim_kegiatan
            inner join dim_perjanjian dp on dim_kegiatan.id_perjanjian = dp.id_perjanjian
            inner join dim_date ddmulai on ddmulai.id_date = dim_kegiatan.id_tanggal_mulai
            inner join dim_date ddselesai on ddselesai.id_date = dim_kegiatan.id_tanggal_selesai
    where jenis_kegiatan = 'KULIAH UMUM' and dim_kegiatan.id_perjanjian is not null
    and ddselesai.tahun between %(From)s and %(To)s
    group by ddselesai.tahun
    order by ddselesai.tahun asc
            ''', {'From': valueFrom, 'To': valueTo})
    fig = px.line(df, x=df['Tahun'], y=df['Jumlah Kegiatan'],text=df['Jumlah Kegiatan'])
    fig.update_traces(mode='lines+markers+text',textposition="top center")
    #fig.update_traces(textposition="top center")
    return fig


@app.callback(
    Output('grf_pesertaKulum', 'figure'),
    Input('grf_pesertaKulum', 'id'),
    Input('drpdwn_pesertaKulum', 'value')
)
def graphKegPeserta(id, waktu):
    df = data.getDataFrameFromDBwithParams('''
    select tahun, nama_kegiatan as 'Nama Kegiatan',count(id_mahasiswa) jumlah from fact_kegiatan_mahasiswa fkm
inner join dim_kegiatan dk on fkm.id_kegiatan = dk.id_kegiatan
inner join dim_date dd on dd.id_date=dk.id_tanggal_mulai
where jenis_kegiatan = 'KULIAH UMUM'
and tahun=%(tahun)s
group by tahun,dk.id_kegiatan,dk.nama_kegiatan
order by tahun asc
    ''', {'tahun': waktu})

    if (len(df['Nama Kegiatan'])) != 0:
        fig = px.bar(df, y=df['Nama Kegiatan'], x=df['jumlah'],orientation='h',text_auto=True)
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Data Tidak Ditemukan!",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig

@app.callback(
    Output('grf_rekognisiDosen', 'figure'),
    Input('grf_rekognisiDosen', 'id'),
    Input('drpdwn_kegRekoginisiDosen', 'value'),
    Input('drpdwn_FromTahunkegRekoginisiDosen', 'value'),
    Input('drpdwn_ToTahunkegRekoginisiDosen', 'value')
)
def graphKegRecognisiDosen(id,wilayahValue,valueFrom, valueTo):
    #df = dfRekognisiDosenGraf
    df = data.getDataFrameFromDBwithParams('''
        select tahun as 'Tahun',count(judul_rekognisi) as 'Jumlah Rekognisi'
from fact_rekognisi_dosen frd
inner join dim_date dd on dd.id_date=frd.id_tanggal_mulai
inner join dim_dosen d on frd.id_dosen = d.id_dosen
where d.id_prodi = 9
and wilayah = %(wilayah)s
and tahun between %(From)s and %(To)s
group by tahun
order by tahun asc
        ''', {'wilayah': wilayahValue,'From': valueFrom, 'To': valueTo})
    print(len(df['Tahun']))
    if (len(df['Tahun'])) != 0:
        fig = px.bar(df, y=df['Jumlah Rekognisi'], x=df['Tahun'], orientation='v',text_auto=True)
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Data Tidak Ditemukan!",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig
@app.callback(
    Output('grf_prestasinonakademik', 'figure'),
    Input('grf_prestasinonakademik', 'id'),
    Input('drpdwn_prestasiNonAkademikMahasiswa', 'value'),
    Input('drpdwn_FromPrestasiNonAkademikMahasiswa', 'value'),
    Input('drpdwn_ToPrestasiNonAkademikMahasiswa', 'value')
)
def graphPrestasiNonAkademik(id,wilayahValue,valueFrom, valueTo):
    #df = dfRekognisiDosenGraf
    df = data.getDataFrameFromDBwithParams('''
        select distinct tahun as 'Tahun', count(fact.wilayah_nama) as 'Jumlah Prestasi Mahasiswa'
    from fact_kegiatan_mahasiswa fact
    inner join dim_kegiatan keg on keg.id_kegiatan = fact.id_kegiatan
    inner join dim_date dat on keg.id_tanggal_mulai = dat.id_date
    where sifat_partisipasi = 'PM' and is_akademis = 0 and fact.wilayah_nama = %(wilayah)s
    and tahun between %(From)s and %(To)s
group by fact.wilayah_nama,tahun
order by tahun asc 
        ''', {'wilayah': wilayahValue,'From': valueFrom, 'To': valueTo})

    if (len(df['Tahun'])) != 0:
        fig = px.bar(df, y=df['Jumlah Prestasi Mahasiswa'], x=df['Tahun'], orientation='v',text_auto=True)
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Data Tidak Ditemukan!",
                                 font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                 yshift=10)
        return fig


@app.callback(
    Output('grf_prestasiakademik', 'figure'),
    Input('grf_prestasiakademik', 'id'),
    Input('drpdwn_prestasiAkademikMahasiswa', 'value'),
    Input('drpdwn_FromPrestasiAkademikMahasiswa', 'value'),
    Input('drpdwn_ToPrestasiAkademikMahasiswa', 'value')
)
def graphPrestasiAkademik(id,wilayahValue,valueFrom, valueTo):
    #df = dfRekognisiDosenGraf
    df = data.getDataFrameFromDBwithParams('''
        select distinct tahun as 'Tahun', count(fact.wilayah_nama) as 'Jumlah Prestasi Mahasiswa'
    from fact_kegiatan_mahasiswa fact
    inner join dim_kegiatan keg on keg.id_kegiatan = fact.id_kegiatan
    inner join dim_date dat on keg.id_tanggal_mulai = dat.id_date
    where sifat_partisipasi = 'PM' and is_akademis = 1 and fact.wilayah_nama = %(wilayah)s
    and tahun between %(From)s and %(To)s
group by fact.wilayah_nama,tahun
order by tahun asc
        ''', {'wilayah': wilayahValue,'From': valueFrom, 'To': valueTo})

    df1 = dfJumlahMhsKuliahUmum
    df2 = pd.DataFrame()
    print(df2)
    # df2['tahun'] = df1['tahun'].unique()
    df2['total_mhs'] = df1.groupby(['tahun']).sum()
    df2['jumlah_kuliah_umum'] = df1.groupby(['tahun']).count()
    df2['rata-rata'] = (df2['total_mhs'] / df2['jumlah_kuliah_umum'])
    print(df2)
    if (len(df['Tahun'])) != 0:
        fig = px.bar(df, y=df['Jumlah Prestasi Mahasiswa'], x=df['Tahun'], orientation='v',text_auto=True)
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Data Tidak Ditemukan!",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


@app.callback(
    Output('grf_tipeKerjasama', 'figure'),
    Input('grf_tipeKerjasama', 'id'),
    Input('drpdwn_FromTipeKegiatan', 'value'),
    Input('drpdwn_ToTipeKegiatan', 'value')
    #Input('drpdwn_kegDosen', 'value')
)
def graphTipeKegiatan(id,valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''
    select ddselesai.tahun as Tahun,CASE WHEN dp.tipe_perjanjian = 'MO' THEN 'MOU'
		WHEN dp.tipe_perjanjian = 'PK' THEN 'PERJANJIAN KERJASAMA'
		ELSE 'SURAT PERJANJIAN' END AS 'Tipe Kerjasama', count(dp.tipe_perjanjian) as Jumlah
        from dim_kegiatan
            inner join dim_perjanjian dp on dim_kegiatan.id_perjanjian = dp.id_perjanjian
            inner join br_mitra_perjanjian bmp on bmp.id_perjanjian = dim_kegiatan.id_perjanjian
            inner join dim_mitra dm on bmp.id_mitra = dm.id_mitra
            inner join dim_date ddmulai on ddmulai.id_date = dim_kegiatan.id_tanggal_mulai
            inner join dim_date ddselesai on ddselesai.id_date = dim_kegiatan.id_tanggal_selesai
    where dim_kegiatan.id_perjanjian is not null
    and ddselesai.tahun between %(From)s and %(To)s
    group by ddselesai.tahun, `Tipe Kerjasama`
    order by ddselesai.tahun asc ;
    ''',{'From': valueFrom, 'To': valueTo})
    
    dfTotal = df.groupby(['Tahun']).sum().reset_index()
    fig = px.bar(
        df,
        y=df['Jumlah'],
        x=df['Tahun'],
        color=df['Tipe Kerjasama'],
        orientation='v',
    )
    fig.add_scatter(
        x=dfTotal['Tahun'],
        y=dfTotal['Jumlah'],
        showlegend=False,
        mode='text',
        text=dfTotal['Jumlah'],
        textposition="top center"
    )

    fig.update_layout()
    return fig


@app.callback(
    Output('grf_reratamhskulum', 'figure'),
    Input('grf_reratamhskulum','id')
)
def grafRerataPersentasiMhsMbkm(id):
    df1 = dfJumlahMhsKuliahUmum
    df2 = pd.DataFrame()
    print(df2)
    #df2['tahun'] = df1['tahun'].unique()
    df2['total_mhs'] = df1.groupby(['tahun']).sum()
    df2['jumlah_kuliah_umum'] = df1.groupby(['tahun']).count()
    df2['rata-rata'] = round((df2['total_mhs'] / df2['jumlah_kuliah_umum']),2)
    print(df2)
    fig = px.bar(df2, y=df2['rata-rata'], x=df2.index, orientation='v',text_auto=True)
    #fig.update_traces(textposition="top center")
    return fig
