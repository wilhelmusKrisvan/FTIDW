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

tbl_prestasiAkademik = pd.read_sql('''select  nama_kegiatan, tahun, 
    if(wilayah_nama='LOKAL','v','') as Lokal,
    if(wilayah_nama='REGIONAL','v','') as Regional,
    if(wilayah_nama='NASIONAL','v','') as Nasional,
    if(wilayah_nama='INTERNASIONAL','v','') as Internasional,
prestasi from(
    select distinct nama_kegiatan, tahun, fact.wilayah_nama, replace(jenis_partisipasi, 'L', 'I') as prestasi
    from fact_kegiatan_mahasiswa fact
    inner join dim_kegiatan keg on keg.id_kegiatan = fact.id_kegiatan
    inner join dim_date dat on keg.id_tanggal_mulai = dat.id_date
    where sifat_partisipasi = 'PM' and is_akademis = 1
) data 
order by tahun, nama_kegiatan''', con)

tbl_prestasiNonAkademik = pd.read_sql('''select nama_kegiatan, tahun, 
    if(wilayah_nama='LOKAL','v','') as Lokal,
    if(wilayah_nama='REGIONAL','v','') as Regional,
    if(wilayah_nama='NASIONAL','v','') as Nasional,
    if(wilayah_nama='INTERNASIONAL','v','') as Internasional,
prestasi from(
    select distinct nama_kegiatan, tahun, fact.wilayah_nama, replace(jenis_partisipasi, 'L', 'I') as prestasi
    from fact_kegiatan_mahasiswa fact
    inner join dim_kegiatan keg on keg.id_kegiatan = fact.id_kegiatan
    inner join dim_date dat on keg.id_tanggal_mulai = dat.id_date
    where sifat_partisipasi = 'PM' and is_akademis = 0
) data 
order by tahun''', con)

tbl_kerjasama = pd.read_sql('''select kode_perjanjian "Kode Perjanjian", no_perjanjian "No Perjanjian", concat(mulai.hari_dalam_bulan," ", mulai.nama_bulan, " ", mulai.tahun) as tglMulai, concat(selesai.hari_dalam_bulan," ", selesai.nama_bulan, " ", selesai.tahun) as tglSelesai ,
max(Penelitian) "Jumlah Penelitan", max(pkm) "Jumlah PkM",  max(kp) "Jumlah KP" from (    
    
    select id_perjanjian, kode_perjanjian, tipe_perjanjian, no_perjanjian, id_tanggal_mulai,  id_tanggal_selesai,
    max(case when jenis = 'Penelitian' then jumlah end) Penelitian,
    max(case when jenis = 'Pkm' then jumlah end) Pkm, null as KP
    from (
        select dim_perjanjian.id_perjanjian, kode_perjanjian, tipe_perjanjian, no_perjanjian, wilayah, br_pp_perjanjian.jenis, dim_perjanjian.id_tanggal_mulai, dim_perjanjian.id_tanggal_selesai, count(*) as "jumlah"
        from dim_perjanjian
        inner join br_pp_perjanjian on dim_perjanjian.id_perjanjian = br_pp_perjanjian.id_perjanjian
        group by dim_perjanjian.id_perjanjian, kode_perjanjian, tipe_perjanjian, no_perjanjian, wilayah,dim_perjanjian.id_tanggal_mulai, dim_perjanjian.id_tanggal_selesai,br_pp_perjanjian.jenis
    ) ppp
    group by id_perjanjian, kode_perjanjian, tipe_perjanjian, no_perjanjian, id_tanggal_mulai, id_tanggal_selesai
    
    union
    
    
    select fact_kp.id_perjanjian, kode_perjanjian, tipe_perjanjian, no_perjanjian, dim_perjanjian.id_tanggal_mulai, dim_perjanjian.id_tanggal_selesai, null as Penelitian, null as KP, count(*) as KP
    from fact_kp
    inner join dim_perjanjian on fact_kp.id_perjanjian = dim_perjanjian.id_perjanjian
    group by fact_kp.id_perjanjian, kode_perjanjian, tipe_perjanjian, no_perjanjian, dim_perjanjian.id_tanggal_mulai, dim_perjanjian.id_tanggal_selesai

) data 
inner join dim_date mulai on mulai.id_date = data.id_tanggal_mulai
inner join dim_date selesai on selesai.id_date = data.id_tanggal_selesai
group by kode_perjanjian, no_perjanjian,  tglMulai, tglSelesai
order by tglMulai''', con)

