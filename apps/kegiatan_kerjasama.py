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

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

# Kegiatan Dosen
dfrekognisiDosen = data.getPrestasiRekognisiDosen()
dfkegiatandosen = data.getKegiatanDosen()
# Prestasi Mahasiswa
dfprestasiakademik = data.getPrestasiAkademik()
dfprestasinonakademik = data.getPrestasiNonAkademik()
# Kulum
dfKulum = data.getKegKulUmMOU()
dfrerataKulum = data.getRerataJumlPesertaKulUm()
dfRekognisiDosenGraf = data.getRekognisiDosen()

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


kegiatan_dosen = dbc.Container([
    dbc.Card([
        html.H5('DOSEN',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Kegiatan Rekognisi Dosen', value='rekognisiDosen',
                    children=[
                        dbc.Container([
                            dbc.Card([
                                dbc.CardLink(
                                    dbc.CardBody([
                                        dbc.Col([
                                            html.Br(),
                                            html.H6('Filter Wilayah :'),
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
                                        ], width=3),
                                        dcc.Graph(
                                            id='grf_rekognisiDosen',
                                        ),
                                        dbc.Button('Lihat Tabel',
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

            #######################################################
            dcc.Tab(label='Jumlah Kegiatan Dosen Tiap Tahun', value='kegDosen',
                    children=[
                        dbc.Container([
                            dbc.Col([
                                html.Br(),
                                html.H6('Filter tahun :'),
                                dcc.Dropdown(
                                    id='drpdwn_kegDosen',
                                    options=[
                                        {'label': '2022', 'value': '2022'},
                                        {'label': '2021', 'value': '2021'},
                                        {'label': '2020', 'value': '2020'},
                                        {'label': '2019', 'value': '2019'},
                                        {'label': '2018', 'value': '2018'},
                                        {'label': '2017', 'value': '2017'},
                                    ],
                                    value='2020',
                                    style={'color': 'black'},
                                    clearable=False,
                                ),
                            ], width=3),
                            dbc.CardLink([
                                dcc.Graph(id='grf_kegDosen'),
                                dbc.Button('Lihat Tabel',
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
        html.H5('PRESTASI MAHASISWA',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Prestasi Akademik Mahasiswa', value='prestasiMhs',
                    children=[
                        dbc.CardLink([
                            dbc.Col([
                                html.Br(),
                                html.H6('Filter Wilayah :'),
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
                            ], width=3),
                            dcc.Graph(id='grf_prestasiakademik'),
                            dbc.Button('Lihat Tabel',
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
                        dbc.CardLink([
                            dbc.Col([
                                html.Br(),
                                html.H6('Filter Wilayah :'),
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
                            ], width=3),
                            dcc.Graph(id='grf_prestasinonakademik'),
                            dbc.Button('Lihat Tabel',
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
        html.H5('KEGIATAN KULIAH UMUM',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Jumlah Kegiatan Kuliah Umum Yang Mempunya Perjanjian Kerjasama', value='Kulum',
                    children=[
                        dbc.CardLink([
                            dcc.Graph(id='grf_Kulum'),
                            dbc.Button('Lihat Tabel',
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
                                        {'name': i, 'id': i} for i in dfKulum.columns
                                    ],
                                    data=dfKulum.to_dict('records'),
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
            dcc.Tab(label='Jumlah Peserta Kegiatan Kuliah Umum', value='pesertaKulum',
                    children=[
                        dbc.Col([
                            html.Br(),
                            html.H6('Filter tahun :'),
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
                        ], width=3),
                        dbc.CardLink([
                            dcc.Graph(id='grf_pesertaKulum'),
                            dbc.Button('Lihat Tabel',
                                       id='cll_grfpesertaKulum',
                                       n_clicks=0,
                                       style=button_style)
                        ], id='cll_grfpesertaKulum',
                            n_clicks=0),
                    ],
                    style=tab_style, selected_style=selected_style),
        ], style=tabs_styles, id='tab_Kegkulum', value='Kulum'),
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_Kegkulum',
        is_open=False
    )
], style=cont_style)

layout = html.Div([
    html.Div(html.H1('Analisis Kegiatan dan Kerjasama',
                     style={'margin-top': '30px', 'textAlign': 'center'}
                     )
             ),
    html.Div([kegiatan_dosen]),
    html.Div([kegiatanMahasiswa]),
    html.Div([kerjasama], style={'margin-bottom': '50px'}),
    dbc.Container([
        dcc.Link([
            dbc.Button('^', style=buttonLink_style),
        ], href='#name'),
    ], style={'margin-left': '90%'}),
], style={'justify-content': 'center'})


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
order by `Jumlah Kegiatan` desc
    ''', {'tahun': waktu})
    fig = px.bar(df, y=df['Jumlah Kegiatan'], x=df['Nama Dosen'])
    fig.update_layout(xaxis_tickangle=-45)
    return fig


@app.callback(
    Output('grf_Kulum', 'figure'),
    Input('grf_Kulum', 'id'),
)
def graphKulum(id):
    df = dfKulum
    fig = px.line(df, x=df['Tahun'], y=df['Jumlah Kuliah Umum'])
    fig.update_traces(mode='lines+markers')
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
    fig = px.bar(df, y=df['Nama Kegiatan'], x=df['jumlah'],orientation='h')
    return fig

@app.callback(
    Output('grf_rekognisiDosen', 'figure'),
    Input('grf_rekognisiDosen', 'id'),
    Input('drpdwn_kegRekoginisiDosen', 'value')
)
def graphKegRecognisiDosen(id,wilayahValue):
    #df = dfRekognisiDosenGraf
    df = data.getDataFrameFromDBwithParams('''
        select tahun as 'Tahun',count(judul_rekognisi) as 'Jumlah Rekognisi'
from fact_rekognisi_dosen frd
inner join dim_date dd on dd.id_date=frd.id_tanggal_mulai
inner join dim_dosen d on frd.id_dosen = d.id_dosen
where d.id_prodi = 9
  
  and wilayah = %(wilayah)s
group by tahun
order by tahun desc
        ''', {'wilayah': wilayahValue})
    fig = px.bar(df, y=df['Jumlah Rekognisi'], x=df['Tahun'], orientation='v')
    return fig

@app.callback(
    Output('grf_prestasinonakademik', 'figure'),
    Input('grf_prestasinonakademik', 'id'),
    Input('drpdwn_prestasiNonAkademikMahasiswa', 'value')
)
def graphPrestasiNonAkademik(id,wilayahValue):
    #df = dfRekognisiDosenGraf
    df = data.getDataFrameFromDBwithParams('''
        select distinct tahun as 'Tahun', count(fact.wilayah_nama) as 'Jumlah Prestasi Mahasiswa'
    from fact_kegiatan_mahasiswa fact
    inner join dim_kegiatan keg on keg.id_kegiatan = fact.id_kegiatan
    inner join dim_date dat on keg.id_tanggal_mulai = dat.id_date
    where sifat_partisipasi = 'PM' and is_akademis = 0 and fact.wilayah_nama = %(wilayah)s
group by fact.wilayah_nama,tahun
order by tahun desc 
        ''', {'wilayah': wilayahValue})
    fig = px.bar(df, y=df['Jumlah Prestasi Mahasiswa'], x=df['Tahun'], orientation='v')
    return fig


@app.callback(
    Output('grf_prestasiakademik', 'figure'),
    Input('grf_prestasiakademik', 'id'),
    Input('drpdwn_prestasiAkademikMahasiswa', 'value')
)
def graphPrestasiAkademik(id,wilayahValue):
    #df = dfRekognisiDosenGraf
    df = data.getDataFrameFromDBwithParams('''
        select distinct tahun as 'Tahun', count(fact.wilayah_nama) as 'Jumlah Prestasi Mahasiswa'
    from fact_kegiatan_mahasiswa fact
    inner join dim_kegiatan keg on keg.id_kegiatan = fact.id_kegiatan
    inner join dim_date dat on keg.id_tanggal_mulai = dat.id_date
    where sifat_partisipasi = 'PM' and is_akademis = 1 and fact.wilayah_nama = %(wilayah)s
group by fact.wilayah_nama,tahun
order by tahun desc
        ''', {'wilayah': wilayahValue})
    fig = px.bar(df, y=df['Jumlah Prestasi Mahasiswa'], x=df['Tahun'], orientation='v')
    return fig
