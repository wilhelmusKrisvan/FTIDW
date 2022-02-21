import dash
import pandas as pd
import dash_table as dt
import plotly.express as px
import dash_bootstrap_components as dbc
from apps import pmb, kbm, mbkm, kegiatan_kerjasama, tgsakhir, alumni, ppp, dosen
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from appConfig import app, server
from dash import html, dcc
import model.dao_mbkm as data
from datetime import date

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

listDropdown = []
for x in range(0, 5):
    counter = x + 1
    listDropdown.append(
        str(int(date.today().strftime('%Y')) - 5 + x) + '/' + str(int(date.today().strftime('%Y')) - 4 + x))

dfmahasiswambkm = data.getMahasiswaMBKMperSemester()
dfmitrambkm = data.getMitraMBKM()
dfjumlmitrambkm = data.getJumlMitraMBKMperSemester()
dfdosbingmbkm = data.getDosbingMBKMperSemester()
dfreratasksmbkm = data.getRerataSKSMBKMperSemester()

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

card_style = {
    'border': '1px solid #fafafa',
    'border-radius': '10px',
    'padding': '10px'
}

ttlgrf_style = {
    'textAlign': 'center',
    'padding': '10px',
    'color': 'black'
}

button_style = {
    'width': '120px',
    'height': '50px',
    'border-radius': '10px',
    'box-shadow': '5px 10px 20px #ebedeb',
    'border': '1px solid #fafafa',
    'color': 'white',
    'background-color': '#2780e3',
    'right': '0',
}

dftrmitraMBKM = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H5('Daftar Mitra MBKM', style=ttlgrf_style),
                dt.DataTable(
                    id='dfmitrambkm',
                    columns=[
                        {'name': i, 'id': i} for i in dfmitrambkm.columns
                    ],
                    data=dfmitrambkm.to_dict('records'),
                    sort_action='native',
                    sort_mode='multi',
                    style_table={'padding': '10px', 'overflowX': 'auto'},
                    style_header={'textAlign': 'center'},
                    style_data={'font-size': '80%', 'textAlign': 'center'},
                    style_cell={'width': 95},
                    page_size=10,
                )
            ], style=cardgrf_style),
        ], width=12)
    ], style={'margin-top': '10px'})
], style=cont_style)

# +grafcollapse
jumlmitraMBKM = dbc.Container([
    dbc.Card([
        html.H5('Jumlah Mitra MBKM per Semester',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H6('Dari:'),
                        html.Div([
                            dcc.Dropdown(
                                options=[{'label': i, 'value': i} for i in listDropdown],
                                value=listDropdown[0],
                                id='Fromdrpdwn_jumlmitrambkm',
                                style={'color': 'black'},
                                clearable=False,
                                placeholder='-',
                            ),
                        ]),
                    ], width=3),
                    dbc.Col([
                        html.H6('Sampai:'),
                        html.Div([
                            dcc.Dropdown(
                                options=[{'label': i, 'value': i} for i in listDropdown],
                                value=listDropdown[4],
                                id='Todrpdwn_jumlmitrambkm',
                                style={'color': 'black'},
                                clearable=False,
                                placeholder='-',
                            ),
                        ]),
                    ], width=3)
                ]),
                dcc.Graph(id='grf_jumlmitrambkm'),
                dbc.Button('Lihat Tabel',
                           id='cll_grfjumlmitrambkm',
                           n_clicks=0,
                           style=button_style)
            ]),
            id='cll_grfjumlmitrambkm',
            n_clicks=0
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_jumlmitrambkm',
                columns=[
                    {'name': i, 'id': i} for i in dfjumlmitrambkm.columns],
                data=dfjumlmitrambkm.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'padding': '10px', 'overflowX': 'auto'},
                style_header={'textAlign': 'center'},
                style_data={'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 95},
                page_size=10,
                export_format='xlsx'
            ), style=cardgrf_style
        ),
        id='cll_tbljumlmitrambkm',
        is_open=False
    )
], style=cont_style)

