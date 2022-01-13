import dash
import pandas as pd
import dash_table as dt
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output, State
from dask.array.tests.test_array_core import test_blockwise_1_in_shape_I
from sqlalchemy import create_engine
from appConfig import app, server
import model.dao_kegiatankerjasama as data

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

dfprestasiakademik = data.getPrestasiAkademik()
dfprestasinonakademik = data.getPrestasiNonAkademik()
dfkerjasama = data.getKerjasama()
dfkerjasamakegiatan = data.getKerjasamaKegiatan()
dfkerjasamakp = data.getKerjasamaKP()
dfkerjasamapp = data.getKerjasamaPP()
dfkegiatandosen = data.getKegiatanDosen()

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

kegiatanDosen = html.Div([
    dbc.Card([
        html.H5('DOSEN',
                style=ttlgrf_style),
    ], style=card_style
    ),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H5('Jumlah Rekognisi Dosen Pertahun', style=ttlgrf_style),
                dt.DataTable(
                    id='dfkegiatandosen',
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
                )
            ], style=cardgrf_style),
        ], width=12),
        dbc.Col([
            dbc.Card([
                html.H5('Rekognisi Dosen Pertahun'),
                dcc.Graph(id='grf_rekogDosen'),
            ], style=card_style)
        ], width=6),
        dbc.Col([
            dbc.Card([
                html.H5('IPK Dosen'),
                dcc.Graph(id='grf_ipkDosenKeg'),
            ], style=card_style)
        ], width=6)
    ], style={'margin-top': '10px'})
], style=cont_style)

kegiatanMahasiswa = html.Div([
    dbc.Card([
        html.H5('MAHASISWA',
                style=ttlgrf_style),
    ],
        style={'border': '1px solid #fafafa',
               'border-radius': '10px',
               'justify-content': 'center',
               'width': '100%',
               'box-shadow': '5px 10px 30px #ebedeb'}
    ),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H5('Prestasi Mahasiswa', style={'text-align': 'center'}),
                dcc.Tabs([
                    dcc.Tab(label='Akademik', value='akademik',
                            children=[
                                dt.DataTable(
                                    id='tbl_presAkademik',
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
                            ], style=tab_style, selected_style=selected_style),
                    dcc.Tab(label='Non Akademik', value='nonakademik',
                            children=[
                                dt.DataTable(
                                    id='tbl_presNonAkademik',
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
                            ], style=tab_style, selected_style=selected_style
                            )
                ], id='tab_prestasimhs',style=tabs_styles, value='akademik')
            ], style=card_style)
        ], width=12),
        dbc.Col([
            dbc.Card([
                html.H3('Kuliah Umum dengan MOU/Perjanjian'),
                dcc.Graph(id='grf_kegKuliah')
            ], style=card_style)
        ], width=12)
    ])
], style=cont_style)

