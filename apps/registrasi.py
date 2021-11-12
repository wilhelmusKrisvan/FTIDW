import dash
import pandas as pd
import dash_table as dt
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from dash.dependencies import Input, Output, State
from dask.array.tests.test_array_core import test_blockwise_1_in_shape_I
from sqlalchemy import create_engine
from appConfig import app, server

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

dfbebanajarinf = pd.read_sql('''select ds.tahun_ajaran, ds.semester_nama, dd.nik, dd.nama, dd.nama_gelar, dm.kode_matakuliah, dm.nama_matakuliah, dm.sks,fact_dosen_mengajar.sifat_mengajar
from fact_dosen_mengajar
inner join dim_semester ds on fact_dosen_mengajar.id_semester = ds.id_semester
inner join dim_dosen dd on fact_dosen_mengajar.id_dosen = dd.id_dosen
inner join dim_matakuliah dm on fact_dosen_mengajar.id_matakuliah = dm.id_matakuliah
where is_batal = 0 and dd.id_prodi = 9
order by ds.tahun_ajaran, ds.semester, dd.nama''', con)

tbl_dosenTetap = pd.read_sql('''select nama, nik, nomor_induk,tipe_nomor_induk,jenis_kelamin,no_sertifikat, status_yayasan from dim_dosen
where id_prodi = 9 and status_yayasan = "TETAP"''', con)

tbl_dosenIndustri = pd.read_sql('''select * from dim_dosen''', con)

dfjafunglast = pd.read_sql('''
select replace(jabatan_dosen,'T','') as 'Jabatan Dosen', count(*) as 'Jumlah' from (    
    select distinct jabatan_dosen, data.id_dosen from(
        select factGol.id_dosen, max(id_tanggal_terima_jabatan) as id_tanggal_terima_jabatan from fact_golongan_dosen_pemerintah factGol
        inner join dim_dosen dimD on factGol.id_dosen = dimD.id_dosen
        inner join dim_date tglJabat on tglJabat.id_date = factGol.id_tanggal_terima_jabatan
        where id_prodi = 9
        group by id_dosen 
    ) data
    inner join fact_golongan_dosen_pemerintah factGol2 on data.id_tanggal_terima_jabatan = factGol2.id_tanggal_terima_jabatan and data.id_dosen = factGol2.id_dosen
    -- group by jabatan_dosen
    order by data.id_dosen
)data2
group by 'Jabatan Dosen'
order by 'Jabatan Dosen' ''', con)

dfjafunggrowth = pd.read_sql('''
select Jabatan_dosen,  
sum(if(Tahun=2014,1,0)) as "2014",
sum(if(Tahun=2015,1,0)) as "2015",
sum(if(Tahun=2016,1,0)) as "2016",
sum(if(Tahun=2017,1,0)) as "2017",
sum(if(Tahun=2018,1,0)) as "2018",
sum(if(Tahun=2019,1,0)) as "2019",
sum(if(Tahun=2020,1,0)) as "2020",
sum(if(Tahun=2021,1,0)) as "2021"
from (
    select distinct nama_gelar, jabatan_dosen ,  tglJabat.tahun from fact_golongan_dosen_pemerintah factGol
    inner join dim_dosen dimD on factGol.id_dosen = dimD.id_dosen
    inner join dim_date tglJabat on tglJabat.id_date = factGol.id_tanggal_terima_jabatan
    where id_prodi = 9
)data
where tahun >= 2014 and tahun < 2021
group by jabatan_dosen
order by  jabatan_dosen
''', con)

tbl_matkulBaru = pd.read_sql('''select kode_matakuliah, kelompok_matakuliah, upper(nama_matakuliah), sks  from fact_matakuliah_kurikulum
inner join dim_matakuliah on fact_matakuliah_kurikulum.id_matakuliah = dim_matakuliah.id_matakuliah
where id_kurikulum = 8''', con)

