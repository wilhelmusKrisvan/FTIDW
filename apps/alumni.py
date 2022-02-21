import dash
import pandas as pd
import dash_table as dt
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from appConfig import app, server
from dash import html, dcc
import model.dao_alumni as data

dfmasatunggu = data.getMasaTunggu()
dfmasaTungguGol = data.getMasaTungguperGol()

dfbidangkerja = data.getBidangKerja()
dfwirausaha = data.getWirausaha()
dfGaji = data.getGajiLulusan()

dfskill = data.getSkill()
dfKepuasanPelayanan = data.getKepuasanLayanan()

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
        html.H5('Masa Tunggu Lulusan',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Jumlah Lulusan Dengan Waktu Tunggu mendapat Pekerjaan', value='MsTgglulusan',
                    children=[
                        # dbc.CardLink([
                        #     dcc.Graph(id='grf_MsTgglulusan')
                        # ], id='cll_MsTgglulusan',
                        #     n_clicks=0),
                        dt.DataTable(
                            id='tbl_MsTgglulusan',
                            columns=[
                                {'name': i, 'id': i} for i in dfmasatunggu.columns
                            ],
                            data=dfmasatunggu.to_dict('records'),
                            sort_action='native',
                            sort_mode='multi',
                            style_table={'padding': '10px', 'overflowX': 'auto'},
                            style_header={'textAlign': 'center'},
                            style_data={'font-size': '80%', 'textAlign': 'center'},
                            style_cell={'width': 95},
                            page_size=10,
                            export_format='xlsx'
                        )
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Rata-rata Masa Tunggu Lulusan di Tiap Tahun', value='rateGol',
                    children=[
                        dbc.CardLink([
                            dcc.Graph(id='grf_rateGol')
                        ], id='cll_rateGol',
                            n_clicks=0),
                        # dt.DataTable(
                        #     id='tbl_rateGol',
                        #     columns=[
                        #         {'name': i, 'id': i} for i in dfmasaTungguGol.columns
                        #     ],
                        #     data=dfmasaTungguGol.to_dict('records'),
                        #     sort_action='native',
                        #     sort_mode='multi',
                        #     style_table={'padding': '10px', 'overflowX': 'auto'},
                        #     style_header={'textAlign': 'center'},
                        #     style_data={'font-size': '80%', 'textAlign': 'center'},
                        #     style_cell={'width': 95},
                        #     page_size=10,
                        #     export_format='xlsx'
                        # )
                    ],
                    style=tab_style, selected_style=selected_style),
        ], style=tabs_styles, id='masatunggu', value='MsTgglulusan'),
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_masatunggu',
        is_open=False
    )
], style=cont_style)

