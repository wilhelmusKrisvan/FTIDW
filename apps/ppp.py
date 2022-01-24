import dash
import pandas as pd
import dash_table as dt
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from appConfig import app, server
import model.dao_ppp as data

dfjmlppp = data.getJumlahPPP()
# dfppdosenkpskripsimhs = data.getPPDosenKPSkripsiMhs()
dfpenelitianmhs = data.getPenelitianMhs()
dfpkmmhs = data.getPKMMhs()

tbl_kerjaPeneliti = data.getKerjasamaPenelitian()
tbl_kerjaPKM = data.getKerjasamaPKM()

# GAJEE
dfpenelitiandana = data.getPenelitianDana()
dfpkmdana = data.getPKMDana()

dfkisitasi3th = data.getKISitasi3th()

dfluaranhkidosen = data.getLuaranHKIDosenperTh()
dfluaranttgudosen = data.getLuaranTTGUDosenperTh()
dfluaranbukudosen = data.getLuaranBukuDosenperTh()

dfpublikasimhs = data.getPublikasiMhs()
dfttguadopsimhs = data.getTTGUMhsDiadopsi()
dfluaranhkimhs = data.getLuaranHKIMhsperTh()

dfratajumlpenelitiandosen = data.getRerataJumlPenelitianDosenperTh()
dfratejumlpublikasidosen = data.getRerataJumlPublikasiDosenperTh()

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

