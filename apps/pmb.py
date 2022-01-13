import dash
import dash_table as dt
import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
from appConfig import app
from urllib.request import urlopen
import model.dao_pmb as data
import json

with urlopen(
        'https://raw.githubusercontent.com/wilhelmusKrisvan/GEOJSON_IDN/main/IDN_prov.json') as response:
    province = json.load(response)

dfseleksi = data.getSeleksi()
dfmhsasing = data.getMahasiswaAsing()
dfmhssmasmk = data.getJenisSekolahPendaftar()
dfmhsprovdaftar = data.getProvinsiDaftar()
dfmhsprovlolos = data.getProvinsiLolos()
dfmhsprovregis = data.getProvinsiRegis()
dfmhsrasio = data.getRasioCalonMahasiswa()
dfmhsJml = data.getPerkembanganJumlahMaba()
dfmhsPersenNaik = data.getPersentaseKenaikanMaba()

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

cardoncard_style = {
    'padding': '10px',
}

ttlgrf_style = {
    'textAlign': 'center',
    'padding': '10px',
    'color': 'black'
}

mhsseleksi = dbc.Container([
    dbc.Card([
        html.H5('2.a Seleksi Mahasiswa',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody(
                dcc.Graph(id='grf_mhsseleksi')
            ),
            id='cll_grfseleksi',
            n_clicks=0
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_seleksi',
                columns=[{"name": i, "id": i} for i in dfseleksi.columns],
                data=dfseleksi.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                page_size=10,
                export_format='xlsx'
            ), style=cardgrf_style
        ),
        id='cll_tblseleksi',
        is_open=False
    )
], style=cont_style)

mhsasing = dbc.Container([
    dbc.Card([
        html.H5('2.b Mahasiswa Asing',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='FTI', value='all',
                    children=[
                        dbc.CardLink([dcc.Graph(id='grf_mhsasing')], id='cll_grfasing', n_clicks=0)
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='INF', value='INF',
                    children=[
                        dbc.CardLink([dcc.Graph(id='grf_mhsasingINF')], id='cll_grfasingINF', n_clicks=0)
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='SI', value='SI',
                    children=[
                        dbc.CardLink([dcc.Graph(id='grf_mhsasingSI')], id='cll_grfasingSI', n_clicks=0)
                    ],
                    style=tab_style, selected_style=selected_style)
        ], id='tab_mhsasing', value='all')
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_tblasing',
        is_open=False,

    )
], style=cont_style)

mhsrasio = dbc.Container([
    dbc.Card([
        html.H5('Rasio Daya Tampung : Pendaftar Registrasi Mahasiswa',
                style=ttlgrf_style),
        dbc.CardLink([
            dcc.Graph(id='grf_mhsrasio')
        ], id='cll_grfrasio',
            n_clicks=0)
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_mhsrasio',
                columns=[{"name": i, "id": i} for i in dfmhsrasio.columns],
                data=dfmhsrasio.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                export_format='xlsx',
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 70},
                page_size=10
            ), style=cardgrf_style
        ),
        id='cll_tblrasio',
        is_open=False
    )
], style=cont_style)

mhsasmasmk = dbc.Container([
    dbc.Card([
        html.H5('Asal Sekolah Mahasiswa Pendaftar',
                style=ttlgrf_style),
        dbc.CardLink([
            dcc.Graph(id='grf_mhssmasmk')
        ], id='cll_grfsmasmk',
            n_clicks=0)
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_mhssmasmk',
                columns=[{"name": i, "id": i} for i in dfmhssmasmk.columns],
                data=dfmhssmasmk.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                export_format='xlsx',
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 70},
                page_size=10
            ), style=cardgrf_style
        ),
        id='cll_tblsmasmk',
        is_open=False
    )
], style=cont_style)

