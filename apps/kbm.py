import dash_table as dt
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from appConfig import app, server
import model.dao_kbm as data
from datetime import date

tbl_IpkMahasiswa = data.getIpkMahasiswa()
tbl_matkulBaru = data.getMatkulKurikulumBaru()
tbl_MatkulBatal = data.getMatkulBatal()
tbl_matkulTawar = data.getMatkulTawar()
tbl_mahasiswaAktif = data.getMahasiswaAktif()
tbl_mahasiswaAsing = data.getMahasiswaAsing()
tbl_persentaseMhsTA = data.getPersentaseMahasiswaTidakAktif()
tbl_jumlahDosenMengajar = data.getDosenMengajar()
tbl_jumlahDTT = data.getPersentaseDosenTidakTetap()
tbl_tingkatKepuasan = data.getTingkatKepuasanDosen()
tbl_RasioDosenMhs = data.getRasioDosenMahasiswa()
tbl_rasioDosenMengajarMhs = data.getRasioDosenMengajarMahasiswa()

listDropdown = []
listAngkatan = []
for x in range(0, 5):
    tahun = 5
    yearnow = date.today().strftime('%Y')
    listDropdown.append(
        str(int(yearnow) - tahun + x) + '/' + str(int(yearnow) - (tahun - 1) + x))

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
            dbc.CardBody([
                dcc.Graph(id='grf_ipkMahasiswa'),
                dbc.Button('Lihat Tabel', id='cll_grfipkMahasiswa', n_clicks=0,
                           style=button_style),
            ])
        ])
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card([
            dt.DataTable(
                id='tbl_MhsIpk',
                columns=[
                    {'name': i, 'id': i} for i in tbl_IpkMahasiswa.columns
                ],
                data=tbl_IpkMahasiswa.to_dict('records'),
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
        id='cll_ipkMahasiswa',
        is_open=False
    )
], style=cont_style)

mahasiswa = dbc.Container([
    dbc.Card([
        html.H5('Mahasiswa',
                style=ttlgrf_style),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.P('Dari', style={'color': 'black'}),
                    dcc.Dropdown(
                        id='Fromdrpdwn_mhs',
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
                        id='Todrpdwn_mhs',
                        options=[{'label': i, 'value': i} for i in listDropdown],
                        value=listDropdown[len(listDropdown) - 1],
                        style={'color': 'black'},
                        clearable=False,
                        placeholder='Sampai',
                    ),
                ]),
            ], width=6),
        ], style={'padding': '15px'}),
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Mahasiswa Aktif', value='mhsaktif',
                        children=[
                            dbc.CardBody([
                                dcc.Graph(id='grf_mahasiswaAktif'),
                                dbc.Button('Lihat Tabel', id='cll_grfmhsaktif', n_clicks=0,
                                           style=button_style),
                            ]),
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Mahasiswa Asing', value='mhsasing',
                        children=[
                            dbc.CardBody([
                                dcc.Graph(id='grf_mahasiswaAsing'),
                                dbc.Button('Lihat Tabel', id='cll_grfmhsasing', n_clicks=0,
                                           style=button_style),
                            ]),
                        ], style=tab_style, selected_style=selected_style)
            ], style=tab_style, id='tab_mahasiswa', value='mhsaktif'
            )
        ])
    ], style=cardgrf_style
    ),
    dbc.Collapse(
        id='cll_tblmahasiswa',
        is_open=False
    )
], style=cont_style)

