import dash
import pandas as pd
import dash_table as dt
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from appConfig import app, server
import model.data as data

tbl_matkulBaru = data.getMatkulBaru()
tbl_MatkulBatal = data.getMatkulBatal()
tbl_matkulTawar = data.getMatkulTawar()
tbl_mahasiswaAktif = data.getMahasiswaAktif()
tbl_mahasiswaAsing = data.getMahasiswaAsing()
tbl_persentaseMhsTA = data.getPersentaseMahasiswaTidakAktif()
tbl_jumlahDosenMengajar = data.getDosenMengajar()
tbl_jumlahDTT = data.getPersentaseDosenTidakTetap()
tbl_tingkatKepuasan = data.getTingkatKepuasanDosen()
tbl_RasioDosenMhs = data.getRasioDosenMahasiswa()
tbl_rasioDosenMengajarMhs = data.getRasioDosenMengajarMahasiswa()

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

ipkmahasiswa = dbc.Container([
    dbc.Card([
        html.H5('Rata-rata IPK Mahasiswa Aktif Tiap Semester',
                style=ttlgrf_style),
        dbc.CardBody(
            dcc.Graph(id='grf_ipkMahasiswa')
        )
    ], style=cardgrf_style)
], style=cont_style)

mahasiswa = dbc.Container([
    dbc.Card([
        html.H5('Mahasiswa',
                style=ttlgrf_style),
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Mahasiswa Aktif', value='mhsaktif',
                        children=[
                            dbc.CardLink([
                                dcc.Graph(id='grf_mahasiswaAktif')],
                                id='cll_grfmhsaktif', n_clicks=0
                            )
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Mahasiswa Asing', value='mhsasing',
                        children=[
                            dbc.CardLink([
                                dcc.Graph(id='grf_mahasiswaAsing')],
                                id='cll_grfmhsasing', n_clicks=0
                            )
                        ], style=tab_style, selected_style=selected_style)
            ], style=tab_style, id='tab_mahasiswa', value='mhsaktif'
            )
        ])
    ], style=cardgrf_style
    ),
    dbc.Collapse(
        id='cll_tblmahasiswa',
        is_open=False
    )
], style=cont_style)

mahasiswaTA = dbc.Container([
    dbc.Card([
        html.H5('Mahasiswa Tidak Aktif terhadap Mahasiswa Aktif',
                style=ttlgrf_style),
        html.Div([
            dt.DataTable(
                id='tbl_MhsTA',
                columns=[
                    {'name': i, 'id': i} for i in tbl_persentaseMhsTA.columns
                ],
                data=tbl_persentaseMhsTA.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'padding': '10px', 'overflowX': 'auto'},
                style_header={'font-size': '80%', 'textAlign': 'center'},
                style_data={'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 95},
                export_format='xlsx',
                page_size=10,
            )
        ])
    ], style=cardgrf_style
    ),
    dbc.Collapse(
        id='cll_tblMhsTA',
        is_open=False
    )
], style=cont_style)

jumlahDosen = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                html.H5('Jumlah Dosen yang Mengajar di Informatika Tiap Semester',
                        style=ttlgrf_style),
                html.Div([
                    dt.DataTable(
                        id='tbl_Dosen',
                        columns=[
                            {'name': i, 'id': i} for i in tbl_jumlahDosenMengajar.columns
                        ],
                        data=tbl_jumlahDosenMengajar.to_dict('records'),
                        sort_action='native',
                        sort_mode='multi',
                        style_table={'padding': '10px', 'overflowX': 'auto'},
                        style_header={'font-size': '80%', 'textAlign': 'center'},
                        style_data={'font-size': '80%', 'textAlign': 'center'},
                        style_cell={'width': 95},
                        export_format='xlsx',
                        page_size=10,
                    )
                ])
            ], style=cardgrf_style
            ),
        ),
        dbc.Col(
            dbc.Card([
                html.H5('Persentase Dosen Tidak Tetap Terhadap Seluruh Dosen',
                        style=ttlgrf_style),
                html.Div([
                    dt.DataTable(
                        id='tbl_DTT',
                        columns=[
                            {'name': i, 'id': i} for i in tbl_jumlahDTT.columns
                        ],
                        data=tbl_jumlahDTT.to_dict('records'),
                        sort_action='native',
                        sort_mode='multi',
                        style_table={'padding': '10px', 'overflowX': 'auto'},
                        style_header={'font-size': '80%', 'textAlign': 'center'},
                        style_data={'font-size': '80%', 'textAlign': 'center'},
                        style_cell={'width': 95},
                        export_format='xlsx',
                        page_size=10,
                    )
                ])
            ], style=cardgrf_style
            ),
        )
    ], style={'margin-top': '10px'}),

    dbc.Collapse(
        id='cll_tblDosen',
        is_open=False
    )
], style=cont_style)

