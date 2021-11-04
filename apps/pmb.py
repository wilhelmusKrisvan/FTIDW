import dash
import pandas as pd
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from plotly.subplots import make_subplots

from dash.dependencies import Input, Output, State
from appConfig import app

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

dfseleksi = pd.read_sql('''select 
dataMahasiswa.tahun_aka as 'Tahun Ajaran', dy_tampung as 'Daya Tampung',jml_pendaftar as 'Pendaftar', 
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

dfmhsasing = pd.read_sql('''
select data.nama_prodi as 'Program Studi', tahun_semster as 'Tahun Ajaran', jumlah as 'Jumlah', parttime as 'Parttime', (jumlah - parttime) as 'Fulltime'
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

dfmhsrasio = pd.read_sql('''
select tahun_ajaran as 'Tahun Ajaran', jumlah as 'Jumlah', pendaftar_regis as 'Pendaftar Registrasi',
concat(round(jumlah/jumlah,0) ,' : ', round(pendaftar_regis/jumlah,2)) as 'Rasio Daya Tampung : Pendaftar Registrasi'
from(
    SELECT ds.tahun_ajaran,ds.kode_semester,dt.jumlah,
        sum(case when id_tanggal_registrasi is not null and id_prodi_diterima = 9 then 1 else 0 end) as pendaftar_regis
    FROM fact_pmb
    inner join dim_semester ds on fact_pmb.id_semester = ds.id_semester
    inner join dim_daya_tampung dt on ds.id_semester = dt.id_semester and dt.id_prodi = 9
    group by ds.kode_semester, ds.tahun_ajaran,dt.jumlah
    order by ds.tahun_ajaran
) as DataMentah
''', con)

dfmhssmasmk = pd.read_sql('''
select
       (case
           when tipe_sekolah_asal=1 then "NEGERI"
           WHEN tipe_sekolah_asal=2 THEN "SWASTA"
           when tipe_sekolah_asal=3 then "N/A"
       END)
           as 'Tipe Sekolah Asal', ds.tahun_ajaran as 'Tahun Ajaran', count(kode_pendaftar) AS 'Jumlah Pendaftar'
from fact_pmb
inner join dim_semester ds on fact_pmb.id_semester = ds.id_semester
where fact_pmb.id_prodi_diterima = 9 and fact_pmb.id_tanggal_registrasi is not null
group by ds.tahun_ajaran,'Tipe Sekolah Asal'
order by ds.tahun_ajaran
''', con)

dfmhsprovdaftar = pd.read_sql('''
select
    dl.provinsi as 'Provinsi', ds.tahun_ajaran as 'Tahun Ajaran', count(kode_pendaftar) AS 'Jumlah Pendaftar'
from fact_pmb
inner join dim_semester ds on fact_pmb.id_semester = ds.id_semester
inner join dim_lokasi dl ON fact_pmb.id_lokasi_rumah = dl.id_lokasi
group by ds.tahun_ajaran, dl.provinsi
order by ds.tahun_ajaran, dl.provinsi
''', con)

dfmhsprovlolos = pd.read_sql('''
select
    dl.provinsi as 'Provinsi', ds.tahun_ajaran as 'Tahun Ajaran', count(kode_pendaftar) AS 'Pendaftar Lolos Seleksi'
from fact_pmb
inner join dim_semester ds on fact_pmb.id_semester = ds.id_semester
inner join dim_lokasi dl ON fact_pmb.id_lokasi_rumah = dl.id_lokasi
where fact_pmb.id_tanggal_lolos_seleksi is not null and fact_pmb.id_prodi_diterima = 9
group by ds.tahun_ajaran, dl.provinsi
order by ds.tahun_ajaran, dl.provinsi
''', con)

dfmhsprovregis = pd.read_sql('''
select
    dl.provinsi as 'Provinsi', ds.tahun_ajaran as 'Tahun Ajaran', count(kode_pendaftar) AS 'Pendaftar Registrasi Ulang'
from fact_pmb
inner join dim_semester ds on fact_pmb.id_semester = ds.id_semester
inner join dim_lokasi dl ON fact_pmb.id_lokasi_rumah = dl.id_lokasi
where fact_pmb.id_prodi_diterima = 9 and fact_pmb.id_tanggal_registrasi is not null
group by ds.tahun_ajaran, dl.provinsi
order by ds.tahun_ajaran, dl.provinsi
''', con)

tabs_styles = {
    'background': '#FFFFFF',
    'border': 'white'
}

tab_style = {
    "background": "#FFFFFF",
    'border-bottom-color': '#ededed',
    'border-top-color': 'white',
    'border-left-color': 'white',
    'border-right-color': 'white',
    'align-items': 'center',
    'justify-content': 'center'
}

selected_style = {
    "background": "#FFFFFF",
    'align-items': 'center',
    'border-bottom': '3px solid',
    'border-top-color': 'white',
    'border-bottom-color': '#2780e3',
    'border-left-color': 'white',
    'border-right-color': 'white'

}

mhsseleksi = dbc.Container([
    dbc.Card([
        html.H5('2.a Seleksi Mahasiswa',
                style={'textAlign': 'center', 'padding': '10px'}),
        dbc.CardLink(
            dbc.CardBody(
                dcc.Graph(id='grf_mhsseleksi')
            ),
            id='cll_grfseleksi',
            n_clicks=0
        ),
    ]),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_seleksi',
                columns=[{"name": i, "id": i} for i in dfseleksi.columns],
                data=dfseleksi.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                page_size=10
            )
        ),
        id='cll_tblseleksi',
        is_open=False
    )
], style={'margin-top': '50px', 'justify-content': 'center'})