mahasiswaTA = dbc.Container([
    dbc.Card([
        html.H5('Mahasiswa Tidak Aktif terhadap Mahasiswa Aktif',
                style=ttlgrf_style),
        dbc.CardBody([
            html.Div([
                html.P('Tahun Angkatan', style={'color': 'black'}),
                dcc.Dropdown(
                    id='Angkatandrpdwn_MhsTA',
                    options=[{'label': i, 'value': i} for i in listAngkatan],
                    value=listAngkatan[len(listAngkatan) - 1],
                    style={'color': 'black'},
                    clearable=False,
                    placeholder='Tahun Angkatan',
                ),
            ]),
            dcc.Graph(id='grf_MhsTA'),
            dbc.Button('Lihat Tabel', id='cll_grfMhsTA', n_clicks=0, style=button_style),
        ])
    ], style=cardgrf_style
    ),
    dbc.Collapse(
        dbc.Card([
            dt.DataTable(
                id='tbl_MhsTA',
                columns=[
                    {'name': i, 'id': i} for i in tbl_persentaseMhsTA.columns
                ],
                data=tbl_persentaseMhsTA.to_dict('records'),
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
        id='cll_tblMhsTA',
        is_open=False
    )
], style=cont_style)

jumlahDosen = dbc.Container([
    dbc.Card([
        html.H5('Dosen',
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
            ], width=6),
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
            ], width=6),
        ], style={'padding': '15px'}),
        dcc.Tabs([
            dcc.Tab(label='Dosen Mengajar', value='dosenAjar',
                    children=[
                        dbc.CardBody([
                            dcc.Graph(id='grf_dosenAjar'),
                            dbc.Button('Lihat Tabel', id='cll_grfdosenAjar', n_clicks=0, style=button_style),
                        ])
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Dosen Tidak Tetap : Dosen', value='dosenNon',
                    children=[
                        dbc.CardBody([
                            dcc.Graph(id='grf_dosenNon'),
                            dbc.Button('Lihat Tabel', id='cll_grfdosenNon', n_clicks=0, style=button_style),
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
            dcc.Graph(id='grf_KepuasanMhs'),
            dbc.Button('Lihat Tabel', id='cll_grfKepuasanMhs', n_clicks=0, style=button_style),
        ])
    ], style=cardgrf_style
    ),
    dbc.Collapse(
        dbc.Card([
            dt.DataTable(
                id='tbl_KepuasanMhs',
                columns=[
                    {'name': i, 'id': i} for i in tbl_tingkatKepuasan.columns
                ],
                data=tbl_tingkatKepuasan.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'padding': '10px', 'overflowX': 'auto'},
                style_header={'font-size': '80%', 'textAlign': 'center'},
                style_data={'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 95},
                export_format='xlsx',
                page_size=10,
            )
        ], style=cardtbl_style
        ),
        id='cll_tblKepuasanMhs',
        is_open=False
    )
], style=cont_style)

Dosen = dbc.Container([
    dbc.Card([
        html.H5('Rasio Dosen',
                style=ttlgrf_style),
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Rasio Dosen : Mahasiswa', value='dosen',
                        children=[
                            dbc.Card([
                                dt.DataTable(
                                    id='tbl_DosenMhs',
                                    columns=[
                                        {'name': i, 'id': i} for i in tbl_RasioDosenMhs.columns
                                    ],
                                    data=tbl_RasioDosenMhs.to_dict('records'),
                                    sort_action='native',
                                    sort_mode='multi',
                                    style_table={'padding': '10px', 'overflowX': 'auto'},
                                    style_header={'font-size': '80%', 'textAlign': 'center'},
                                    style_data={'font-size': '80%', 'textAlign': 'center'},
                                    style_cell={'width': 95},
                                    export_format='xlsx',
                                    page_size=10,
                                )
                            ], )
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Rasio Dosen Mengajar : Mahasiswa', value='dosenMengajar',
                        children=[
                            dbc.Card([
                                dt.DataTable(
                                    id='tbl_DosenMengajarMhs',
                                    columns=[
                                        {'name': i, 'id': i} for i in tbl_rasioDosenMengajarMhs.columns
                                    ],
                                    data=tbl_rasioDosenMengajarMhs.to_dict('records'),
                                    sort_action='native',
                                    sort_mode='multi',
                                    style_table={'padding': '10px', 'overflowX': 'auto'},
                                    style_header={'font-size': '80%', 'textAlign': 'center'},
                                    style_data={'font-size': '80%', 'textAlign': 'center'},
                                    style_cell={'width': 95},
                                    export_format='xlsx',
                                    page_size=10,
                                )
                            ], )
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

matkul = dbc.Container([
    dbc.Card([
        html.H5('Daftar Matakuliah',
                style=ttlgrf_style),
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Kurikulum', value='kurikulum',
                        children=[
                            dt.DataTable(
                                id='tbl_matkulBaru',
                                columns=[
                                    {'name': i, 'id': i} for i in tbl_matkulBaru.columns
                                ],
                                data=tbl_matkulBaru.to_dict('records'),
                                sort_action='native',
                                sort_mode='multi',
                                style_table={'padding': '10px', 'overflowX': 'auto'},
                                style_header={'font-size': '80%', 'textAlign': 'center'},
                                style_data={'font-size': '80%', 'textAlign': 'center'},
                                style_cell={'width': 95},
                                export_format='xlsx',
                                page_size=10,
                            )
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Batal dengan Keterangan Dosen', value='batal',
                        children=[
                            dt.DataTable(
                                id='tbl_matkulBatal',
                                columns=[
                                    {'name': i, 'id': i} for i in tbl_MatkulBatal.columns
                                ],
                                data=tbl_MatkulBatal.to_dict('records'),
                                sort_action='native',
                                sort_mode='multi',
                                style_table={'padding': '10px', 'overflowX': 'auto'},
                                style_header={'font-size': '80%', 'textAlign': 'center'},
                                style_data={'font-size': '80%', 'textAlign': 'center'},
                                style_cell={'width': 95},
                                export_format='xlsx',
                                page_size=10,
                            )
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Ditawarkan Setiap Semester', value='ts',
                        children=[
                            dt.DataTable(
                                id='tbl_matkulTawar',
                                columns=[
                                    {'name': i, 'id': i} for i in tbl_matkulTawar.columns
                                ],
                                data=tbl_matkulTawar.to_dict('records'),
                                sort_action='native',
                                sort_mode='multi',
                                style_table={'padding': '10px', 'overflowX': 'auto'},
                                style_header={'font-size': '80%', 'textAlign': 'center'},
                                style_data={'font-size': '80%', 'textAlign': 'center'},
                                style_cell={'width': 95},
                                export_format='xlsx',
                                page_size=10,
                            )
                        ], style=tab_style, selected_style=selected_style)
            ], style=tab_style, id='tab_kurikulum', value='kurikulum'
            )
        ])
    ], style=cardtbl_style
    ),
    dbc.Collapse(
        id='cll_tblmatkul',
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
    html.Div([mahasiswa]),
    html.Div([mahasiswaTA]),
    html.Div([jumlahDosen]),
    html.Div([tingkatKepuasan]),
    html.Div([Dosen]),
    html.Div([matkul], style={'margin-bottom': '50px'}),
    dbc.Container([
        dcc.Link([
            dbc.Button('^', style=buttonLink_style),
        ], href='#name'),
    ], style={'margin-left': '90%'}),
], style={'width': '100%'})


# CALLBACK COLLAPSE
@app.callback(
    Output('cll_ipkMahasiswa', 'is_open'),
    Input('cll_grfipkMahasiswa', 'n_clicks'),
    State('cll_ipkMahasiswa', 'is_open')
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('cll_tblmahasiswa', 'is_open'),
    Output('cll_tblmahasiswa', 'children'),
    [Input("cll_grfmhsaktif", "n_clicks"),
     Input("cll_grfmhsasing", "n_clicks"),
     Input("tab_mahasiswa", "value")],
    [State("cll_tblmahasiswa", "is_open")])
def toggle_collapse(naktif, nasing, mhs, is_open):
    isiAktif = dbc.Card(
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
    isiAsing = dbc.Card(
        dt.DataTable(
            id='tbl_mahasiswaAsing',
            columns=[{"name": i, "id": i} for i in tbl_mahasiswaAsing.columns],
            data=tbl_mahasiswaAsing.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    ),
    if naktif and mhs == 'mhsaktif':
        return not is_open, isiAktif
    if nasing and mhs == 'mhsasing':
        return not is_open, isiAsing
    return is_open, None


@app.callback(
    Output('cll_tblMhsTA', "is_open"),
    [Input("cll_grfMhsTA", "n_clicks")],
    [State('cll_tblMhsTA', "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('cll_tblJmlDosen', 'is_open'),
    Output('cll_tblJmlDosen', 'children'),
    [Input("cll_grfdosenAjar", "n_clicks"),
     Input("cll_grfdosenNon", "n_clicks"),
     Input("tab_Jmldosen", "value")],
    [State('cll_tblJmlDosen', "is_open")])
def toggle_collapse(najar, non, dsn, is_open):
    isiAjar = dbc.Card(
        dt.DataTable(
            id='tbl_Dosen',
            columns=[
                {'name': i, 'id': i} for i in tbl_jumlahDosenMengajar.columns
            ],
            data=tbl_jumlahDosenMengajar.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'font-size': '80%', 'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            export_format='xlsx',
            page_size=10,
        ), style=cardtbl_style
    ),
    isiNon = dbc.Card(
        dt.DataTable(
            id='tbl_DTT',
            columns=[
                {'name': i, 'id': i} for i in tbl_jumlahDTT.columns
            ],
            data=tbl_jumlahDTT.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'font-size': '80%', 'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            export_format='xlsx',
            page_size=10,
        ), style=cardtbl_style
    ),
    if najar and dsn == 'dosenAjar':
        return not is_open, isiAjar
    if non and dsn == 'dosenNon':
        return not is_open, isiNon
    return is_open, None


@app.callback(
    Output('cll_tblKepuasanMhs', "is_open"),
    [Input("cll_grfKepuasanMhs", "n_clicks")],
    [State('cll_tblKepuasanMhs', "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# CALLBACK GRAPH
@app.callback(
    Output("grf_ipkMahasiswa", 'figure'),
    Input('Fromdrpdwn_ipkMahasiswa', 'value'),
    Input('Todrpdwn_ipkMahasiswa', 'value'),
)
def FillIpkMahasiswa(valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''select ds.tahun_ajaran 'Tahun Ajaran', ds.semester_nama Semester, avg(ipk) as "Rata-Rata"
from fact_mahasiswa_status fms 
inner join dim_semester ds on ds.id_semester = fms.id_semester
where ds.tahun_ajaran between %(From)s and %(To)s and fms.status = 'AK'
group by ds.tahun_ajaran, ds.semester_nama
order by ds.tahun_ajaran, ds.semester_nama''', {'From': valueFrom, 'To': valueTo})
    fig = px.bar(df, x=df['Tahun Ajaran'], y=df['Rata-Rata'], color=df['Semester'])
    fig.update_layout(barmode='group')
    return fig


@app.callback(
    Output("grf_mahasiswaAktif", 'figure'),
    Input('Fromdrpdwn_mhs', 'value'),
    Input('Todrpdwn_mhs', 'value'),
)
def FillAktif(valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''select ds.tahun_ajaran 'Tahun Ajaran', ds.semester_nama Semester, 
    count(*) as 'Jumlah Mahasiswa Aktif' from fact_mahasiswa_status fms
inner join dim_semester ds on ds.id_semester = fms.id_semester
where fms.status = 'AK' and ds.tahun_ajaran between %(From)s and %(To)s
group by ds.tahun_ajaran, ds.semester_nama
order by ds.tahun_ajaran, ds.semester_nama
''', {'From': valueFrom, 'To': valueTo})
    fig = px.bar(df, x=df['Tahun Ajaran'], y=df['Jumlah Mahasiswa Aktif'], color=df['Semester'])
    fig.update_layout(barmode='group')
    return fig


@app.callback(
    Output("grf_mahasiswaAsing", 'figure'),
    Input('Fromdrpdwn_mhs', 'value'),
    Input('Todrpdwn_mhs', 'value'),
)
def FillAsing(valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''
    select ds.tahun_ajaran 'Tahun Ajaran', 
    count(*) as 'Jumlah Mahasiswa Asing' from fact_mahasiswa_status fms
inner join dim_semester ds on ds.id_semester = fms.id_semester
inner join dim_mahasiswa dm on dm.id_mahasiswa = fms.id_mahasiswa
where warga_negara ='WNA'and tahun_ajaran between %(From)s and %(To)s
group by tahun_ajaran
order by tahun_ajaran ''', {'From': valueFrom, 'To': valueTo})
    fig = px.bar(df, x=df['Tahun Ajaran'], y=df['Jumlah Mahasiswa Asing'])
    return fig


@app.callback(
    Output('grf_MhsTA', 'figure'),
    Input('Angkatandrpdwn_MhsTA', 'value')
)
def MhsTA(valueAngkatan):
    df = data.getDataFrameFromDBwithParams('''select ak.tahun_angkatan 'Tahun Angkatan', 
    ak.tahun_ajaran, 
    ak.jumlah 'Mahasiswa Aktif',
    concat(if(substr(ak.kode_semester,5,1)='1','Ganjil','Genap')) Semester,
    ifnull(ta.jumlah,0) 'Mahasiswa Tidak Aktif',
    IFNULL(ta.jumlah / ak.jumlah * 100,0) Persentase
from (select ds.tahun_ajaran,tahun_angkatan, ds.kode_semester,count(distinct (dm.nim)) jumlah
      from fact_mahasiswa_status fms
               inner join dim_mahasiswa dm on fms.id_mahasiswa = dm.id_mahasiswa
               inner join dim_semester ds on fms.id_semester= ds.id_semester
      where tahun_angkatan = %(TA)s
        and (status = 'AK'or status='CS')
        and ds.tahun_ajaran between 
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
        and id_prodi=9
      group by ds.tahun_ajaran,tahun_angkatan,ds.kode_semester) ak
    left join
     (select ds.tahun_ajaran,tahun_angkatan, ds.kode_semester, count(distinct (dm.nim)) jumlah
      from fact_mahasiswa_status fms
               inner join dim_mahasiswa dm on fms.id_mahasiswa = dm.id_mahasiswa
               inner join dim_semester ds on fms.id_semester= ds.id_semester
      where tahun_angkatan = %(TA)s
        and status = 'TA'
        and ds.tahun_ajaran between 
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
        and id_prodi=9
      group by ds.tahun_ajaran,tahun_angkatan, ds.kode_semester) ta
on ak.tahun_angkatan = ta.tahun_angkatan
and ak.kode_semester=ta.kode_semester
order by ak.tahun_ajaran asc, Semester asc''', {'TA': valueAngkatan})
    fig = px.bar(x=df['tahun_ajaran'], y=df['Persentase'], color=df['Semester'], barmode='group',
                 labels=dict(x="Tahun Ajaran", y="Persentase", color="Semester"))
    fig.update_yaxes(categoryorder='category ascending')
    fig.update_layout(xaxis_title="Tahun Ajaran",
                      yaxis_title="Persentase",
                      yaxis=dict(tickformat=",.2f"))
    return fig


@app.callback(
    Output('grf_dosenAjar', 'figure'),
    Input('Fromdrpdwn_Jmldosen', 'value'),
    Input('Todrpdwn_Jmldosen', 'value')
)
def DosenAjar(valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''
    select tahun_ajaran 'Tahun Ajaran',semester_nama 'Semester',
    count(distinct fdm.id_dosen) 'Jumlah' from fact_dosen_mengajar fdm
inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
inner join dim_semester ds on fdm.id_semester = ds.id_semester
where tahun_ajaran between %(From)s and %(To)s
group by tahun_ajaran, semester_nama
order by tahun_ajaran asc,semester_nama asc''', {'From': valueFrom, 'To': valueTo})
    fig = px.bar(df, x=df['Tahun Ajaran'], y=df['Jumlah'], color=df['Semester'], barmode='group')
    return fig


@app.callback(
    Output('grf_dosenNon', 'figure'),
    Input('Fromdrpdwn_Jmldosen', 'value'),
    Input('Todrpdwn_Jmldosen', 'value')
)
def DosenNon(valueFrom, valueTo):
    df = data.getDataFrameFromDBwithParams('''
    select semua.tahun_ajaran 'Tahun Ajaran',semua.semester_nama 'Semester',
       tetap.jumlah 'Dosen Tidak Tetap',semua.jumlah 'Semua Dosen',(tetap.jumlah/semua.jumlah)*100 as 'Persentase' from
(select tahun_ajaran,semester_nama,count(distinct fdm.id_dosen) jumlah from fact_dosen_mengajar fdm
inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
inner join dim_semester ds on fdm.id_semester = ds.id_semester
where tahun_ajaran between %(From)s and %(To)s and status_dosen='Kontrak'
group by tahun_ajaran, semester_nama) tetap,
(select tahun_ajaran,semester_nama,count(distinct fdm.id_dosen) jumlah from fact_dosen_mengajar fdm
inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
inner join dim_semester ds on fdm.id_semester = ds.id_semester
where tahun_ajaran between %(From)s and %(To)s
group by tahun_ajaran, semester_nama) semua
where semua.semester_nama=tetap.semester_nama and
      semua.tahun_ajaran=tetap.tahun_ajaran
order by semua.tahun_ajaran asc, semua.semester_nama asc''', {'From': valueFrom, 'To': valueTo})
    fig = px.line(df, x=df['Tahun Ajaran'], y=df['Persentase'], color=df['Semester'])
    fig.update_traces(mode='lines+markers')
    return fig


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
order by nama asc,tahun_ajaran asc, semester_nama asc''', {'TA': thnAjar, 'Smt': Smt})
    fig = px.bar(df, x=df['Rata-rata'], y=df['Nama Dosen'], color=df['Predikat'], orientation='h',
                 hover_name=df['Nama Dosen'],
                 color_discrete_map={
                     'SANGAT BAIK': 'rgb(0, 130, 10)',
                     'BAIK': 'rgb(225, 210, 0)',
                     'CUKUP BAIK': 'orange',
                     'KURANG BAIK': 'red'
                 })
    return fig