tingkatKepuasan = dbc.Container([
    dbc.Card([
        html.H5('Tingkat Kepuasan Mahasiswa Terhadap Dosen',
                style=ttlgrf_style),
        html.Div([
            dt.DataTable(
                id='tbl_KepuasanMhs',
                columns=[
                    {'name': i, 'id': i} for i in tbl_tingkatKepuasan.columns
                ],
                data=tbl_tingkatKepuasan.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'padding': '10px', 'overflowX': 'auto'},
                style_header={'font-size': '80%', 'textAlign': 'center'},
                style_data={'font-size': '80%', 'textAlign': 'center'},
                style_cell={'width': 95},
                export_format='xlsx',
                page_size=10,
            )
        ])
    ], style=cardgrf_style
    ),
    dbc.Collapse(
        id='cll_tblKepuasanMhs',
        is_open=False
    )
], style=cont_style)

Dosen = dbc.Container([
    dbc.Card([
        html.H5('Rasio Dosen',
                style=ttlgrf_style),
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Rasio Dosen : Mahasiswa', value='dosen',
                        children=[
                            dt.DataTable(
                                id='tbl_DosenMhs',
                                columns=[
                                    {'name': i, 'id': i} for i in tbl_RasioDosenMhs.columns
                                ],
                                data=tbl_RasioDosenMhs.to_dict('records'),
                                sort_action='native',
                                sort_mode='multi',
                                style_table={'padding': '10px', 'overflowX': 'auto'},
                                style_header={'font-size': '80%', 'textAlign': 'center'},
                                style_data={'font-size': '80%', 'textAlign': 'center'},
                                style_cell={'width': 95},
                                export_format='xlsx',
                                page_size=10,
                            )
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Rasio Dosen Mengajar : Mahasiswa', value='dosenMengajar',
                        children=[
                            dt.DataTable(
                                id='tbl_DosenMengajarMhs',
                                columns=[
                                    {'name': i, 'id': i} for i in tbl_rasioDosenMengajarMhs.columns
                                ],
                                data=tbl_rasioDosenMengajarMhs.to_dict('records'),
                                sort_action='native',
                                sort_mode='multi',
                                style_table={'padding': '10px', 'overflowX': 'auto'},
                                style_header={'font-size': '80%', 'textAlign': 'center'},
                                style_data={'font-size': '80%', 'textAlign': 'center'},
                                style_cell={'width': 95},
                                export_format='xlsx',
                                page_size=10,
                            )
                        ], style=tab_style, selected_style=selected_style),
            ], style=tab_style, id='tab_dosen', value='dosen'
            )
        ])
    ], style=cardgrf_style
    ),
    dbc.Collapse(
        id='cll_tblDosen',
        is_open=False
    )
], style=cont_style)

matkul = dbc.Container([
    dbc.Card([
        html.H5('Daftar Matakuliah',
                style=ttlgrf_style),
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Matakuliah Kurikulum', value='kurikulum',
                        children=[
                            dt.DataTable(
                                id='tbl_matkulBaru',
                                columns=[
                                    {'name': i, 'id': i} for i in tbl_matkulBaru.columns
                                ],
                                data=tbl_matkulBaru.to_dict('records'),
                                sort_action='native',
                                sort_mode='multi',
                                style_table={'padding': '10px', 'overflowX': 'auto'},
                                style_header={'font-size': '80%', 'textAlign': 'center'},
                                style_data={'font-size': '80%', 'textAlign': 'center'},
                                style_cell={'width': 95},
                                export_format='xlsx',
                                page_size=10,
                            )
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Matakuliah Batal dengan Keterangan Dosen', value='batal',
                        children=[
                            dt.DataTable(
                                id='tbl_matkulBatal',
                                columns=[
                                    {'name': i, 'id': i} for i in tbl_MatkulBatal.columns
                                ],
                                data=tbl_MatkulBatal.to_dict('records'),
                                sort_action='native',
                                sort_mode='multi',
                                style_table={'padding': '10px', 'overflowX': 'auto'},
                                style_header={'font-size': '80%', 'textAlign': 'center'},
                                style_data={'font-size': '80%', 'textAlign': 'center'},
                                style_cell={'width': 95},
                                export_format='xlsx',
                                page_size=10,
                            )
                        ], style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Matakuliah Ditawarkan Setiap TS', value='ts',
                        children=[
                            dt.DataTable(
                                id='tbl_matkulTawar',
                                columns=[
                                    {'name': i, 'id': i} for i in tbl_matkulTawar.columns
                                ],
                                data=tbl_matkulTawar.to_dict('records'),
                                sort_action='native',
                                sort_mode='multi',
                                style_table={'padding': '10px', 'overflowX': 'auto'},
                                style_header={'font-size': '80%', 'textAlign': 'center'},
                                style_data={'font-size': '80%', 'textAlign': 'center'},
                                style_cell={'width': 95},
                                export_format='xlsx',
                                page_size=10,
                            )
                        ], style=tab_style, selected_style=selected_style)
            ], style=tab_style, id='tab_kurikulum', value='kurikulum'
            )
        ])
    ], style=cardgrf_style
    ),
    dbc.Collapse(
        id='cll_tblmatkul',
        is_open=False
    )
], style=cont_style)


