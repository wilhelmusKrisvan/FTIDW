import dash
import pandas as pd
import dash_table as dt
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from sqlalchemy import create_engine
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
from appConfig import app

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

dfdosbing = pd.read_sql('''
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

dflulusan = pd.read_sql('''select tahun_ajaran_yudisium as 'Tahun Lulus', count(id_mahasiswa) "Jumlah Lulusan",  min(ipk) "Min. IPK", avg(ipk) as 'Rata-rata IPK' ,  max(ipk) "Max. IPK"
from fact_yudisium
group by tahun_ajaran_yudisium
order by tahun_ajaran_yudisium''', con)

dfjmlskripsi = pd.read_sql('''
select tahun_ajaran_yudisium as 'Tahun Lulus', count(id_mahasiswa) "Jumlah Lulusan",  min(ipk) "Min. IPK", avg(ipk) as 'Rata-rata IPK' ,  max(ipk) "Max. IPK"
from fact_yudisium
group by tahun_ajaran_yudisium
order by tahun_ajaran_yudisium 
''', con)

dfavgmasa = pd.read_sql('''
select concat(round((masa_studi-mods)/12,0) ," tahun ", mods, " bulan")  as "masa studi" , tahun_ajaran_yudisium 
from (
select  mod(masa_studi,12) as mods, masa_studi, tahun_ajaran_yudisium
from (
select round(avg(masa_studi_dalam_bulan),0) as "masa_studi", tahun_ajaran_yudisium from fact_yudisium
group by tahun_ajaran_yudisium) as data_mentah
) as data_ready
order by tahun_ajaran_yudisium
''', con)

dfallmasa = pd.read_sql('''
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
''', con)

tbl_ipklulusan = pd.read_sql('''
select tahun_ajaran_yudisium as 'Tahun Lulus', count(id_mahasiswa) "Jumlah Lulusan",  min(ipk) "Min. IPK", avg(ipk) as 'Rata-rata IPK' ,  max(ipk) "Max. IPK"
from fact_yudisium
group by tahun_ajaran_yudisium
order by tahun_ajaran_yudisium
''', con)

tbl_masastudilulusan = pd.read_sql('''
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
''', con)

tbl_masastudilulusan = pd.read_sql('''
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
''', con)

Fillsemester = pd.read_sql('select tahun_ajaran from dim_semester', con)
semester = Fillsemester['tahun_ajaran'].dropna().unique()

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

dosbing = dbc.Container([
    dbc.Card([
        html.H5('3.b. Dosen Pembimbing Tugas Akhir',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody([
                dcc.Dropdown(
                    id='drpdwn_TA',
                    options=[{'label': i, 'value': i} for i in semester],
                    value='2015/2016',
                    style={'width': '100%', 'color': 'black', 'margin': '0px'},
                    className='card-body',
                    clearable=False
                ),
                dcc.Graph(id='grf_dosbing')
            ]),
            id='cll_grfdosbing',
            n_clicks=0
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_dosbing',
                columns=[{"name": i, "id": i} for i in dfdosbing.columns],
                data=dfdosbing.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                page_size=10,
                export_format='xlsx'
            ), style=cardgrf_style
        ),
        id='cll_tbldosbing',
        is_open=False
    )
], style=cont_style)

lulusan = dbc.Container([
    dbc.Card([
        html.H5('8.a. IPK Lulusan',
                style=ttlgrf_style),
        dbc.CardLink([dcc.Graph(id='grf_ipklulusan')], id='cll_grflulusan', n_clicks=0),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_lulusan',
                columns=[{"name": i, "id": i} for i in dflulusan.columns],
                data=dflulusan.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                page_size=10,
                export_format='xlsx'
            ), style=cardgrf_style
        ),
        id='cll_tbllulusan',
        is_open=False,
    )
], style=cont_style)

masa_studi = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.CardLink(
                dbc.Card(
                    dt.DataTable(
                        id='tbl_avgmasa',
                        columns=[{"name": i, "id": i} for i in dfavgmasa.columns],
                        data=dfavgmasa.to_dict('records'),
                        sort_action='native',
                        sort_mode='multi',
                        style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                        style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                        style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                        page_size=10
                    ),
                    style={'border': '1px solid #fafafa',
                           'border-radius': '10px',
                           'padding': '10px',
                           'width':'570px',
                           'height': '217.78px',
                           'justify-content':'center',
                           'box-shadow': '5px 10px 30px #ebedeb'}
                ),
                id='cll_tblavgmasa',
                n_clicks=0
            ), width=6
        ),
        dbc.Col(
            dbc.CardLink(
                dbc.Card(
                    dcc.Graph(
                        id='grf_masastudi',
                        style={'height': '100%'}
                    ),
                    style={'border': '1px solid #fafafa',
                           'border-radius': '10px',
                           'padding': '10px',
                           'height': '217.78px',
                           'justify-content':'center',
                           'box-shadow': '5px 10px 30px #ebedeb'},
                ),
                id='cll_tblallmasa',
                n_clicks=0
            ), width=6
        )
    ]),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_allmasa',
                columns=[{"name": i, "id": i} for i in dfallmasa.columns],
                data=dfallmasa.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                page_size=10
            ), style=cardgrf_style
        ),
        id='cll_tblallmasa',
        is_open=False
    )
], style=cont_style)

kp_prodi = dbc.Container([
    dbc.Card([
        html.H5('KP Prodi Informatika',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='All', value='all',
                    children=[
                        dbc.CardLink([dcc.Graph(id='grf_kpall')], id='cll_grfkpall', n_clicks=0)
                    ], style=tab_style, selected_style=selected_style),
            dcc.Tab(label='PKM Dosen', value='PKMDosen',
                    children=[
                        dbc.CardLink([dcc.Graph(id='grf_kppkm')], id='cll_grfpkm', n_clicks=0)
                    ], style=tab_style, selected_style=selected_style)
        ], id='tab_kpall', value='all')
    ], style=cardgrf_style)
], style=cont_style)

# tridharma = dbc.CardGroup([
#     dbc.Row(
#         dbc.Card('Luaran dan Capaian Tridharma Berkaitan Capaian Pembelajaran dan Pendidikan',
#                  style={'justify-content': 'center', 'width': '1200px', 'textAlign': 'center'}
#                  )
#         , style={'z-index': '2'}),
#     dbc.Row([
#         dbc.Card([
#             '8.a. IPK Lulusan',
#             dt.DataTable(
#                 id='tbl_ipklulusan',
#                 columns=[{"name": i, "id": i} for i in tbl_ipklulusan.columns],
#                 data=tbl_ipklulusan.to_dict('records'),
#                 sort_action='native',
#                 sort_mode='multi',
#                 style_table={'width': '600px', 'padding': '10px'},
#                 style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
#                 style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'}
#             )
#         ], style={'textAlign': 'center', 'padding-top': '10px'}),
#         dbc.Card([
#             '8.c.4. Masa Studi Lulusan Program Sarjana',
#             dt.DataTable(
#                 id='tbl_masastudilulusan',
#                 columns=[{"name": i, "id": i} for i in tbl_masastudilulusan.columns],
#                 data=tbl_masastudilulusan.to_dict('records'),
#                 sort_action='native',
#                 sort_mode='multi',
#                 style_table={'width': '600px', 'padding': '10px'},
#                 style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
#                 style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'}
#
#             )
#         ], style={'textAlign': 'center', 'padding-top': '10px'})
#     ])
# ], style={'margin-top': '20px', 'justify-content': 'center'})

layout = html.Div([
    html.Div(html.H1('Analisis Skripsi, KP, dan Yudisium Prodi Informatika',
                     style={'margin-top': '30px', 'textAlign': 'center'}
                     )
             ),
    html.Div([dosbing]),
    html.Div([lulusan]),
    html.Div([masa_studi]),
    html.Div([kp_prodi], style={'margin-bottom': '50px'})
], style={'justify-content': 'center'})


@app.callback(
    Output("cll_tblallmasa", "is_open"),
    [Input("cll_tblavgmasa", "n_clicks")],
    [State("cll_tblallmasa", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tbldosbing", "is_open"),
    [Input("cll_grfdosbing", "n_clicks")],
    [State("cll_tbldosbing", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tbllulusan", "is_open"),
    [Input("cll_grflulusan", "n_clicks")],
    [State("cll_tbllulusan", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('grf_dosbing', 'figure'),
    Input('grf_dosbing', 'id'),
    Input('drpdwn_TA', 'value'),
)
def graphDosbing(id, value):
    df = pd.read_sql('''select count(*) as "Jumlah Skripsi",dim_dosen.nama as "Nama Dosen", dim_semester.semester,
CASE dim_semester.semester
    WHEN 1 THEN "Ganjil"
    WHEN 2 THEN "Genap"
  END as "Semester Tahun Ajaran"
from fact_skripsi
inner join dim_dosen on fact_skripsi.id_dosen_pembimbing1 = dim_dosen.id_dosen and dim_dosen.id_prodi = 9
inner join dim_semester on dim_semester.id_semester = fact_skripsi.id_semester 
where dim_semester.tahun_ajaran=%(tahun_ajaran)s
group by dim_dosen.nama, dim_semester.semester,"Semester Tahun Ajaran"
order by dim_dosen.nama, dim_semester.semester''', con, params={'tahun_ajaran': value})
    fig = px.bar(df, y=df['Nama Dosen'], x=df['Jumlah Skripsi'], color=df['Semester Tahun Ajaran'], barmode='group')
    return fig


@app.callback(
    Output('grf_masastudi', 'figure'),
    Input('grf_masastudi', 'id')
)
def graphLulusSkripsi(id):
    df = pd.read_sql('''
    select count(*) as 'Jumlah Mahasiswa', dim_semester.tahun_ajaran as 'Tahun Ajaran'
from fact_skripsi
inner join(
select count(*) as jumlah, id_mahasiswa from fact_skripsi
group by id_mahasiswa
) data_skripsi on data_skripsi.id_mahasiswa = fact_skripsi.id_mahasiswa AND data_skripsi.jumlah=1
inner join dim_semester on dim_semester.id_semester = fact_skripsi.id_semester
where id_dosen_penguji1 <>''
group by dim_semester.tahun_ajaran
order by dim_semester.tahun_ajaran
    ''', con)
    fig = px.bar(df, y=df['Jumlah Mahasiswa'], x=df['Tahun Ajaran'], barmode='group')
    return fig


@app.callback(
    Output('grf_ipklulusan', 'figure'),
    Input('grf_ipklulusan', 'id'),
)
def graphIPKLulusan(id):
    dfavg = pd.read_sql('''select avg(ipk) as 'Rata-rata IPK' ,  tahun_ajaran_yudisium as 'Tahun Ajaran'
from fact_yudisium
group by tahun_ajaran_yudisium
order by tahun_ajaran_yudisium''', con)
    dfmax = pd.read_sql('''select max(ipk) as 'IPK' ,  tahun_ajaran_yudisium as 'Tahun Ajaran'
from fact_yudisium
group by tahun_ajaran_yudisium
order by tahun_ajaran_yudisium''', con)
    dfmin = pd.read_sql('''select min(ipk) as 'IPK' ,  tahun_ajaran_yudisium as 'Tahun Ajaran'
    from fact_yudisium
    group by tahun_ajaran_yudisium
    order by tahun_ajaran_yudisium''', con)
    fig = px.bar(dfavg, y=dfavg['Rata-rata IPK'], x=dfavg['Tahun Ajaran'], color=px.Constant('Rata-rata IPK'),
                 labels=dict(x="Tahun Ajaran", y="IPK", color="IPK"))
    fig.add_scatter(y=dfmax['IPK'], x=dfmax['Tahun Ajaran'],
                    name='IPK Tertinggi',
                    hovertemplate="IPK=Tertinggi <br>IPK=%{y} </br> Tahun Ajaran= %{x}")
    fig.add_scatter(y=dfmin['IPK'], x=dfmin['Tahun Ajaran'],
                    name='IPK Terendah',
                    hovertemplate="IPK=Terendah <br>IPK=%{y} </br> Tahun Ajaran= %{x}"
                    )
    return fig


@app.callback(
    Output('grf_jmllulusan', 'figure'),
    Input('grf_jmllulusan', 'id'),
)
def graphJmlLulusan(id):
    df = pd.read_sql('''select count(*) as "Jumlah Mahasiswa", dim_semester.tahun_ajaran as "Tahun Ajaran"
from fact_skripsi
inner join(
select count(*) as jumlah, id_mahasiswa from fact_skripsi
group by id_mahasiswa
) data_skripsi on data_skripsi.id_mahasiswa = fact_skripsi.id_mahasiswa AND data_skripsi.jumlah=1
inner join dim_semester on dim_semester.id_semester = fact_skripsi.id_semester
where id_dosen_penguji1 <>''
group by dim_semester.tahun_ajaran
order by dim_semester.tahun_ajaran''', con)
    fig = px.bar(df, y=df['Jumlah Mahasiswa'], x=df['Tahun Ajaran'], color=px.Constant('Jumlah Mahasiswa'),
                 labels=dict(x="Tahun Ajaran", y="Jumlah", color="Keterangan"))
    return fig
