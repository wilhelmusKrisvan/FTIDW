import dash
import pandas as pd
import dash_table as dt
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from appConfig import app, server
from dash import html, dcc
from datetime import date
import model.dao_alumni as data
import time

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

cardtbl_style = {
    'border': '1px solid #fafafa',
    'border-radius': '10px',
    'padding': '20px 10px 60px 10px',
    'box-shadow': '5px 10px 30px #ebedeb'
}

ttlgrf_style = {
    'textAlign': 'center',
    'padding': '10px',
    'color': 'black'
}

buttonLink_style = {
    'position': 'fixed',
    'width': '60px',
    'height': '60px',
    'bottom': '40px',
    'right': '40px',
    'background-color': '#2780e3',
    'color': 'white',
    'border-radius': '50px',
    'text-align': 'center',
    'box-shadow': '5px 10px 20px #ebedeb',
    'border': '1px solid #fafafa'
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
    'position': 'absolute',
    'margin': '-50px 25px 10px 10px',
}

listDropdownTA = []
for x in range(0, 5):
    counter = x + 1
    listDropdownTA.append(
        str(int(date.today().strftime('%Y')) - 5 + x) + '/' + str(int(date.today().strftime('%Y')) - 4 + x))

listDropdownTh = []
for x in range(0, 5):
    counter = x + 1
    listDropdownTh.append(str(int(date.today().strftime('%Y')) - 5 + x))

masatunggu = dbc.Container([
    dbc.Card([
        html.H5('Masa Tunggu Lulusan',
                style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Dari :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrMasaStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[0],
                        style={'color': 'black'},
                        placeholder='Pilih Tahun Awal',
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Sampai :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrMasaEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[3],
                        style={'color': 'black'},
                        placeholder='Pilih Tahun Akhir',
                        clearable=False
                    )
                ])
            ])
        ]),
        dcc.Tabs([
            #ini
            dcc.Tab(label='Jumlah Lulusan per Kategori', value='MsTgglulusan',
                    children=[
                        html.Div([
                            dcc.Loading(
                                id='loading-1',
                                type="default",
                                children=dcc.Graph(id='grf_MsTgglulusan')),
                            dbc.Button('Lihat Semua Data', id='cll_MsTgglulusan', n_clicks=0,
                                       style=button_style)
                        ])
                    ], style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Rata-rata Jumlah Lulusan per Kategori', value='rateGol',
                    children=[
                        html.Div([
                            dcc.Loading(
                                id='loading-1',
                                type="default",
                                children=dcc.Graph(id='grf_rateGol')),
                            dbc.Button('Lihat Semua Data', id='cll_rateGol', n_clicks=0,
                                       style=button_style)
                        ])
                    ],
                    style=tab_style, selected_style=selected_style),
        ], style=tabs_styles, id='tab_masatunggu', value='MsTgglulusan'),
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_tblmasatunggu',
        is_open=False
    )
], style=cont_style)

lulusan = dbc.Container([
    dbc.Card([
        html.H5('Lulusan',
                style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Dari :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrLulusanStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[0],
                        style={'color': 'black'},
                        placeholder='Pilih Tahun Awal',
                        clearable=False
                    )
                ]),
                dbc.Col([
                    html.P('Sampai :', style={'marginBottom': 0}),
                    dcc.Dropdown(
                        id='fltrLulusanEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                        value=listDropdownTh[3],
                        style={'color': 'black'},
                        placeholder='Pilih Tahun Akhir',
                        clearable=False
                    )
                ])
            ])
        ]),
        dcc.Tabs([
            dcc.Tab(label='Tingkat Kesesuaian Bidang Kerja', value='bidkerja',
                    children=[
                        html.Div([
                            dcc.Loading(
                                id='loading-1',
                                type="default",
                                children=dcc.Graph(id='grf_bidangKerja')),
                            dbc.Button('Lihat Semua Data', id='cll_bidangKerja', n_clicks=0,
                                       style=button_style)
                        ])
                    ], style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Lulusan Berwirausaha', value='wirausaha',
                    children=[
                        html.Div([
                            dcc.Loading(
                                id='loading-1',
                                type="default",
                                children=dcc.Graph(id='grf_alumniWirausaha')),
                            dbc.Button('Lihat Semua Data', id='cll_alumniWirausaha', n_clicks=0,
                                       style=button_style)
                        ])
                    ], style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Rerata Gaji Alumni Pekerjaan <6 Bulan ', value='gaji6bln',
                    children=[
                        html.Div([
                            dcc.Loading(
                                id='loading-1',
                                type="default",
                                children=dcc.Graph(id='grf_gaji')),
                            dbc.Button('Lihat Semua Data', id='cll_gaji', n_clicks=0,
                                       style=button_style)
                        ])
                    ], style=tab_style, selected_style=selected_style),
        ], style=tabs_styles, id='tab_lulusan', value='bidkerja')
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_lulusan',
        is_open=False
    )
], style=cont_style)

