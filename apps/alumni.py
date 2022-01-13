import dash
import pandas as pd
import dash_table as dt
import plotly.express as px
import dash_bootstrap_components as dbc
from apps import pmb, kbm, kegiatan_kerjasama, tgsakhir, alumni, ppp
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from appConfig import app, server
from dash import html, dcc
import model.dao_alumni as data

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

dfmasatunggu = data.getMasaTunggu()
dfbidangkerja = data.getBidangKerja()
dftempatkerja = data.getTempatKerja()
dfskill = data.getSkill()
dfjabatan = data.getJabatan()
dfperusahaan = data.getPerusahaan()

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

masatunggu = dbc.Container([
    dbc.Card([
        html.H5('8.d.1 Waktu Tunggu Lulusan Program Sarjana',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody(
                dcc.Graph(id='grf_masatunggu')
            ),
            id='cll_grfmasatunggu',
            n_clicks=0
        )
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_masatunggu',
                columns=[
                    {'name': 'Tahun Lulus', 'id': 'tahun_lulus'},
                    {'name': 'Lulusan', 'id': 'Lulusan'},
                    {'name': 'Lulusan Terlacak', 'id': 'Lulusan Terlacak'},
                    {'name': '<6 Bulan', 'id': '<6 BULAN'},
                    {'name': '6-18 Bulan', 'id': '6-18 BULAN'},
                    {'name': '>18 Bulan', 'id': '>18 BULAN'},
                    {'name': 'Lainnya', 'id': 'LAINNYA'}
                ],
                data=dfmasatunggu.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'}
            ), style=cardgrf_style
        ),
        id='cll_tblmasatunggu',
        is_open=False
    )
], style=cont_style)

bidangkerja = dbc.Container([
    dbc.Card([
        html.H5('8.d.2 Kesesuaian Bidang Kerja Lulusan',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody(
                dcc.Graph(id='grf_bidangkerja')
            ),
            id='cll_grfbidangkerja',
            n_clicks=0
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_bidangkerja',
                columns=[{"name": i, "id": i} for i in dfbidangkerja.columns],
                data=dfbidangkerja.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'}
            ), style=cardgrf_style
        ),
        id='cll_tblbidangkerja',
        is_open=False
    )
], style=cont_style)

tempatkerja = dbc.Container([
    dbc.Card([
        html.H5('8.e.1 Tempat Kerja Lulusan',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody(
                dcc.Graph(id='grf_tempatkerja')
            ),
            id='cll_grftempatkerja',
            n_clicks=0
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_tempatkerja',
                columns=[{"name": i, "id": i} for i in dftempatkerja.columns],
                data=dftempatkerja.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'}
            ), style=cardgrf_style
        ),
        id='cll_tblseleksi',
        is_open=False
    )
], style=cont_style)

kemampuan = dbc.Container([
    dbc.Card([
        html.H5('8.e.1 Kemampuan Lulusan',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody(
                dcc.Graph(id='grf_skill')
            ),
            id='cll_grfskill',
            n_clicks=0
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_skill',
                columns=[{"name": i, "id": i} for i in dfskill.columns],
                data=dfskill.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'}
            ), style=cardgrf_style
        ),
        id='cll_tblskill',
        is_open=False
    )
], style=cont_style)

jabatan = dbc.Container([
    dbc.Card([
        html.H5('Posisi Jabatan Lulusan pada Perusahaan',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody(
                dcc.Graph(id='grf_jabatan')
            ),
            id='cll_grfjabatan',
            n_clicks=0
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_jabatan',
                columns=[{"name": i, "id": i} for i in dfjabatan.columns],
                data=dfjabatan.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'}
            ), style=cardgrf_style
        ),
        id='cll_tbljabatan',
        is_open=False
    )
], style=cont_style)

perusahaan = dbc.Container([
    dbc.Card([
        html.H5('Lulusan pada Perusahaan',
                style=ttlgrf_style),
        dbc.CardLink(
            dbc.CardBody(
                dcc.Graph(id='grf_perusahaan')
            ),
            id='cll_grfperusahaan',
            n_clicks=0
        ),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_perusahaan',
                columns=[{"name": i, "id": i} for i in dfperusahaan.columns],
                data=dfperusahaan.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'}
            ), style=cardgrf_style
        ),
        id='cll_tblperusahaan',
        is_open=False
    )
], style=cont_style)

tracerstudy = dbc.Container([
    html.Div([
        html.H1('Analisis Lulusan, Tracer Study, Kepuasan Fasilitas dan Layanan',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Alumni', value='alumni',
                    children=[
                        masatunggu,
                        bidangkerja,
                        tempatkerja,
                        kemampuan,
                        jabatan,
                        perusahaan
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Fasilitas & Layanan', value='fasilitaslayanan',
                    children=[

                    ],
                    style=tab_style, selected_style=selected_style)
        ], style=tabs_styles, value='alumni')
    ])
], style=cont_style)

