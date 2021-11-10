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
nama as 'Nama Dosen', -- max(IF(tahun_ajaran = "2019/2020", JumlahSkripsi, 0)) AS "2019/2020",
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

dfjmlskripsi = pd.read_sql('''select tahun_ajaran_yudisium as 'Tahun Lulus', count(id_mahasiswa) "Jumlah Lulusan",  min(ipk) "Min. IPK", avg(ipk) as 'Rata-rata IPK' ,  max(ipk) "Max. IPK"
from fact_yudisium
group by tahun_ajaran_yudisium
order by tahun_ajaran_yudisium ''', con)

dfavgmasa = pd.read_sql('''
select 
    concat(round((masa_studi-mods)/12,0) ," tahun ", mods, " bulan")  as "Masa Studi" , 
    tahun_ajaran_yudisium as 'TA Yudisium'
from (
select  mod(masa_studi,12) as mods, masa_studi, tahun_ajaran_yudisium
from (
select round(avg(masa_studi_dalam_bulan),0) as "masa_studi", tahun_ajaran_yudisium from fact_yudisium
group by tahun_ajaran_yudisium) as data_mentah
) as data_ready
order by tahun_ajaran_yudisium
''', con)

dfallmasa = pd.read_sql('''
select
       TahunMAsuk as 'TA Masuk',
       `< 3 Tahun`, `3 - 3.5 Tahun`, `3.5 - 4.5 Tahun`, `4.5 - 7 Tahun`, `> 7 Tahun`,
       tahun_ajaran as 'TA' from
(select concat(dim_mahasiswa.tahun_angkatan,'/',cast(dim_mahasiswa.tahun_angkatan+1 as char(4))) as TahunMAsuk,
SUM(case when masa_studi_dalam_bulan < 36 then 1 else 0 end) as '< 3 Tahun',
SUM(case when masa_studi_dalam_bulan >= 36 AND masa_studi_dalam_bulan <42 then 1 else 0 end) as '3 - 3.5 Tahun',
SUM(case when masa_studi_dalam_bulan >= 42 AND masa_studi_dalam_bulan <54  then 1 else 0 end) as '3.5 - 4.5 Tahun',
SUM(case when masa_studi_dalam_bulan >= 54 AND masa_studi_dalam_bulan <=84 then 1 else 0 end) as '4.5 - 7 Tahun',
SUM(case when masa_studi_dalam_bulan >= 85 then 1 else 0 end) as '> 7 Tahun'
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

# dfmhsKP= pd.read_sql('''''',con)

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

dfkpall = pd.read_sql('''select count(*) as 'Jumlah KP', dim_semester.tahun_ajaran as "Tahun Ajaran",x.gasal as "Gasal",y.genap as "Genap" from fact_kp
inner join dim_semester on dim_semester.id_semester = fact_kp.id_semester
inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa = fact_kp.id_mahasiswa AND dim_mahasiswa.id_prodi = 9
inner join (select count(*) as gasal, dim_semester.tahun_ajaran from fact_kp
inner join dim_semester on dim_semester.id_semester = fact_kp.id_semester
inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa = fact_kp.id_mahasiswa AND dim_mahasiswa.id_prodi = 9
where dim_semester.semester = 1
group by dim_semester.tahun_ajaran
order by  dim_semester.tahun_ajaran)x on x.tahun_ajaran=dim_semester.tahun_ajaran
inner join (select count(*) as genap, dim_semester.tahun_ajaran from fact_kp
inner join dim_semester on dim_semester.id_semester = fact_kp.id_semester
inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa = fact_kp.id_mahasiswa AND dim_mahasiswa.id_prodi = 9
where dim_semester.semester = 2
group by dim_semester.tahun_ajaran
order by  dim_semester.tahun_ajaran)y on y.tahun_ajaran=dim_semester.tahun_ajaran
group by dim_semester.tahun_ajaran,x.gasal,y.genap
order by  dim_semester.tahun_ajaran''', con)

dfkppkm = pd.read_sql('''
select dim_semester.tahun_ajaran as 'Tahun Ajaran', count(*) as 'Jumlah KP' 
from fact_kp
inner join dim_semester on dim_semester.id_semester= fact_kp.id_semester 
inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa = fact_kp.id_mahasiswa AND dim_mahasiswa.id_prodi = 9
where fact_kp.is_pen_pkm = 1
group by dim_semester.tahun_ajaran
order by dim_semester.tahun_ajaran
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
                    style={'color': 'black'},
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
    dbc.CardLink(
        dbc.Card([
            html.H5('Grafik Lulusan Skripsi Tepat Waktu',
                    style=ttlgrf_style),
            dcc.Graph(
                id='grf_masastudi',
                style={'height': '100%'}
            )],
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
                html.H5('Rata-rata Masa Studi Lulusan',
                        style=ttlgrf_style),
                dt.DataTable(
                    id='tbl_avgmasa',
                    columns=[{"name": i, "id": i} for i in dfavgmasa.columns],
                    data=dfavgmasa.to_dict('records'),
                    sort_action='native',
                    sort_mode='multi',
                    style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                    style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    page_size=5
                )],
                style={'border': '1px solid #fafafa',
                       'border-radius': '10px',
                       'padding': '10px',
                       'width': '100%',
                       'height': '339px',
                       'justify-content': 'right',
                       'box-shadow': '5px 10px 30px #ebedeb'}
            ), width=3
        ),
        dbc.Col(
            dbc.Card([
                html.H5('Masa Studi Lulusan Program Sarjana',
                        style=ttlgrf_style),
                dt.DataTable(
                    id='tbl_allmasa',
                    columns=[{"name": i, "id": i} for i in dfallmasa.columns],
                    data=dfallmasa.to_dict('records'),
                    sort_action='native',
                    sort_mode='multi',
                    style_table={'width': '100%', 'height': '100%', 'padding': '10px',
                                 'overflowY': 'auto', 'margin-top': '25px'},
                    style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    page_size=5
                )
            ], style=cardgrf_style
            ), width=9
        )
    ], style={'margin-top': '10px'})
], style=cont_style)