tbl_MatkulBatal = pd.read_sql('''select ds.tahun_ajaran, ds.semester_nama, dd.nik, dd.nama, dd.nama_gelar, dm.kode_matakuliah, dm.nama_matakuliah
from fact_dosen_mengajar
inner join dim_dosen dd on fact_dosen_mengajar.id_dosen = dd.id_dosen
inner join dim_semester ds on fact_dosen_mengajar.id_semester = ds.id_semester
inner join dim_matakuliah dm on dm.id_matakuliah = fact_dosen_mengajar.id_matakuliah
where is_batal = 1
order by ds.tahun_ajaran, ds.semester, dd.nama''', con)

tbl_mahasiswaAktif = pd.read_sql('''select ds.tahun_ajaran, ds.semester_nama, count(*) as jumlah_mahasiswa_aktif from fact_mahasiswa_status fms
inner join dim_semester ds on ds.id_semester = fms.id_semester
where fms.status = 'AK' and ds.tahun_ajaran in ('2015/2016','2016/2017','2017/2018','2018/2019','2019/2020')
group by ds.tahun_ajaran, ds.semester_nama
order by ds.tahun_ajaran, ds.semester_nama''', con)

tbl_mahasiswaAsing = pd.read_sql('''select tahun_angkatan, count(*) as jumlah_mahasiswa_asing from dim_mahasiswa 
where warga_negara ='WNA' and tahun_angkatan >= 2015 group by tahun_angkatan order by tahun_angkatan''', con)

tbl_matkulTawar = pd.read_sql('''select distinct ds.tahun_ajaran, ds.semester_nama
     , dm.kode_matakuliah, dm.nama_matakuliah, dm.sks, dm.kelompok_matakuliah
     -- , kapasitas_kelas
     -- , sifat_mengajar
     -- , total_pertemuan
from fact_registrasi_matakuliah
inner join dim_matakuliah dm on fact_registrasi_matakuliah.id_matakuliah = dm.id_matakuliah
inner join dim_semester ds on fact_registrasi_matakuliah.id_semester = ds.id_semester
order by ds.tahun_ajaran, ds.semester, kelompok_matakuliah, nama_matakuliah''', con)

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

ttlgrf_style = {
    'textAlign': 'center',
    'padding': '10px',
    'color': 'black'
}

bebandosen = dbc.Container([
    dbc.CardLink(
        dbc.Card([
            html.H5('Beban Mengajar Dosen',
                    style=ttlgrf_style),
        ],
            style={'border': '1px solid #fafafa',
                   'border-radius': '10px',
                   'justify-content': 'center',
                   'width': '100%',
                   'box-shadow': '5px 10px 30px #ebedeb'}
        )
    ),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                html.H5('Rata-rata Beban Mengajar Dosen',
                        style=ttlgrf_style),
                dcc.Graph(id='grf_bebanDosen',
                          style={'height': '100%'})
            ], style={'border': '1px solid #fafafa',
                      'border-radius': '10px',
                      'padding': '10px',
                      'width': '100%',
                      'height': '339px',
                      'justify-content': 'right',
                      'box-shadow': '5px 10px 30px #ebedeb'}
            ), width=5
        ),
        dbc.Col(
            dbc.Card([
                html.H5('Beban Mengajar Dosen Inforamatika',
                        style=ttlgrf_style),
                dt.DataTable(
                    id='tbl_bebanajar',
                    columns=[{"name": i, "id": i} for i in dfbebanajarinf.columns],
                    data=dfbebanajarinf.to_dict('records'),
                    sort_action='native',
                    sort_mode='multi',
                    style_table={'width': '100%', 'height': '100%', 'padding': '10px',
                                 'overflowY': 'auto', 'margin-top': '25px'},
                    style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    page_size=5
                )
            ], style=cardgrf_style
            ), width=7
        )
    ], style={'margin-top': '10px'})
], style=cont_style)

ipkdosen = dbc.Container([
    dbc.Card([
        html.H5('Rata-rata IPK Dosen',
                style=ttlgrf_style),
        dbc.CardBody(
            dcc.Graph(id='grf_ipkDosen')
        )
    ], style=cardgrf_style)
], style=cont_style)

