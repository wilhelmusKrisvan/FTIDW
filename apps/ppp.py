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

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

dfjmlppp = data.getJumlahPPP()
dfpenelitiandana = data.getPenelitianDana()
dfpkmdana = data.getPKMDana()

dfpenelitianmhs = data.getPenelitianMhs()
dfpkmmhs = data.getPKMMhs()
dfpublikasimhs = data.getPublikasiMhs()
dfttguadopsimhs = data.getTTGUMhsDiadopsi()
dfluaranhkimhs = data.getLuaranHKIMhsperTh()
dfppdosenkpskripsimhs = data.getPPDosenKPSkripsiMhs()

tbl_kerjasamaPP = data.getKerjasamaPP()
dfkisitasi3th = data.getKISitasi3th()
dfluaranhkidosen = data.getLuaranHKIDosenperTh()
dfluaranttgudosen = data.getLuaranTTGUDosenperTh()
dfluaranbukudosen = data.getLuaranBukuDosenperTh()

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

penelitianDana = html.Div([
    dbc.Row([
        dbc.Col([
                html.H5('Penelitian dan Sumber Dana', style=ttlgrf_style),
                dt.DataTable(
                    id='dfpenelitiandana',
                    columns=[
                        {'name': i, 'id': i} for i in dfpenelitiandana.columns
                    ],
                    data=dfpenelitiandana.to_dict('records'),
                    sort_action='native',
                    sort_mode='multi',
                    style_table={'padding': '10px', 'overflowX': 'auto'},
                    style_header={'textAlign': 'center'},
                    style_data={'font-size': '80%', 'textAlign': 'center'},
                    style_cell={'width': 95},
                    page_size=10,
                )
        ], width=12),
    ])
], style={'margin-top': '50px', 'width': '100%'})

pkmDana = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H5('PKM dan Sumber Dana',
                        style=ttlgrf_style),
                dt.DataTable(
                    id='dfpkmdana',
                    columns=[
                        {'name': i, 'id': i} for i in dfpkmdana.columns
                    ],
                    data=dfpkmdana.to_dict('records'),
                    sort_action='native',
                    sort_mode='multi',
                    style_table={'padding': '10px', 'overflowX': 'auto'},
                    style_header={'textAlign': 'center'},
                    style_data={'font-size': '80%', 'textAlign': 'center'},
                    style_cell={'width': 95},
                    page_size=10,
                )
            ], style=card_style),
        ], width=12),
    ])
], style=card_style)

grafikPenelitian = html.Div([
    dbc.Row([
        dbc.Col([
            html.H5('Penelitian Dosen',
                    style=ttlgrf_style),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H3('Penelitian PerTahun'),
            dcc.Graph(id='grf_DosenPenelitian'),
        ], width=6),
        dbc.Col([
            html.H3('Perbandingan Asal Sumber Dana Penelitian'),
            dcc.Graph(id='grf_bdgDosenPenelitian')
        ], width=6)
    ])
], style=card_style)

grafikPkm = html.Div([
    dbc.Row([
        dbc.Col([
            html.H5('PKM dan Sumber Dana',
                    style=ttlgrf_style),
        ])
    ], style={'z-index': '2'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3('Pkm PerTahun'),
                dcc.Graph(id='grf_DosenPkm'),
            ], style={'justify-content': 'center'})
        ], width=6),
        dbc.Col([
            dbc.Card([
                html.H3('Perbandingan Asal Sumber Dana Pkm'),
                dcc.Graph(id='grf_bdgDosenPkm'),
            ], style={'justify-content': 'center'})
        ], width=6)
    ])
], style=card_style)

penelitianMhs = html.Div([
    dbc.Row([
        dbc.Col([
            html.H5('Keterlibatan Mahasiswa',
                    style=ttlgrf_style),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H3('Penelitian Melibatkan Mahasiswa', style={'text-align': 'center'}),
            html.Div([
                dt.DataTable(
                    id='dfpenelitianmhs',
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
                )
            ])
        ], width=12),
    ])
], style=card_style)

pkmMhs = html.Div([
    dbc.Row([
        dbc.Col([
            html.H5('Keterlibatan Mahasiswa',
                    style=ttlgrf_style),
        ])
    ], style={'z-index': '2'}),
    dbc.Row([
        dbc.Col([
            html.H3('PkM Melibatkan Mahasiswa', style={'text-align': 'center'}),
            html.Div([
                dt.DataTable(
                    id='dfpkmmhs',
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
                )
                ])
        ], width=12),
    ])
], style=card_style)

