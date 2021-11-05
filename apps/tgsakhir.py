import dash
import pandas as pd
import dash_table as dt
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from sqlalchemy import create_engine
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
from appConfig import app

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

tbl_dosbing = pd.read_sql('''
select 
nama, -- max(IF(tahun_ajaran = "2019/2020", JumlahSkripsi, 0)) AS "2019/2020",
max(IF(tahun_ajaran = "2018/2019", JumlahSkripsi, 0)) AS "2018/2019",
max(IF(tahun_ajaran = "2017/2018", JumlahSkripsi, 0)) AS "2017/2018",
max(IF(tahun_ajaran = "2016/2017", JumlahSkripsi, 0)) AS "2016/2017",
max(IF(tahun_ajaran = "2015/2016", JumlahSkripsi, 0)) AS "2015/2016",
max(IF(tahun_ajaran = "2014/2015", JumlahSkripsi, 0)) AS "2014/2015"
from (

        select count(*) as "JumlahSkripsi", fact_skripsi.id_dosen_pembimbing1, dim_dosen.nama, dim_semester.tahun_ajaran

    from fact_skripsi
    inner join dim_dosen on fact_skripsi.id_dosen_pembimbing1 = dim_dosen.id_dosen and dim_dosen.id_prodi = 9 and dim_dosen.status_dikti = 'Tetap'
    inner join dim_semester on fact_skripsi.id_semester = dim_semester.id_semester
    inner join (
    
        select * from dim_semester
        where id_semester <= (select id_semester 
        from dim_semester
        where tahun_ajaran='2018/2019' limit 1) and semester = 1 
        order by id_semester desc
    
    ) tigasmstr on tigasmstr.tahun_ajaran = dim_semester.tahun_ajaran  
    
    group by fact_skripsi.id_dosen_pembimbing1, dim_dosen.nama, dim_semester.tahun_ajaran
    order by  dim_semester.tahun_ajaran, fact_skripsi.id_dosen_pembimbing1

)data
group by nama
order by nama
''', con)

tbl_ipklulusan=pd.read_sql('''
select tahun_ajaran_yudisium as 'Tahun Lulus', count(id_mahasiswa) "Jumlah Lulusan",  min(ipk) "Min. IPK", avg(ipk) as 'Rata-rata IPK' ,  max(ipk) "Max. IPK"
from fact_yudisium
group by tahun_ajaran_yudisium
order by tahun_ajaran_yudisium
''',con)

tbl_masastudilulusan=pd.read_sql('''
select * from 
(select concat(dim_mahasiswa.tahun_angkatan,'/',cast(dim_mahasiswa.tahun_angkatan+1 as char(4))) as TahunMAsuk,
SUM(case when masa_studi_dalam_bulan < 36 then 1 else 0 end) as '< 3 Tahun',
SUM(case when masa_studi_dalam_bulan >= 36 AND masa_studi_dalam_bulan <42 then 1 else 0 end) as '3 - 3.5 Tahun',
SUM(case when masa_studi_dalam_bulan >= 42 AND masa_studi_dalam_bulan <54  then 1 else 0 end) as '3.5 - 4.5 Tahun',
SUM(case when masa_studi_dalam_bulan >= 54 AND masa_studi_dalam_bulan <=84 then 1 else 0 end) as '4.5 - 7 Tahun',
SUM(case when masa_studi_dalam_bulan >= 85 then 1 else 0 end) as '> 7 tahun'
from fact_yudisium
inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa=fact_yudisium.id_mahasiswa
group by TahunMAsuk
order by TahunMAsuk) lulusan
left join (
    select count(id_mahasiswa), tahun_ajaran from fact_pmb
    inner join dim_semester on dim_semester.id_semester=fact_pmb.id_semester AND id_prodi_diterima = 9
    group by tahun_ajaran
    order by tahun_ajaran
) mhsditerima on mhsditerima.tahun_ajaran = TahunMAsuk
''',con)

tbl_masastudilulusan=pd.read_sql('''
select * from 
(select concat(dim_mahasiswa.tahun_angkatan,'/',cast(dim_mahasiswa.tahun_angkatan+1 as char(4))) as TahunMAsuk,
SUM(case when masa_studi_dalam_bulan < 36 then 1 else 0 end) as '< 3 Tahun',
SUM(case when masa_studi_dalam_bulan >= 36 AND masa_studi_dalam_bulan <42 then 1 else 0 end) as '3 - 3.5 Tahun',
SUM(case when masa_studi_dalam_bulan >= 42 AND masa_studi_dalam_bulan <54  then 1 else 0 end) as '3.5 - 4.5 Tahun',
SUM(case when masa_studi_dalam_bulan >= 54 AND masa_studi_dalam_bulan <=84 then 1 else 0 end) as '4.5 - 7 Tahun',
SUM(case when masa_studi_dalam_bulan >= 85 then 1 else 0 end) as '> 7 tahun'
from fact_yudisium
inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa=fact_yudisium.id_mahasiswa
group by TahunMAsuk
order by TahunMAsuk) lulusan
left join (
    select count(id_mahasiswa), tahun_ajaran from fact_pmb
    inner join dim_semester on dim_semester.id_semester=fact_pmb.id_semester AND id_prodi_diterima = 9
    group by tahun_ajaran
    order by tahun_ajaran
) mhsditerima on mhsditerima.tahun_ajaran = TahunMAsuk
''',con)

dosbing = dbc.CardGroup([
    dbc.Row(
        dbc.Card('3.b Dosen Tetap Pembimbing Tugas Akhir / Skripsi Mahasiswa',
                 style={'justify-content': 'center', 'width': '1200px', 'textAlign': 'center'}
                 )
        , style={'z-index': '2'}
    ),
    dbc.Row(
        dbc.Card(
            dt.DataTable(
                id='tbl_dosbing',
                columns=[{"name": i, "id": i} for i in tbl_dosbing.columns],
                data=tbl_dosbing.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '1200px', 'padding': '10px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'}
            )
        )
    )
], style={'margin-top': '50px', 'justify-content': 'center'})

tridharma = dbc.CardGroup([
    dbc.Row(
        dbc.Card('Luaran dan Capaian Tridharma Berkaitan Capaian Pembelajaran dan Pendidikan',
                 style={'justify-content': 'center', 'width': '1200px', 'textAlign': 'center'}
                 )
        , style={'z-index': '2'}),
    dbc.Row([
        dbc.Card([
            '8.a. IPK Lulusan',
            dt.DataTable(
                id='tbl_ipklulusan',
                columns=[{"name": i, "id": i} for i in tbl_ipklulusan.columns],
                data=tbl_ipklulusan.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '600px', 'padding': '10px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'}
            )
        ], style={'textAlign':'center','padding-top':'10px'}),
        dbc.Card([
            '8.c.4. Masa Studi Lulusan Program Sarjana',
            dt.DataTable(
                id='tbl_masastudilulusan',
                columns=[{"name": i, "id": i} for i in tbl_masastudilulusan.columns],
                data=tbl_masastudilulusan.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '600px', 'padding': '10px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'}

            )
        ], style={'textAlign':'center','padding-top':'10px'})
    ])
], style={'margin-top': '20px', 'justify-content': 'center'})

layout = html.Div([
    html.Div(html.H1('Analisis Skripsi, KP, dan Yudisium Prodi Informatika',
                     style={'margin-top': '30px', 'textAlign': 'center'}
                     )
             ),
    html.Div([dosbing]),
    html.Div([tridharma], style={'margin-bottom': '50px'})
], style={'justify-content': 'center'})