layout = html.Div([
    html.Div(html.H1('Analisis KBM Prodi Informatika',
                     style={'margin-top': '30px', 'textAlign': 'center'}
                     )
             ),
    html.Div([ipkmahasiswa]),
    html.Div([mahasiswa]),
    html.Div([mahasiswaTA]),
    html.Div([jumlahDosen]),
    html.Div([tingkatKepuasan]),
    html.Div([Dosen]),
    html.Div([matkul], style={'margin-bottom': '50px'}),
], style={'width': '100%'})


@app.callback(
    Output('cll_tblmahasiswa', 'is_open'),
    Output('cll_tblmahasiswa', 'children'),
    [Input("cll_grfmhsaktif", "n_clicks"),
     Input("cll_grfmhsasing", "n_clicks"),
     Input("tab_mahasiswa", "value")],
    [State("cll_tblmahasiswa", "is_open")])
def toggle_collapse(naktif, nasing, mhs, is_open):
    isiAktif = dbc.Card(
        dt.DataTable(
            id='tbl_mahasiswaAktif',
            columns=[{"name": i, "id": i} for i in tbl_mahasiswaAktif.columns],
            data=tbl_mahasiswaAktif.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            page_size=10,
            export_format='xlsx'
        ), style=cardgrf_style
    ),
    isiAsing = dbc.Card(
        dt.DataTable(
            id='tbl_mahasiswaAsing',
            columns=[{"name": i, "id": i} for i in tbl_mahasiswaAsing.columns],
            data=tbl_mahasiswaAsing.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
            style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
            page_size=10,
            export_format='xlsx'
        ), style=cardgrf_style
    ),
    if naktif and mhs == 'mhsaktif':
        return not is_open, isiAktif
    if nasing and mhs == 'mhsasing':
        return not is_open, isiAsing
    return is_open, None


@app.callback(
    Output("grf_ipkMahasiswa", 'figure'), Input('grf_ipkMahasiswa', 'id')
)
def FillIpkMahasiswa(id):
    df = data.getDataFrameFromDB('''select ds.tahun_ajaran 'Tahun Ajaran', ds.semester, avg(ipk) as "Rata-Rata"
from fact_mahasiswa_status fms 
inner join dim_semester ds on ds.id_semester = fms.id_semester
where ds.tahun_ajaran in ('2015/2016','2016/2017','2017/2018','2018/2019','2019/2020') and fms.status = 'AK'
group by ds.tahun_ajaran, ds.semester
order by ds.tahun_ajaran, ds.semester''')
    fig = px.bar(df, x=df['Tahun Ajaran'], y=df['Rata-Rata'], color=df['semester'])
    fig.update_layout(barmode='group')
    return fig

@app.callback(
    Output("grf_mahasiswaAktif", 'figure'), Input('grf_mahasiswaAktif', 'id')
)
def FillAktif(id):
    df = data.getDataFrameFromDB('''select ds.tahun_ajaran 'Tahun Ajaran', ds.semester_nama Semester, 
    count(*) as 'Jumlah Mahasiswa Aktif' from fact_mahasiswa_status fms
inner join dim_semester ds on ds.id_semester = fms.id_semester
where fms.status = 'AK' and ds.tahun_ajaran in ('2015/2016','2016/2017','2017/2018','2018/2019','2019/2020')
group by ds.tahun_ajaran, ds.semester_nama
order by ds.tahun_ajaran, ds.semester_nama
''')
    fig = px.bar(df, x=df['Tahun Ajaran'], y=df['Jumlah Mahasiswa Aktif'], color=df['Semester'])
    fig.update_layout(barmode='group')
    return fig

@app.callback(
    Output("grf_mahasiswaAsing", 'figure'), Input('grf_mahasiswaAsing', 'id')
)
def FillAsing(id):
    df = data.getDataFrameFromDB('''select tahun_angkatan 'Tahun Ajaran', count(*) as 'Jumlah Mahasiswa Asing' from dim_mahasiswa 
where warga_negara ='WNA' and tahun_angkatan >= 2015
group by tahun_angkatan
order by tahun_angkatan''')
    fig = px.bar(df, x=df['Tahun Ajaran'], y=df['Jumlah Mahasiswa Asing'])
    return fig