daftardosen = dbc.Container([
    dbc.Card([
        html.H5('Daftar Dosen',
                style=ttlgrf_style),
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Dosen Tetap Informatika', value='tetapinf',
                        children=[
                            dt.DataTable(
                                id='tbl_dosenTetap',
                                columns=[
                                    {'name': i, 'id': i} for i in tbl_dosenTetap.columns
                                ],
                                data=tbl_dosenTetap.to_dict('records'),
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
                dcc.Tab(label='Dosen Industri/Praktisi', value='industri',
                        children=[
                            dt.DataTable(
                                id='tbl_dosenIndustri',
                                columns=[
                                    {'name': i, 'id': i} for i in tbl_dosenIndustri.columns
                                ],
                                data=tbl_dosenIndustri.to_dict('records'),
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
            ], style=tab_style, id='tab_tetapinf', value='tetapinf'
            )
        ])
    ], style=cardgrf_style
    ),
    dbc.Collapse(
        id='cll_tbldosen',
        is_open=False
    )
], style=cont_style)

jafung = dbc.Container([
    dbc.Card([
        html.H5('Profil Jabatan Fungsional Dosen',
                style=ttlgrf_style),
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Jabatan Fungsional Dosen Terakhir', value='jafunglast',
                        children=[
                            dbc.CardLink([
                                dcc.Graph(id='grf_jafunglast')],
                                id='cll_grfjafunglast', n_clicks=0
                            )
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Peningkatan Jabatan Fungsional Dosen', value='jafunggrowth',
                        children=[
                            dbc.CardLink([
                                dcc.Graph(id='grf_jafunggrowth')],
                                id='cll_grfjafunggrowth', n_clicks=0
                            )
                        ], style=tab_style, selected_style=selected_style)
            ], style=tab_style, id='tab_jafung', value='jafunglast'
            )
        ])
    ], style=cardgrf_style
    ),
    dbc.Collapse(
        id='cll_tbljafung',
        is_open=False
    )
], style=cont_style)

pendidikandosen = dbc.Container([
    dbc.Card([
        html.H5('Pendidikan Terakhir Dosen',
                style=ttlgrf_style),
        dbc.CardBody(
            dcc.Graph(id='grf_pendidikan')
        )
    ], style=cardgrf_style)
], style=cont_style)

ipkmahasiswa = dbc.Container([
    dbc.Card([
        html.H5('Rata-rata IPK Mahasiswa Aktif Tiap Semester',
                style=ttlgrf_style),
        dbc.CardBody(
            dcc.Graph(id='grf_ipkMosen')
        )
    ], style=cardgrf_style)
], style=cont_style)

