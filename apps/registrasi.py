import dash
import pandas as pd
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dask.array.tests.test_array_core import test_blockwise_1_in_shape_I
from sqlalchemy import create_engine
from appConfig import app, server

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

tbl_bebanDosen = pd.read_sql('''select ds.tahun_ajaran, ds.semester_nama, dd.nik, dd.nama, dd.nama_gelar, dm.kode_matakuliah, dm.nama_matakuliah, dm.sks,fact_dosen_mengajar.sifat_mengajar
from fact_dosen_mengajar
inner join dim_semester ds on fact_dosen_mengajar.id_semester = ds.id_semester
inner join dim_dosen dd on fact_dosen_mengajar.id_dosen = dd.id_dosen
inner join dim_matakuliah dm on fact_dosen_mengajar.id_matakuliah = dm.id_matakuliah
where is_batal = 0 and dd.id_prodi = 9
order by ds.tahun_ajaran, ds.semester, dd.nama''', con)

tbl_dosenTetap = pd.read_sql('''select nama, nik, nomor_induk,tipe_nomor_induk,jenis_kelamin,no_sertifikat, status_yayasan from dim_dosen
where id_prodi = 9 and status_yayasan = "TETAP"''', con)

tbl_dosenIndustri = pd.read_sql('''select * from dim_dosen''', con)

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

bebanDosen = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card('Beban Mengajar Dosen',
                     style={'justify-content': 'center', 'width': '100%', 'textAlign': 'center'}
                     )
        ])
    ], style={'z-index': '2'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('Beban Mengajar Dosen Prodi Informatika', style={'text-align': 'center'}),
                html.Div([
                    dt.DataTable(
                        id='tbl_bebanDosen',
                        columns=[
                            {'name': i, 'id': i} for i in tbl_bebanDosen.columns
                        ],
                        data=tbl_bebanDosen.to_dict('records'),
                        sort_action='native',
                        sort_mode='multi',
                        style_table={'padding': '10px', 'overflowX': 'auto'},
                        style_header={'textAlign': 'center'},
                        style_data={'font-size': '80%', 'textAlign': 'center'},
                        style_cell={'width': 95},
                        page_size=10,
                    )
                ])
            ], style={'height': '450px'}),
        ], width=12),
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='grf_bebanDosen'),
            ], style={'justify-content': 'center'})
        ], width=6),
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='grf_ipkDosen'),
            ], style={'justify-content': 'center'})
        ], width=6)
    ])
], style={'margin-top': '50px', 'width': '100%'})

dosen = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card('Daftar Dosen',
                     style={'justify-content': 'center', 'width': '100%', 'textAlign': 'center'}
                     )
        ])
    ], style={'z-index': '2'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('Daftar Dosen Tetap Informatika', style={'text-align': 'center'}),
                html.Div([
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
                        page_size=10,
                    )
                ])
            ], style={'height': '450px'}),
        ], width=12),
        dbc.Col([
            dbc.Card([
                html.H3('Daftar Dosen Industi/Praktisi', style={'text-align': 'center'}),
                html.Div([
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
                        page_size=10,
                    )
                ])
            ], style={'height': '450px'})
        ], width=12)
    ])
], style={'margin-top': '50px', 'width': '100%'})

matkul = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card('Matakuliah',
                     style={'justify-content': 'center', 'width': '100%', 'textAlign': 'center'}
                     )
        ])
    ], style={'z-index': '2'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('Daftar Matakuliah Kurikulum', style={'text-align': 'center'}),
                html.Div([
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
                        page_size=10,
                    )
                ])
            ], style={'height': '450px'}),
        ], width=12),
        dbc.Col([
            dbc.Card([
                html.H3('Daftar Matakuliah Batal dengan Keterangan Dosen', style={'text-align': 'center'}),
                html.Div([
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
                        page_size=10,
                    )
                ])
            ], style={'height': '450px'})
        ], width=12)
    ])
], style={'margin-top': '50px', 'width': '100%'})

