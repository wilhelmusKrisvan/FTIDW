import dash_table as dt
import numpy as np
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from appConfig import app, server
import model.dao_kbm as data
from datetime import date

tbl_IpkMahasiswa = data.getIpkMahasiswa()
tbl_matkulBaru = data.getMatkulKurikulumBaru()
tbl_MatkulBatal = data.getMatkulBatal()
tbl_matkulTawar = data.getMatkulTawar()
tbl_persentaseMhsTA = data.getPersentaseMahasiswaTidakAktif()
tbl_jumlahDosenMengajar = data.getDosenMengajar()
tbl_jumlahDTT = data.getPersentaseDosenTidakTetap()
tbl_tingkatKepuasan = data.getTingkatKepuasanDosen()
tbl_RasioDosenMhs = data.getRasioDosenMahasiswa()
tbl_rasioDosenMengajarMhs = data.getRasioDosenMengajarMahasiswa()
dfKurikulum = data.getKurikulum()

listDropdown = []
listAngkatan = []
listTahun = []
listKurikulum = dfKurikulum['kode_kurikulum'].dropna().unique()
for x in range(0, 5):
    tahun = 5
    yearnow = date.today().strftime('%Y')
    listDropdown.append(
        str(int(yearnow) - tahun + x) + '/' + str(int(yearnow) - (tahun - 1) + x))

for x in range(0, 5):
    tahun = 5
    yearnow = date.today().strftime('%Y')
    listTahun.append(
        str(int(yearnow) - tahun + x))

for x in range(0, 7):
    yearnow = date.today().strftime('%Y')
    listAngkatan.append(int(yearnow) - x)

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


def tabel(data):
    return dbc.Card([
        dt.DataTable(
            id='tbl_MhsIpk',
            columns=[
                {'name': i, 'id': i} for i in data.columns
            ],
            data=data.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'font-size': '80%', 'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            export_format='xlsx',
            page_size=10,
        )
    ], style=cardtbl_style),


ipkmahasiswa = dbc.Container([
    dbc.Card([
        html.H5('Rata-rata IPK Mahasiswa Aktif Tiap Semester',
                style=ttlgrf_style),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.P('Dari', style={'color': 'black'}),
                        dcc.Dropdown(
                            id='Fromdrpdwn_ipkMahasiswa',
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
                            id='Todrpdwn_ipkMahasiswa',
                            options=[{'label': i, 'value': i} for i in listDropdown],
                            value=listDropdown[len(listDropdown) - 1],
                            style={'color': 'black'},
                            clearable=False,
                            placeholder='Sampai',
                        ),
                    ]),
                ], width=6),
            ]),
            dcc.Tabs([
                dcc.Tab([
                    dbc.CardBody([
                        dcc.Loading([
                            dcc.Graph(id='grf_ipkMahasiswa'),
                        ], type='default'),
                        dbc.Button('Lihat Semua Data', id='cll_grfipkMahasiswa', n_clicks=0,
                                   style=button_style),
                    ])
                ], style=tab_style, selected_style=selected_style, label='IPK Mahasiswa Aktif', value='ipk_aktif'),
                dcc.Tab([
                    dbc.CardBody([
                        dcc.Loading([
                            dcc.Graph(id='grf_ipkAngkatan'),
                        ], type='default'),
                        dbc.Button('Lihat Semua Data', id='cll_grfipkAngkatan', n_clicks=0,
                                   style=button_style),
                    ])
                ], style=tab_style, selected_style=selected_style, label='IPK Mahasiswa per Angkatan',
                    value='ipk_angkatan')
            ], id='tab_ipk', value='ipk_aktif'),

        ])
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_ipkMahasiswa',
        is_open=False
    )
], style=cont_style)

mahasiswaTA = dbc.Container([
    dbc.Card([
        html.H5('Student Body Mahasiswa',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab([
                dbc.CardBody([
                    html.Div([
                        html.P('Tahun Angkatan', style={'color': 'black'}),
                        dbc.Row([
                            dbc.Col([
                                dcc.Dropdown(
                                    id='Angkatandrpdwn_MhsTA',
                                    options=[{'label': i, 'value': i} for i in listAngkatan],
                                    value=listAngkatan[len(listAngkatan) - 1],
                                    style={'color': 'black'},
                                    clearable=False,
                                    placeholder='Tahun Angkatan',
                                ),
                            ]),
                        ]),
                    ]),
                    dcc.Loading([
                        dcc.Graph(id='grf_MhsTA'),
                    ], type="default"),
                    dbc.Button('Lihat Semua Data', id='cll_grfMhsTA', n_clicks=0, style=button_style),
                ])
            ], label='Mahasiswa per Status', value='mhs_status', style=tab_style, selected_style=selected_style),
            dcc.Tab([
                dbc.CardBody([
                    dcc.Loading([
                        dcc.Graph(id='grf_MhsDO'),
                    ], type="default"),
                    dbc.Button('Lihat Semua Data', id='cll_grfMhsDO', n_clicks=0, style=button_style),
                ])
            ], label='Mahasiswa Undur Diri dan Drop Out', value='mhs_do', style=tab_style,
                selected_style=selected_style)
        ], id='tab_studentBody', value='mhs_status'),
    ], style=cardgrf_style
    ),
    dbc.Collapse(
        id='cll_tblMhsTA',
        is_open=False
    )
], style=cont_style)