mhsprovinsi = dbc.Container([
    dbc.Card([
        html.H5('Lokasi Asal Calon Mahasiswa',
                style=ttlgrf_style),
        html.Div(
            dcc.Tabs([
                dcc.Tab(label='Pendaftar', value='daftar',
                        children=[
                            dbc.Card([
                                dbc.Row([
                                    dbc.Col([
                                        dcc.RadioItems(
                                            id='radio_daftar',
                                            options=[{'label': 'Persebaran', 'value': 'geojson'},
                                                     {'label': 'Jumlah', 'value': 'bar'}
                                                     ],
                                            value='geojson',
                                            style={'width': '100%', 'padding-bottom': '0px',
                                                   'padding-top': '0.7rem'},
                                            className='card-body',
                                            labelStyle={'display': 'block'}
                                        ),
                                    ], width=6),
                                    dbc.Col([
                                        html.Div([
                                            dcc.Dropdown(
                                                id='drpdwn_TAdaftar',
                                                options=[{'label': '2015/2016', 'value': '2015/2016'}],
                                                value='2015/2016',
                                                style={'color': 'black'},
                                                clearable=False,
                                            ),
                                        ],id='visi_TAdaftar')
                                    ], width=6),
                                ]),
                                dbc.CardLink(
                                    dcc.Graph(id='grf_mhsprovdaftar'),
                                    id='cll_grfmhsprovdaftar', n_clicks=0
                                ),
                            ], style={'padding': '10px', 'border': 'white'})
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Lolos Seleksi', value='lolos',
                        children=[
                            dbc.Card([
                                dbc.Row([
                                    dbc.Col([
                                        dcc.RadioItems(
                                            id='radio_lolos',
                                            options=[{'label': 'Persebaran', 'value': 'geojson'},
                                                     {'label': 'Jumlah', 'value': 'bar'}
                                                     ],
                                            value='geojson',
                                            style={'width': '100%', 'padding-bottom': '0px',
                                                   'padding-top': '0.7rem'},
                                            className='card-body',
                                            labelStyle={'display': 'block'}
                                        ),
                                    ], width=6),
                                    dbc.Col([
                                        html.Div([
                                            dcc.Dropdown(
                                                id='drpdwn_TAlolos',
                                                options=[{'label': '2015/2016', 'value': '2015/2016'}],
                                                value='2015/2016',
                                                style={'color': 'black'},
                                                clearable=False,
                                            ),
                                        ], id='visi_TAlolos')
                                    ], width=6),
                                ]),
                                dbc.CardLink(
                                    dcc.Graph(id='grf_mhsprovlolos'),
                                    id='cll_grfmhsprovlolos', n_clicks=0
                                ),
                            ], style={'padding': '10px', 'border': 'white'})
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Registrasi Ulang', value='regis',
                        children=[
                            dbc.Card([
                                dbc.Row([
                                    dbc.Col([
                                        dcc.RadioItems(
                                            id='radio_regis',
                                            options=[{'label': 'Persebaran', 'value': 'geojson'},
                                                     {'label': 'Jumlah', 'value': 'bar'}
                                                     ],
                                            value='geojson',
                                            style={'width': '100%', 'padding-bottom': '0px',
                                                   'padding-top': '0.7rem'},
                                            className='card-body',
                                            labelStyle={'display': 'block'}
                                        ),
                                    ], width=6),
                                    dbc.Col([
                                        html.Div([
                                            dcc.Dropdown(
                                                id='drpdwn_TAregis',
                                                options=[{'label': '2015/2016', 'value': '2015/2016'}],
                                                value='2015/2016',
                                                style={'color': 'black'},
                                                clearable=False,
                                            ),
                                        ], id='visi_TAregis')
                                    ], width=6),
                                ]),
                                dbc.CardLink(
                                    dcc.Graph(id='grf_mhsprovregis'),
                                    id='cll_grfmhsprovregis', n_clicks=0
                                ),
                            ], style={'padding': '10px', 'border': 'white'})
                        ], style=tab_style, selected_style=selected_style)
            ], style=tabs_styles, id='tab_mhsprov', value='daftar'
            )
        )
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_tblmhsprov',
        is_open=False
    ),
], style=cont_style)

mhsKembangJml = dbc.Container([
    dbc.Card([
        html.H5('Perkembangan Jumlah Penerimaan Mahasiswa Baru',
                style=ttlgrf_style),
        dbc.CardLink([
            dcc.Graph(id='grf_mhsJml')
        ], id='cll_grfJml',
            n_clicks=0)
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_Jml',
                columns=[{"name": i, "id": i} for i in dfmhsJml.columns],
                data=dfmhsJml.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                export_format='xlsx',
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 70},
                page_size=10
            ), style=cardgrf_style
        ),
        id='cll_tblJml',
        is_open=False
    )
], style=cont_style)

mhsPersenNaik = dbc.Container([
    dbc.Card([
        html.H5('Persentase Kenaikan Penerimaan Mahasiswa Baru',
                style=ttlgrf_style),
        dbc.CardLink([
            dcc.Graph(id='grf_mhsPersenNaik')
        ], id='cll_grfPersenNaik',
            n_clicks=0)
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_PersenNaik',
                columns=[{"name": i, "id": i} for i in dfmhsPersenNaik.columns],
                data=dfmhsPersenNaik.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                export_format='xlsx',
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 70},
                page_size=10
            ), style=cardgrf_style
        ),
        id='cll_tblPersenNaik',
        is_open=False
    )
], style=cont_style)