# +grafcollapse
dosbingMBKM = dbc.Container([
    dbc.Card([
        html.H5('Jumlah Dosen Pembimbing MBKM',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H6('Dari:'),
                        html.Div([
                            dcc.Dropdown(
                                options=[{'label': i, 'value': i} for i in listDropdown],
                                value=listDropdown[0],
                                id='Fromdrpdwn_dosbingmbkm',
                                style={'color': 'black'},
                                clearable=False,
                                placeholder='-',
                            ),
                        ]),
                    ], width=3),
                    dbc.Col([
                        html.H6('Sampai:'),
                        html.Div([
                            dcc.Dropdown(
                                options=[{'label': i, 'value': i} for i in listDropdown],
                                value=listDropdown[4],
                                id='Todrpdwn_dosbingmbkm',
                                style={'color': 'black'},
                                clearable=False,
                                placeholder='-',
                            ),
                        ]),
                    ], width=3)
                ]),
                dcc.Graph(id='grf_jumldosbingmbkm'),
                dbc.Button('Lihat Tabel',
                           id='cll_grfjumldosbingmbkm',
                           n_clicks=0,
                           style=button_style)
            ]),
            id='cll_grfjumldosbingmbkm',
            n_clicks=0
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_dosbingmbkm',
                columns=[
                    {'name': i, 'id': i} for i in dfdosbingmbkm.columns
                ],
                data=dfdosbingmbkm.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'padding': '10px', 'overflowX': 'auto'},
                style_header={'textAlign': 'center'},
                style_data={'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 95},
                page_size=10,
                export_format='xlsx'
            ), style=cardgrf_style
        ),
        id='cll_tbljumldosbingmbkm',
        is_open=False
    )
], style=cont_style)

# +grafcollapse
mahasiswaMBKM = dbc.Container([
    dbc.Card([
        html.H5('Jumlah Mahasiswa MBKM',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H6('Dari:'),
                        html.Div([
                        dcc.Dropdown(
                            options=[{'label': i, 'value': i} for i in listDropdown],
                            value=listDropdown[0],
                            id='Fromdrpdwn_mhsseleksi',
                            style={'color': 'black'},
                            clearable=False,
                            placeholder='-',
                        ),
                        ]),
                    ],width=3),
                    dbc.Col([
                        html.H6('Sampai:'),
                        html.Div([
                            dcc.Dropdown(
                                options=[{'label': i, 'value': i} for i in listDropdown],
                                value=listDropdown[4],
                                id='Todrpdwn_mhsseleksi',
                                style={'color': 'black'},
                                clearable=False,
                                placeholder='-',
                            ),
                        ]),
                    ],width=3)
                ]),
                dcc.Graph(id='grf_mahasiswambkm'),
                dbc.Button('Lihat Tabel',
                           id='cll_grfmahasiswambkm',
                           n_clicks=0,
                           style=button_style)
            ]),
            id='cll_grfmahasiswambkm',
            n_clicks=0
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_mahasiswambkm',
                columns=[
                    {'name': i, 'id': i} for i in dfmahasiswambkm.columns
                ],
                data=dfmahasiswambkm.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'padding': '10px', 'overflowX': 'auto'},
                style_header={'textAlign': 'center'},
                style_data={'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 95},
                page_size=10,
                export_format='xlsx'
            ), style=cardgrf_style
        ),
        id='cll_tblmahasiswambkm',
        is_open=False
    )
], style=cont_style)