kepuasan = dbc.Container([
    dbc.Card([
        html.H5('Kepuasan',
                style=ttlgrf_style),
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Kepuasan Lulusan Terhadap Layanan UKDW', value='layananukdw',
                        children=[
                            html.Div([
                                dcc.Loading(
                                    id='loading-1',
                                    type="default",
                                    children=dcc.Graph(id='grf_layananukdw')),
                                dbc.Button('Lihat Semua Data', id='cll_grfLayananUKDW', n_clicks=0,
                                           style=button_style)
                            ]),
                        ],
                        style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Kepuasan Pengguna Terhadap Jenis Kemampuan Lulusan', value='skill',
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
                            html.Div([
                                dcc.Loading(
                                    id='loading-1',
                                    type="default",
                                    children=dcc.Graph(id='grf_skill')),
                                dbc.Button('Lihat Semua Data', id='cll_grfSkill', n_clicks=0,
                                           style=button_style)
                            ]),
                        ],
                        style=tab_style, selected_style=selected_style),
            ], style=tabs_styles, id='tab_kepuasan', value='layananukdw'),
        ])
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
    html.Div([kepuasan], style={'margin-bottom': '50px'}),
    dbc.Container([
        dcc.Link([
            dbc.Button('^', style=buttonLink_style),
        ], href='#name')
    ], style={'margin-left': '90%'})
], style={'justify-content': 'center'})


# CONTROL COLLAPSE
@app.callback(
    Output('cll_tblmasatunggu', 'is_open'),
    Output('cll_tblmasatunggu', 'children'),
    [Input('cll_MsTgglulusan', 'n_clicks'),
     Input('cll_rateGol', 'n_clicks'),
     Input('tab_masatunggu', 'value')],
    [State('cll_tblmasatunggu', 'is_open')]
)
def toggle_collapse(mstgg, msrerata, n, is_open):
    isiMasaTunggu = dbc.Card(
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
        ),style=cardtbl_style
    ),
    isiRerataMasaTunggu = dbc.Card(
        dt.DataTable(
            id='tbl_rateGol',
            columns=[
                {'name': i, 'id': i} for i in dfmasaTungguGol.columns
            ],
            data=dfmasaTungguGol.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ), style=cardtbl_style
    )
    if n and mstgg == 'MsTgglulusan':
        return not is_open, isiMasaTunggu
    elif n and msrerata == 'rateGol':
        return not is_open, isiRerataMasaTunggu
    return is_open, None


@app.callback(
    Output('cll_lulusan', 'is_open'),
    Output('cll_lulusan', 'children'),
    [Input('cll_bidangKerja', 'n_clicks'),
     Input('cll_alumniWirausaha', 'n_clicks'),
     Input('cll_gaji', 'n_clicks'),
     Input('tab_lulusan', 'value')],
    [State('cll_lulusan', 'is_open')]
)
def toggle_collapse(bidker, wira, gaji, lulusan, is_open):
    isiBidKer = dbc.Card(
        dt.DataTable(
            id='tbl_bidker',
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
        ),style=cardtbl_style
    )
    isiWirausaha = dbc.Card(
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
        ),style=cardtbl_style
    )
    isiGaji = dbc.Card(
        dt.DataTable(
            id='tbl_gaji',
            columns=[
                {'name': i, 'id': i} for i in dfGaji.columns
            ],
            data=dfGaji.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        ),style=cardtbl_style
    )
    if bidker and lulusan == 'bidkerja':
        return not is_open, isiBidKer
    if wira and lulusan == 'wirausaha':
        return not is_open, isiWirausaha
    if gaji and lulusan == 'gaji6bln':
        return not is_open, isiGaji
    return is_open, None