layout = html.Div([
    html.Div(html.H1('Analisis Mahasiswa Baru Prodi Informatika',
                     style={'margin-top': '30px', 'textAlign': 'center'}
                     )
             ),
    html.Div([mhsseleksi]),
    html.Div([mhsasing]),
    html.Div([mhsrasio]),
    html.Div([mhsasmasmk]),
    html.Div([mhsprovinsi]),
    html.Div([mhsKembangJml]),
    html.Div([mhsPersenNaik],style={'margin-bottom': '50px'}),
], style={'justify-content': 'center'})



# CONTROL COLLAPSE
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
    Output("cll_tblasing", "children"),
    [Input("cll_grfasing", "n_clicks"),
     Input("cll_grfasingINF", "n_clicks"),
     Input("cll_grfasingSI", "n_clicks"),
     Input('tab_mhsasing', 'value')],
    [State("cll_tblasing", "is_open")])
def toggle_collapse(nall, ninf, nsi, mhs, is_open):
    isiMhsAsing = dbc.Card(
        dt.DataTable(
            id='tbl_mhsasing',
            columns=[{"name": i, "id": i} for i in dfmhsasing.columns],
            data=dfmhsasing.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            export_format='xlsx',
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 70},
            page_size=10
        ), style=cardgrf_style
    )
    if nall and mhs == 'all':
        return not is_open, isiMhsAsing
    if ninf and mhs == 'INF':
        return not is_open, isiMhsAsing
    if nsi and mhs == 'SI':
        return not is_open, isiMhsAsing
    return is_open, None

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
def toggle_collapse(ndaftar, nlolos, nregis, prov, is_open):
    isiDaftar = dbc.Card(
        dt.DataTable(
            id='tbl_mhsprovdaftar',
            columns=[{"name": i, "id": i} for i in dfmhsprovdaftar.columns],
            data=dfmhsprovdaftar.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            export_format='xlsx',
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 70},
            page_size=10
        ), style=cardgrf_style
    ),
    isiLolos = dbc.Card(
        dt.DataTable(
            id='tbl_mhsprovlolos',
            columns=[{"name": i, "id": i} for i in dfmhsprovlolos.columns],
            data=dfmhsprovlolos.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            export_format='xlsx',
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 70},
            page_size=10
        ), style=cardgrf_style
    ),
    isiRegis = dbc.Card(
        dt.DataTable(
            id='tbl_mhsprovregis',
            columns=[{"name": i, "id": i} for i in dfmhsprovregis.columns],
            data=dfmhsprovregis.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            export_format='xlsx',
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 70},
            page_size=10
        ), style=cardgrf_style
    ),
    if ndaftar and prov == 'daftar':
        return not is_open, isiDaftar
    if nlolos and prov == 'lolos':
        return not is_open, isiLolos
    if nregis and prov == 'regis':
        return not is_open, isiRegis
    return is_open, None