pppMhs = dbc.Container([
    dbc.Card([
        html.H5('Penelitian PKM Publikasi',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='PPP Dosen', value='pppdosen',
                    children=[
                        dt.DataTable(
                            id='tbl_pppDosen',
                            columns=[
                                {'name': i, 'id': i} for i in dfjmlppp.columns
                            ],
                            data=dfjmlppp.to_dict('records'),
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
            dcc.Tab(label='Jumlah Pengabdian Dosen yang Melibatkan Mahasiswa di Tiap Tahun Ajaran', value='pkmdosenmhs',
                    children=[
                        dt.DataTable(
                            id='tbl_pkmDosenMhs',
                            columns=[
                                {'name': i, 'id': i} for i in dfpkmmhs.columns
                            ],
                            data=dfpkmmhs.to_dict('records'),
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
            dcc.Tab(label='Jumlah Penelitian Dosen yang Melibatkan Mahasiswa di Tiap Tahun Ajaran',
                    value='telitidosenmhs',
                    children=[
                        dt.DataTable(
                            id='tbl_telitiDosenMhs',
                            columns=[
                                {'name': i, 'id': i} for i in dfpenelitianmhs.columns
                            ],
                            data=dfpenelitianmhs.to_dict('records'),
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
        ], style=tabs_styles, value='pppdosen'),
    ], style=cardgrf_style)
], style=cont_style)

kerjasamaPPP = dbc.Container([
    dbc.Card([
        html.H5('Kegiatan Dengan Mitra',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Kegiatan dengan lembaga mitra dalam bidang Penelitian', value='kerjaTeliti',
                    children=[
                        dt.DataTable(
                            id='tbl_kerjaTeliti',
                            columns=[
                                {'name': i, 'id': i} for i in tbl_kerjaPeneliti.columns
                            ],
                            data=tbl_kerjaPeneliti.to_dict('records'),
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
            dcc.Tab(label='Kegiatan dengan lembaga mitra dalam bidang Pengabdian', value='kerjaPKM',
                    children=[
                        dt.DataTable(
                            id='tbl_kerjaPKM',
                            columns=[
                                {'name': i, 'id': i} for i in tbl_kerjaPKM.columns
                            ],
                            data=tbl_kerjaPKM.to_dict('records'),
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
        ], style=tabs_styles, value='kerjaTeliti'),
    ], style=cardgrf_style)
], style=cont_style)

sitasi = dbc.Container([
    dbc.Card([
        html.H5('Jumlah Karya Ilmiah yang Disitasi',
                style=ttlgrf_style),
        dt.DataTable(
            id='tbl_Sitasi',
            columns=[
                {'name': i, 'id': i} for i in dfkisitasi3th.columns
            ],
            data=dfkisitasi3th.to_dict('records'),
            sort_action='native',
            sort_mode='multi',
            style_table={'padding': '10px', 'overflowX': 'auto'},
            style_header={'textAlign': 'center'},
            style_data={'font-size': '80%', 'textAlign': 'center'},
            style_cell={'width': 95},
            page_size=10,
            export_format='xlsx'
        )
    ], style=cardgrf_style)
], style=cont_style)

luaran = dbc.Container([
    dbc.Card([
        html.H5('Luaran PPP Dosen',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Jumlah luaran HKI yang dihasilkan Dosen', value='HKIDosen',
                    children=[
                        dt.DataTable(
                            id='tbl_HKIDosen',
                            columns=[
                                {'name': i, 'id': i} for i in dfluaranhkidosen.columns
                            ],
                            data=dfluaranhkidosen.to_dict('records'),
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
            dcc.Tab(label='Jumlah luaran TTGU yang dihasilkan Dosen', value='TTGUDosen',
                    children=[
                        dt.DataTable(
                            id='tbl_TTGUDosen',
                            columns=[
                                {'name': i, 'id': i} for i in dfluaranttgudosen.columns
                            ],
                            data=dfluaranttgudosen.to_dict('records'),
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
            dcc.Tab(label='Jumlah luaran Buku yang dihasilkan Dosen', value='BukuDosen',
                    children=[
                        dt.DataTable(
                            id='tbl_BukuDosen',
                            columns=[
                                {'name': i, 'id': i} for i in dfluaranbukudosen.columns
                            ],
                            data=dfluaranbukudosen.to_dict('records'),
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
        ], style=tabs_styles, value='HKIDosen'),
    ], style=cardgrf_style)
], style=cont_style)

luaranMhs = dbc.Container([
    dbc.Card([
        html.H5('Luaran PPP Mahasiswa',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Jumlah Publikasi Mahasiswa', value='pubMhs',
                    children=[
                        dt.DataTable(
                            id='tbl_pubMhs',
                            columns=[
                                {'name': i, 'id': i} for i in dfpublikasimhs.columns
                            ],
                            data=dfpublikasimhs.to_dict('records'),
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
            dcc.Tab(label='Jumlah TTGU Mahasiswa', value='ttguMhs',
                    children=[
                        dt.DataTable(
                            id='tbl_ttguMhs',
                            columns=[
                                {'name': i, 'id': i} for i in dfttguadopsimhs.columns
                            ],
                            data=dfttguadopsimhs.to_dict('records'),
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
            dcc.Tab(label='Jumlah Luaran HKI Mahasiswa', value='HKIMhs',
                    children=[
                        dt.DataTable(
                            id='tbl_HKIMhs',
                            columns=[
                                {'name': i, 'id': i} for i in dfluaranhkimhs.columns
                            ],
                            data=dfluaranhkimhs.to_dict('records'),
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
        ], style=tabs_styles, value='pubMhs'),
    ], style=cardgrf_style)
], style=cont_style)

rerata = dbc.Container([
    dbc.Card([
        html.H5('Rata - Rata PPP',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Rata-rata Jumlah Penelitian Dosen', value='reTelitiDosen',
                    children=[
                        dt.DataTable(
                            id='tbl_reTelitiDosen',
                            columns=[
                                {'name': i, 'id': i} for i in dfratajumlpenelitiandosen.columns
                            ],
                            data=dfratajumlpenelitiandosen.to_dict('records'),
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
            dcc.Tab(label='Rata-rata Jumlah Publikasi Dosen', value='rePubDosen',
                    children=[
                        dt.DataTable(
                            id='rePubDosen',
                            columns=[
                                {'name': i, 'id': i} for i in dfratejumlpublikasidosen.columns
                            ],
                            data=dfratejumlpublikasidosen.to_dict('records'),
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
        ], style=tabs_styles, value='reTelitiDosen'),
    ], style=cardgrf_style)
], style=cont_style)

layout = html.Div([
    html.Div(html.H1('Analisis Penelitian, Pengabdian, Publikasi, dan Luaran',
                     style={'margin-top': '30px', 'textAlign': 'center'}
                     )
             ),
    html.Div([pppMhs]),
    html.Div([kerjasamaPPP]),
    html.Div([sitasi]),
    html.Div([luaran]),
    html.Div([luaranMhs]),
    html.Div([rerata], style={'margin-bottom': '50px'})
], style={'justify-content': 'center'})

# @app.callback(
#     Output("grf_DosenPenelitian", 'figure'), Input('grf_DosenPenelitian', 'id')
# )
# def FillPenelitianDosen(id):
#     df = pd.read_sql('''select tahun, count(*) as Jumlah
# from fact_penelitian fact
# inner join dim_penelitian_pkm on fact.id_penelitian = dim_penelitian_pkm.id_penelitian_pkm
# inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
# group by tahun
# order by tahun''', con)
#     fig = px.line(df, x=df['tahun'], y=df['Jumlah'])
#     fig.update_traces(mode='lines+markers')
#     return fig


# @app.callback(
#     Output("grf_bdgDosenPenelitian", 'figure'), Input('grf_bdgDosenPenelitian', 'id')
# )
# def FillbdgPenelitianDosen(id):
#     df = pd.read_sql('''select Tahun, dim_sumber_dana.status "Asal Sumber Dana", count(*) as Jumlah
# from fact_penelitian fact
# inner join dim_penelitian_pkm on fact.id_penelitian = dim_penelitian_pkm.id_penelitian_pkm
# inner join br_pp_dana on dim_penelitian_pkm.id_penelitian_pkm = br_pp_dana.id_penelitian_pkm
# inner join dim_sumber_dana on br_pp_dana.id_sumber_dana = dim_sumber_dana.id_sumber_dana
# inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
# group by Tahun, "Asal Sumber Dana"
# order by Tahun''', con)
#     fig = px.bar(df, x=df['Tahun'], y=df['Jumlah'], color=df['Asal Sumber Dana'])
#     fig.update_layout(barmode='group')
#     return fig


# @app.callback(
#     Output("grf_DosenPkm", 'figure'), Input('grf_DosenPkm', 'id')
# )
# def FillPkmDosen(id):
#     df = pd.read_sql('''select tahun, count(*) as Jumlah
# from fact_pkm fact
# inner join dim_penelitian_pkm on fact.id_pkm = dim_penelitian_pkm.id_penelitian_pkm
# inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
# group by tahun
# order by tahun''', con)
#     fig = px.line(df, x=df['tahun'], y=df['Jumlah'])
#     fig.update_traces(mode='lines+markers')
#     return fig


# @app.callback(
#     Output("grf_bdgDosenPkm", 'figure'), Input('grf_bdgDosenPkm', 'id')
# )
# def FillbdgPkmDosen(id):
#     df = pd.read_sql('''select Tahun, dim_sumber_dana.status "Asal Sumber Dana", count(*) as Jumlah
# from fact_pkm fact
# inner join dim_penelitian_pkm on fact.id_pkm = dim_penelitian_pkm.id_penelitian_pkm
# inner join br_pp_dana on dim_penelitian_pkm.id_penelitian_pkm = br_pp_dana.id_penelitian_pkm
# inner join dim_sumber_dana on br_pp_dana.id_sumber_dana = dim_sumber_dana.id_sumber_dana
# inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
# group by Tahun, "Asal Sumber Dana"
# order by Tahun''', con)
#     fig = px.bar(df, x=df['Tahun'], y=df['Jumlah'], color=df['Asal Sumber Dana'])
#     fig.update_layout(barmode='group')
#     return fig