@app.callback(
    Output('grf_bidangKerja', 'figure'),
    Input('fltrLulusanStart', 'value'),
    Input('fltrLulusanEnd', 'value')
)
def graphBidKerja(start, end):
    df = data.getDataFrameFromDBwithParams('''
    select data2.tahun_lulus as "Tahun Lulus", 
            TINGGI as 'Tinggi', SEDANG as 'Sedang', RENDAH as 'Rendah', LAINNYA as 'Lainnya',
            lulusan.jumlah as "Lulusan", terlacak.jumlah as "Lulusan Terlacak" 
     from
     (
        select tahun_lulus,
            SUM(IF( tingkat_kesesuaian_bidang_kerja = "TINGGI", data.jumlah, 0)) AS "TINGGI",
            SUM(IF( tingkat_kesesuaian_bidang_kerja = "SEDANG", data.jumlah, 0)) AS "SEDANG",
            SUM(IF( tingkat_kesesuaian_bidang_kerja = "RENDAH", data.jumlah, 0)) AS "RENDAH",
            SUM(IF( tingkat_kesesuaian_bidang_kerja = "LAINNYA", data.jumlah, 0)) AS "LAINNYA"
        from (
            select count(*) as jumlah, ifnull(tingkat_kesesuaian_bidang_kerja,"LAINNYA") as tingkat_kesesuaian_bidang_kerja,tahun_lulus
            from fact_tracer_study fact
            inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
            group by tahun_lulus,tingkat_kesesuaian_bidang_kerja
            order by tahun_lulus asc
            )data
            group by tahun_lulus
    ) data2
    left join (
        select count(id_mahasiswa) as jumlah, tahun_lulus
        from (select *, if(semester_yudisium = 'GENAP', substr(tahun_ajaran_yudisium,6,4),substr(tahun_ajaran_yudisium,1,4)) as tahun_lulus
        from fact_yudisium) data
        group by tahun_lulus
    )lulusan on lulusan.tahun_lulus = data2.tahun_lulus
    left join(
        select count(id_mahasiswa) as jumlah, tahun_lulus
        from dim_lulusan
        inner join fact_tracer_study on dim_lulusan.id_lulusan = fact_tracer_study.id_lulusan
        group by tahun_lulus
    )terlacak on terlacak.tahun_lulus = data2.tahun_lulus
    where data2.tahun_lulus between %(start)s and %(end)s
    order by data2.tahun_lulus
    ''',{'start':start,'end':end})
    fig = px.bar(df, x=df['Tahun Lulus'], y=df.columns[1:5])
    fig.update_layout(barmode='group', yaxis_title='Jumlah Lulusan', xaxis_title='Tahun Lulus', legend_title='Tingkat Kesesuaian')
    return fig

@app.callback(
    Output('grf_alumniWirausaha', 'figure'),
    Input('fltrLulusanStart', 'value'),
    Input('fltrLulusanEnd', 'value')
)
def graphWirausaha(start, end):
    df = data.getDataFrameFromDBwithParams('''
    select tahun_lulus 'Tahun Lulus', count(distinct fts.id_lulusan) 'Jumlah Wirausahawan'
    from fact_tracer_study fts
             inner join dim_lulusan dl on fts.id_lulusan = dl.id_lulusan
             inner join dim_organisasi_pengguna_lulusan dopl
                        on dl.id_organisasi_pengguna_lulusan = dopl.id_organisasi_pengguna_lulusan
    where jenis_organisasi='WIRASWASTA'
      and tahun_lulus between %(start)s and %(end)s
    group by tahun_lulus
    order by tahun_lulus;
    ''',{'start':start,'end':end})
    fig = px.line(df, x=df['Tahun Lulus'],y=df['Jumlah Wirausahawan'])
    fig.update_traces(mode='lines+markers')
    return fig

@app.callback(
    Output('grf_gaji', 'figure'),
    Input('fltrLulusanStart', 'value'),
    Input('fltrLulusanEnd', 'value')
)
def graphGaji(start, end):
    df = data.getDataFrameFromDBwithParams('''
    select tahun_lulus 'Tahun Lulus',ceiling(avg(pendapatan_utama)) 'Rerata Pendapatan' 
    from fact_tracer_study fts
        inner join dim_lulusan dl on fts.id_lulusan = dl.id_lulusan
    where waktu_tunggu like 'KURANG 6 BULAN'
        and tahun_lulus between %(start)s and %(end)s
    group by tahun_lulus
    order by tahun_lulus
    ''',{'start':start,'end':end})
    fig = px.line(df, x=df['Tahun Lulus'],y=df['Rerata Pendapatan'])
    fig.update_traces(mode='lines+markers')
    return fig

@app.callback(
    Output('cll_kepuasan', 'is_open'),
    Output('cll_kepuasan', 'children'),
    [Input("cll_grfLayananUKDW", "n_clicks"),
     Input("cll_grfSkill", "n_clicks"),
     Input("tab_kepuasan", "value")],
    [State("cll_kepuasan", "is_open")])
def toggle_collapse(nlayanan, nskill, puas, is_open):
    isiLayanan = dbc.Card(
        dt.DataTable(
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
        ), style=cardtbl_style
    )
    isiSkill = dbc.Card(
        dt.DataTable(
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
        ), style=cardtbl_style
    )
    if nlayanan and puas == 'layananukdw':
        return not is_open, isiLayanan
    if nskill and puas == 'skill':
        return not is_open, isiSkill
    return is_open, None