jumlahDosen = dbc.Container([
    dbc.Card([
        html.H5('Rasio Dosen',
                style=ttlgrf_style),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.P('Dari', style={'color': 'black'}),
                    dcc.Dropdown(
                        id='Fromdrpdwn_Jmldosen',
                        options=[{'label': i, 'value': i} for i in listDropdown],
                        value=listDropdown[0],
                        style={'color': 'black'},
                        clearable=False,
                        placeholder='Dari',
                    ),
                ]),
            ]),
            dbc.Col([
                html.Div([
                    html.P('Sampai', style={'color': 'black'}),
                    dcc.Dropdown(
                        id='Todrpdwn_Jmldosen',
                        options=[{'label': i, 'value': i} for i in listDropdown],
                        value=listDropdown[len(listDropdown) - 1],
                        style={'color': 'black'},
                        clearable=False,
                        placeholder='Sampai',
                    ),
                ]),
            ]),
        ], style={'padding': '15px'}),
        dcc.Tabs([
            dcc.Tab(label='Rasio Dosen Mengajar (Informatika : Non Informatika)', value='dosenAjar',
                    children=[
                        dbc.CardBody([
                            dcc.Loading([
                                dcc.Graph(id='grf_dosenAjar'),
                            ], type="default"),
                            dbc.Button('Lihat Semua Data', id='cll_grfdosenAjar', n_clicks=0, style=button_style),
                        ])
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Dosen Tidak Tetap : Dosen Mengajar', value='dosenNon',
                    children=[
                        dbc.CardBody([
                            dcc.Loading([
                                dcc.Graph(id='grf_dosenNon'),
                            ], type="default"),
                            dbc.Button('Lihat Semua Data', id='cll_grfdosenNon', n_clicks=0, style=button_style),
                        ])
                    ],
                    style=tab_style, selected_style=selected_style),
        ], id='tab_Jmldosen', value='dosenAjar')
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_tblJmlDosen',
        is_open=False
    )
], style=cont_style)

rasioDosen = dbc.Container([
    dbc.Card([
        html.H5('Rasio Dosen Terhadap Mahasiswa',
                style=ttlgrf_style),
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Rasio Dosen : Mahasiswa', value='dosen',
                        children=[
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        html.Div([
                                            html.P('Dari', style={'color': 'black'}),
                                            dcc.Dropdown(
                                                id='Fromdrpdwn_dosen',
                                                options=[{'label': i, 'value': i} for i in listDropdown],
                                                value=listDropdown[0],
                                                style={'color': 'black'},
                                                clearable=False,
                                                placeholder='Dari',
                                            ),
                                        ], id='visiTahun_dosen'),
                                    ], width=6),
                                    dbc.Col([
                                        html.Div([
                                            html.P('Sampai', style={'color': 'black'}),
                                            dcc.Dropdown(
                                                id='Todrpdwn_dosen',
                                                options=[{'label': i, 'value': i} for i in listDropdown],
                                                value=listDropdown[len(listDropdown) - 1],
                                                style={'color': 'black'},
                                                clearable=False,
                                                placeholder='Sampai',
                                            ),
                                        ], id='visiSemester_dosen')
                                    ], width=6),
                                ]),
                                # dbc.Card(
                                #     dbc.CardBody([
                                #         html.P('Rasio Dosen : Mahasiswa', className='card-title',
                                #                style={'textAlign': 'center', 'fontSize': 17, 'color': 'black'}),
                                #         html.P(id='rasio_dosen',
                                #                className='card-text')
                                #     ]), style={'margin-top': '25px'}),
                                dcc.Loading([
                                    dcc.Graph(id='grf_dosen'),
                                ], type="default"),
                                dbc.Button('Lihat Semua Data', id='cll_grfdosen', n_clicks=0, style=button_style),
                            ])
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Rasio Dosen Mengajar : Mahasiswa', value='dosenMengajar',
                        children=[
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        html.Div([
                                            html.P('Dari', style={'color': 'black'}),
                                            dcc.Dropdown(
                                                id='Fromdrpdwn_dosenMengajar',
                                                options=[{'label': i, 'value': i} for i in listDropdown],
                                                value=listDropdown[0],
                                                style={'color': 'black'},
                                                clearable=False,
                                                placeholder='Dari',
                                            ),
                                        ], id='visiTahun_dosenMengajar'),
                                    ], width=6),
                                    dbc.Col([
                                        html.Div([
                                            html.P('Sampai', style={'color': 'black'}),
                                            dcc.Dropdown(
                                                id='Todrpdwn_dosenMengajar',
                                                options=[{'label': i, 'value': i} for i in listDropdown],
                                                value=listDropdown[len(listDropdown) - 1],
                                                style={'color': 'black'},
                                                clearable=False,
                                                placeholder='Sampai',
                                            ),
                                        ], id='visiSemester_dosenMengajar')
                                    ], width=6),
                                ]),
                                # dbc.Card(
                                #     dbc.CardBody([
                                #         html.P('Rasio Dosen Mengajar : Mahasiswa', className='card-title',
                                #                style={'textAlign': 'center', 'fontSize': 17, 'color': 'black'}),
                                #         html.P(id='rasio_dosenMengajar',
                                #                className='card-text')
                                #     ]), style={'margin-top': '25px'}),
                                dcc.Loading([
                                    dcc.Graph(id='grf_dosenMengajar'),
                                ], type="default"),
                                dbc.Button('Lihat Semua Data', id='cll_grfdosenMengajar', n_clicks=0,
                                           style=button_style),
                            ])
                        ], style=tab_style, selected_style=selected_style),
            ], style=tab_style, id='tab_dosen', value='dosen'
            )
        ])
    ], style=cardtbl_style
    ),
    dbc.Collapse(
        id='cll_tblDosen',
        is_open=False
    )
], style=cont_style)