kerjasama = html.Div([
    dbc.Card([
        html.H5('KERJASAMA',
                style=ttlgrf_style),
    ], style=card_style
    ),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H5('Rekap Jumlah Kerjasama', style={'text-align': 'center'}),
                dt.DataTable(
                    id='dfkerjasama',
                    columns=[
                        {'name': i, 'id': i} for i in dfkerjasama.columns
                    ],
                    data=dfkerjasama.to_dict('records'),
                    sort_action='native',
                    sort_mode='multi',
                    style_table={'padding': '10px', 'overflowX': 'auto'},
                    style_header={'textAlign': 'center'},
                    style_data={'font-size': '80%', 'textAlign': 'center'},
                    style_cell={'width': 95},
                    page_size=10,
                )
            ], style=card_style),
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H5('Kerjasama', style={'text-align': 'center'}),
                dcc.Tabs([
                    dcc.Tab(label='Kegiatan', value='kegiatan',
                            children=[
                                dt.DataTable(
                                    id='tbl_kerjasamaKeg',
                                    columns=[
                                        {'name': i, 'id': i} for i in dfkerjasamakegiatan.columns
                                    ],
                                    data=dfkerjasamakegiatan.to_dict('records'),
                                    sort_action='native',
                                    sort_mode='multi',
                                    style_table={'padding': '10px', 'overflowX': 'auto'},
                                    style_header={'textAlign': 'center'},
                                    style_data={'font-size': '80%', 'textAlign': 'center'},
                                    style_cell={'width': 95},
                                    page_size=10,
                                )
                            ],
                            style=tab_style, selected_style=selected_style),
                    dcc.Tab(label='KP', value='kp',
                            children=[
                                dt.DataTable(
                                    id='dfkerjasamakp',
                                    columns=[
                                        {'name': i, 'id': i} for i in dfkerjasamakp.columns
                                    ],
                                    data=dfkerjasamakp.to_dict('records'),
                                    sort_action='native',
                                    sort_mode='multi',
                                    style_table={'padding': '10px', 'overflowX': 'auto'},
                                    style_header={'textAlign': 'center'},
                                    style_data={'font-size': '80%', 'textAlign': 'center'},
                                    style_cell={'width': 95},
                                    page_size=10,
                                )
                            ],
                            style=tab_style, selected_style=selected_style),
                    dcc.Tab(label='Penelitian dan PKM', value='ppkm',
                            children=[
                                dt.DataTable(
                                    id='dfkerjasamapp',
                                    columns=[
                                        {'name': i, 'id': i} for i in dfkerjasamapp.columns
                                    ],
                                    data=dfkerjasamapp.to_dict('records'),
                                    sort_action='native',
                                    sort_mode='multi',
                                    style_table={'padding': '10px', 'overflowX': 'auto'},
                                    style_header={'textAlign': 'center'},
                                    style_data={'font-size': '80%', 'textAlign': 'center'},
                                    style_cell={'width': 95},
                                    page_size=10,
                                )
                            ],
                            style=tab_style, selected_style=selected_style)
                ],value='kegiatan'),
            ], style=card_style),
        ], width=12),
    ])
], style=cont_style)

kegiatankerjasama = dbc.Container([
    html.Div([
        html.H1('Analisis Kegiatan Kerjasama',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Kegiatan', value='kegiatan',
                    children=[
                        kegiatanDosen,
                        kegiatanMahasiswa
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Kerjasama', value='kerjasama',
                    children=[
                        kerjasama
                    ],
                    style=tab_style, selected_style=selected_style)
        ], style=tabs_styles, value='kegiatan')
    ])
], style=cont_style)

layout = html.Div([
    html.Div([kegiatankerjasama], style={'margin-bottom': '50px'})
], style={'justify-content': 'center'})

@app.callback(
    Output("grf_kegKuliah", 'figure'), Input('grf_kegKuliah', 'id')
)
def FillIKUwithMOU(id):
    df = pd.read_sql('''select ddselesai.tahun, count(dim_kegiatan.nama_kegiatan) as jumlah_kuliah_umum
     -- , ddmulai.tanggal as tanggal_mulai, ddselesai.tanggal as tanggal_selesai
from dim_kegiatan
inner join dim_perjanjian dp on dim_kegiatan.id_perjanjian = dp.id_perjanjian
inner join dim_date ddmulai on ddmulai.id_date = dim_kegiatan.id_tanggal_mulai
inner join dim_date ddselesai on ddselesai.id_date = dim_kegiatan.id_tanggal_selesai
where jenis_kegiatan = 'KULIAH UMUM' and dim_kegiatan.id_perjanjian is not null
group by ddselesai.tahun''', con)
    fig = px.bar(df, x=df['tahun'], y=df['jumlah_kuliah_umum'])
    return fig


@app.callback(
    Output("grf_rekogDosen", 'figure'), Input('grf_rekogDosen', 'id')
)
def FillKegDosen(id):
    df = pd.read_sql('''select Tahun, count(*) as jumlah from fact_rekognisi_dosen
inner join dim_date on dim_date.id_date = fact_rekognisi_dosen.id_tanggal_mulai
group by tahun
order by tahun''', con)
    fig = px.line(df, x=df['Tahun'], y=df['jumlah'])
    fig.update_traces(mode='lines+markers')
    return fig


@app.callback(
    Output("grf_ipkDosenKeg", 'figure'), Input('grf_ipkDosenKeg', 'id')
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
