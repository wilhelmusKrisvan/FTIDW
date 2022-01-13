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
import model.dao_tgsakhir as data

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

dfdosbing = data.getMahasiswaBimbinganSkripsi()
dflulusan = data.getIPK()

dfavgmasa = data.getRateMasaStudi()
dfmasastudilulusan = data.getMasaStudi()
dfkppkm = data.getMahasiswaKPpkm()
dfkpall = data.getMahasiswaKP()

dfskripmhs = data.getMhahasiswaSkripsipkm()
dfmitra = data.getMitraKP()
dfttgumhs = data.getTTGU()
dfpersen_mhsLulus = data.getMahasiswaLulus()
dfpersen_mhsLulusAngkt = data.getMahasiswaLulusBandingTotal()

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

ipk_lulusan = dbc.Container([
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
        dbc.Col([
            dbc.CardLink(
                dbc.Card([
                    html.H5('Grafik Lulusan Setiap Tahun Ajaran',
                            style=ttlgrf_style),
                    dcc.Graph(
                        id='grf_jmllulusan',
                        style={'height': '100%'}
                    )],
                    style={'border': '1px solid #fafafa',
                           'border-radius': '10px',
                           'justify-content': 'center',
                           'width': '100%',
                           'box-shadow': '5px 10px 30px #ebedeb'}
                )
            ),
        ]),
        dbc.Col([
            dbc.CardLink(
                dbc.Card([
                    html.H5('Grafik Mahasiswa Lulus Skripsi Tepat Waktu',
                            style=ttlgrf_style),
                    dcc.Graph(
                        id='grf_skriplulusan',
                        style={'height': '100%'}
                    )],
                    style={'border': '1px solid #fafafa',
                           'border-radius': '10px',
                           'justify-content': 'center',
                           'width': '100%',
                           'box-shadow': '5px 10px 30px #ebedeb'}
                )
            ),
        ])
    ], style={'margin-top': '10px'}),
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
                    columns=[{"name": i, "id": i} for i in dfmasastudilulusan.columns],
                    data=dfmasastudilulusan.to_dict('records'),
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

ttguKP = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                html.H5('Mahasiswa KP yang Memiliki output Teknologi Tepat Guna (TTGU)',
                        style=ttlgrf_style),
                dt.DataTable(
                    id='tbl_ttgumhs',
                    columns=[{"name": i, "id": i} for i in dfttgumhs.columns],
                    data=dfttgumhs.to_dict('records'),
                    sort_action='native',
                    sort_mode='multi',
                    style_table={'width': '100%', 'height': '100%', 'padding': '10px',
                                 'overflowY': 'auto', 'margin-top': '25px'},
                    style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    page_size=5
                )
            ], style=cardgrf_style
            ),
        )
    ], style={'margin-top': '10px'})
], style=cont_style)

skripsi = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                html.H5('Mahasiswa Skripsi Terlibat PKM',
                        style=ttlgrf_style),
                dt.DataTable(
                    id='tbl_skripmhs',
                    columns=[{"name": i, "id": i} for i in dfskripmhs.columns],
                    data=dfskripmhs.to_dict('records'),
                    sort_action='native',
                    sort_mode='multi',
                    style_table={'width': '100%', 'height': '100%', 'padding': '10px',
                                 'overflowY': 'auto', 'margin-top': '25px'},
                    style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    page_size=5
                )
            ], style=cardgrf_style
            ),
        )
    ], style={'margin-top': '10px'})
], style=cont_style)

mitra = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                html.H5('Mitra yang Terlibat di setiap Semester berdasarkan Tingkat Wilayah',
                        style=ttlgrf_style),
                dt.DataTable(
                    id='tbl_mitra',
                    columns=[{"name": i, "id": i} for i in dfmitra.columns],
                    data=dfmitra.to_dict('records'),
                    sort_action='native',
                    sort_mode='multi',
                    style_table={'width': '100%', 'height': '100%', 'padding': '10px',
                                 'overflowY': 'auto', 'margin-top': '25px'},
                    style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    page_size=5
                )
            ], style=cardgrf_style
            ),
        )
    ], style={'margin-top': '10px'})
], style=cont_style)

persen_mhsLulus = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                html.H5('Persentase Mahasiswa Lulus Tepat Waktu setiap Tahun Ajaran',
                        style=ttlgrf_style),
                dt.DataTable(
                    id='tbl_persen_mhsLulus',
                    columns=[{"name": i, "id": i} for i in dfpersen_mhsLulus.columns],
                    data=dfpersen_mhsLulus.to_dict('records'),
                    sort_action='native',
                    sort_mode='multi',
                    style_table={'width': '100%', 'height': '100%', 'padding': '10px',
                                 'overflowY': 'auto', 'margin-top': '25px'},
                    style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    page_size=5
                )
            ], style=cardgrf_style
            ),
        ),
        dbc.Col([
            dbc.Card([
                html.H5('Persentase Mahasiswa Lulus dibanding Total Jumlah Mahasiswa',
                        style=ttlgrf_style),
                dt.DataTable(
                    id='tbl_persen_mhsLulusAngkt',
                    columns=[{"name": i, "id": i} for i in dfpersen_mhsLulusAngkt.columns],
                    data=dfpersen_mhsLulusAngkt.to_dict('records'),
                    sort_action='native',
                    sort_mode='multi',
                    style_table={'width': '100%', 'height': '100%', 'padding': '10px',
                                 'overflowY': 'auto', 'margin-top': '25px'},
                    style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                    page_size=3
                )
            ], style=cardgrf_style
            ),
        ]),
    ], style={'margin-top': '10px'})
], style=cont_style)