tingkatKepuasan = dbc.Container([
    dbc.Card([
        html.H5('Tingkat Kepuasan Mahasiswa Terhadap Dosen',
                style=ttlgrf_style),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.P('Tahun Ajaran', style={'color': 'black'}),
                    dcc.Dropdown(
                        id='drpdwn_KepuasanMhs',
                        options=[{'label': i, 'value': i} for i in listDropdown],
                        value=listDropdown[0],
                        style={'color': 'black'},
                        clearable=False,
                        placeholder='Tahun Ajaran',
                    ),
                ]),
            ], width=6),
            dbc.Col([
                html.Div([
                    html.P('Semester', style={'color': 'black'}),
                    dcc.Dropdown(
                        id='Smtdrpdwn_KepuasanMhs',
                        options=[{'label': 'GASAL', 'value': 'GASAL'},
                                 {'label': 'GENAP', 'value': 'GENAP'}, ],
                        value='GASAL',
                        style={'color': 'black'},
                        clearable=False,
                        placeholder='Semester',
                    ),
                ]),
            ], width=6),
        ], style={'padding': '15px'}),
        dbc.CardBody([
            dcc.Loading([
                dcc.Graph(id='grf_KepuasanMhs'),
            ], type="default"),
            dbc.Button('Lihat Semua Data', id='cll_grfKepuasanMhs', n_clicks=0, style=button_style),
        ])
    ], style=cardgrf_style
    ),
    dbc.Collapse(
        tabel(tbl_tingkatKepuasan),
        id='cll_tblKepuasanMhs',
        is_open=False
    )
], style=cont_style)

matkulKurikulum = dbc.Container([
    dbc.Card([
        html.H5('Daftar Kelompok Matakuliah per Kurikulum',
                style=ttlgrf_style),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.P('Kurikulum', style={'color': 'black'}),
                        # dcc.Dropdown(
                        #     id='Kuridrpdwn_matkulKuri',
                        #     options=[{'label': i, 'value': i} for i in listKurikulum],
                        #     value=listKurikulum[len(listKurikulum) - 1],
                        #     style={'color': 'black'},
                        #     clearable=False,
                        #     placeholder='Dari',
                        # ),
                    ]),
                ], width=12),
            ]),
            dbc.CardBody([
                dcc.Loading([
                    dcc.Graph(id='grf_matkulKuri'),
                ], type="default"),
                dbc.Button('Lihat Semua Data', id='cll_grfMatkulKuri', n_clicks=0,
                           style=button_style),
            ])
        ])
    ], style=cardgrf_style),
    dbc.Collapse(
        tabel(tbl_matkulBaru),
        id='cll_matkulKuri',
        is_open=False
    )
], style=cont_style)

matkulBatalTawar = dbc.Container([
    dbc.Card([
        html.H5('Matakuliah yang Dibatalkan',
                style=ttlgrf_style),
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Rasio Matakuliah Batal : Kelas Ditawarkan', value='matkulBtlTawar',
                        children=[
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        html.Div([
                                            html.P('Dari', style={'color': 'black'}),
                                            dcc.Dropdown(
                                                id='Fromdrpdwn_matkulBtlTawar',
                                                options=[{'label': i, 'value': i} for i in listDropdown],
                                                value=listDropdown[0],
                                                style={'color': 'black'},
                                                clearable=False,
                                                placeholder='Tahun Ajaran',
                                            ),
                                        ]),
                                    ], width=6),
                                    dbc.Col([
                                        html.Div([
                                            html.P('Sampai', style={'color': 'black'}),
                                            dcc.Dropdown(
                                                id='Todrpdwn_matkulBtlTawar',
                                                options=[{'label': i, 'value': i} for i in listDropdown],
                                                value=listDropdown[len(listDropdown) - 4],
                                                style={'color': 'black'},
                                                clearable=False,
                                                placeholder='Tahun Ajaran',
                                            ),
                                        ]),
                                    ], width=6),
                                ], style={'padding': '15px'}),
                                dbc.CardBody([
                                    dcc.Loading([
                                        dcc.Graph(id='grf_matkulBtlTawar'),
                                    ], type="default"),
                                    dbc.Button('Lihat Semua Data', id='cll_grfMatkulBtlTawar', n_clicks=0,
                                               style=button_style),
                                ])
                            ])
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Matakuliah Dibatalkan Berdasarkan Dosen', value='dosenBatal',
                        children=[
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        html.Div([
                                            html.P('Tahun Ajaran', style={'color': 'black'}),
                                            dcc.Dropdown(
                                                id='TAdrpdwn_dosenBatal',
                                                options=[{'label': i, 'value': i} for i in listDropdown],
                                                value=listDropdown[0],
                                                style={'color': 'black'},
                                                clearable=False,
                                                placeholder='Tahun Ajaran',
                                            ),
                                        ]),
                                    ]),
                                    dbc.Col([
                                        html.Div([
                                            html.P('Semester', style={'color': 'black'}),
                                            dcc.Dropdown(
                                                id='Smtdrpdwn_dosenBatal',
                                                options=[{'label': 'GASAL', 'value': 'GASAL'},
                                                         {'label': 'GENAP', 'value': 'GENAP'}],
                                                value='GASAL',
                                                style={'color': 'black'},
                                                clearable=False,
                                                placeholder='Tahun Ajaran',
                                            ),
                                        ]),
                                    ]),
                                ], style={'padding': '15px'}),
                                dbc.CardBody([
                                    dcc.Loading([
                                        dcc.Graph(id='grf_dosenBatal'),
                                    ], type="default"),
                                    dbc.Button('Lihat Semua Data', id='cll_grfDosenBatal', n_clicks=0,
                                               style=button_style),
                                ])
                            ])
                        ], style=tab_style, selected_style=selected_style),
            ], style=tab_style, id='tab_matkulBatalTawar', value='matkulBtlTawar'
            )
        ])
    ], style=cardtbl_style
    ),
    dbc.Collapse(
        id='cll_tblMatkulBatal',
        is_open=False
    )
], style=cont_style)