mhsasing = dbc.Container([
    dbc.Card([
        html.H5('2.b Mahasiswa Asing',
                style={'textAlign': 'center', 'padding': '10px'}),
        dcc.Tabs([
            dcc.Tab(label='FTI',
                    children=[
                        dbc.CardLink([dcc.Graph(id='grf_mhsasing')], id='cll_grfasing', n_clicks=0)
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='INF',
                    children=[
                        dbc.CardLink([dcc.Graph(id='grf_mhsasingINF')], id='cll_grfasing', n_clicks=0)
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='SI',
                    children=[
                        dbc.CardLink([dcc.Graph(id='grf_mhsasingSI')], id='cll_grfasing', n_clicks=0)
                    ],
                    style=tab_style, selected_style=selected_style)
        ])
    ], style={'padding': '10px'}),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_mhsasing',
                columns=[{"name": i, "id": i} for i in dfmhsasing.columns],
                data=dfmhsasing.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 70},
                page_size=10
            )
        ),
        id='cll_tblasing',
        is_open=False
    )
], style={'margin-top': '20px', 'justify-content': 'center'})

mhsrasio = dbc.Container([
    dbc.Card([
        html.H5('Rasio Daya Tampung : Pendaftar Registrasi Mahasiswa',
                style={'textAlign': 'center', 'padding': '10px'}),
        dbc.CardLink([
            dcc.Graph(id='grf_mhsrasio')
        ], id='cll_grfrasio',
            n_clicks=0)
    ]),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_mhsrasio',
                columns=[{"name": i, "id": i} for i in dfmhsrasio.columns],
                data=dfmhsrasio.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 70},
                page_size=10
            )
        ),
        id='cll_tblrasio',
        is_open=False
    )
], style={'margin-top': '20px', 'justify-content': 'center'})

mhsasmasmk = dbc.Container([
    dbc.Card([
        html.H5('Asal Sekolah Mahasiswa Pendaftar',
                style={'textAlign': 'center', 'padding': '10px'}),
        dbc.CardLink([
            dcc.Graph(id='grf_mhssmasmk')
        ], id='cll_grfsmasmk',
            n_clicks=0)
    ]),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_mhssmasmk',
                columns=[{"name": i, "id": i} for i in dfmhssmasmk.columns],
                data=dfmhssmasmk.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 70},
                page_size=10
            )
        ),
        id='cll_tblsmasmk',
        is_open=False
    )
], style={'margin-top': '20px', 'justify-content': 'center'})