tbl_kerjasamaKegiatan = pd.read_sql('''select ddselesai.tahun as tahun_selesai,
       dk.jenis_kegiatan,dk.nama_kegiatan,  dk.is_akademis,
       CASE WHEN dp.tipe_perjanjian = 'MO' THEN 'MOU'
		WHEN dp.tipe_perjanjian = 'PK' THEN 'PERJANJIAN KERJASAMA'
		ELSE 'NONE' END AS tipe_perjanjian,       
		dp.no_perjanjian,
		CASE WHEN dm.wilayah = '1' THEN 'LOKAL'
		WHEN dm.wilayah = '2' THEN 'REGIONAL'
		WHEN dm.wilayah = '3' THEN 'NASIONAL'
        WHEN dm.wilayah = '4' THEN 'INTERNASIONAL'
		ELSE 'NONE' END AS wilayah_mitra,  dm.jenis_mitra,
       dm.nama_mitra
       
from dim_kegiatan dk
inner join dim_perjanjian dp on dp.id_perjanjian = dk.id_perjanjian
inner join br_mitra_perjanjian bmp on bmp.id_perjanjian = dk.id_perjanjian
inner join dim_mitra dm on bmp.id_mitra = dm.id_mitra
inner join dim_date ddselesai on ddselesai.id_date = dk.id_tanggal_selesai
inner join dim_date ddmulai on ddmulai.id_date = dk.id_tanggal_mulai

where dk.id_perjanjian is not null
''', con)

tbl_kerjasamaKP = pd.read_sql('''select distinct tahun_ajaran, ds.semester_nama, ddselesai.tahun as tahun_selesai,
       fact_kp.jenis_kp, CASE WHEN dp.tipe_perjanjian = 'MO' THEN 'MOU' ELSE 'PERJANJIAN KERJASAMA' END AS tipe_perjanjian
       , dp.no_perjanjian
       , CASE WHEN dm.wilayah = '1' THEN 'LOKAL'
		WHEN dm.wilayah = '2' THEN 'REGIONAL'
		WHEN dm.wilayah = '3' THEN 'NASIONAL'
        WHEN dm.wilayah = '3' THEN 'INTERNASIONAL'
		ELSE 'NONE' END AS wilayah_mitra
       , dm.jenis_mitra, dm.nama_mitra
       from fact_kp
inner join dim_perjanjian dp on fact_kp.id_perjanjian = dp.id_perjanjian
inner join br_mitra_perjanjian bmp on dp.id_perjanjian = bmp.id_perjanjian
inner join dim_mitra dm on bmp.id_mitra = dm.id_mitra
inner join dim_semester ds on fact_kp.id_semester = ds.id_semester
inner join dim_date ddselesai on ddselesai.id_date = fact_kp.id_tanggal_selesai

where fact_kp.id_perjanjian is not null''', con)

tbl_kerjasamaPP = pd.read_sql('''select ddselesai.tahun as tahun_selesai,
       br_pp_perjanjian.jenis, dpp.judul , CASE WHEN dp.tipe_perjanjian = 'MO' THEN 'MOU' ELSE 'PERJANJIAN KERJASAMA' END AS tipe_perjanjian
       , dp.no_perjanjian
       , CASE WHEN dm.wilayah = '1' THEN 'LOKAL'
		WHEN dm.wilayah = '2' THEN 'REGIONAL'
		WHEN dm.wilayah = '3' THEN 'NASIONAL'
        WHEN dm.wilayah = '3' THEN 'INTERNASIONAL'
		ELSE 'NONE' END AS wilayah_mitra
       , dm.jenis_mitra, dm.nama_mitra
from br_pp_perjanjian
inner join dim_penelitian_pkm dpp on br_pp_perjanjian.id_penelitian_pkm = dpp.id_penelitian_pkm
inner join dim_perjanjian dp on br_pp_perjanjian.id_perjanjian = dp.id_perjanjian
inner join br_mitra_perjanjian bmp on dp.id_perjanjian = bmp.id_perjanjian
inner join dim_mitra dm on bmp.id_mitra = dm.id_mitra
inner join dim_date ddselesai on ddselesai.id_date = dpp.id_tanggal_selesai
inner join dim_date ddmulai on ddmulai.id_date = dpp.id_tanggal_mulai''', con)