# +grafcollapse
reratasksMBKM = dbc.Container([
    dbc.Card([
        html.H5('Rata-rata Konversi SKS MBKM',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H6('Dari:'),
                        html.Div([
                            dcc.Dropdown(
                                options=[{'label': i, 'value': i} for i in listDropdown],
                                value=listDropdown[0],
                                id='Fromdrpdwn_reratasksmbkm',
                                style={'color': 'black'},
                                clearable=False,
                                placeholder='-',
                            ),
                        ]),
                    ], width=3),
                    dbc.Col([
                        html.H6('Sampai:'),
                        html.Div([
                            dcc.Dropdown(
                                options=[{'label': i, 'value': i} for i in listDropdown],
                                value=listDropdown[4],
                                id='Todrpdwn_reratasksmbkm',
                                style={'color': 'black'},
                                clearable=False,
                                placeholder='-',
                            ),
                        ]),
                    ], width=3)
                ]),
                dcc.Graph(id='grf_reratasksmbkm'),
                dbc.Button('Lihat Tabel',
                           id='cll_grfreratasksmbkm',
                           n_clicks=0,
                           style=button_style)
            ]),
            id='cll_grfreratasksmbkm',
            n_clicks=0
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_reratasksmbkm',
                columns=[
                    {'name': i, 'id': i} for i in dfreratasksmbkm.columns
                ],
                data=dfreratasksmbkm.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'padding': '10px', 'overflowX': 'auto'},
                style_header={'textAlign': 'center'},
                style_data={'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 95},
                page_size=10,
                export_format='xlsx'
            ), style=cardgrf_style
        ),
        id='cll_tblreratasksmbkm',
        is_open=False
    )
], style=cont_style)