mhsprovinsi = dbc.Container([
    dbc.Card([
        html.H5('Lokasi Asal Mahasiswa Pendaftar',
                style={'textAlign': 'center', 'padding': '10px'}),
        html.Div(
            dcc.Tabs([
                dcc.Tab(label='Pendaftar', value='daftar',
                        children=[
                            dbc.CardLink(
                                dcc.Graph(id='grf_mhsprovdaftar'),
                                id='cll_grfmhsprovdaftar', n_clicks=0
                            )
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Lolos Seleksi', value='lolos',
                        children=[
                            dbc.CardLink(
                                dcc.Graph(id='grf_mhsprovlolos'),
                                id='cll_grfmhsprovlolos', n_clicks=0
                            )
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Registrasi Ulang', value='regis',
                        children=[
                            dbc.CardLink(
                                dcc.Graph(id='grf_mhsprovregis'),
                                id='cll_grfmhsprovregis', n_clicks=0
                            )
                        ], style=tab_style, selected_style=selected_style)
            ], style=tabs_styles, id='tab_mhsprov', value='daftar'
            )
        )
    ], style={'padding': '10px'}),
    dbc.Collapse(

        id='cll_tblmhsprov',
        is_open=False
    ),
], style={'margin-top': '20px', 'justify-content': 'center'})


@app.callback(

    Output("cll_tblseleksi", "is_open"),
    [Input("cll_grfseleksi", "n_clicks")],
    [State("cll_tblseleksi", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tblasing", "is_open"),
    [Input("cll_grfasing", "n_clicks")],
    [State("cll_tblasing", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tblrasio", "is_open"),
    [Input("cll_grfrasio", "n_clicks")],
    [State("cll_tblrasio", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tblsmasmk", "is_open"),
    [Input("cll_grfsmasmk", "n_clicks")],
    [State("cll_tblsmasmk", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tblmhsprov", "is_open"),
    Output("cll_tblmhsprov", "children"),
    [Input("cll_grfmhsprovdaftar", "n_clicks"),
     Input("cll_grfmhsprovlolos", "n_clicks"),
     Input("cll_grfmhsprovregis", "n_clicks"),
     Input("tab_mhsprov", "value")],
    [State("cll_tblmhsprov", "is_open")])
def toggle_collapse(ndaftar, nlolos,nregis, prov, is_open):
    isiDaftar = dbc.Card(
        dt.DataTable(
            id='tbl_mhsprovdaftar',
            columns=[{"name": i, "id": i} for i in dfmhsprovdaftar.columns],
            data=dfmhsprovdaftar.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'overflowX': 'auto'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 70},
            page_size=10
        )
    ),
    isiLolos = dbc.Card(
        dt.DataTable(
            id='tbl_mhsprovlolos',
            columns=[{"name": i, "id": i} for i in dfmhsprovlolos.columns],
            data=dfmhsprovlolos.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'overflowX': 'auto'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 70},
            page_size=10
        )
    ),
    isiRegis=dbc.Card(
        dt.DataTable(
            id='tbl_mhsprovregis',
            columns=[{"name": i, "id": i} for i in dfmhsprovregis.columns],
            data=dfmhsprovregis.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'overflowX': 'auto'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 70},
            page_size=10
        )
    ),
    if ndaftar and prov == 'daftar':
        return not is_open, isiDaftar
    if nlolos and prov == 'lolos':
        return not is_open, isiLolos
    if nregis and prov == 'regis':
        return not is_open, isiRegis
    return is_open, None

layout = html.Div([
    html.Div(html.H1('Analisis Mahasiswa Baru Prodi Informatika',
                     style={'margin-top': '30px', 'textAlign': 'center'}
                     )
             ),
    html.Div([mhsseleksi]),
    html.Div([mhsasing]),
    html.Div([mhsrasio]),
    html.Div([mhsasmasmk]),
    html.Div([mhsprovinsi], style={'margin-bottom': '50px'})
], style={'justify-content': 'center'})


@app.callback(
    Output('grf_mhsseleksi', 'figure'),
    Input('grf_mhsseleksi', 'id')
)
def graphSeleksi(id):
    df = dfseleksi
    fig = px.bar(df, x=df['Tahun Ajaran'], y=df['Daya Tampung'], color=px.Constant('Daya Tampung'),
                 labels=dict(x="Tahun Ajaran", y="Jumlah", color="Jenis Pendaftar"))
    fig.add_scatter(x=df['Tahun Ajaran'], y=df['Pendaftar'], name='Pendaftar',
                    hovertemplate="Jenis Pendaftar=Pendaftar <br>Jumlah=%{y} </br> Tahun Ajaran= %{x}")
    fig.add_scatter(x=df['Tahun Ajaran'], y=df['Lolos Seleksi'], name='Lolos Seleksi',
                    line=dict(color='rgb(228, 245, 0)'),
                    hovertemplate="Jenis Pendaftar=Lolos Seleksi <br>Jumlah=%{y} </br> Tahun Ajaran= %{x}")
    fig.add_scatter(x=df['Tahun Ajaran'], y=df['Baru Reguler'], name='Baru Reguler',
                    line=dict(color='rgb(0, 143, 245)'),
                    hovertemplate="Jenis Pendaftar=Baru Reguler <br>Jumlah=%{y} </br> Tahun Ajaran= %{x}")
    fig.add_scatter(x=df['Tahun Ajaran'], y=df['Baru Transfer'], name='Baru Transfer',
                    line=dict(color='rgb(35, 68, 145)'),
                    hovertemplate="Jenis Pendaftar=Baru Transfer <br>Jumlah=%{y} </br> Tahun Ajaran= %{x}")
    fig.add_scatter(x=df['Tahun Ajaran'], y=df['Aktif Reguler'], name='Aktif Reguler',
                    line=dict(color='rgb(54, 235, 54)'),
                    hovertemplate="Jenis Pendaftar=Aktif Reguler <br>Jumlah=%{y} </br> Tahun Ajaran= %{x}")
    fig.add_scatter(x=df['Tahun Ajaran'], y=df['Aktif Transfer'], name='Aktif Transfer',
                    line=dict(color='rgb(35, 145, 35)'),
                    hovertemplate="Jenis Pendaftar=Aktif Transfer <br>Jumlah=%{y} </br> Tahun Ajaran= %{x}")
    return fig


@app.callback(
    Output('grf_mhsasing', 'figure'),
    Input('grf_mhsasing', 'id')
)
def graphMhsAsing(id):
    df = pd.read_sql('''select tahun_semster as "Tahun Semester", Jumlah, parttime,(Jumlah - parttime) as fulltime
from (
select concat(cast(tahun_angkatan-1 as char(4)),'/',tahun_angkatan) as tahun_semster, count(*) as Jumlah,
SUM(if(substr(nim,3,3)= 'ASG', 1, 0)) AS parttime
from dim_mahasiswa
inner join dim_prodi on dim_mahasiswa.id_prodi = dim_prodi.id_prodi AND (dim_prodi.id_prodi = 9||10)
where warga_negara = 'WNA'
group by tahun_semster, tahun_angkatan
) data
inner join dim_semester on dim_semester.tahun_ajaran = data.tahun_semster AND semester = 1 and dim_semester.id_semester <= (select id_semester from dim_semester where tahun_ajaran='2018/2019' limit 1)
order by tahun_semster asc''', con)
    fig = px.bar(df, x=df['Tahun Semester'], y=df['Jumlah'], color=px.Constant('Jumlah Total'),
                 labels=dict(x="Tahun Semester", y="Jumlah", color="Jenis Mahasiswa"))
    fig.add_scatter(x=df['Tahun Semester'], y=df['fulltime'], name='Full Time',
                    hovertemplate="Jenis Pendaftar=Full Time <br>Jumlah=%{y} </br> Tahun Semester= %{x}")
    fig.add_scatter(x=df['Tahun Semester'], y=df['parttime'], name='Part Time',
                    hovertemplate="Jenis Pendaftar=Part Time <br>Jumlah=%{y} </br> Tahun Semester= %{x}")
    return fig


@app.callback(
    Output('grf_mhsasingINF', 'figure'),
    Input('grf_mhsasingINF', 'id')
)
def graphMhsAsingINF(id):
    df = pd.read_sql('''select data.nama_prodi,tahun_semster as "Tahun Semester", Jumlah, parttime, (jumlah - parttime) as fulltime
from (
select dim_prodi.nama_prodi, concat(cast(tahun_angkatan-1 as char(4)),'/',tahun_angkatan) as tahun_semster, count(*) as jumlah,
SUM(if(substr(nim,3,3)= 'ASG', 1, 0)) AS parttime
from dim_mahasiswa
inner join dim_prodi on dim_mahasiswa.id_prodi = dim_prodi.id_prodi AND (dim_prodi.id_prodi = 9)
where warga_negara = 'WNA'
group by dim_prodi.nama_prodi,tahun_semster, tahun_angkatan
) data
inner join dim_semester on dim_semester.tahun_ajaran = data.tahun_semster AND semester = 1 and dim_semester.id_semester <= (select id_semester from dim_semester where tahun_ajaran='2018/2019' limit 1)
order by nama_prodi, tahun_semster asc''', con)
    fig = px.bar(df, x=df['Tahun Semester'], y=df['Jumlah'], color=px.Constant('Jumlah Total'),
                 labels=dict(x="Tahun Semester", y="Jumlah", color="Jenis Mahasiswa"))
    fig.add_scatter(x=df['Tahun Semester'], y=df['fulltime'], name='Full Time',
                    hovertemplate="Jenis Pendaftar=Full Time <br>Jumlah=%{y} </br> Tahun Semester= %{x}")
    fig.add_scatter(x=df['Tahun Semester'], y=df['parttime'], name='Part Time',
                    hovertemplate="Jenis Pendaftar=Part Time <br>Jumlah=%{y} </br> Tahun Semester= %{x}")
    return fig


@app.callback(
    Output('grf_mhsasingSI', 'figure'),
    Input('grf_mhsasingSI', 'id')
)
def graphMhsAsingSI(id):
    df = pd.read_sql('''select data.nama_prodi,tahun_semster as "Tahun Semester", Jumlah, parttime, (jumlah - parttime) as fulltime
from (
select dim_prodi.nama_prodi, concat(cast(tahun_angkatan-1 as char(4)),'/',tahun_angkatan) as tahun_semster, count(*) as jumlah,
SUM(if(substr(nim,3,3)= 'ASG', 1, 0)) AS parttime
from dim_mahasiswa
inner join dim_prodi on dim_mahasiswa.id_prodi = dim_prodi.id_prodi AND (dim_prodi.id_prodi = 10)
where warga_negara = 'WNA'
group by dim_prodi.nama_prodi,tahun_semster, tahun_angkatan
) data
inner join dim_semester on dim_semester.tahun_ajaran = data.tahun_semster AND semester = 1 and dim_semester.id_semester <= (select id_semester from dim_semester where tahun_ajaran='2018/2019' limit 1)
order by nama_prodi, tahun_semster asc''', con)
    fig = px.bar(df, x=df['Tahun Semester'], y=df['Jumlah'], color=px.Constant('Jumlah Total'),
                 labels=dict(x="Tahun Semester", y="Jumlah", color="Jenis Mahasiswa"))
    fig.add_scatter(x=df['Tahun Semester'], y=df['fulltime'], name='Full Time',
                    hovertemplate="Jenis Pendaftar=Full Time <br>Jumlah=%{y} </br> Tahun Semester= %{x}")
    fig.add_scatter(x=df['Tahun Semester'], y=df['parttime'], name='Part Time',
                    hovertemplate="Jenis Pendaftar=Part Time <br>Jumlah=%{y} </br> Tahun Semester= %{x}")
    return fig


@app.callback(
    Output('grf_mhsrasio', 'figure'),
    Input('grf_mhsrasio', 'id')
)
def graphRasioDTPR(id):
    df_dayaTampung = pd.read_sql('''select ds.tahun_ajaran as 'Tahun Ajaran', ddt.jumlah as "Jumlah Daya Tampung" from dim_daya_tampung ddt
inner join dim_semester ds on ddt.id_semester = ds.id_semester
where id_prodi = 9 and ds.tahun_ajaran in ('2015/2016',
'2016/2017','2017/2018','2018/2019')''', con)
    df_pendaftarRegistrasi = pd.read_sql('''select ds.tahun_ajaran as 'Tahun Ajaran', count(*)  as 'Jumlah Pendaftar'  from fact_pmb fpmb
inner join  dim_semester ds on fpmb.id_semester = ds.id_semester
where fpmb.id_tanggal_registrasi is not null and fpmb.id_prodi_diterima = 9
group by ds.tahun_ajaran
order by ds.tahun_ajaran''', con)
    df_lolosSeleksi = pd.read_sql('''select ds.tahun_ajaran as 'Tahun Ajaran', count(*)  as 'Jumlah Pendaftar' from fact_pmb fpmb
inner join  dim_semester ds on fpmb.id_semester = ds.id_semester
where fpmb.id_tanggal_lolos_seleksi is not null and fpmb.id_prodi_diterima = 9
group by ds.tahun_ajaran
order by ds.tahun_ajaran''', con)
    df_pendaftar = pd.read_sql('''select ds.tahun_ajaran as 'Tahun Ajaran', count(*)  as 'Jumlah Pendaftar'  from fact_pmb fpmb
inner join  dim_semester ds on fpmb.id_semester = ds.id_semester
group by ds.tahun_ajaran 
order by ds.tahun_ajaran''', con)
    fig = px.bar(df_dayaTampung, x=df_dayaTampung['Tahun Ajaran'], y=df_dayaTampung['Jumlah Daya Tampung'],
                 color=px.Constant('Daya Tampung'), labels=dict(x="Tahun Ajaran", y="Jumlah", color="Jenis Pendaftar"))
    fig.add_scatter(x=df_pendaftarRegistrasi['Tahun Ajaran'], y=df_pendaftarRegistrasi['Jumlah Pendaftar'],
                    name='Teregistrasi',
                    hovertemplate="Jenis Pendaftar=Teregistrasi <br>Jumlah=%{y} </br> Tahun Akdemik= %{x}")
    fig.add_scatter(x=df_lolosSeleksi['Tahun Ajaran'], y=df_lolosSeleksi['Jumlah Pendaftar'], name='Lolos Seleksi',
                    hovertemplate="Jenis Pendaftar=Lolos Seleksi <br>Jumlah=%{y} </br> Tahun Akdemik= %{x}")
    fig.add_scatter(x=df_pendaftar['Tahun Ajaran'], y=df_pendaftar['Jumlah Pendaftar'], name='Pendaftar',
                    hovertemplate="Jenis Pendaftar=Pendaftar <br>Jumlah=%{y} </br> Tahun Akdemik= %{x}")
    return fig


@app.callback(
    Output('grf_mhssmasmk', 'figure'),
    Input('grf_mhssmasmk', 'id')
)
def graphAsalSekolah(id):
    df = dfmhssmasmk
    fig = px.bar(df, x=df['Tahun Ajaran'], y=df['Jumlah Pendaftar'], color=df['Tipe Sekolah Asal'])
    fig.update_layout(barmode='group')
    return fig


@app.callback(
    Output('grf_mhsprovdaftar', 'figure'),
    Input('grf_mhsprovdaftar', 'id')
)
def graphProvincePendaftar(id):
    df = dfmhsprovdaftar
    fig = px.bar(df, x=df['Provinsi'], y=df['Jumlah Pendaftar'], color=df['Tahun Ajaran'])
    fig.update_layout(barmode='group')
    return fig


@app.callback(
    Output('grf_mhsprovlolos', 'figure'),
    Input('grf_mhsprovlolos', 'id')
)
def graphProvinceSeleksi(id):
    df = dfmhsprovlolos
    fig = px.bar(df, x=df['Provinsi'], y=df['Pendaftar Lolos Seleksi'], color=df['Tahun Ajaran'])
    fig.update_layout(barmode='group')
    return fig


@app.callback(
    Output('grf_mhsprovregis', 'figure'),
    Input('grf_mhsprovregis', 'id')
)
def graphProvinceRegis(id):
    df = dfmhsprovregis
    fig = px.bar(df, x=df['Provinsi'], y=df['Pendaftar Registrasi Ulang'], color=df['Tahun Ajaran'])
    fig.update_layout(barmode='group')
    return fig