mahasiswa = dbc.Container([
    dbc.Card([
        html.H5('Mahasiswa',
                style=ttlgrf_style),
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Mahasiswa Aktif', value='mhsaktif',
                        children=[
                            dbc.CardLink([
                                dcc.Graph(id='grf_mahasiswaAktif')],
                                id='cll_grfmhsaktif', n_clicks=0
                            )
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Mahasiswa Asing', value='mhsasing',
                        children=[
                            dbc.CardLink([
                                dcc.Graph(id='grf_mahasiswaAsing')],
                                id='cll_grfmhsasing', n_clicks=0
                            )
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

matkul = dbc.Container([
    dbc.Card([
        html.H5('Daftar Matakuliah',
                style=ttlgrf_style),
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Matakuliah Kurikulum', value='kurikulum',
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
                dcc.Tab(label='Matakuliah Batal dengan Keterangan Dosen', value='batal',
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
                dcc.Tab(label='Matakuliah Ditawarkan Setiap TS', value='ts',
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
    ], style=cardgrf_style
    ),
    dbc.Collapse(
        id='cll_tblmatkul',
        is_open=False
    )
], style=cont_style)

tab_dosen = html.Div([
    html.Div(
        html.H1(
            'Analisis Dosen',
            style={'margin-top': '30px', 'text-align': 'center'}
        )
    ),
    bebandosen,
    ipkdosen,
    daftardosen,
    matkul,
    jafung,
    pendidikandosen
]),

tab_mahasiswa = html.Div([
    html.Div(
        html.H1(
            'Analisis Mahasiswa',
            style={'margin-top': '30px', 'text-align': 'center'}
        )
    ),
    ipkmahasiswa,
    mahasiswa,
    matkul
])

layout = html.Div([
    dbc.Container([
        dbc.Card([
            dbc.CardHeader([
                dbc.Tabs([
                    dbc.Tab(label='Dosen', tab_id='dosen'),
                    dbc.Tab(label='Mahasiswa', tab_id='mahasiswa'),
                ], active_tab='dosen', id='cardTabsRegistrasi')
            ]),
            dbc.CardBody([

            ], id='cardContentRegistrasi'),
        ], style={'margin': '25px'})
    ], fluid=True)
], style={'width': '100%'})


@app.callback(
    Output("cardContentRegistrasi", "children"),
    [Input("cardTabsRegistrasi", "active_tab")]
)
def tab_contentRegistrasi(active_tab):
    if active_tab == 'dosen':
        return tab_dosen
    if active_tab == 'mahasiswa':
        return tab_mahasiswa


@app.callback(
    Output('cll_tbljafung', 'is_open'),
    Output('cll_tbljafung', 'children'),
    [Input("cll_grfjafunglast", "n_clicks"),
     Input("cll_grfjafunggrowth", "n_clicks"),
     Input("tab_jafung", "value")],
    [State("cll_tbljafung", "is_open")])
def toggle_collapse(nlast, ngrowth, jafung, is_open):
    isiLast = dbc.Card(
        dt.DataTable(
            id='tbl_jafunglast',
            columns=[{"name": i, "id": i} for i in dfjafunglast.columns],
            data=dfjafunglast.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            page_size=10,
            export_format='xlsx'
        ), style=cardgrf_style
    ),
    isiGrowth = dbc.Card(
        dt.DataTable(
            id='tbl_jafunggrowth',
            columns=[{"name": i, "id": i} for i in dfjafunggrowth.columns],
            data=dfjafunggrowth.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            page_size=10,
            export_format='xlsx'
        ), style=cardgrf_style
    ),
    if nlast and jafung == 'jafunglast':
        return not is_open, isiLast
    if ngrowth and jafung == 'jafunggrowth':
        return not is_open, isiGrowth
    return is_open, None


@app.callback(
    Output("grf_ipkDosen", 'figure'), Input('grf_ipkDosen', 'id')
)
def FillIpkDosen(id):
    df = pd.read_sql('''select ds.tahun_ajaran, ds.semester_nama, round(avg(fid.ipk),2) as "Rata-Rata"
from fact_ipk_dosen fid
inner join dim_dosen ddo on ddo.id_dosen = fid.id_dosen
inner join dim_semester ds on ds.id_semester = fid.id_semester
group by ds.tahun_ajaran, ds.semester_nama
order by ds.tahun_ajaran, ds.semester_nama''', con)
    fig = px.bar(df, x=df['tahun_ajaran'], y=df['Rata-Rata'], color=df['semester_nama'])
    fig.update_layout(barmode='group')
    return fig


@app.callback(
    Output('grf_jafunglast', 'figure'),
    Input('grf_jafunglast', 'id')
)
def graphJabatanDosen(id):
    df = dfjafunglast
    fig = px.bar(df, x=df["Jabatan Dosen"], y=df['Jumlah'], color=px.Constant('Jenis Jabatan'),
                 labels=dict(x="Jabatan Dosen", y="Jumlah", color="Jenis Jabatan"))
    return fig


@app.callback(
    Output('grf_jafunggrowth', 'figure'),
    Input('grf_jafunggrowth', 'id')
)
def graphPeningkatanJabatan(id):
    df = pd.read_sql('''select Jabatan_dosen as "Jabatan Dosen", Tahun, count(*) as Jumlah
from (
    select distinct nama_gelar, jabatan_dosen ,  tglJabat.tahun from fact_golongan_dosen_pemerintah factGol
    inner join dim_dosen dimD on factGol.id_dosen = dimD.id_dosen
    inner join dim_date tglJabat on tglJabat.id_date = factGol.id_tanggal_terima_jabatan
    where id_prodi = 9
)data
where tahun >= 2014 and tahun < 2021
group by `Jabatan Dosen`, tahun
order by `Jabatan Dosen`, tahun''', con)
    fig = px.bar(df, x=df["Tahun"], y=df['Jumlah'], color=df['Jabatan Dosen'],
                 labels=dict(x="Tahun", y="Jumlah", color="Jenis Jabatan"))
    return fig


@app.callback(
    Output('grf_pendidikan','figure'),
    Input('grf_pendidikan','id')
)
def graphPiePendidikan(id):
    df = pd.read_sql('''select tingkat_pendidikan as 'Tingkat Pendidikan', count(*) Jumlah  from (
    select dim_dosen.id_dosen, nama, max(tingkat_pendidikan) tingkat_pendidikan from fact_pendidikan_dosen
    inner join dim_dosen on dim_dosen.id_dosen = fact_pendidikan_dosen.id_dosen
    where id_prodi = 9 and status_Dosen = 'Tetap'
    group by dim_dosen.id_dosen, nama
    order by nama
) data
group by 'Tingkat Pendidikan'
order by 'Tingkat Pendidikan' ''',con)
    angka= df['Jumlah'].sum()
    fig = go.Figure(data=[go.Pie(labels=df['Tingkat Pendidikan'], values=df['Jumlah'], hole=.4,)])
    fig.update_layout(
        legend_title_text='Tingkat Pendidikan',
        annotations=[dict(text=f"{angka}", showarrow=False, font_size=15)]
    )
    return fig

@app.callback(
    Output("grf_ipkMahasiswa", 'figure'), Input('grf_ipkMahasiswa', 'id')
)
def FillIpkMahasiswa(id):
    df = pd.read_sql('''select ds.tahun_ajaran, ds.semester, avg(ipk) as "Rata-Rata"
from fact_mahasiswa_status fms 
inner join dim_semester ds on ds.id_semester = fms.id_semester
where ds.tahun_ajaran in ('2015/2016','2016/2017','2017/2018','2018/2019','2019/2020') and fms.status = 'AK'
group by ds.tahun_ajaran, ds.semester
order by ds.tahun_ajaran, ds.semester''', con)
    fig = px.bar(df, x=df['tahun_ajaran'], y=df['Rata-Rata'], color=df['semester'])
    fig.update_layout(barmode='group')
    return fig


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
        ), style=cardgrf_style
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
        ), style=cardgrf_style
    ),
    if naktif and mhs == 'mhsaktif':
        return not is_open, isiAktif
    if nasing and mhs == 'mhsasing':
        return not is_open, isiAsing
    return is_open, None


@app.callback(
    Output("grf_mahasiswaAktif", 'figure'), Input('grf_mahasiswaAktif', 'id')
)
def FillAktif(id):
    df = pd.read_sql('''select ds.tahun_ajaran, ds.semester_nama, count(*) as jumlah_mahasiswa_aktif from fact_mahasiswa_status fms
inner join dim_semester ds on ds.id_semester = fms.id_semester
where fms.status = 'AK' and ds.tahun_ajaran in ('2015/2016','2016/2017','2017/2018','2018/2019','2019/2020')
group by ds.tahun_ajaran, ds.semester_nama
order by ds.tahun_ajaran, ds.semester_nama
''', con)
    fig = px.bar(df, x=df['tahun_ajaran'], y=df['jumlah_mahasiswa_aktif'], color=df['semester_nama'])
    fig.update_layout(barmode='group')
    return fig


@app.callback(
    Output("grf_mahasiswaAsing", 'figure'), Input('grf_mahasiswaAsing', 'id')
)
def FillAsing(id):
    df = pd.read_sql('''select tahun_angkatan, count(*) as jumlah_mahasiswa_asing from dim_mahasiswa 
where warga_negara ='WNA' and tahun_angkatan >= 2015
group by tahun_angkatan
order by tahun_angkatan''', con)
    fig = px.bar(df, x=df['tahun_angkatan'], y=df['jumlah_mahasiswa_asing'])
    return fig