lulusan = dbc.Container([
    dbc.Card([
        html.H5('Lulusan',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Jumlah Lulusan Berdasarkan Tingkat Kesesuaian Bidang Kerja', value='bidangKerja',
                    children=[
                        # dbc.CardLink([
                        #     dcc.Graph(id='grf_bidangKerja')
                        # ], id='cll_grfbidangKerja',
                        #     n_clicks=0),
                        dt.DataTable(
                            id='tbl_bidangKerja',
                            columns=[
                                {'name': i, 'id': i} for i in dfbidangkerja.columns
                            ],
                            data=dfbidangkerja.to_dict('records'),
                            sort_action='native',
                            sort_mode='multi',
                            style_table={'padding': '10px', 'overflowX': 'auto'},
                            style_header={'textAlign': 'center'},
                            style_data={'font-size': '80%', 'textAlign': 'center'},
                            style_cell={'width': 95},
                            page_size=10,
                            export_format='xlsx'
                        )
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Jumlah Lulusan yang Berwirausaha', value='wirausaha',
                    children=[
                        # dbc.CardLink([
                        #     dcc.Graph(id='grf_wirausaha')
                        # ], id='cll_grfwirausaha',
                        #     n_clicks=0),
                        dt.DataTable(
                            id='tbl_wirausaha',
                            columns=[
                                {'name': i, 'id': i} for i in dfwirausaha.columns
                            ],
                            data=dfwirausaha.to_dict('records'),
                            sort_action='native',
                            sort_mode='multi',
                            style_table={'padding': '10px', 'overflowX': 'auto'},
                            style_header={'textAlign': 'center'},
                            style_data={'font-size': '80%', 'textAlign': 'center'},
                            style_cell={'width': 95},
                            page_size=10,
                            export_format='xlsx'
                        )
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Rata-rata Gaji Alumni yang Mendapatkan Pekerjaan < 6 Bulan',
                    value='gaji',
                    children=[
                        dbc.CardLink([
                            dcc.Graph(id='grf_gaji')
                        ], id='cll_grfgaji',
                            n_clicks=0),
                        # dt.DataTable(
                        #     id='tbl_gaji',
                        #     columns=[
                        #         {'name': i, 'id': i} for i in dfGaji.columns
                        #     ],
                        #     data=dfGaji.to_dict('records'),
                        #     sort_action='native',
                        #     sort_mode='multi',
                        #     style_table={'padding': '10px', 'overflowX': 'auto'},
                        #     style_header={'textAlign': 'center'},
                        #     style_data={'font-size': '80%', 'textAlign': 'center'},
                        #     style_cell={'width': 95},
                        #     page_size=10,
                        #     export_format='xlsx'
                        # )
                    ],
                    style=tab_style, selected_style=selected_style),
        ], style=tabs_styles, id='lulusan', value='bidangKerja'),
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_lulusan',
        is_open=False
    )
], style=cont_style)

kepuasan = dbc.Container([
    dbc.Card([
        html.H5('Kepuasan Pengguna Lulusan',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Tingkat Kepuasan Mahasiswa Terhadap Layanan UKDW', value='Layanan',
                    children=[
                        dbc.CardLink([
                            dcc.Graph(id='grf_Layanan')
                        ], id='cll_grfLayanan',
                            n_clicks=0),
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Tingkat Kepuasan Pengguna Lulusan Berdasarkan Jenis Kemampuan Lulusan', value='skill',
                    children=[
                        dcc.Dropdown(
                            id='drpdwn_skill',
                            options=[{'label': 'INTEGRITAS', 'value': 'integritas'},
                                     {'label': 'KEAHLIAN BIDANG ILMU', 'value': 'keahlian_bidang_ilmu'},
                                     {'label': 'KEMAMPUAN BAHASA ASING', 'value': 'kemampuan_bahasa_asing'},
                                     {'label': 'PENGGUNAAN TEKNOLOGI INFORMASI', 'value': 'penggunaan_teknologi'},
                                     {'label': 'KOMUNIKASI', 'value': 'komunikasi'},
                                     {'label': 'KERJASAMA TIM', 'value': 'kerjasama_tim'},
                                     {'label': 'PENGEMBANGAN DIRI', 'value': 'pengembangan_diri'}, ],
                            value='integritas',
                            style={'color': 'black'},
                            clearable=False,
                        ),
                        dbc.CardLink([
                            dcc.Graph(id='grf_skill')
                        ], id='cll_grfskill',
                            n_clicks=0),
                    ],
                    style=tab_style, selected_style=selected_style),
        ], style=tabs_styles, id='tab_kepuasan', value='Layanan'),
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_kepuasan',
        is_open=False
    )
], style=cont_style)

layout = html.Div([
    html.Div(html.H1('Analisis Alumni',
                     style={'margin-top': '30px', 'textAlign': 'center'}
                     )
             ),
    html.Div([masatunggu]),
    html.Div([lulusan]),
    html.Div([kepuasan], style={'margin-bottom': '50px'})
], style={'justify-content': 'center'})


# CONTROL COLLAPSE
@app.callback(
    Output('cll_kepuasan', 'is_open'),
    Output('cll_kepuasan', 'children'),
    [Input("cll_grfLayanan", "n_clicks"),
     Input("cll_grfskill", "n_clicks"),
     Input("tab_kepuasan", "value")],
    [State("cll_kepuasan", "is_open")])
def toggle_collapse(nlayanan, nskill, puas, is_open):
    isiLayanan = dt.DataTable(
        id='tbl_Layanan',
        columns=[
            {'name': i, 'id': i} for i in dfKepuasanPelayanan.columns
        ],
        data=dfKepuasanPelayanan.to_dict('records'),
        sort_action='native',
        sort_mode='multi',
        style_table={'padding': '10px', 'overflowX': 'auto'},
        style_header={'textAlign': 'center'},
        style_data={'font-size': '80%', 'textAlign': 'center'},
        style_cell={'width': 95},
        page_size=10,
        export_format='xlsx'
    )
    isiSkill = dt.DataTable(
        id='tbl_skill',
        columns=[
            {'name': i, 'id': i} for i in dfskill.columns
        ],
        data=dfskill.to_dict('records'),
        sort_action='native',
        sort_mode='multi',
        style_table={'padding': '10px', 'overflowX': 'auto'},
        style_header={'textAlign': 'center'},
        style_data={'font-size': '80%', 'textAlign': 'center'},
        style_cell={'width': 95},
        page_size=10,
        export_format='xlsx'
    )
    if nlayanan and puas == 'Layanan':
        return not is_open, isiLayanan
    if nskill and puas == 'skill':
        return not is_open, isiSkill
    return is_open, None


@app.callback(
    Output('grf_rateGol', 'figure'),
    Input('grf_rateGol', 'id')
)
def graphRateGol(id):
    df = dfmasaTungguGol
    fig = px.line(df, x=df['Tahun'], y=df['Jumlah'], color=df['Waktu'])
    fig.update_traces(mode='lines+markers')
    return fig


# @app.callback(
#     Output('grf_wirausaha', 'figure'),
#     Input('grf_wirausaha', 'id')
# )
# def graphWirausaha(id):
#     df = dfwirausaha
#     fig = px.bar(df, x=df['Tahun Lulus'], y=df['Tinggi'])
#     fig.add_bar(x=df['Tahun Lulus'],y=df['Sedang'])
#     fig.add_bar(x=df['Tahun Lulus'],y=df['Rendah'])
#     fig.add_bar(x=df['Tahun Lulus'], y=df['Lainnya'])
#     return fig


@app.callback(
    Output('grf_gaji', 'figure'),
    Input('grf_gaji', 'id')
)
def graphGaji(id):
    df = dfGaji
    fig = px.line(df, x=df['Tahun'], y=df['Pendapatan'])
    fig.update_traces(mode='lines+markers')
    return fig


@app.callback(
    Output('grf_Layanan', 'figure'),
    Input('grf_Layanan', 'id')
)
def graphLayanan(id):
    df = dfKepuasanPelayanan
    fig = px.pie(df, values=df['persentase'], names=df['Nilai'])
    return fig


@app.callback(
    Output('grf_skill', 'figure'),
    Input('grf_skill', 'id'),
    Input('drpdwn_skill', 'value'),
    Input('drpdwn_skill', 'label')
)
def graphSkill(id, valueDropDown, labelSkill):
    df = data.getDataFrameFromDB('''
    select kriteria as Kriteria,
    round(SANGATBAIK/(SANGATBAIK+BAIK+CUKUP+IF(KURANG=NULL,0,KURANG))*100,2) as "Sangat Baik",
    round(BAIK/(SANGATBAIK+BAIK+CUKUP+IF(KURANG=NULL,0,KURANG))*100,2) as "Baik",
    round(CUKUP/(SANGATBAIK+BAIK+CUKUP+IF(KURANG=NULL,0,KURANG))*100,2) as "Cukup",
    round(IF(KURANG=NULL,0,KURANG)/(SANGATBAIK+BAIK+CUKUP+IF(KURANG=NULL,0,KURANG))*100,2) as "Kurang"
    from (
    select 'KRITERIA' as kriteria,
        sum(case when {kolom} = "SANGAT BAIK" then jumlah end) as "SANGATBAIK",
        sum(case when {kolom} = "BAIK" then jumlah end) as "BAIK",
        sum(case when {kolom} = "CUKUP" then jumlah end) as "CUKUP",
        sum(if({kolom}="KURANG",jumlah,0)) as "KURANG"
        from(
            select ifnull({kolom}, 'LAINNYA') as {kolom}, count(*) jumlah
            from fact_kepuasan_pengguna_lulusan fact
            inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
            group by {kolom}
        ) as data
    ) dataJumlah'''.format(kolom=valueDropDown))
    values = [f"{df['Sangat Baik'].iloc[-1]:,.1f}", f"{df['Baik'].iloc[-1]:,.1f}",
              f"{df['Cukup'].iloc[-1]:,.1f}", f"{df['Kurang'].iloc[-1]:,.1f}"]
    label = ['Sangat Baik', 'Baik', 'Cukup', 'Kurang']
    fig = go.Figure(data=[go.Pie(labels=label, values=values)])
    return fig

# @app.callback(
#     Output('grf_bidangkerja', 'figure'),
#     Input('grf_bidangkerja', 'id')
# )
# def graphBidangKerja(id):
#     df = pd.read_sql('''select count(*) as Jumlah,
#     ifnull(tingkat_kesesuaian_bidang_kerja,"LAINNYA") as "Kesesuaian Bidang Kerja",
#     ifnull(lulusan.jumlah,0) as "Jumlah Lulusan", dim_lulusan.tahun_lulus as "Tahun Lulus"
#         from fact_tracer_study fact
#         inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
# left join(
#     select count(id_mahasiswa) as jumlah, tahun_lulus
#     from (select *, if(semester_yudisium = 'GENAP', substr(tahun_ajaran_yudisium,6,4),substr(tahun_ajaran_yudisium,1,4)) as tahun_lulus
#     from fact_yudisium) data
#     group by tahun_lulus
# )lulusan on lulusan.tahun_lulus = dim_lulusan.tahun_lulus
# group by dim_lulusan.tahun_lulus,`Kesesuaian Bidang Kerja`,`Jumlah Lulusan`
#         order by dim_lulusan.tahun_lulus asc''', con)
#     fig = px.bar(df, x=df["Tahun Lulus"], y=df["Jumlah"], color=df["Kesesuaian Bidang Kerja"], barmode='stack',
#                  labels=dict(x="Tahun Lulus", y="Jumlah", color="Lulusan"))
#     fig.add_scatter(x=df["Tahun Lulus"], y=df["Jumlah Lulusan"], name='Lulusan', mode='lines+markers',
#                     hovertemplate="Lulusan=Total Lulusan <br>Jumlah=%{y} </br> Tahun Lulus=%{x}")
#     return fig


# @app.callback(
#     Output('grf_tempatkerja', 'figure'),
#     Input('grf_tempatkerja', 'id')
# )
# def graphTempatKerja(id):
#     df = dftempatkerja
#     fig = px.line(df, x=df["Tahun Lulus"], y=df["Lulusan Terlacak"], color=px.Constant('Lulusan Terlacak'),
#                   labels=dict(x="Tahun Lulus", y="Lingkup Kerja", color="Lulusan"))
#     fig.add_bar(x=df["Tahun Lulus"], y=df["Lokal/Regional"], name='Lokal/Regional',
#                 hovertemplate="Lulusan=Total Lulusan <br>Tahun Lulus=%{x} </br> Jumlah=%{y}")
#     fig.add_bar(x=df["Tahun Lulus"], y=df["Nasional"], name='Nasional',
#                 hovertemplate="Lulusan=Total Lulusan <br>Tahun Lulus=%{x} </br> Jumlah=%{y}")
#     fig.add_bar(x=df["Tahun Lulus"], y=df["Internasional"], name='Internasional',
#                 hovertemplate="Lulusan=Total Lulusan <br>Tahun Lulus=%{x} </br> Jumlah=%{y}")
#     fig.update_layout(barmode='stack')
#     # fig.add_scatter(x=df["Tahun Lulus"], y=df["Lulusan Terlacak"], name='Lulusan Terlacak', mode='lines+markers',
#     #                 hovertemplate="Lulusan=Total Lulusan <br>Tahun Lulus=%{x} </br> Jumlah=%{y}")
#     return fig

# @app.callback(
#     Output('grf_jabatan', 'figure'),
#     Input('grf_jabatan', 'id')
# )
# def graphJabatan(id):
#     df = pd.read_sql('''select count(*) as Jumlah, ifnull(posisi_jabatan_alumni,'LAINNYA') as Posisi, posisi_jabatan_alumni
# from fact_tracer_study tracer
# inner join dim_lulusan on dim_lulusan.id_lulusan = tracer.id_lulusan
# group by posisi, posisi_jabatan_alumni
# order by posisi_jabatan_alumni desc''', con)
#     fig = px.bar(df, x=df['Posisi'], y=df['Jumlah'], color=px.Constant('Jabatan'),
#                  labels=dict(x="Jabatan", y="Jumlah", color="Jabatan"))
#     return fig

# @app.callback(
#     Output('grf_perusahaan', 'figure'),
#     Input('grf_perusahaan', 'id')
# )
# def graphPerusahaan(id):
#     df = pd.read_sql('''select count(*) as Jumlah, nama_mapping_organisasi as "Perusahaan"
#     from fact_tracer_study tracer
#     inner join dim_lulusan on tracer.id_lulusan = dim_lulusan.id_lulusan
#     inner join dim_organisasi_pengguna_lulusan org on dim_lulusan.id_organisasi_pengguna_lulusan = org.id_organisasi_pengguna_lulusan
#     group by `Perusahaan`
#     order by jumlah desc
#     limit 15''', con)
#     fig = px.bar(df, x=df['Perusahaan'], y=df['Jumlah'], color=px.Constant('Perusahaan'),
#                  labels=dict(x="Perusahaan", y="Jumlah", color="Perusahaan"))
#     return fig