layout = html.Div([
    html.Div(html.H1('Analisis KBM Prodi Informatika',
                     style={'margin-top': '30px', 'textAlign': 'center'}
                     )
             ),
    html.A(className='name'),
    html.Div([ipkmahasiswa]),
    html.Div([mahasiswaTA]),
    html.Div([jumlahDosen]),
    html.Div([rasioDosen]),
    html.Div([tingkatKepuasan]),
    html.Div([matkulKurikulum]),
    html.Div([matkulBatalTawar], style={'margin-bottom': '50px'}),
    dbc.Container([
        dcc.Link([
            dbc.Button('^', style=buttonLink_style),
        ], href='#name'),
    ], style={'margin-left': '90%'}),
], style={'width': '100%'})


# CALLBACK COLLAPSE
@app.callback(
    Output('cll_ipkMahasiswa', 'is_open'),
    Output('cll_ipkMahasiswa', 'children'),
    Input('cll_grfipkMahasiswa', 'n_clicks'),
    Input('cll_grfipkAngkatan', 'n_clicks'),
    Input("tab_ipk", "value"),
    State('cll_ipkMahasiswa', 'is_open')
)
def toggle_collapse(nMhs, nAngkatan, tab, is_open):
    isiMhs = tabel(tbl_IpkMahasiswa)
    isiAngkatan = tabel(data.getIpkAngkatan())
    if nMhs and tab == 'ipk_aktif':
        return not is_open, isiMhs
    if nAngkatan and tab == 'ipk_angkatan':
        return not is_open, isiAngkatan
    return is_open, None


@app.callback(
    Output('cll_tblMhsTA', "is_open"),
    Output('cll_tblMhsTA', "children"),
    [Input("cll_grfMhsTA", "n_clicks"),
     Input("cll_grfMhsDO", "n_clicks"),
     Input('tab_studentBody','value')],
    [State('cll_tblMhsTA', "is_open")])
def toggle_collapse(nTA,nDO,tab, is_open):
    isiStatus = tabel(data.getPersentaseMahasiswaTidakAktif())
    isiDO = tabel(data.getPersentaseMahasiswaDO())
    if nTA and tab == 'mhs_status':
        return not is_open, isiStatus
    if nDO and tab == 'mhs_do':
        return not is_open, isiDO
    return is_open, None


@app.callback(
    Output('cll_tblJmlDosen', 'is_open'),
    Output('cll_tblJmlDosen', 'children'),
    [Input("cll_grfdosenAjar", "n_clicks"),
     Input("cll_grfdosenNon", "n_clicks"),
     Input("tab_Jmldosen", "value")],
    [State('cll_tblJmlDosen', "is_open")])
def toggle_collapse(najar, non, dsn, is_open):
    isiAjar = tabel(tbl_jumlahDosenMengajar)
    isiNon = tabel(tbl_jumlahDTT)
    if najar and dsn == 'dosenAjar':
        return not is_open, isiAjar
    if non and dsn == 'dosenNon':
        return not is_open, isiNon
    return is_open, None


@app.callback(
    Output('cll_tblDosen', 'is_open'),
    Output('cll_tblDosen', 'children'),
    [Input("cll_grfdosen", "n_clicks"),
     Input("cll_grfdosenMengajar", "n_clicks"),
     Input("tab_dosen", "value")],
    [State('cll_tblDosen', "is_open")])
def toggle_collapse(najar, non, dsn, is_open):
    isiDosen = tabel(tbl_RasioDosenMhs)
    isiAjar = tabel(tbl_rasioDosenMengajarMhs)
    if najar and dsn == 'dosen':
        return not is_open, isiDosen
    if non and dsn == 'dosenMengajar':
        return not is_open, isiAjar
    return is_open, None