Akademik = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card('Prestasi Mahasiswa',
                     style={'justify-content': 'center', 'width': '100%', 'textAlign': 'center'}
                     )
        ])
    ], style={'z-index': '2'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('Prestasi Akademik Mahasiswa', style={'text-align': 'center'}),
                html.Div([
                    dt.DataTable(
                        id='tbl_bebanDosen',
                        columns=[
                            {'name': i, 'id': i} for i in tbl_prestasiAkademik.columns
                        ],
                        data=tbl_prestasiAkademik.to_dict('records'),
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
                html.H3('Prestasi Akademik Non Mahasiswa', style={'text-align': 'center'}),
                html.Div([
                    dt.DataTable(
                        id='tbl_bebanDosen',
                        columns=[
                            {'name': i, 'id': i} for i in tbl_prestasiNonAkademik.columns
                        ],
                        data=tbl_prestasiNonAkademik.to_dict('records'),
                        sort_action='native',
                        sort_mode='multi',
                        style_table={'padding': '10px', 'overflowX': 'auto'},
                        style_header={'textAlign': 'center'},
                        style_data={'font-size': '80%', 'textAlign': 'center'},
                        style_cell={'width': 95},
                        page_size=10,
                    )
                ])
            ], style={'height': '450px'})
        ], width=12),
    ])
], style={'margin-top': '50px', 'width': '100%'})

kegKuliah = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card('Prestasi Mahasiswa',
                     style={'justify-content': 'center', 'width': '100%', 'textAlign': 'center'}
                     )
        ])
    ], style={'z-index': '2'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='grf_kegKuliah'),
            ], style={'height': '450px'})
        ], width=12),
    ])
], style={'margin-top': '50px', 'width': '100%'})

kerjasama = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card('Kerjasama',
                     style={'justify-content': 'center', 'width': '100%', 'textAlign': 'center'}
                     )
        ])
    ], style={'z-index': '2'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('Daftar Kerjasama', style={'text-align': 'center'}),
                html.Div([
                    dt.DataTable(
                        id='tbl_kerjasama',
                        columns=[
                            {'name': i, 'id': i} for i in tbl_kerjasama.columns
                        ],
                        data=tbl_kerjasama.to_dict('records'),
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
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('Daftar Kerjasama Kegiatan', style={'text-align': 'center'}),
                html.Div([
                    dt.DataTable(
                        id='tbl_kerjasamaKeg',
                        columns=[
                            {'name': i, 'id': i} for i in tbl_kerjasamaKegiatan.columns
                        ],
                        data=tbl_kerjasamaKegiatan.to_dict('records'),
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
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('Daftar Kerjasama KP', style={'text-align': 'center'}),
                html.Div([
                    dt.DataTable(
                        id='tbl_kerjasamaKP',
                        columns=[
                            {'name': i, 'id': i} for i in tbl_kerjasamaKP.columns
                        ],
                        data=tbl_kerjasamaKP.to_dict('records'),
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
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('Daftar Kerjasama Penelitian dan PkM', style={'text-align': 'center'}),
                html.Div([
                    dt.DataTable(
                        id='tbl_kerjasamaPP',
                        columns=[
                            {'name': i, 'id': i} for i in tbl_kerjasamaPP.columns
                        ],
                        data=tbl_kerjasamaPP.to_dict('records'),
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

tab_kegiatan = html.Div([
    html.Div(
        html.H1(
            'Analisis Kegiatan',
            style={'margin-top': '30px', 'text-align': 'center'}
        )
    ),
    Akademik,
    kegKuliah
]),
tab_kerjasama = html.Div([
    html.Div(
        html.H1(
            'Analisis Kerjasama',
            style={'margin-top': '30px', 'text-align': 'center'}
        )
    ),
    kerjasama
])

layout = html.Div([
    dbc.Container([
        dbc.Card([
            dbc.CardHeader([
                dbc.Tabs([
                    dbc.Tab(label='Kegiatan', tab_id='kegiatan'),
                    dbc.Tab(label='Kerjasama', tab_id='kerjasama'),
                ], active_tab='kegiatan', id='cardTabsKerjasama')
            ]),
            dbc.CardBody([

            ], id='cardContentKerjasama'),
        ], style={'margin': '25px'})
    ], fluid=True),
], style={'width': '100%'})


@app.callback(
    Output("cardContentKerjasama", "children"), [Input("cardTabsKerjasama", "active_tab")]
)
def tab_contentKerjasama(active_tab):
    if active_tab == 'kegiatan':
        return tab_kegiatan
    if active_tab == 'kerjasama':
        return tab_kerjasama