@app.callback(
    Output("cll_tblJml", "is_open"),
    [Input("cll_grfJml", "n_clicks")],
    [State("cll_tblJml", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("cll_tblPersenNaik", "is_open"),
    [Input("cll_grfPersenNaik", "n_clicks")],
    [State("cll_tblPersenNaik", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open



# SHOW GRAPHIC ANALYSIS
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
    df = data.getDataFrameFromDB('''select tahun_semster as "Tahun Semester", Jumlah, parttime,(Jumlah - parttime) as fulltime
from (
select concat(cast(tahun_angkatan-1 as char(4)),'/',tahun_angkatan) as tahun_semster, count(*) as Jumlah,
SUM(if(substr(nim,3,3)= 'ASG', 1, 0)) AS parttime
from dim_mahasiswa
inner join dim_prodi on dim_mahasiswa.id_prodi = dim_prodi.id_prodi AND (dim_prodi.id_prodi = 9||10)
where warga_negara = 'WNA'
group by tahun_semster, tahun_angkatan
) data
inner join dim_semester on dim_semester.tahun_ajaran = data.tahun_semster AND semester = 1 and dim_semester.id_semester <= (select id_semester from dim_semester where tahun_ajaran='2018/2019' limit 1)
order by tahun_semster asc''')
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
    df = data.getDataFrameFromDB('''select data.nama_prodi,tahun_semster as "Tahun Semester", Jumlah, parttime, (jumlah - parttime) as fulltime
from (
select dim_prodi.nama_prodi, concat(cast(tahun_angkatan-1 as char(4)),'/',tahun_angkatan) as tahun_semster, count(*) as jumlah,
SUM(if(substr(nim,3,3)= 'ASG', 1, 0)) AS parttime
from dim_mahasiswa
inner join dim_prodi on dim_mahasiswa.id_prodi = dim_prodi.id_prodi AND (dim_prodi.id_prodi = 9)
where warga_negara = 'WNA'
group by dim_prodi.nama_prodi,tahun_semster, tahun_angkatan
) data
inner join dim_semester on dim_semester.tahun_ajaran = data.tahun_semster AND semester = 1 and dim_semester.id_semester <= (select id_semester from dim_semester where tahun_ajaran='2018/2019' limit 1)
order by nama_prodi, tahun_semster asc''')
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
    df = data.getDataFrameFromDB('''select data.nama_prodi,tahun_semster as "Tahun Semester", Jumlah, parttime, (jumlah - parttime) as fulltime
from (
select dim_prodi.nama_prodi, concat(cast(tahun_angkatan-1 as char(4)),'/',tahun_angkatan) as tahun_semster, count(*) as jumlah,
SUM(if(substr(nim,3,3)= 'ASG', 1, 0)) AS parttime
from dim_mahasiswa
inner join dim_prodi on dim_mahasiswa.id_prodi = dim_prodi.id_prodi AND (dim_prodi.id_prodi = 10)
where warga_negara = 'WNA'
group by dim_prodi.nama_prodi,tahun_semster, tahun_angkatan
) data
inner join dim_semester on dim_semester.tahun_ajaran = data.tahun_semster AND semester = 1 and dim_semester.id_semester <= (select id_semester from dim_semester where tahun_ajaran='2018/2019' limit 1)
order by nama_prodi, tahun_semster asc''')
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
    df_dayaTampung = data.getDataFrameFromDB('''select ds.tahun_ajaran as 'Tahun Ajaran', ddt.jumlah as "Jumlah Daya Tampung" from dim_daya_tampung ddt
inner join dim_semester ds on ddt.id_semester = ds.id_semester
where id_prodi = 9 and ds.tahun_ajaran in ('2015/2016',
'2016/2017','2017/2018','2018/2019')''')
    df_pendaftarRegistrasi = data.getDataFrameFromDB('''select ds.tahun_ajaran as 'Tahun Ajaran', count(*)  as 'Jumlah Pendaftar'  from fact_pmb fpmb
inner join  dim_semester ds on fpmb.id_semester = ds.id_semester
where fpmb.id_tanggal_registrasi is not null and fpmb.id_prodi_diterima = 9
group by ds.tahun_ajaran
order by ds.tahun_ajaran''')
    df_lolosSeleksi = data.getDataFrameFromDB('''select ds.tahun_ajaran as 'Tahun Ajaran', count(*)  as 'Jumlah Pendaftar' from fact_pmb fpmb
inner join  dim_semester ds on fpmb.id_semester = ds.id_semester
where fpmb.id_tanggal_lolos_seleksi is not null and fpmb.id_prodi_diterima = 9
group by ds.tahun_ajaran
order by ds.tahun_ajaran''')
    df_pendaftar = data.getDataFrameFromDB('''select ds.tahun_ajaran as 'Tahun Ajaran', count(*)  as 'Jumlah Pendaftar'  from fact_pmb fpmb
inner join  dim_semester ds on fpmb.id_semester = ds.id_semester
group by ds.tahun_ajaran 
order by ds.tahun_ajaran''')
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
    Output('grf_jsonprovdaftar', 'figure'),
    Output('grf_jsonprovlolos', 'figure'),
    Output('grf_jsonprovregis', 'figure'),
    Input('grf_jsonprovdaftar', 'id')
)
def graphProvinceJson(id):
    figdaftar = px.choropleth_mapbox(dfmhsprovdaftar, geojson=province, locations="Provinsi",
                                     color_continuous_scale="Viridis",
                                     featureidkey="properties.Propinsi",
                                     center={"lat": -0.789275, "lon": 113.921327}, zoom=3.5,
                                     mapbox_style="carto-positron",
                                     color='Jumlah Pendaftar')
    figlolos = px.choropleth_mapbox(dfmhsprovlolos, geojson=province, locations="Provinsi",
                                    color_continuous_scale="Viridis",
                                    featureidkey="properties.Propinsi",
                                    center={"lat": -0.789275, "lon": 113.921327}, zoom=3.5,
                                    mapbox_style="carto-positron",
                                    color='Pendaftar Lolos Seleksi')
    figregis = px.choropleth_mapbox(dfmhsprovregis, geojson=province, locations="Provinsi",
                                    color_continuous_scale="Viridis",
                                    featureidkey="properties.Propinsi",
                                    center={"lat": -0.47399, "lon": 113.29266}, zoom=3.5,
                                    mapbox_style="carto-positron",
                                    color='Pendaftar Registrasi Ulang')
    return figdaftar, figlolos, figregis

@app.callback(
    Output('grf_mhsprovdaftar', 'figure'),
    Output('visi_TAdaftar', 'hidden'),
    Input('drpdwn_TAdaftar', 'value'),
    Input('radio_daftar', 'value')
)
def graphProvinceDaftar(valueDrpdwn, valueRadio):
    dfJson = data.getDataFrameFromDBwithParams('''select
    dl.provinsi as 'Provinsi', ds.tahun_ajaran as 'Tahun Ajaran', count(kode_pendaftar) AS 'Jumlah Pendaftar'
from fact_pmb
inner join dim_semester ds on fact_pmb.id_semester = ds.id_semester
inner join dim_lokasi dl ON fact_pmb.id_lokasi_rumah = dl.id_lokasi
where ds.tahun_ajaran=%(TA)s
group by ds.tahun_ajaran, dl.provinsi
order by ds.tahun_ajaran, dl.provinsi''', {'TA': valueDrpdwn})
    if valueRadio == 'bar':
        bardaftar = px.bar(dfmhsprovdaftar, x=dfmhsprovdaftar['Provinsi'], y=dfmhsprovdaftar['Jumlah Pendaftar'],
                           color=dfmhsprovdaftar['Tahun Ajaran'], barmode='group')
        bardaftar.update_layout(xaxis=go.layout.XAxis(tickangle=45))
        return bardaftar, True
    else:
        jsondaftar = px.choropleth_mapbox(dfJson, geojson=province, locations="Provinsi",
                                          color_continuous_scale="Viridis",
                                          featureidkey="properties.Propinsi",
                                          center={"lat": -0.47399, "lon": 113.29266}, zoom=3.25,
                                          mapbox_style="carto-positron",
                                          color='Jumlah Pendaftar')
        return jsondaftar, False

@app.callback(
    Output('grf_mhsprovlolos', 'figure'),
    Output('visi_TAlolos', 'hidden'),
    Input('drpdwn_TAlolos', 'value'),
    Input('radio_lolos', 'value')
)
def graphProvinceLolos(valueDrpdwn, valueRadio):
    dfJson = data.getDataFrameFromDBwithParams('''select
    dl.provinsi as 'Provinsi', ds.tahun_ajaran as 'Tahun Ajaran', count(kode_pendaftar) AS 'Pendaftar Lolos Seleksi'
from fact_pmb
inner join dim_semester ds on fact_pmb.id_semester = ds.id_semester
inner join dim_lokasi dl ON fact_pmb.id_lokasi_rumah = dl.id_lokasi
where fact_pmb.id_tanggal_lolos_seleksi is not null and fact_pmb.id_prodi_diterima = 9
and ds.tahun_ajaran=%(TA)s
group by ds.tahun_ajaran, dl.provinsi
order by ds.tahun_ajaran, dl.provinsi''', {'TA': valueDrpdwn})
    if valueRadio == 'bar':
        barlolos = px.bar(dfmhsprovlolos, x=dfmhsprovlolos['Provinsi'], y=dfmhsprovlolos['Pendaftar Lolos Seleksi'],
                           color=dfmhsprovlolos['Tahun Ajaran'], barmode='group')
        barlolos.update_layout(xaxis=go.layout.XAxis(tickangle=45))
        return barlolos, True
    else:
        jsonlolos = px.choropleth_mapbox(dfJson, geojson=province, locations="Provinsi",
                                          color_continuous_scale="Viridis",
                                          featureidkey="properties.Propinsi",
                                          center={"lat": -0.47399, "lon": 113.29266}, zoom=3.25,
                                          mapbox_style="carto-positron",
                                          color='Pendaftar Lolos Seleksi')
        return jsonlolos, False

@app.callback(
    Output('grf_mhsprovregis', 'figure'),
    Output('visi_TAregis', 'hidden'),
    Input('drpdwn_TAregis', 'value'),
    Input('radio_regis', 'value')
)
def graphProvinceRegis(valueDrpdwn, valueRadio):
    dfJson = data.getDataFrameFromDBwithParams('''select
    dl.provinsi as 'Provinsi', ds.tahun_ajaran as 'Tahun Ajaran', count(kode_pendaftar) AS 'Pendaftar Registrasi Ulang'
from fact_pmb
inner join dim_semester ds on fact_pmb.id_semester = ds.id_semester
inner join dim_lokasi dl ON fact_pmb.id_lokasi_rumah = dl.id_lokasi
where fact_pmb.id_prodi_diterima = 9 and fact_pmb.id_tanggal_registrasi is not null
and ds.tahun_ajaran=%(TA)s
group by ds.tahun_ajaran, dl.provinsi
order by ds.tahun_ajaran, dl.provinsi''', {'TA': valueDrpdwn})
    if valueRadio == 'bar':
        barregis = px.bar(dfmhsprovregis, x=dfmhsprovregis['Provinsi'], y=dfmhsprovregis['Pendaftar Registrasi Ulang'],
                           color=dfmhsprovregis['Tahun Ajaran'], barmode='group')
        barregis.update_layout(xaxis=go.layout.XAxis(tickangle=45))
        return barregis, True
    else:
        jsonregis = px.choropleth_mapbox(dfJson, geojson=province, locations="Provinsi",
                                          color_continuous_scale="Viridis",
                                          featureidkey="properties.Propinsi",
                                          center={"lat": -0.789275, "lon": 113.921327}, zoom=3.25,
                                          mapbox_style="carto-positron",
                                          color='Pendaftar Registrasi Ulang')
        return jsonregis, False

@app.callback(
    Output('grf_mhsJml', 'figure'),
    Input('grf_mhsJml', 'id')
)
def graphPerkembanganJumlahMaba(id):
    df = dfmhsJml
    fig = px.line(df, x=df['Tahun Ajaran'], y=df['Jumlah'],)
    fig.update_traces(mode='lines+markers')
    return fig

@app.callback(
    Output('grf_mhsPersenNaik', 'figure'),
    Input('grf_mhsPersenNaik', 'id')
)
def graphPersentaseKenaikanMaba(id):
    df = dfmhsPersenNaik
    fig = px.line(df, x=df['Tahun Ajaran'], y=df['% Pertumbuhan'])
    fig.update_traces(mode='lines+markers')
    return fig