layout = html.Div([
    html.Div([tracerstudy], style={'margin-bottom': '50px'})
], style={'justify-content': 'center'})


@app.callback(
    Output("cll_tblmasatunggu", "is_open"),
    [Input("cll_grfmasatunggu", "n_clicks")],
    [State("cll_tblmasatunggu", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tbltempatkerja", "is_open"),
    [Input("cll_grftempatkerja", "n_clicks")],
    [State("cll_tbltempatkerja", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tblbidangkerja", "is_open"),
    [Input("cll_grfbidangkerja", "n_clicks")],
    [State("cll_tblbidangkerja", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tblskill", "is_open"),
    [Input("cll_grfskill", "n_clicks")],
    [State("cll_tblskill", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tbljabatan", "is_open"),
    [Input("cll_grfjabatan", "n_clicks")],
    [State("cll_tbljabatan", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tblperusahaan", "is_open"),
    [Input("cll_grfperusahaan", "n_clicks")],
    [State("cll_tblperusahaan", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('grf_masatunggu', 'figure'),
    Input('grf_masatunggu', 'id')
)
def graphMasaTunggu(id):
    df = pd.read_sql('''select count(*) as Jumlah, ifnull(waktu_tunggu,"LAINNYA") as "Waktu Tunggu",
    ifnull(lulusan.jumlah,0) as "Lulusan",dim_lulusan.tahun_lulus as "Tahun Lulus"
        from fact_tracer_study fact
        inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
left join (
    select count(id_mahasiswa) as jumlah, tahun_lulus
    from (select *, if(semester_yudisium = 'GENAP', substr(tahun_ajaran_yudisium,6,4),substr(tahun_ajaran_yudisium,1,4)) as tahun_lulus
    from fact_yudisium) data
    group by tahun_lulus
)lulusan on lulusan.tahun_lulus = dim_lulusan.tahun_lulus
group by `Waktu Tunggu` ,dim_lulusan.tahun_lulus,Lulusan
        order by dim_lulusan.tahun_lulus asc''', con)
    fig = px.bar(df, x=df["Tahun Lulus"], y=df["Jumlah"], color=df["Waktu Tunggu"], barmode='stack',
                 labels=dict(x="Tahun Lulus", y="Jumlah", color="Lulusan"))
    fig.add_scatter(x=df["Tahun Lulus"], y=df["Lulusan"], name='Lulusan',
                    hovertemplate="Lulusan=Total Lulusan <br>Jumlah=%{y} </br> Tahun Lulus=%{x}", mode='lines+markers')
    return fig


@app.callback(
    Output('grf_bidangkerja', 'figure'),
    Input('grf_bidangkerja', 'id')
)
def graphBidangKerja(id):
    df = pd.read_sql('''select count(*) as Jumlah, 
    ifnull(tingkat_kesesuaian_bidang_kerja,"LAINNYA") as "Kesesuaian Bidang Kerja", 
    ifnull(lulusan.jumlah,0) as "Jumlah Lulusan", dim_lulusan.tahun_lulus as "Tahun Lulus"
        from fact_tracer_study fact
        inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
left join(
    select count(id_mahasiswa) as jumlah, tahun_lulus
    from (select *, if(semester_yudisium = 'GENAP', substr(tahun_ajaran_yudisium,6,4),substr(tahun_ajaran_yudisium,1,4)) as tahun_lulus
    from fact_yudisium) data
    group by tahun_lulus
)lulusan on lulusan.tahun_lulus = dim_lulusan.tahun_lulus
group by dim_lulusan.tahun_lulus,`Kesesuaian Bidang Kerja`,`Jumlah Lulusan`
        order by dim_lulusan.tahun_lulus asc''', con)
    fig = px.bar(df, x=df["Tahun Lulus"], y=df["Jumlah"], color=df["Kesesuaian Bidang Kerja"], barmode='stack',
                 labels=dict(x="Tahun Lulus", y="Jumlah", color="Lulusan"))
    fig.add_scatter(x=df["Tahun Lulus"], y=df["Jumlah Lulusan"], name='Lulusan', mode='lines+markers',
                    hovertemplate="Lulusan=Total Lulusan <br>Jumlah=%{y} </br> Tahun Lulus=%{x}")
    return fig


@app.callback(
    Output('grf_tempatkerja', 'figure'),
    Input('grf_tempatkerja', 'id')
)
def graphTempatKerja(id):
    df = dftempatkerja
    fig = px.line(df, x=df["Tahun Lulus"], y=df["Lulusan Terlacak"], color=px.Constant('Lulusan Terlacak'),
                  labels=dict(x="Tahun Lulus", y="Lingkup Kerja", color="Lulusan"))
    fig.add_bar(x=df["Tahun Lulus"], y=df["Lokal/Regional"], name='Lokal/Regional',
                hovertemplate="Lulusan=Total Lulusan <br>Tahun Lulus=%{x} </br> Jumlah=%{y}")
    fig.add_bar(x=df["Tahun Lulus"], y=df["Nasional"], name='Nasional',
                hovertemplate="Lulusan=Total Lulusan <br>Tahun Lulus=%{x} </br> Jumlah=%{y}")
    fig.add_bar(x=df["Tahun Lulus"], y=df["Internasional"], name='Internasional',
                hovertemplate="Lulusan=Total Lulusan <br>Tahun Lulus=%{x} </br> Jumlah=%{y}")
    fig.update_layout(barmode='stack')
    # fig.add_scatter(x=df["Tahun Lulus"], y=df["Lulusan Terlacak"], name='Lulusan Terlacak', mode='lines+markers',
    #                 hovertemplate="Lulusan=Total Lulusan <br>Tahun Lulus=%{x} </br> Jumlah=%{y}")
    return fig


# @app.callback(
#     Output('grf_skill','figure'),
#     Input('grf_skill','id')
# )
# def graphSkill(id):
#     df= pd.read_sql('''''',con)
#     fig=px.bar(df,x=df["Integritas"],y=df["Sangat Baik"],color=df['Kriteria'],
#                labels=dict(x="Tahun Lulus", y="Lingkup Kerja", color="Lulusan"))
#     fig.add_bar(x=df["Tahun Lulus"],y=df["Nasional"],name='Nasional',
#                     hovertemplate="Lulusan=Total Lulusan <br>Jumlah=%{y} </br> Tahun Lulus=%{x}")
#     fig.add_bar(x=df["Tahun Lulus"], y=df["Internasional"], name='Internasional',
#                 hovertemplate="Lulusan=Total Lulusan <br>Jumlah=%{y} </br> Tahun Lulus=%{x}")
#     return fig

@app.callback(
    Output('grf_jabatan', 'figure'),
    Input('grf_jabatan', 'id')
)
def graphJabatan(id):
    df = pd.read_sql('''select count(*) as Jumlah, ifnull(posisi_jabatan_alumni,'LAINNYA') as Posisi, posisi_jabatan_alumni
from fact_tracer_study tracer
inner join dim_lulusan on dim_lulusan.id_lulusan = tracer.id_lulusan
group by posisi, posisi_jabatan_alumni
order by posisi_jabatan_alumni desc''', con)
    fig = px.bar(df, x=df['Posisi'], y=df['Jumlah'], color=px.Constant('Jabatan'),
                 labels=dict(x="Jabatan", y="Jumlah", color="Jabatan"))
    return fig


# @app.callback(
#     Output('grf_skill','figure'),
#     Input('grf_skill','id')
# )
# def graphSkill(id):
#     df= pd.read_sql('''''',con)
#     fig=px.bar(df,x=df["Integritas"],y=df["Sangat Baik"],color=df['Kriteria'],
#                labels=dict(x="Tahun Lulus", y="Lingkup Kerja", color="Lulusan"))
#     fig.add_bar(x=df["Tahun Lulus"],y=df["Nasional"],name='Nasional',
#                     hovertemplate="Lulusan=Total Lulusan <br>Jumlah=%{y} </br> Tahun Lulus=%{x}")
#     fig.add_bar(x=df["Tahun Lulus"], y=df["Internasional"], name='Internasional',
#                 hovertemplate="Lulusan=Total Lulusan <br>Jumlah=%{y} </br> Tahun Lulus=%{x}")
#     return fig

@app.callback(
    Output('grf_perusahaan', 'figure'),
    Input('grf_perusahaan', 'id')
)
def graphPerusahaan(id):
    df = pd.read_sql('''select count(*) as Jumlah, nama_mapping_organisasi as "Perusahaan"
    from fact_tracer_study tracer
    inner join dim_lulusan on tracer.id_lulusan = dim_lulusan.id_lulusan
    inner join dim_organisasi_pengguna_lulusan org on dim_lulusan.id_organisasi_pengguna_lulusan = org.id_organisasi_pengguna_lulusan
    group by `Perusahaan`
    order by jumlah desc
    limit 15''', con)
    fig = px.bar(df, x=df['Perusahaan'], y=df['Jumlah'], color=px.Constant('Perusahaan'),
                 labels=dict(x="Perusahaan", y="Jumlah", color="Perusahaan"))
    return fig