@app.callback(
    Output('cll_tblKepuasanMhs', "is_open"),
    [Input("cll_grfKepuasanMhs", "n_clicks")],
    [State('cll_tblKepuasanMhs', "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('cll_matkulKuri', "is_open"),
    [Input("cll_grfMatkulKuri", "n_clicks")],
    [State('cll_matkulKuri', "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tblMatkulBatal", "is_open"),
    Output("cll_tblMatkulBatal", "children"),
    [Input("cll_grfMatkulBtlTawar", "n_clicks"),
     Input("cll_grfDosenBatal", "n_clicks"),
     Input('tab_matkulBatalTawar', 'value')],
    [State("cll_tblMatkulBatal", "is_open")])
def toggle_collapse(nBanding, nDosen, tab, is_open):
    isiTawar = tabel(tbl_matkulTawar)
    isiBatal = tabel(tbl_MatkulBatal)
    if nBanding and tab == 'matkulBtlTawar':
        return not is_open, isiTawar
    if nDosen and tab == 'dosenBatal':
        return not is_open, isiBatal
    return is_open, None


# CALLBACK GRAPH
# Rata-rata IPK Mahasiswa Aktif Tiap Semester
@app.callback(
    Output("grf_ipkMahasiswa", 'figure'),
    Input('Fromdrpdwn_ipkMahasiswa', 'value'),
    Input('Todrpdwn_ipkMahasiswa', 'value'),
)
def FillIpkMahasiswa(valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''select 
    ds.tahun_ajaran 'Tahun Ajaran', ds.semester_nama Semester, round(avg(ipk),2) as "Rata-Rata"
from fact_mahasiswa_status fms 
inner join dim_semester ds on ds.id_semester = fms.id_semester
where ds.tahun_ajaran between %(From)s and %(To)s and (fms.status != 'UD' OR fms.status != 'DO')
group by ds.tahun_ajaran, ds.semester_nama
order by ds.tahun_ajaran, ds.semester_nama
''', {'From': valueFrom, 'To': valueTo})
    if (len(df['Tahun Ajaran']) != 0):
        fig = px.bar(df, x=df['Tahun Ajaran'], y=df['Rata-Rata'], color=df['Semester'])
        fig.update_layout(barmode='group')
        fig.add_hrect(y0=0, y1=2, fillcolor='red', opacity=0.1)
        fig.add_hrect(y0=2, y1=3.15, fillcolor='yellow', opacity=0.1)
        fig.add_hrect(y0=3.15, y1=4, fillcolor='green', opacity=0.1)
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


@app.callback(
    Output("grf_ipkAngkatan", 'figure'),
    Input('Fromdrpdwn_ipkMahasiswa', 'value'),
    Input('Todrpdwn_ipkMahasiswa', 'value'),
)
def FillIpkAngkatan(valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''
    select 
    concat(ds.tahun_ajaran,' ',ds.semester_nama) 'Tahun Ajaran', 
    tahun_angkatan Angkatan,avg(ipk) as "Rata-Rata"
    from fact_mahasiswa_status fms 
    inner join dim_semester ds on ds.id_semester = fms.id_semester
    inner join dim_mahasiswa dm on fms.id_mahasiswa = dm.id_mahasiswa
    where ds.tahun_ajaran between %(From)s and %(To)s and (fms.status != 'UD' OR fms.status != 'DO')
    group by `Tahun Ajaran`,tahun_angkatan,ds.tahun_ajaran, ds.semester_nama
    order by ds.tahun_ajaran, tahun_angkatan''', {'From': valueFrom, 'To': valueTo})
    if (len(df['Tahun Ajaran']) != 0):
        fig = px.bar(df, x=df['Tahun Ajaran'], y=df['Rata-Rata'], color=df['Angkatan'])
        fig.update_layout(barmode='group')
        fig.add_hrect(y0=0, y1=2, fillcolor='red', opacity=0.1)
        fig.add_hrect(y0=2, y1=3.15, fillcolor='yellow', opacity=0.1)
        fig.add_hrect(y0=3.15, y1=4, fillcolor='green', opacity=0.1)
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


# Student Body Mahasiswa per status
@app.callback(
    Output('grf_MhsTA', 'figure'),
    Input('Angkatandrpdwn_MhsTA', 'value'),
)
def MhsTA(valueAngkatan):
    df = data.getDataFrameFromDBwithParams('''
    select mhs.`Tahun Ajaran`,mhs.tahun_angkatan,status,mhs.jumlah Mahasiswa,total.jumlah Total,
       round((mhs.jumlah/total.jumlah)*100,2) Persentase
from(select concat(ds.tahun_ajaran,' ', ds.semester_nama) 'Tahun Ajaran', dm.tahun_angkatan,
       status,count(distinct (dm.nim)) jumlah
      from fact_mahasiswa_status fms
               inner join dim_mahasiswa dm on fms.id_mahasiswa = dm.id_mahasiswa
               inner join dim_semester ds on fms.id_semester= ds.id_semester
      where dm.tahun_angkatan = %(TA)s
        and ds.tahun_ajaran between
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
        and id_prodi=9
      group by `Tahun Ajaran`,dm.tahun_angkatan,status) mhs
inner join (select concat(ds.tahun_ajaran,' ', ds.semester_nama) 'Tahun Ajaran',
                tahun_angkatan,count(distinct (dm.nim)) jumlah
      from fact_mahasiswa_status fms
               inner join dim_mahasiswa dm on fms.id_mahasiswa = dm.id_mahasiswa
               inner join dim_semester ds on fms.id_semester= ds.id_semester
      where tahun_angkatan = %(TA)s
        and ds.tahun_ajaran between
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
        and id_prodi=9
      group by `Tahun Ajaran`,tahun_angkatan) total on total.`Tahun Ajaran`=mhs.`Tahun Ajaran`
order by `Tahun Ajaran`''', {'TA': valueAngkatan})
    if (len(df['Tahun Ajaran']) != 0):
        fig = px.bar(x=df['Tahun Ajaran'], y=df['Persentase'], color=df['status'], barmode='stack', )
        fig.update_yaxes(categoryorder='category ascending')
        fig.update_layout(xaxis_title="Tahun Ajaran",
                          yaxis_title="Persentase (%)", legend_title='Status')
        # fig.update_traces(hovertemplate="<br> Jumlah Mahasiswa=%{y} </br> Tahun Ajaran= %{x}")
        # yaxis=dict(tickformat=",.2f"))
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


@app.callback(
    Output('grf_MhsDO', 'figure'),
    Input('Angkatandrpdwn_MhsTA', 'value'),
)
def MhsDO(valueAngkatan):
    df = data.getDataFrameFromDBwithParams('''
    select mhs.`Tahun Ajaran`,status,mhs.jumlah Mahasiswa,total.jumlah Total,
       round((mhs.jumlah/total.jumlah)*100,2) Persentase
from(select concat(ds.tahun_ajaran,' ', ds.semester_nama) 'Tahun Ajaran',
       status,count(distinct (dm.nim)) jumlah
      from fact_mahasiswa_status fms
               inner join dim_mahasiswa dm on fms.id_mahasiswa = dm.id_mahasiswa
               inner join dim_semester ds on fms.id_semester= ds.id_semester
      where (status='DO' or status='UD')
        and ds.tahun_ajaran between
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
        and id_prodi=9
      group by `Tahun Ajaran`,status) mhs
inner join (select concat(ds.tahun_ajaran,' ', ds.semester_nama) 'Tahun Ajaran',
                count(distinct (dm.nim)) jumlah
      from fact_mahasiswa_status fms
               inner join dim_mahasiswa dm on fms.id_mahasiswa = dm.id_mahasiswa
               inner join dim_semester ds on fms.id_semester= ds.id_semester
      where ds.tahun_ajaran between
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
        and id_prodi=9
      group by `Tahun Ajaran`) total on total.`Tahun Ajaran`=mhs.`Tahun Ajaran`
order by `Tahun Ajaran`''', {'TA': valueAngkatan})
    if (len(df['Tahun Ajaran']) != 0):
        fig = px.bar(x=df['Tahun Ajaran'], y=df['Persentase'], color=df['status'], barmode='group', )
        fig.update_yaxes(categoryorder='category ascending')
        fig.add_hrect(y0=0, y1=10, fillcolor='green', opacity=0.1)
        fig.add_hrect(y0=10, y1=15, fillcolor='yellow', opacity=0.1)
        fig.add_hrect(y0=15, y1=50, fillcolor='red', opacity=0.1)
        fig.update_layout(xaxis_title="Tahun Ajaran",
                          yaxis_title="Persentase (%)", legend_title='Status')
        # fig.update_traces(hovertemplate="<br> Jumlah Mahasiswa=%{y} </br> Tahun Ajaran= %{x}")
        # yaxis=dict(tickformat=",.2f"))
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


# Rasio Dosen
@app.callback(
    Output('grf_dosenAjar', 'figure'),
    Input('Fromdrpdwn_Jmldosen', 'value'),
    Input('Todrpdwn_Jmldosen', 'value'),
)
def DosenAjar(valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''
    select data.`Tahun Ajaran`,data.Prodi,data.Jumlah,total.Jumlah Total, 
    round((data.Jumlah/total.Jumlah)*100,2) Persentase from
    (select concat(tahun_ajaran,' ',semester_nama) 'Tahun Ajaran','NON INFORMATIKA' as Prodi,
    count(distinct fdm.id_dosen) 'Jumlah' from fact_dosen_mengajar fdm
inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
inner join dim_semester ds on fdm.id_semester = ds.id_semester
where id_prodi!=9 and tahun_ajaran between %(From)s and %(To)s
group by tahun_ajaran, semester_nama,'Tahun Ajaran'
    union all
    select concat(tahun_ajaran,' ',semester_nama) 'Tahun Ajaran','INFORMATIKA' as Prodi,
    count(distinct fdm.id_dosen) 'Jumlah' from fact_dosen_mengajar fdm
inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
inner join dim_semester ds on fdm.id_semester = ds.id_semester
where id_prodi=9 and tahun_ajaran between %(From)s and %(To)s
group by tahun_ajaran, semester_nama,'Tahun Ajaran'
order by 1 asc,2 asc)data
inner join (select concat(tahun_ajaran,' ',semester_nama) 'Tahun Ajaran',
    count(distinct fdm.id_dosen) 'Jumlah' from fact_dosen_mengajar fdm
inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
inner join dim_semester ds on fdm.id_semester = ds.id_semester
where tahun_ajaran between %(From)s and %(To)s
group by tahun_ajaran, semester_nama,'Tahun Ajaran')total on total.`Tahun Ajaran`=data.`Tahun Ajaran`
order by data.`Tahun Ajaran`,data.Prodi
''', {'From': valueFrom, 'To': valueTo})
    if (len(df['Tahun Ajaran']) != 0):
        fig = px.bar(df, x=df['Tahun Ajaran'], y=df['Persentase'], color=df['Prodi'], barmode='stack')
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


# Rasio Dosen
@app.callback(
    Output('grf_dosenNon', 'figure'),
    Input('Fromdrpdwn_Jmldosen', 'value'),
    Input('Todrpdwn_Jmldosen', 'value'),
)
def DosenNon(valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''
    select semua.`Tahun Ajaran`,
       tetap.jumlah 'Dosen Tidak Tetap',semua.jumlah 'Semua Dosen Mengajar',(tetap.jumlah/semua.jumlah)*100 as 'Persentase' from
(select concat(tahun_ajaran,' ',semester_nama) 'Tahun Ajaran', count(distinct fdm.id_dosen) jumlah from fact_dosen_mengajar fdm
inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
inner join dim_semester ds on fdm.id_semester = ds.id_semester
where tahun_ajaran between %(From)s and %(To)s and status_dosen='Kontrak'
group by `Tahun Ajaran`) tetap,
(select concat(tahun_ajaran,' ',semester_nama) 'Tahun Ajaran',count(distinct fdm.id_dosen) jumlah from fact_dosen_mengajar fdm
inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
inner join dim_semester ds on fdm.id_semester = ds.id_semester
where tahun_ajaran between %(From)s and %(To)s 
group by `Tahun Ajaran`) semua
where semua.`Tahun Ajaran`=tetap.`Tahun Ajaran`
order by semua.`Tahun Ajaran` asc''', {'From': valueFrom, 'To': valueTo})
    if (len(df['Tahun Ajaran']) != 0):
        fig = px.bar(df, x=df['Tahun Ajaran'], y=df['Semua Dosen Mengajar'], color=px.Constant('Semua Dosen Mengajar'),
                     labels=dict(x='Tahun Ajaran', y='Jumlah Dosen', color='Jenis Dosen'))
        # fig.update_traces(mode='lines+markers')
        fig.add_bar(x=df['Tahun Ajaran'], y=df['Dosen Tidak Tetap'], name='Dosen Tidak Tetap', )
        fig.update_traces(hovertemplate="<br> Jumlah Dosen=%{y} </br> Tahun Ajaran= %{x}")
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


# Rasio Dosen Terhadap Mahasiswa
@app.callback(
    Output('grf_dosenMengajar', 'figure'),
    # Output('rasio_dosenMengajar', 'style'),
    # Output('rasio_dosenMengajar', 'children'),
    Input('Fromdrpdwn_dosenMengajar', 'value'),
    Input('Todrpdwn_dosenMengajar', 'value'),
    # Input('Semesterdrpdwn_dosenMengajar', 'value')
)
def graphDosenMengajar(valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''
    select concat(data.tahun_ajaran,' ',data.semester_nama) AS 'Tahun Ajaran',
       dosen.jumlah 'Jumlah Dosen',data.jumlah 'Jumlah Mahasiswa',
       round((data.jumlah/dosen.jumlah),2) 'Rasio' from
(select substr(kode_semester,1,4) 'tahun', kode_semester, count(distinct fdm.id_dosen) jumlah
     from fact_dosen_mengajar fdm
         inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
         inner join dim_semester ds on fdm.id_semester = ds.id_semester
     where substr(kode_semester,1,4)>=year(now())-5
     and tahun_ajaran between %(From)s and %(To)s
     group by tahun,kode_semester) dosen
inner join
    (select substr(ds.kode_semester,1,4) tahun,ds.kode_semester,ds.semester_nama,ds.tahun_ajaran,count(distinct fms.id_mahasiswa) jumlah
      from fact_mahasiswa_status fms
               inner join dim_mahasiswa dm on fms.id_mahasiswa = dm.id_mahasiswa
               inner join dim_semester ds on fms.id_semester= ds.id_semester
      where (status = 'AK' or status='CS' or status='TA')
        and substr(ds.kode_semester,1,4)>=year(now())-5
        and tahun_ajaran between %(From)s and %(To)s
      group by ds.kode_semester,ds.semester_nama,ds.tahun_ajaran,tahun) data
on data.kode_semester=dosen.kode_semester
order by `Tahun Ajaran`
''', {'From': valueFrom, 'To': valueTo})
    # rasioMengajar = df['Rasio'].values[0]
    # txtRasioMengajar = '1 : ' + str(df['Rasio'].values[0])
    # if rasioMengajar >= 15 and rasioMengajar <= 30:
    #     style = {'textAlign': 'center', 'fontSize': 20,
    #              'color': 'rgb(34, 255, 0)'}
    # else:
    #     style = {'textAlign': 'center', 'fontSize': 20,
    #              'color': 'rgb(235, 65, 50)'}
    # dfBar = data.dfRasioDosenMengajarBar(valueTahun, valueSemester)
    if (len(df['Tahun Ajaran']) != 0):
        fig = px.line(df, x=df['Tahun Ajaran'], y=df['Rasio'])
        fig.update_traces(mode='lines+markers')
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


# Rasio Dosen Terhadap Mahasiswa
@app.callback(
    Output('grf_dosen', 'figure'),
    # Output('rasio_dosen', 'style'),
    # Output('rasio_dosen', 'children'),
    Input('Fromdrpdwn_dosen', 'value'),
    Input('Todrpdwn_dosen', 'value')
)
def graphDosen(valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''
    select concat(data.tahun_ajaran,' ', data.semester_nama) as 'Tahun Ajaran',
               dosen.Jumlah 'Jumlah Dosen',data.jumlah 'Jumlah Mahasiswa', 
               round((data.jumlah/dosen.jumlah),2) 'Rasio' from
        (select sum(Jumlah) as Jumlah,cast(year(now())-1 as char) as tahun from
            (select count(*) as Jumlah,year(tanggal_masuk) as tahun
            from dim_dosen
            where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
            group by tahun) data
            where data.tahun<=year(now())-1
            union all
            select sum(Jumlah) as Jumlah,cast(year(now())-2 as char) as tahun from
            (select count(*) as Jumlah,year(tanggal_masuk) as tahun
            from dim_dosen
            where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
            group by tahun) data
            where data.tahun<=year(now())-2
            union all
            select sum(Jumlah) as Jumlah,cast(year(now())-3 as char) as tahun from
            (select count(*) as Jumlah,year(tanggal_masuk) as tahun
            from dim_dosen
            where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
            group by tahun) data
            where data.tahun<=year(now())-3
            union all
            select sum(Jumlah) as Jumlah,cast(year(now())-4 as char) as tahun from
            (select count(*) as Jumlah,year(tanggal_masuk) as tahun
            from dim_dosen
            where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
            group by tahun) data
            where data.tahun<=year(now())-4
            union all 
            select sum(Jumlah) as Jumlah,cast(year(now())-5 as char) as tahun from
            (select count(*) as Jumlah,year(tanggal_masuk) as tahun
            from dim_dosen
            where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
            group by tahun) data
            where data.tahun<=year(now())-5) dosen
        inner join
            (select 
            if(substr(ds.kode_semester,5,1)='2',
            cast(substr(ds.kode_semester,1,4) as int)+1,
            substr(ds.kode_semester,1,4)) tahun,ds.semester_nama,ds.tahun_ajaran,
            count(distinct fms.id_mahasiswa_status) jumlah
              from fact_mahasiswa_status fms
                       inner join dim_mahasiswa dm on fms.id_mahasiswa_status = dm.id_mahasiswa
                       inner join dim_semester ds on fms.id_semester= ds.id_semester
              where (status = 'AK' or status='CS' or status='TA')
                and ds.tahun_ajaran between 
        concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
              group by ds.semester_nama,tahun,ds.tahun_ajaran) data
        on data.tahun=dosen.tahun
        where tahun_ajaran between %(From)s and %(To)s
        order by `Tahun Ajaran`
        ''', {'From': valueFrom, 'To': valueTo})
    # rasio = float(f"{df['Rasio'].agg({'Rasio': np.sum}).iloc[-1]:,.2f}")
    # txtRasio = '1 : ' + str(rasio)
    # if rasio >= 15 and rasio <= 30:
    #     style = {'textAlign': 'center', 'fontSize': 20,
    #              'color': 'rgb(34, 255, 0)'}
    # else:
    #     style = {'textAlign': 'center', 'fontSize': 20,
    #              'color': 'rgb(235, 65, 50)'}
    # dfBar = data.dfRasioDosenBar(valueTahun, valueSemester)
    if (len(df['Tahun Ajaran']) != 0):
        fig = px.line(df, x=df['Tahun Ajaran'], y=df['Rasio'], )
        fig.update_traces(mode='lines+markers')
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


# Tingkat Kepuasan Mahasiswa Terhadap Dosen
@app.callback(
    Output('grf_KepuasanMhs', 'figure'),
    Input('drpdwn_KepuasanMhs', 'value'),
    Input('Smtdrpdwn_KepuasanMhs', 'value')
)
def FillKepuasanMhs(thnAjar, Smt):
    df = data.getDataFrameFromDBwithParams(
        '''select tahun_ajaran 'Tahun Ajaran', semester_nama Semester, nama 'Nama Dosen', 
    Rata2 'Rata-rata',
       case
        when round(Rata2)>=0 and round(Rata2)<=25 then 'KURANG BAIK'
        when round(Rata2)>=26 and round(Rata2)<=50 then 'CUKUP BAIK'
        when round(Rata2)>51 and round(Rata2)<=75 then 'BAIK'
        when round(Rata2)>=76 and round(Rata2)<=100 then 'SANGAT BAIK'
       END AS Predikat
from
(select tahun_ajaran,semester_nama, nama,((avg(q1)+avg(q2)+avg(q3)+avg(q4)+avg(q5)+avg(q6)+
       avg(q7)+avg(q8)+avg(q9)+avg(q10)+avg(q11)+avg(q12))/12) Rata2
from fact_dosen_mengajar fdm
inner join dim_semester ds on fdm.id_semester = ds.id_semester
inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
where ds.tahun_ajaran between 
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1) and id_prodi=9
group by tahun_ajaran,semester_nama,nama) kepuasan
where kepuasan.tahun_ajaran=%(TA)s and kepuasan.semester_nama LIKE %(Smt)s
order by Rata2 asc,tahun_ajaran asc, semester_nama asc''', {'TA': thnAjar, 'Smt': Smt})
    if (len(df['Rata-rata']) != 0):
        fig = px.bar(df, x=df['Rata-rata'], y=df['Nama Dosen'], color=df['Predikat'], orientation='h',
                     hover_name=df['Nama Dosen'],
                     color_discrete_map={
                         'SANGAT BAIK': 'rgb(0, 130, 10)',
                         'BAIK': 'rgb(225, 210, 0)',
                         'CUKUP BAIK': 'orange',
                         'KURANG BAIK': 'red'
                     })
        fig.add_vrect(x0=0, x1=25, fillcolor='red', opacity=0.1)
        fig.add_vrect(x0=25, x1=50, fillcolor='orange', opacity=0.1)
        fig.add_vrect(x0=50, x1=75, fillcolor='yellow', opacity=0.1)
        fig.add_vrect(x0=75, x1=100, fillcolor='green', opacity=0.1)
        fig.update_layout(
            yaxis=dict(tickvals=df['Nama Dosen'].unique())
        )
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


# Daftar Kelompok Matakuliah per Kurikulum
@app.callback(
    Output('grf_matkulKuri', 'figure'),
    Input('grf_matkulKuri', 'id')
)
def graphKurikulum(id):
    df = data.getDataFrameFromDB('''
    select
    count(nama_matakuliah) 'Jumlah Matakuliah',kode_kurikulum 'Kurikulum',
    kelompok_matakuliah 'Kelompok Matakuliah'
    from fact_matakuliah_kurikulum fmk
inner join dim_matakuliah dm on fmk.id_matakuliah = dm.id_matakuliah
inner join dim_kurikulum dk on dk.id_kurikulum = fmk.id_kurikulum
group by kode_kurikulum,kelompok_matakuliah
order by kode_kurikulum,kelompok_matakuliah desc
    ''')
    if (len(df['Jumlah Matakuliah']) != 0):
        fig = px.bar(df, y=df['Jumlah Matakuliah'], x=df['Kurikulum'],
                     color=df['Kelompok Matakuliah'].replace(np.nan, '-'), barmode='stack')
        # fig = px.line(df, x=df['Kelompok Matakuliah'], y=df['Jumlah Matakuliah'])
        # fig.update_traces(mode='lines+markers')
        fig.update_layout(xaxis_title="Kurikulum",
                          yaxis_title="Jumlah Matakuliah", legend_title='Jenis Matakuliah')
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig, None, None


@app.callback(
    Output('grf_matkulBtlTawar', 'figure'),
    Input('Fromdrpdwn_matkulBtlTawar', 'value'),
    Input('Todrpdwn_matkulBtlTawar', 'value')
)
def graphBatalTawar(valueFrom, valueTo):
    dfBatal = data.dfBatalTawar(valueFrom, valueTo)
    if (len(dfBatal['Semester']) != 0):
        fig = px.bar(dfBatal, x=dfBatal['Semester'], y=dfBatal['Jumlah Matakuliah Yang Ditawarkan'],
                     color=dfBatal['Tipe'], barmode='stack')
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


@app.callback(
    Output('grf_dosenBatal', 'figure'),
    Input('TAdrpdwn_dosenBatal', 'value'),
    Input('Smtdrpdwn_dosenBatal', 'value')
)
def graphDosenBatal(valueTA, valueSmt):
    df = data.getDataFrameFromDBwithParams('''
    select concat(ds.semester_nama,' ',ds.tahun_ajaran) Semester, 
    dd.nama Nama, count(dm.nama_matakuliah) 'Jumlah Matakuliah',ds.semester_nama
from fact_dosen_mengajar
inner join dim_dosen dd on fact_dosen_mengajar.id_dosen = dd.id_dosen
inner join dim_semester ds on fact_dosen_mengajar.id_semester = ds.id_semester
inner join dim_matakuliah dm on dm.id_matakuliah = fact_dosen_mengajar.id_matakuliah
where is_batal = 1 
and dm.id_prodi=9
and ds.tahun_ajaran=%(year)s and ds.semester_nama=%(smt)s
and dm.id_matakuliah not in (242,245,5,3,189,188,371,513,512,514,516,283,523,525,519,520,522,524,216)
group by ds.tahun_ajaran, ds.semester_nama, dd.nama, Semester
order by  count(dm.nama_matakuliah) asc
    ''', {'year': valueTA, 'smt': valueSmt})
    if (len(df['Jumlah Matakuliah']) != 0):
        fig = px.bar(df, x=df['Jumlah Matakuliah'], y=df['Nama'], color=df['semester_nama'], barmode='group')
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig
