import dash
import pandas as pd
import dash_table as dt
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from appConfig import app, server

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

tbl_jmlPPP = pd.read_sql('''select Nama, Tahun, max(Penelitian) Penelitian, max(pkm) as pkm , max(publikasi) as "Publikasi Penelitan dan PKM", max(LuaranLainnya) as "Luaran Lainnya" from (

   ( select nama, dim_dosen.id_dosen, tahun, count(*) as Penelitian, null as pkm, null as publikasi, null as LuaranLainnya from fact_penelitian fact
    inner join dim_penelitian_pkm dim on dim.id_penelitian_pkm = fact.id_penelitian
    inner join br_pp_dosen on fact.id_penelitian = br_pp_dosen.id_penelitian_pkm
    inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen and id_prodi = 9 
    inner join dim_date on dim_date.id_date = dim.id_tanggal_mulai
    group by nama,dim_dosen.id_dosen, tahun
    order by nama, tahun)
    union 
    (select nama, dim_dosen.id_dosen, tahun, null as Penelitian, count(*) as pkm , null as publikasi, null as LuaranLainnya  from fact_pkm fact
    inner join dim_penelitian_pkm dim on dim.id_penelitian_pkm = fact.id_pkm
    inner join br_pp_dosen on fact.id_pkm = br_pp_dosen.id_penelitian_pkm
    inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen and id_prodi = 9 
    inner join dim_date on dim_date.id_date = dim.id_tanggal_mulai
    group by dim_dosen.id_dosen, nama, tahun
    order by nama, tahun)
    union
    (select nama, dimdos.id_dosen, tahun_publikasi as tahun, null as Penelitian, null as pkm, count(*) as publikasi, null as LuaranLainnya from fact_publikasi fact
        inner join dim_publikasi dimpub on fact.id_publikasi = dimpub.id_publikasi
        inner join br_pub_dosen brpub on fact.id_publikasi = brpub.id_publikasi
        inner join dim_dosen dimdos on brpub.id_dosen = dimdos.id_dosen and id_prodi = 9  
        group by nama, dimdos.id_dosen, tahun_publikasi
        order by nama)        
    union
    (select nama, dim_dosen.id_dosen, tahun, 
        null as Penelitian, null as pkm, null as publikasi ,  
        count(*) LuaranLainnya
        from fact_luaran_lainnya fatl
        inner join dim_luaran_lainnya diml on fatl.id_luaran_lainnya = diml.id_luaran_lainnya
        inner join br_pp_luaranlainnya brl on fatl.id_luaran_lainnya = brl.id_luaranlainnya
        inner join br_pp_dosen brpp on brpp.id_penelitian_pkm = brl.id_penelitian_pkm
        inner join dim_dosen on brpp.id_Dosen = dim_dosen.id_dosen and id_prodi = 9  
        inner join dim_date on dim_date.id_date = diml.id_tanggal_luaran
        group by  nama, dim_dosen.id_dosen, tahun)
    
) data
where tahun >2014
group by nama, tahun
order by nama, tahun''', con)

tbl_penelitianDana = pd.read_sql('''select Tahun, judul_penelitian as "Judul Penelitan", dim_penelitian_pkm.wilayah_nama "Nama Wilayah", br_pp_dana.besaran_dana "Jumlah Dana", dim_sumber_dana.jenis_sumber_dana "Sumber Dana", dim_sumber_dana.status "Asal Sumber Dana"
from fact_penelitian fact
inner join dim_penelitian_pkm on fact.id_penelitian = dim_penelitian_pkm.id_penelitian_pkm
inner join br_pp_dana on dim_penelitian_pkm.id_penelitian_pkm = br_pp_dana.id_penelitian_pkm
inner join dim_sumber_dana on br_pp_dana.id_sumber_dana = dim_sumber_dana.id_sumber_dana
inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
order by tahun, judul_penelitian''', con)

tbl_pkmDana = pd.read_sql('''select fact.id_pkm, jumlah_Dosen "Jumlah Dosen", GROUP_CONCAT(distinct dim_dosen.nama  SEPARATOR', ')  "Nama Dosen", judul_pkm "Judul PkM", jumlah_mahasiswa "Jumlah Mahasiswa", 
    GROUP_CONCAT(distinct dim_mahasiswa.nama  SEPARATOR', ') "Nama Mahasiswa",  Tahun 
from fact_pkm fact
inner join dim_penelitian_pkm on fact.id_pkm = dim_penelitian_pkm.id_penelitian_pkm
inner join br_pp_dosen on fact.id_pkm = br_pp_dosen.id_penelitian_pkm
inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen
inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
inner join br_pp_mahasiswa on fact.id_pkm = br_pp_mahasiswa.id_penelitian_pkm
inner join dim_mahasiswa on br_pp_mahasiswa.id_mahasiswa = dim_mahasiswa.id_mahasiswa 
group by fact.id_pkm, jumlah_Dosen,judul_pkm, jumlah_mahasiswa, tahun
order by tahun, judul_pkm''', con)

tbl_penelitianMhs = pd.read_sql('''select fact.id_penelitian, jumlah_Dosen, GROUP_CONCAT(distinct dim_dosen.nama  SEPARATOR', ') namaDosen, judul_penelitian, jumlah_mahasiswa, GROUP_CONCAT(distinct dim_mahasiswa.nama  SEPARATOR', ') namaMahasiswa,  tahun from fact_penelitian fact
inner join dim_penelitian_pkm on fact.id_penelitian = dim_penelitian_pkm.id_penelitian_pkm
inner join dim_penelitian_pkm dim on dim.id_penelitian_pkm = fact.id_penelitian
    inner join br_pp_dosen on fact.id_penelitian = br_pp_dosen.id_penelitian_pkm
    inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen
    inner join dim_date on dim_date.id_date = dim.id_tanggal_mulai
    inner join br_pp_mahasiswa on fact.id_penelitian = br_pp_mahasiswa.id_penelitian_pkm
    inner join dim_mahasiswa on br_pp_mahasiswa.id_mahasiswa = dim_mahasiswa.id_mahasiswa 
    group by fact.id_penelitian, jumlah_Dosen,judul_penelitian, jumlah_mahasiswa, tahun''', con)

tbl_pkmMhs = pd.read_sql('''select fact.id_pkm, jumlah_Dosen "Jumlah Dosen", GROUP_CONCAT(distinct dim_dosen.nama  SEPARATOR', ')  "Nama Dosen", judul_pkm "Judul PkM", jumlah_mahasiswa "Jumlah Mahasiswa", 
    GROUP_CONCAT(distinct dim_mahasiswa.nama  SEPARATOR', ') "Nama Mahasiswa",  Tahun 
from fact_pkm fact
inner join dim_penelitian_pkm on fact.id_pkm = dim_penelitian_pkm.id_penelitian_pkm
inner join br_pp_dosen on fact.id_pkm = br_pp_dosen.id_penelitian_pkm
inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen
inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
inner join br_pp_mahasiswa on fact.id_pkm = br_pp_mahasiswa.id_penelitian_pkm
inner join dim_mahasiswa on br_pp_mahasiswa.id_mahasiswa = dim_mahasiswa.id_mahasiswa 
group by fact.id_pkm, jumlah_Dosen,judul_pkm, jumlah_mahasiswa, tahun
order by tahun, judul_pkm''', con)

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

ppp = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card('Jumlah Penelitian PKM Publikasi',
                     style={'justify-content': 'center', 'width': '100%', 'textAlign': 'center'}
                     )
        ])
    ], style={'z-index': '2'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('Jumlah Penelitian PKM Publikasi PerDosen PerTahun', style={'text-align': 'center'}),
                html.Div([
                    dt.DataTable(
                        id='tbl_pppDosen',
                        columns=[
                            {'name': i, 'id': i} for i in tbl_jmlPPP.columns
                        ],
                        data=tbl_jmlPPP.to_dict('records'),
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

penelitianDana = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card('Penelitian dan Sumber Dana',
                     style={'justify-content': 'center', 'width': '100%', 'textAlign': 'center'}
                     )
        ])
    ], style={'z-index': '2'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('Daftar Penelitian dan Sumber Dana', style={'text-align': 'center'}),
                html.Div([
                    dt.DataTable(
                        id='tbl_penelitianDana',
                        columns=[
                            {'name': i, 'id': i} for i in tbl_penelitianDana.columns
                        ],
                        data=tbl_penelitianDana.to_dict('records'),
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

grafikPenelitian = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card('Penelitian Dosen',
                     style={'justify-content': 'center', 'width': '100%', 'textAlign': 'center'}
                     )
        ])
    ], style={'z-index': '2'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('Penelitian PerTahun'),
                dcc.Graph(id='grf_DosenPenelitian'),
            ], style={'justify-content': 'center'})
        ], width=6),
        dbc.Col([
            dbc.Card([
                html.H3('Perbandingan Asal Sumber Dana Penelitian'),
                dcc.Graph(id='grf_bdgDosenPenelitian'),
            ], style={'justify-content': 'center'})
        ], width=6)
    ])
], style={'margin-top': '50px', 'width': '100%'})

penelitianMhs = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card('Keterlibatan Mahasiswa',
                     style={'justify-content': 'center', 'width': '100%', 'textAlign': 'center'}
                     )
        ])
    ], style={'z-index': '2'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('Penelitian Melibatkan Mahasiswa', style={'text-align': 'center'}),
                html.Div([
                    dt.DataTable(
                        id='tbl_penelitianMhs',
                        columns=[
                            {'name': i, 'id': i} for i in tbl_penelitianMhs.columns
                        ],
                        data=tbl_penelitianMhs.to_dict('records'),
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

pkmDana = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card('PkM dan Sumber Dana',
                     style={'justify-content': 'center', 'width': '100%', 'textAlign': 'center'}
                     )
        ])
    ], style={'z-index': '2'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('Daftar PkM dan Sumber Dana', style={'text-align': 'center'}),
                html.Div([
                    dt.DataTable(
                        id='tbl_pkmDana',
                        columns=[
                            {'name': i, 'id': i} for i in tbl_pkmDana.columns
                        ],
                        data=tbl_pkmDana.to_dict('records'),
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

grafikPkm = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card('Pkm Dosen',
                     style={'justify-content': 'center', 'width': '100%', 'textAlign': 'center'}
                     )
        ])
    ], style={'z-index': '2'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('Pkm PerTahun'),
                dcc.Graph(id='grf_DosenPkm'),
            ], style={'justify-content': 'center'})
        ], width=6),
        dbc.Col([
            dbc.Card([
                html.H3('Perbandingan Asal Sumber Dana Pkm'),
                dcc.Graph(id='grf_bdgDosenPkm'),
            ], style={'justify-content': 'center'})
        ], width=6)
    ])
], style={'margin-top': '50px', 'width': '100%'})

pkmMhs = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card('Keterlibatan Mahasiswa',
                     style={'justify-content': 'center', 'width': '100%', 'textAlign': 'center'}
                     )
        ])
    ], style={'z-index': '2'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('PkM Melibatkan Mahasiswa', style={'text-align': 'center'}),
                html.Div([
                    dt.DataTable(
                        id='tbl_pkmMhs',
                        columns=[
                            {'name': i, 'id': i} for i in tbl_pkmMhs.columns
                        ],
                        data=tbl_pkmMhs.to_dict('records'),
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
                html.H3('Kerjasama Penelitian dan PkM', style={'text-align': 'center'}),
                html.Div([
                    dt.DataTable(
                        id='tbl_kerjasamaPPP',
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

tab_penelitian = html.Div([
    html.Div(
        html.H1(
            'Analisis Penelitian',
            style={'margin-top': '30px', 'text-align': 'center'}
        )
    ),
    penelitianDana,
    grafikPenelitian,
    penelitianMhs,
]),

tab_pkm = html.Div([
    html.Div(
        html.H1(
            'Analisis Penelitian',
            style={'margin-top': '30px', 'text-align': 'center'}
        )
    ),
    pkmDana,
    grafikPkm,
    pkmMhs,
]),

layout = html.Div([
    dbc.Container([
        html.H1(
            'Analisis PPP',
            style={'margin-top': '30px', 'text-align': 'center'}
        ),
        ppp,
        kerjasama,
        dbc.Card([
            dbc.CardHeader([
                dbc.Tabs([
                    dbc.Tab(label='Penelitian', tab_id='penelitian'),
                    dbc.Tab(label='PkM', tab_id='pkm'),
                ], active_tab='penelitian', id='cardTabsPPP')
            ]),
            dbc.CardBody([

            ], id='cardContentPPP'),
        ], style={'margin': '25px'})

    ], fluid=True),
], style={'width': '100%'})


@app.callback(
    Output("cardContentPPP", "children"), [Input("cardTabsPPP", "active_tab")]
)
def tab_contentRegistrasi(active_tab):
    if active_tab == 'penelitian':
        return tab_penelitian
    if active_tab == 'pkm':
        return tab_pkm

@app.callback(
    Output("grf_DosenPenelitian", 'figure'), Input('grf_DosenPenelitian', 'id')
)
def FillPenelitianDosen(id):
    df = pd.read_sql('''select tahun, count(*) as Jumlah
from fact_penelitian fact
inner join dim_penelitian_pkm on fact.id_penelitian = dim_penelitian_pkm.id_penelitian_pkm
inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
group by tahun
order by tahun''', con)
    fig = px.line(df, x=df['tahun'], y=df['Jumlah'])
    fig.update_traces(mode='lines+markers')
    return fig

@app.callback(
    Output("grf_bdgDosenPenelitian", 'figure'), Input('grf_bdgDosenPenelitian', 'id')
)
def FillbdgPenelitianDosen(id):
    df = pd.read_sql('''select Tahun, dim_sumber_dana.status "Asal Sumber Dana", count(*) as Jumlah
from fact_penelitian fact
inner join dim_penelitian_pkm on fact.id_penelitian = dim_penelitian_pkm.id_penelitian_pkm
inner join br_pp_dana on dim_penelitian_pkm.id_penelitian_pkm = br_pp_dana.id_penelitian_pkm
inner join dim_sumber_dana on br_pp_dana.id_sumber_dana = dim_sumber_dana.id_sumber_dana
inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
group by Tahun, "Asal Sumber Dana"
order by Tahun''', con)
    fig = px.bar(df, x=df['Tahun'], y=df['Jumlah'], color=df['Asal Sumber Dana'])
    fig.update_layout(barmode='group')
    return fig

@app.callback(
    Output("grf_DosenPkm", 'figure'), Input('grf_DosenPkm', 'id')
)
def FillPkmDosen(id):
    df = pd.read_sql('''select tahun, count(*) as Jumlah
from fact_pkm fact
inner join dim_penelitian_pkm on fact.id_pkm = dim_penelitian_pkm.id_penelitian_pkm
inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
group by tahun
order by tahun''', con)
    fig = px.line(df, x=df['tahun'], y=df['Jumlah'])
    fig.update_traces(mode='lines+markers')
    return fig

@app.callback(
    Output("grf_bdgDosenPkm", 'figure'), Input('grf_bdgDosenPkm', 'id')
)
def FillbdgPkmDosen(id):
    df = pd.read_sql('''select Tahun, dim_sumber_dana.status "Asal Sumber Dana", count(*) as Jumlah
from fact_pkm fact
inner join dim_penelitian_pkm on fact.id_pkm = dim_penelitian_pkm.id_penelitian_pkm
inner join br_pp_dana on dim_penelitian_pkm.id_penelitian_pkm = br_pp_dana.id_penelitian_pkm
inner join dim_sumber_dana on br_pp_dana.id_sumber_dana = dim_sumber_dana.id_sumber_dana
inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
group by Tahun, "Asal Sumber Dana"
order by Tahun''', con)
    fig = px.bar(df, x=df['Tahun'], y=df['Jumlah'], color=df['Asal Sumber Dana'])
    fig.update_layout(barmode='group')
    return fig