mahasiswa = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card('Mahasiswa',
                     style={'justify-content': 'center', 'width': '100%', 'textAlign': 'center'}
                     )
        ])
    ], style={'z-index': '2'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('Daftar Mahasiswa Aktif', style={'text-align': 'center'}),
                html.Div([
                    dt.DataTable(
                        id='tbl_mahasiswaAktif',
                        columns=[
                            {'name': i, 'id': i} for i in tbl_mahasiswaAktif.columns
                        ],
                        data=tbl_mahasiswaAktif.to_dict('records'),
                        sort_action='native',
                        sort_mode='multi',
                        style_table={'padding': '10px', 'overflowX': 'auto'},
                        style_header={'textAlign': 'center'},
                        style_data={'font-size': '80%', 'textAlign': 'center'},
                        style_cell={'width': 95},
                        page_size=10,
                    )
                ])
            ], style={'height': '450px'}),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='grf_mahasiswaAktif',style={'height': '450px',}),
            ], style={ 'justify-content': 'center'})
        ], width=6),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('Daftar Mahasiswa Asing', style={'text-align': 'center'}),
                html.Div([
                    dt.DataTable(
                        id='tbl_mahasiswaAsing',
                        columns=[
                            {'name': i, 'id': i} for i in tbl_mahasiswaAsing.columns
                        ],
                        data=tbl_mahasiswaAsing.to_dict('records'),
                        sort_action='native',
                        sort_mode='multi',
                        style_table={'padding': '10px', 'overflowX': 'auto'},
                        style_header={'textAlign': 'center'},
                        style_data={'font-size': '80%', 'textAlign': 'center'},
                        style_cell={'width': 95},
                        page_size=10,
                    )
                ])
            ], style={'height': '300px'}),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='grf_mahasiswaAsing',style={'height': '300px',}),
            ], style={ 'justify-content': 'center'})
        ], width=6),
    ])
], style={'margin-top': '50px', 'width': '100%'})

ipkMahasiswa = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card('IPK Mahasiswa',
                     style={'justify-content': 'center', 'width': '100%', 'textAlign': 'center'}
                     )
        ])
    ], style={'z-index': '2'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='grf_bebanDosen'),
            ], style={'justify-content': 'center'})
        ], width=12),
    ])
], style={'margin-top': '50px', 'width': '100%'})

matkulTawar = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card('Matakuliah',
                     style={'justify-content': 'center', 'width': '100%', 'textAlign': 'center'}
                     )
        ])
    ], style={'z-index': '2'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('Daftar Matakuliah Ditawarkan Setiap TS', style={'text-align': 'center'}),
                html.Div([
                    dt.DataTable(
                        id='tbl_matkulTawar',
                        columns=[
                            {'name': i, 'id': i} for i in tbl_matkulTawar.columns
                        ],
                        data=tbl_matkulTawar.to_dict('records'),
                        sort_action='native',
                        sort_mode='multi',
                        style_table={'padding': '10px', 'overflowX': 'auto'},
                        style_header={'textAlign': 'center'},
                        style_data={'font-size': '80%', 'textAlign': 'center'},
                        style_cell={'width': 95},
                        page_size=10,
                    )
                ])
            ], style={'height': '450px'}),
        ], width=12),
    ])
], style={'margin-top': '50px', 'width': '100%'})

tab_dosen = html.Div([
    html.Div(
        html.H1(
            'Analisis Dosen',
            style={'margin-top': '30px', 'text-align': 'center'}
        )
    ),
    bebanDosen,
    dosen,
    matkul
]),
tab_mahasiswa = html.Div([
    html.Div(
        html.H1(
            'Analisis Mahasiswa',
            style={'margin-top': '30px', 'text-align': 'center'}
        )
    ),
    ipkMahasiswa,
    mahasiswa,
    matkulTawar
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
    ], fluid=True),
    # html.Div([tempatkerja]),
    html.Div([]),
    html.Div([])
], style={'width': '100%'})


@app.callback(
    Output("cardContentRegistrasi", "children"), [Input("cardTabsRegistrasi", "active_tab")]
)
def tab_contentRegistrasi(active_tab):
    if active_tab == 'dosen':
        return tab_dosen
    if active_tab == 'mahasiswa':
        return tab_mahasiswa
