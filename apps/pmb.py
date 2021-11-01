import dash
import pandas as pd
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from sqlalchemy import create_engine
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
from appConfig import app

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

tbl_seleksi = pd.read_sql('''select 
dataMahasiswa.tahun_aka as 'Tahun Akademik', dy_tampung as 'Daya Tampung',jml_pendaftar as 'Pendaftar', 
lolos as 'Lolos Seleksi', baru as 'Baru Reguler', Barutransfer as 'Baru Transfer', 
aktif.jmlaktif as 'Aktif Reguler', 0 as 'Aktif Transfer' from (
    select dataPendaftar.*, count(id_tanggal_lolos_seleksi) as lolos, count(id_mahasiswa) as baru,  
    0 as Barutransfer
    from(
    select dy.id_semester, tahun_ajaran as tahun_aka, dy.jumlah as dy_tampung, count(fpmbDaftar.id_pmb)  as jml_pendaftar 
    from dim_daya_tampung dy
    inner join dim_semester smstr on dy.id_semester = smstr.id_semester
    inner join dim_prodi prodi on prodi.id_prodi = dy.id_prodi
    left join fact_pmb fpmbDaftar on dy.id_semester = fpmbDaftar.id_semester and (fpmbDaftar.id_prodi_pilihan_1 || fpmbDaftar.id_prodi_pilihan_3 || fpmbDaftar.id_prodi_pilihan_3 = 9)
    where kode_prodi = '71' and dy.id_semester <= (select id_semester from dim_semester where tahun_ajaran='2018/2019' limit 1)
    group by tahun_aka, dy_tampung, dy.id_semester
    ) dataPendaftar
    left join fact_pmb fpmbLolos on dataPendaftar.id_semester = fpmbLolos.id_semester and fpmbLolos.id_prodi_diterima = 9
    group by id_semester, tahun_aka,dy_tampung, jml_pendaftar
    order by id_semester asc
)dataMahasiswa
left join (

select count(*) as jmlaktif, tahun_ajaran from fact_mahasiswa_status
left join dim_semester on fact_mahasiswa_status.id_semester = dim_semester.id_semester
where status = 'AK' 
group by tahun_ajaran

)aktif on aktif.tahun_ajaran = tahun_aka ''', con)

tbl_mhsasing = pd.read_sql('''
select data.*, (jumlah - parttime) as fulltime
from (
select dim_prodi.nama_prodi, concat(tahun_angkatan, '/', cast(tahun_angkatan+1 as char(4))) as tahun_semster, count(*) as jumlah,
SUM(if(substr(nim,3,3)= 'ASG', 1, 0)) AS parttime
from dim_mahasiswa
inner join dim_prodi on dim_mahasiswa.id_prodi = dim_prodi.id_prodi AND (dim_prodi.id_prodi = 9 || 10)
where warga_negara = 'WNA'
group by dim_prodi.nama_prodi,tahun_semster, tahun_angkatan
) data
inner join dim_semester on dim_semester.tahun_ajaran = data.tahun_semster AND semester = 1 and dim_semester.id_semester <= (select id_semester from dim_semester where tahun_ajaran = '2018/2019' limit 1)
order by nama_prodi, tahun_semster desc
''', con)

seleksi = dbc.CardGroup([
    dbc.Row(
        dbc.Card('2.a Seleksi Mahasiswa Baru',
                 style={'justify-content': 'center', 'width': '1200px', 'textAlign': 'center'}
                 )
        , style={'z-index': '2'}
    ),
    dbc.Row(
        dbc.Card(
            dt.DataTable(
                id='tbl_seleksi',
                columns=[{"name": i, "id": i} for i in tbl_seleksi.columns],
                data=tbl_seleksi.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '1200px', 'padding': '10px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'}
            )
        )
    ),
    dbc.Row(
        dbc.Card(
            dcc.Graph(id='grf_seleksi')
            , style={'width': '1200px'}
        )
    )
], style={'margin-top': '50px', 'justify-content': 'center'})

mhsasing = dbc.CardGroup([
    dbc.Row(
        dbc.Card('2.b Mahasiswa Asing',
                 style={'justify-content': 'center', 'width': '1200px', 'textAlign': 'center'}
                 )
        , style={'z-index': '2'}
    ),
    dbc.Row(
        dbc.Card(
            dt.DataTable(
                id='tbl_mhsasing',
                columns=[{"name": i, "id": i} for i in tbl_mhsasing.columns],
                data=tbl_mhsasing.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '1200px', 'padding': '10px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'}
            )
        )
    ),
    dbc.Row([
        dbc.Card(
            dcc.Graph(id='grf_mhsasinginf')
            , style={'width': '600px'}
        ),
        dbc.Card(
            dcc.Graph(id='grf_mhsasingsi')
            , style={'width': '600px'}
        )
    ])
], style={'margin-top': '20px', 'justify-content': 'center'})

layout = html.Div([
    html.Div(html.H1('Analisis Mahasiswa Baru Prodi Informatika',
                     style={'margin-top': '30px', 'textAlign': 'center'}
                     )
             ),
    html.Div([seleksi]),
    html.Div([mhsasing], style={'margin-bottom': '50px'})
], style={'justify-content': 'center'})