ppp = dbc.Container([
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
            dcc.Tab(label='Kerjasama Penelitian PKM', value='kerjasamappkm',
                    children=[
                        dt.DataTable(
                            id='tbl_kerjasamaPPP',
                            columns=[
                                {'name': i, 'id': i} for i in tbl_kerjasamaPP.columns
                            ],
                            data=tbl_kerjasamaPP.to_dict('records'),
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
                    style=tab_style, selected_style=selected_style)
        ], style=tabs_styles, value='pppdosen'),
    ], style=cardgrf_style)
], style=cont_style)

analisispp = dbc.Container([
    dbc.Card([
        html.H5('Penelitian & PKM',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Penelitian', value='penelitian',
                    children=[
                        penelitianDana,
                        grafikPenelitian,
                        penelitianMhs
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='PKM', value='pkm',
                    children=[
                        pkmDana,
                        grafikPkm,
                        pkmMhs
                    ],
                    style=tab_style, selected_style=selected_style)
        ], style=tabs_styles, value='penelitian')
    ],style=cardgrf_style)
], style=cont_style)

layout = html.Div([
    html.Div([ppp]),
    html.Div([analisispp], style={'margin-bottom': '50px'})
], style={'justify-content': 'center'})

@app.callback(
    Output("grf_DosenPenelitian", 'figure'), Input('grf_DosenPenelitian', 'id')
)
def FillPenelitianDosen(id):
    df = pd.read_sql('''select tahun, count(*) as Jumlah
from fact_penelitian fact
inner join dim_penelitian_pkm on fact.id_penelitian = dim_penelitian_pkm.id_penelitian_pkm
inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
group by tahun
order by tahun''', con)
    fig = px.line(df, x=df['tahun'], y=df['Jumlah'])
    fig.update_traces(mode='lines+markers')
    return fig


@app.callback(
    Output("grf_bdgDosenPenelitian", 'figure'), Input('grf_bdgDosenPenelitian', 'id')
)
def FillbdgPenelitianDosen(id):
    df = pd.read_sql('''select Tahun, dim_sumber_dana.status "Asal Sumber Dana", count(*) as Jumlah
from fact_penelitian fact
inner join dim_penelitian_pkm on fact.id_penelitian = dim_penelitian_pkm.id_penelitian_pkm
inner join br_pp_dana on dim_penelitian_pkm.id_penelitian_pkm = br_pp_dana.id_penelitian_pkm
inner join dim_sumber_dana on br_pp_dana.id_sumber_dana = dim_sumber_dana.id_sumber_dana
inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
group by Tahun, "Asal Sumber Dana"
order by Tahun''', con)
    fig = px.bar(df, x=df['Tahun'], y=df['Jumlah'], color=df['Asal Sumber Dana'])
    fig.update_layout(barmode='group')
    return fig


@app.callback(
    Output("grf_DosenPkm", 'figure'), Input('grf_DosenPkm', 'id')
)
def FillPkmDosen(id):
    df = pd.read_sql('''select tahun, count(*) as Jumlah
from fact_pkm fact
inner join dim_penelitian_pkm on fact.id_pkm = dim_penelitian_pkm.id_penelitian_pkm
inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
group by tahun
order by tahun''', con)
    fig = px.line(df, x=df['tahun'], y=df['Jumlah'])
    fig.update_traces(mode='lines+markers')
    return fig


@app.callback(
    Output("grf_bdgDosenPkm", 'figure'), Input('grf_bdgDosenPkm', 'id')
)
def FillbdgPkmDosen(id):
    df = pd.read_sql('''select Tahun, dim_sumber_dana.status "Asal Sumber Dana", count(*) as Jumlah
from fact_pkm fact
inner join dim_penelitian_pkm on fact.id_pkm = dim_penelitian_pkm.id_penelitian_pkm
inner join br_pp_dana on dim_penelitian_pkm.id_penelitian_pkm = br_pp_dana.id_penelitian_pkm
inner join dim_sumber_dana on br_pp_dana.id_sumber_dana = dim_sumber_dana.id_sumber_dana
inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
group by Tahun, "Asal Sumber Dana"
order by Tahun''', con)
    fig = px.bar(df, x=df['Tahun'], y=df['Jumlah'], color=df['Asal Sumber Dana'])
    fig.update_layout(barmode='group')
    return fig