kp_prodi = dbc.Container([
    dbc.Card([
        html.H5('KP Prodi Informatika',
                style=ttlgrf_style),
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='All', value='all',
                        children=[
                            dbc.CardLink([
                                dcc.Graph(id='grf_kpall')],
                                id='cll_grfkpall', n_clicks=0
                            )
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='PKM Dosen', value='PKMDosen',
                        children=[
                            dbc.CardLink([
                                dcc.Graph(id='grf_kppkm')],
                                id='cll_grfkppkm', n_clicks=0
                            )
                        ], style=tab_style, selected_style=selected_style)
            ], style=tab_style, id='tab_kpall', value='all'
            )
        ])
    ], style=cardgrf_style
    ),
    dbc.Collapse(
        id='cll_tblkp',
        is_open=False
    )
], style=cont_style)

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


@app.callback(
    Output('grf_masastudi', 'figure'),
    Input('grf_masastudi', 'id'),
)
def graphMasaStudi(id):
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
    fig = px.bar(df, y=df['Jumlah Mahasiswa'], x=df['Tahun Ajaran'])
    return fig


@app.callback(
    Output('grf_kpall', 'figure'),
    Input('grf_kpall', 'id'),
)
def graphJmlMhsKP(id):
    df = pd.read_sql('''select count(*) as 'Jumlah KP', dim_semester.tahun_ajaran as "Tahun Ajaran",if(dim_semester.semester=1,"GASAL","GENAP") as "Semester" from fact_kp
inner join dim_semester on dim_semester.id_semester = fact_kp.id_semester
inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa = fact_kp.id_mahasiswa AND dim_mahasiswa.id_prodi = 9
group by dim_semester.tahun_ajaran, dim_semester.semester
order by  dim_semester.tahun_ajaran, dim_semester.semester''', con)
    fig = px.bar(df, y=df['Jumlah KP'], x=df['Tahun Ajaran'], color=df['Semester'], barmode='group')
    return fig


@app.callback(
    Output('grf_kppkm', 'figure'),
    Input('grf_kppkm', 'id'),
)
def graphJmlMhsKPDosen(id):
    df = dfkppkm
    fig = px.bar(df, y=df['Jumlah KP'], x=df['Tahun Ajaran'])
    return fig


@app.callback(
    Output('cll_tblkp', 'is_open'),
    Output('cll_tblkp', 'children'),
    [Input("cll_grfkpall", "n_clicks"),
     Input("cll_grfkppkm", "n_clicks"),
     Input("tab_kpall", "value")],
    [State("cll_tblkp", "is_open")])
def toggle_collapse(nall, npkm, kp, is_open):
    isiAll = dbc.Card(
        dt.DataTable(
            id='tbl_kpall',
            columns=[{"name": i, "id": i} for i in dfkpall.columns],
            data=dfkpall.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            page_size=10,
            export_format='xlsx'
        ), style=cardgrf_style
    ),
    isiPKM = dbc.Card(
        dt.DataTable(
            id='tbl_kppkm',
            columns=[{"name": i, "id": i} for i in dfkppkm.columns],
            data=dfkppkm.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            page_size=10,
            export_format='xlsx'
        ), style=cardgrf_style
    ),
    if nall and kp == 'all':
        return not is_open, isiAll
    if npkm and kp == 'PKMDosen':
        return not is_open, isiPKM
    return is_open, None
