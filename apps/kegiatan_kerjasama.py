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

card_style = {
    'border': '1px solid #fafafa',
    'border-radius': '10px',
    'margin-top': '10px',
    'padding': '10px',
    'justify-content': 'center',
    'width': '100%',
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

kegiatan_dosen = dbc.Container([
    dbc.Card([
        html.H5('DOSEN',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Kegiatan Rekognisi Dosen', value='rekognisiDosen',
                    children=[
                        dt.DataTable(
                            id='tbl_rekognisiDosen',
                            columns=[
                                {'name': i, 'id': i} for i in dfrekognisiDosen.columns
                            ],
                            data=dfrekognisiDosen.to_dict('records'),
                            sort_action='native',
                            sort_mode='multi',
                            style_table={'padding': '10px', 'overflowX': 'auto'},
                            style_header={'textAlign': 'center'},
                            style_data={'font-size': '80%', 'textAlign': 'center'},
                            style_cell={'width': 95},
                            page_size=10,
                            export_format='xlsx'
                        )
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Jumlah Kegiatan Dosen Tiap Tahun', value='kegDosen',
                    children=[
                        dcc.Dropdown(
                            id='drpdwn_kegDosen',
                            options=[{'label': '2020', 'value': '2020'},
                                     {'label': '2019', 'value': '2019'},
                                     {'label': '2018', 'value': '2018'}, ],
                            value='2020',
                            style={'color': 'black'},
                            clearable=False,
                        ),
                        dbc.CardLink([
                            dcc.Graph(id='grf_kegDosen')
                        ], id='cll_grfkegDosen',
                            n_clicks=0),
                    ],
                    style=tab_style, selected_style=selected_style),
        ], style=tabs_styles, id='tab_kegDosen', value='rekognisiDosen'),
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_kegDosen',
        is_open=False
    )
], style=cont_style)

kegiatanMahasiswa = dbc.Container([
    dbc.Card([
        html.H5('PRESTASI MAHASISWA',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Prestasi Akademik Mahasiswa', value='prestasiMhs',
                    children=[
                        dt.DataTable(
                            id='tbl_prestasiMhs',
                            columns=[
                                {'name': i, 'id': i} for i in dfprestasiakademik.columns
                            ],
                            data=dfprestasiakademik.to_dict('records'),
                            sort_action='native',
                            sort_mode='multi',
                            style_table={'padding': '10px', 'overflowX': 'auto'},
                            style_header={'textAlign': 'center'},
                            style_data={'font-size': '80%', 'textAlign': 'center'},
                            style_cell={'width': 95},
                            page_size=10,
                            export_format='xlsx'
                        )
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Prestasi Non Akademik Mahasiswa', value='NonprestasiMhs',
                    children=[
                        dt.DataTable(
                            id='tbl_NonprestasiMhs',
                            columns=[
                                {'name': i, 'id': i} for i in dfprestasinonakademik.columns
                            ],
                            data=dfprestasinonakademik.to_dict('records'),
                            sort_action='native',
                            sort_mode='multi',
                            style_table={'padding': '10px', 'overflowX': 'auto'},
                            style_header={'textAlign': 'center'},
                            style_data={'font-size': '80%', 'textAlign': 'center'},
                            style_cell={'width': 95},
                            page_size=10,
                            export_format='xlsx'
                        )
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
                            dcc.Graph(id='grf_Kulum')
                        ], id='cll_grfKulum',
                            n_clicks=0),
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Jumlah Peserta Kegiatan Kuliah Umum', value='pesertaKulum',
                    children=[
                        dcc.Dropdown(
                            id='drpdwn_pesertaKulum',
                            options=[{'label': '2019', 'value': '2019'},
                                     {'label': '2018', 'value': '2018'},
                                     {'label': '2017', 'value': '2017'}, ],
                            value='2019',
                            style={'color': 'black'},
                            clearable=False,
                        ),
                        dbc.CardLink([
                            dcc.Graph(id='grf_pesertaKulum')
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
    html.Div([kerjasama], style={'margin-bottom': '50px'})
], style={'justify-content': 'center'})


# CONTROL COLLAPSE
@app.callback(
    Output("cll_kegDosen", "is_open"),
    Output("cll_kegDosen", "children"),
    [Input("cll_grfkegDosen", "n_clicks"),
     Input("tab_kegDosen", "value")],
    [State("cll_kegDosen", "is_open")])
def toggle_collapse(nDosen, tab_keg, is_open):
    isiKegDosen = dt.DataTable(
        id='tbl_kegDosen',
        columns=[
            {'name': i, 'id': i} for i in dfkegiatandosen.columns
        ],
        data=dfkegiatandosen.to_dict('records'),
        sort_action='native',
        sort_mode='multi',
        style_table={'padding': '10px', 'overflowX': 'auto'},
        style_header={'textAlign': 'center'},
        style_data={'font-size': '80%', 'textAlign': 'center'},
        style_cell={'width': 95},
        page_size=10,
        export_format='xlsx'
    )
    if nDosen and tab_keg == 'kegDosen':
        return not is_open, isiKegDosen
    return is_open, None


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


# APPS
@app.callback(
    Output('grf_kegDosen', 'figure'),
    Input('grf_kegDosen', 'id'),
    Input('drpdwn_kegDosen', 'value')
)
def graphKegDosen(id, waktu):
    df = data.getDataFrameFromDBwithParams('''
    select tahun, nama,count(fkd.id_dosen) 'Jumlah Kegiatan' from fact_kegiatan_dosen fkd
inner join dim_kegiatan dk on fkd.id_kegiatan = dk.id_kegiatan
inner join dim_date dd on dd.id_date=dk.id_tanggal_mulai
inner join dim_dosen d on fkd.id_dosen = d.id_dosen
where tahun = %(tahun)s
group by tahun,nama
order by tahun asc, nama asc
    ''', {'tahun': waktu})
    fig = px.bar(df, y=df['Jumlah Kegiatan'], x=df['nama'])
    fig.update_layout(xaxis_tickangle=-45)
    return fig


@app.callback(
    Output('grf_Kulum', 'figure'),
    Input('grf_Kulum', 'id')
)
def graphKulum(id):
    df = dfKulum
    fig = px.line(df, x=df['tahun'], y=df['jumlah_kuliah_umum'])
    fig.update_traces(mode='lines+markers')
    return fig


@app.callback(
    Output('grf_pesertaKulum', 'figure'),
    Input('grf_pesertaKulum', 'id'),
    Input('drpdwn_pesertaKulum', 'value')
)
def graphKegPeserta(id, waktu):
    df = data.getDataFrameFromDBwithParams('''
    select tahun, nama_kegiatan,count(id_mahasiswa) jumlah from fact_kegiatan_mahasiswa fkm
inner join dim_kegiatan dk on fkm.id_kegiatan = dk.id_kegiatan
inner join dim_date dd on dd.id_date=dk.id_tanggal_mulai
where jenis_kegiatan='KULIAH UMUM'
and tahun=%(tahun)s
group by tahun,dk.id_kegiatan,dk.nama_kegiatan
order by tahun asc
    ''', {'tahun': waktu})
    fig = px.bar(df, y=df['nama_kegiatan'], x=df['jumlah'],orientation='h')
    return fig

# @app.callback(
#     Output("grf_kegKuliah", 'figure'), Input('grf_kegKuliah', 'id')
# )
# def FillIKUwithMOU(id):
#     df = pd.read_sql('''select ddselesai.tahun, count(dim_kegiatan.nama_kegiatan) as jumlah_kuliah_umum
#      -- , ddmulai.tanggal as tanggal_mulai, ddselesai.tanggal as tanggal_selesai
# from dim_kegiatan
# inner join dim_perjanjian dp on dim_kegiatan.id_perjanjian = dp.id_perjanjian
# inner join dim_date ddmulai on ddmulai.id_date = dim_kegiatan.id_tanggal_mulai
# inner join dim_date ddselesai on ddselesai.id_date = dim_kegiatan.id_tanggal_selesai
# where jenis_kegiatan = 'KULIAH UMUM' and dim_kegiatan.id_perjanjian is not null
# group by ddselesai.tahun''', con)
#     fig = px.bar(df, x=df['tahun'], y=df['jumlah_kuliah_umum'])
#     return fig
#
#
# @app.callback(
#     Output("grf_rekogDosen", 'figure'), Input('grf_rekogDosen', 'id')
# )
# def FillKegDosen(id):
#     df = pd.read_sql('''select Tahun, count(*) as jumlah from fact_rekognisi_dosen
# inner join dim_date on dim_date.id_date = fact_rekognisi_dosen.id_tanggal_mulai
# group by tahun
# order by tahun''', con)
#     fig = px.line(df, x=df['Tahun'], y=df['jumlah'])
#     fig.update_traces(mode='lines+markers')
#     return fig
#
#
# @app.callback(
#     Output("grf_ipkDosenKeg", 'figure'), Input('grf_ipkDosenKeg', 'id')
# )
# def FillIpkDosen(id):
#     df = pd.read_sql('''select ds.tahun_ajaran, ds.semester_nama, round(avg(fid.ipk),2) as "Rata-Rata"
# from fact_ipk_dosen fid
# inner join dim_dosen ddo on ddo.id_dosen = fid.id_dosen
# inner join dim_semester ds on ds.id_semester = fid.id_semester
# group by ds.tahun_ajaran, ds.semester_nama
# order by ds.tahun_ajaran, ds.semester_nama''', con)
#     fig = px.bar(df, x=df['tahun_ajaran'], y=df['Rata-Rata'], color=df['semester_nama'])
#     fig.update_layout(barmode='group')
#     return fig