#layout
mbkm = dbc.Container([
    html.Div([
        html.H1('Analisis MBKM',
                style=ttlgrf_style),
        html.A(className='name'),
        dcc.Tabs([
            dcc.Tab(label='Mahasiswa', value='mahasiswa',
                    children=[
                        mahasiswaMBKM,
                        reratasksMBKM
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Dosen Pembimbing', value='dosen',
                    children=[
                        dosbingMBKM
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Mitra', value='mitra',
                    children=[
                        jumlmitraMBKM,
                        dftrmitraMBKM
                    ],
                    style=tab_style, selected_style=selected_style)
        ], style=tabs_styles, value='mahasiswa'),\
        html.Br(),
        dbc.Container([
            dcc.Link([
                dbc.Button('^', style=button_style),
            ], href='#name'),
        ],style={'margin-left': '90%',"position": "sticky"}),

    ])
], style=cont_style)

layout = html.Div([
    html.Div([mbkm], style={'margin-bottom': '50px'})
], style={'justify-content': 'center'})

#COLLAPSE CALLBACK
@app.callback(
    Output("cll_tblmahasiswambkm", "is_open"),
    [Input("cll_grfmahasiswambkm", "n_clicks")],
    [State("cll_tblmahasiswambkm", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("cll_tblreratasksmbkm", "is_open"),
    [Input("cll_grfreratasksmbkm", "n_clicks")],
    [State("cll_tblreratasksmbkm", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("cll_tbljumldosbingmbkm", "is_open"),
    [Input("cll_grfjumldosbingmbkm", "n_clicks")],
    [State("cll_tbljumldosbingmbkm", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("cll_tbljumlmitrambkm", "is_open"),
    [Input("cll_grfjumlmitrambkm", "n_clicks")],
    [State("cll_tbljumlmitrambkm", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

#GRAPH CALLBACK
@app.callback(
    Output('grf_mahasiswambkm','figure'),
    Input('Fromdrpdwn_mhsseleksi', 'value'),
    Input('Todrpdwn_mhsseleksi', 'value'),
    #Input('grf_mahasiswambkm','id')
)
def grafMahasiswaMBKM(valueFrom, valueTo):

    #df=dfmahasiswambkm
    print(valueFrom)
    df = data.getDataFrameFromDBwithParams('''
    select concat(ds.semester_nama,' ',ds.tahun_ajaran) Semester,
       (case
            when kode_bkp = 'PP' then 'Pertukaran Pelajar'
            when kode_bkp = 'PI' then 'Proyek Independen'
            when kode_bkp = 'PR' then 'Penelitian & Riset'
            when kode_bkp = 'PD' then 'Pembangunan Desa'
            when kode_bkp = 'PK' then 'Proyek Kemanusiaan'
            when kode_bkp = 'KP' then 'Kerja Praktik'
            when kode_bkp = 'KU' then 'Kewirausahaan'
            when kode_bkp = 'AM' then 'Asisten Mengajar'
            when kode_bkp = 'AK' then 'Ambil Kredit Unit'
            else kode_bkp
    end) as Bentuk,
       count(distinct id_mahasiswa) Jumlah
    from mbkm_matkul_monev
    inner join dim_semester ds on mbkm_matkul_monev.kode_semester = ds.kode_semester
    where ds.tahun_ajaran between 
    %(From)s and %(To)s
    group by ds.kode_semester, Bentuk , Semester
    order by ds.kode_semester
    ''', {'From': valueFrom, 'To': valueTo})
    fig=px.bar(df,x=df['Semester'], y=df['Jumlah'], color=df['Bentuk'])
    fig.update_layout(barmode='group')
    return fig

@app.callback(
    Output('grf_reratasksmbkm','figure'),
    Input('Fromdrpdwn_reratasksmbkm', 'value'),
    Input('Todrpdwn_reratasksmbkm', 'value'),
    #Input('grf_reratasksmbkm','id')
)
def grafRerataKonversiSKS(valueFrom, valueTo):
    #df=dfreratasksmbkm
    df=data.getDataFrameFromDBwithParams('''
    select concat(ds.semester_nama,' ',ds.tahun_ajaran) Semester, count(sks) 'Jumlah SKS'
    from mbkm_matkul_monev mbm
         inner join dim_semester ds on mbm.kode_semester = ds.kode_semester
         inner join dim_matakuliah dm on mbm.kode_matakuliah = dm.kode_matakuliah
    where ds.tahun_ajaran between 
    %(From)s and %(To)s
    group by mbm.kode_semester, Semester
    order by mbm.kode_semester;''', {'From': valueFrom, 'To': valueTo})
    fig=px.line(df, x=df['Semester'], y=df['Jumlah SKS'])
    return fig

@app.callback(
    Output('grf_jumldosbingmbkm','figure'),
    Input('Fromdrpdwn_dosbingmbkm', 'value'),
    Input('Todrpdwn_dosbingmbkm', 'value'),
    #Input('grf_jumldosbingmbkm','id')
)
def grafDosbingMBKM(valueFrom, valueTo):
    #df=dfdosbingmbkm
    df = data.getDataFrameFromDBwithParams('''
    select CONCAT(semester_nama,' ',tahun_ajaran) Semester, count(distinct dd.id_dosen) 'Jumlah Dosen'
    from mbkm_matkul_monev mbm
         inner join dim_semester ds on mbm.kode_semester = ds.kode_semester
         inner join dim_matakuliah dm on mbm.kode_matakuliah = dm.kode_matakuliah
         inner join fact_khs fk on dm.id_matakuliah = fk.id_matakuliah
         inner join fact_dosen_mengajar fdm on dm.id_matakuliah = fdm.id_matakuliah
         inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
    where ds.tahun_ajaran between 
    %(From)s and %(To)s
    group by mbm.kode_semester, Semester
    order by mbm.kode_semester;''', {'From': valueFrom, 'To': valueTo})
    fig=px.bar(df, x=df['Semester'], y=df['Jumlah Dosen'])
    #fig.show
    return fig

@app.callback(
    Output('grf_jumlmitrambkm','figure'),
    Input('Fromdrpdwn_jumlmitrambkm', 'value'),
    Input('Todrpdwn_jumlmitrambkm', 'value'),
    #Input('grf_jumlmitrambkm','id')
)
def grafMitraMBKM(valueFrom, valueTo):
    #df=dfjumlmitrambkm
    df = data.getDataFrameFromDBwithParams('''
    select CONCAT(semester_nama,' ',tahun_ajaran) Semester, count(distinct mitra) 'Jumlah Mitra'
    from mbkm_matkul_monev mmm
    inner join dim_semester ds on mmm.kode_semester = ds.kode_semester
    where ds.tahun_ajaran between 
    %(From)s and %(To)s
    group by ds.kode_semester, Semester
    order by ds.kode_semester
    ''', {'From': valueFrom, 'To': valueTo})
    fig=px.bar(df,x=df['Semester'], y=df['Jumlah Mitra'])
    return fig