@app.callback(
    Output('grf_MsTgglulusan', 'figure'),
    Input('fltrMasaStart', 'value'),
    Input('fltrMasaEnd', 'value')
)
def graphMSLulusan(start, end):
    df = data.getDataFrameFromDBwithParams('''
    select data2.*, lulusan.jumlah as 'Lulusan', terlacak.jumlah as 'Lulusan Terlacak' from
     (
        select tahun_lulus 'Tahun Lulus',
        SUM(IF( waktu_tunggu = 'KURANG 6 BULAN', data.jumlah, 0)) AS '<6 BULAN',
        SUM(IF( waktu_tunggu = '6 - 18 BULAN', data.jumlah, 0)) AS '6-18 BULAN',
        SUM(IF( waktu_tunggu = 'LEBIH 18 BULAN', data.jumlah, 0)) AS '>18 BULAN',
        SUM(IF( waktu_tunggu = 'LAINNYA', data.jumlah, 0)) AS 'LAINNYA'
        from (
            select count(*) as jumlah, ifnull(waktu_tunggu,'LAINNYA') as waktu_tunggu,tahun_lulus
            from fact_tracer_study fact
            inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
            group by waktu_tunggu ,tahun_lulus
            order by tahun_lulus desc
        ) data
        group by tahun_lulus
        order by tahun_lulus
    ) data2
    left join (
        select count(id_mahasiswa) as jumlah, tahun_lulus
        from (select *, if(semester_yudisium = 'GENAP', substr(tahun_ajaran_yudisium,6,4),substr(tahun_ajaran_yudisium,1,4)) as tahun_lulus
        from fact_yudisium) data
        group by tahun_lulus
    )lulusan on lulusan.tahun_lulus = data2.`Tahun Lulus`
    left join(
        select count(id_mahasiswa) as jumlah, tahun_lulus
        from dim_lulusan
        group by tahun_lulus
    )terlacak on terlacak.tahun_lulus = data2.`Tahun Lulus`
    where terlacak.tahun_lulus between %(start)s and %(end)s
    order by data2.`Tahun Lulus`;   
    ''', {'start': start, 'end': end})
    fig = px.bar(df, x=df['Tahun Lulus'], y=df.columns[1:5])
    fig.update_layout(barmode='group', yaxis_title='Jumlah Lulusan', xaxis_title='Tahun Lulus', legend_title='Waktu Tunggu')
    return fig

@app.callback(
    Output('grf_rateGol', 'figure'),
    Input('fltrMasaStart', 'value'),
    Input('fltrMasaEnd', 'value')
)
def graphRataMS(tglstart, tglend):
    df = data.getDataFrameFromDBwithParams('''
    select count(waktu_tunggu) Jumlah, waktu_tunggu Waktu,tahun_lulus Tahun from fact_tracer_study fts
        inner join dim_lulusan dl on fts.id_lulusan = dl.id_lulusan
        where waktu_tunggu is not null and (tahun_lulus between %(start)s and %(end)s)
        group by waktu_tunggu,tahun_lulus
        order by tahun_lulus asc
    ''', {'start': tglstart, 'end': tglend})
    fig = px.line(df, x=df['Tahun'], y=df['Jumlah'], color=df['Waktu'])
    fig.update_traces(mode='lines+markers')
    return fig

@app.callback(
    Output('grf_layananukdw', 'figure'),
    Input('grf_layananukdw', 'id')
)
def graphLayanan(id):
    df = dfKepuasanPelayanan
    fig = px.pie(df, values=df['Persen'], names=df['Nilai'], color=df['Nilai'])
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


@app.callback(
    Output('grf_bidangkerja', 'figure'),
    Input('grf_bidangkerja', 'id')
)
def graphBidangKerja(id):
    df = pd.read_sql('''
    select count(*) as Jumlah,
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
    order by dim_lulusan.tahun_lulus asc''')
    fig = px.bar(df, x=df["Tahun Lulus"], y=df["Jumlah"], color=df["Kesesuaian Bidang Kerja"], barmode='stack',
                 labels=dict(x="Tahun Lulus", y="Jumlah", color="Lulusan"))
    fig.add_scatter(x=df["Tahun Lulus"], y=df["Jumlah Lulusan"], name='Lulusan', mode='lines+markers',
                    hovertemplate="Lulusan=Total Lulusan <br>Jumlah=%{y} </br> Tahun Lulus=%{x}")
    return fig

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