layout = html.Div([
    html.Div(html.H1('Analisis Skripsi, KP, dan Yudisium Prodi Informatika',
                     style={'margin-top': '30px', 'textAlign': 'center'}
                     )
             ),
    html.Div([dosbing]),
    html.Div([ipk_lulusan]),
    html.Div([persen_mhsLulus]),
    html.Div([masa_studi]),
    html.Div([kp_prodi]),
    html.Div([ttguKP]),
    html.Div([skripsi]),
    html.Div([mitra], style={'margin-bottom': '50px'})
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


@app.callback(
    Output('grf_dosbing', 'figure'),
    Input('grf_dosbing', 'id'),
    Input('drpdwn_TA', 'value'),
)
def graphDosbing(id, value):
    df = data.getDataFrameFromDBwithParams('''select tahun_ajaran 'Tahun Ajaran',semester_nama 'Semester',count(id_mahasiswa) 'Jumlah Mahasiswa', nama 'Nama Dosen' 
    from fact_skripsi fs
inner join dim_dosen dd on fs.id_dosen_pembimbing1=dd.id_dosen
inner join dim_semester ds on fs.id_semester = ds.id_semester
where tahun_ajaran=%(tahun_ajaran)s
group by tahun_ajaran,semester_nama,nama
order by tahun_ajaran desc, semester_nama asc''', {'tahun_ajaran': value})
    fig = px.bar(df, y=df['Nama Dosen'], x=df['Jumlah Mahasiswa'], color=df['Semester'], barmode='group')
    return fig


@app.callback(
    Output('grf_ipklulusan', 'figure'),
    Input('grf_ipklulusan', 'id'),
)
def graphIPKLulusan(id):
    dfavg = data.getDataFrameFromDB('''select avg(ipk) as 'Rata-rata IPK' ,  tahun_ajaran_yudisium as 'Tahun Ajaran'
from fact_yudisium
group by tahun_ajaran_yudisium
order by tahun_ajaran_yudisium''')
    dfmax = data.getDataFrameFromDB('''select max(ipk) as 'IPK' ,  tahun_ajaran_yudisium as 'Tahun Ajaran'
from fact_yudisium
group by tahun_ajaran_yudisium
order by tahun_ajaran_yudisium''')
    dfmin = data.getDataFrameFromDB('''select min(ipk) as 'IPK' ,  tahun_ajaran_yudisium as 'Tahun Ajaran'
    from fact_yudisium
    group by tahun_ajaran_yudisium
    order by tahun_ajaran_yudisium''')
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
    df = data.getDataFrameFromDB('''select count(*) as 'Jumlah Mahasiswa', tahun_ajaran_yudisium 'Tahun Ajaran'
from fact_yudisium
group by tahun_ajaran_yudisium
order by tahun_ajaran_yudisium''')
    fig = px.bar(df, y=df['Jumlah Mahasiswa'], x=df['Tahun Ajaran'], color=px.Constant('Jumlah Mahasiswa'),
                 labels=dict(x="Tahun Ajaran", y="Jumlah", color="Keterangan"))
    return fig


@app.callback(
    Output('grf_skriplulusan', 'figure'),
    Input('grf_skriplulusan', 'id'),
)
def graphJmlLulusan(id):
    df = data.getDataFrameFromDB('''select count(*) 'Jumlah Mahasiswa', 
    dim_mahasiswa.tahun_angkatan 'Angkatan',
    dim_semester.tahun_ajaran 'Tahun Ajaran'
from fact_skripsi
inner join(
select count(*) as jumlah, id_mahasiswa from fact_skripsi
group by id_mahasiswa
) data_skripsi on data_skripsi.id_mahasiswa = fact_skripsi.id_mahasiswa AND data_skripsi.jumlah=1
inner join dim_semester on dim_semester.id_semester = fact_skripsi.id_semester
inner join dim_mahasiswa on fact_skripsi.id_mahasiswa = dim_mahasiswa.id_mahasiswa
where id_dosen_penguji1 <>''
group by dim_semester.tahun_ajaran, dim_mahasiswa.tahun_angkatan
order by dim_semester.tahun_ajaran,dim_mahasiswa.tahun_angkatan''')
    fig = px.bar(df, y=df['Jumlah Mahasiswa'], x=df['Tahun Ajaran'], color=df['Angkatan'], barmode='stack')
    return fig


@app.callback(
    Output('grf_kpall', 'figure'),
    Input('grf_kpall', 'id'),
)
def graphJmlMhsKP(id):
    df = dfkpall
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
