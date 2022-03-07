import dash
import pandas as pd
import dash_table as dt
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from appConfig import app, server
from datetime import date
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
dfratajumlpublikasidosen = data.getRerataJumlPublikasiDosenperTh()

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

pppMhs = dbc.Container([
    dbc.Card([
        html.H5('Penelitian PKM Publikasi',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='PPP Dosen', value='pppdosen',
                    children=[
                    dbc.Card(
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
                        ),style=cardtbl_style
                    )
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='PKM Dosen & Mahasiswa', value='pkmdosenmhs',
                    children=[
                        dbc.Card(
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
                            ),style=cardtbl_style
                        )
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Penelitian Dosen & Mahasiswa',
                    value='telitidosenmhs',
                    children=[
                        dbc.Card(
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
                            ),style=cardtbl_style
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
            dcc.Tab(label='Penelitian', value='kerjaTeliti',
                    children=[
                        dbc.Card(
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
                            ), style=cardtbl_style
                        )
                    ],
                    style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Pengabdian', value='kerjaPKM',
                    children=[
                        dbc.Card(
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
                            ), style=cardtbl_style
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
    ], style=cardtbl_style)
], style=cont_style)

luaran = dbc.Container([
    dbc.Card([
        html.H5('Luaran PPP Dosen',
                style=ttlgrf_style),
        html.Div([
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id='fltrLuaranStart',
                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                        value=listDropdownTA[0],
                        style={'color': 'black'},
                        placeholder='Pilih Tahun Awal',
                        clearable=False
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='fltrLuaranEnd',
                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                        value=listDropdownTA[0],
                        style={'color': 'black'},
                        placeholder='Pilih Tahun Akhir',
                        clearable=False
                    )
                )
            ]),
            dcc.Tabs([
                dcc.Tab(label='Hak Kekayaan Intelektual (HKI)', value='HKIDosen',
                        children=[
                            html.Div([
                                dcc.Graph(id='grf_hkiDs'),
                                dbc.Button('Lihat Tabel', id='cll_grfhkiDs', n_clicks=0,
                                           style=button_style)
                            ])
                        ],
                        style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Teknologi Tepat Guna (TTGU)', value='TTGUDosen',
                        children=[
                            html.Div([
                                dcc.Graph(id='grf_ttguDs'),
                                dbc.Button('Lihat Tabel', id='cll_grfttguDs', n_clicks=0,
                                           style=button_style)
                            ])
                        ],
                        style=tab_style, selected_style=selected_style),
                dcc.Tab(label='Buku', value='BukuDosen',
                        children=[
                            html.Div([
                                dcc.Graph(id='grf_bukuDs'),
                                dbc.Button('Lihat Tabel', id='cll_grfbukuDs', n_clicks=0,
                                           style=button_style)
                            ])
                        ],
                        style=tab_style, selected_style=selected_style),
            ], style=tabs_styles, id='tab_luaranDosen', value='HKIDosen'),
        ])
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_luaranPPPDosen',
        is_open=False
    )
], style=cont_style)

luaranMhs = dbc.Container([
    dbc.Card([
        html.H5('Luaran PPP Mahasiswa',
                style=ttlgrf_style),
        dcc.Tabs([
            dcc.Tab(label='Publikasi', value='pubMhs',
                    children=[
                        html.Div([
                            dbc.Row([
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='fltrPubMhsStart',
                                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                                        value=listDropdownTA[0],
                                        style={'color': 'black'},
                                        placeholder='Pilih Tahun Awal',
                                        clearable=False
                                    )
                                ),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='fltrPubMhsEnd',
                                        options=[{'label': i, 'value': i} for i in listDropdownTA],
                                        value=listDropdownTA[3],
                                        style={'color': 'black'},
                                        placeholder='Pilih Tahun Akhir',
                                        clearable=False
                                    )
                                )
                            ])
                        ]),
                        html.Div([
                            dcc.Graph(id='grf_pubMhs'),
                            dbc.Button('Lihat Tabel', id='cll_grfpubMhs', n_clicks=0,
                                       style=button_style)
                        ])
                    ], style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Teknologi Tepat Guna (TTGU)', value='ttguMhs',
                    children=[
                        html.Div([
                            dbc.Row([
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='fltrTTGUMhsStart',
                                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                                        value=listDropdownTh[0],
                                        style={'color': 'black'},
                                        clearable=False
                                    )
                                ),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='fltrTTGUMhsEnd',
                                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                                        value=listDropdownTh[3],
                                        style={'color': 'black'},
                                        placeholder='Pilih Tahun Akhir',
                                        clearable=False
                                    )
                                )
                            ])
                        ]),
                        html.Div([
                            dcc.Graph(id='grf_ttguMhs'),
                            dbc.Button('Lihat Tabel', id='cll_grfttguMhs', n_clicks=0,
                                       style=button_style)
                        ])
                    ], style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Hak Kekayaan Intelektual (HKI)', value='hkiMhs',
                    children=[
                        html.Div([
                            dbc.Row([
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='fltrHKIMhsStart',
                                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                                        value=listDropdownTh[0],
                                        style={'color': 'black'},
                                        placeholder='Pilih Tahun Awal',
                                        clearable=False
                                    )
                                ),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='fltrHKIMhsEnd',
                                        options=[{'label': i, 'value': i} for i in listDropdownTh],
                                        value=listDropdownTh[3],
                                        style={'color': 'black'},
                                        placeholder='Pilih Tahun Akhir',
                                        clearable=False
                                    )
                                )
                            ])
                        ]),
                        html.Div([
                            dcc.Graph(id='grf_hkiMhs'),
                            dbc.Button('Lihat Tabel', id='cll_grfhkiMhs', n_clicks=0,
                                       style=button_style)
                        ])
                    ], style=tab_style, selected_style=selected_style),
        ], style=tabs_styles, id='tab_luaranMhs', value='pubMhs')
], style=cardgrf_style),
    dbc.Collapse(
        id='cll_luaranPPPMhs',
        is_open=False
    )
], style = cont_style)

rerata = dbc.Container([
dbc.Card([
    html.H5('Rata - Rata Jumlah PPP Dosen',
            style=ttlgrf_style),
    html.Div([
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='fltrRerataStart',
                    options=[{'label': i, 'value': i} for i in listDropdownTh],
                    value=listDropdownTh[0],
                    style={'color': 'black'},
                    placeholder='Pilih Tahun Awal',
                    clearable=False
                )
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='fltrRerataEnd',
                    options=[{'label': i, 'value': i} for i in listDropdownTh],
                    value=listDropdownTh[3],
                    style={'color': 'black'},
                    placeholder='Pilih Tahun Akhir',
                    clearable=False
                )
            )

        ]),
        dcc.Tabs([
            dcc.Tab(label='Penelitian', value='reTelitiDosen',
                    children=[
                        html.Div([
                            dcc.Graph(id='grf_reTelitiDosen'),
                            dbc.Button('Lihat Tabel', id='cll_grfreTelitiDosen', n_clicks=0,
                                       style=button_style)
                        ])
                    ], style=tab_style, selected_style=selected_style),
            dcc.Tab(label='Publikasi', value='rePubDosen',
                    children=[
                        html.Div([
                            dcc.Graph(id='grf_rePubDosen'),
                            dbc.Button('Lihat Tabel', id='cll_grfrePubDosen', n_clicks=0,
                                       style=button_style)
                        ])
                    ], style=tab_style, selected_style=selected_style),
        ], style=tabs_styles, id='tab_rerataPPP', value='reTelitiDosen')
    ]),
], style=cardgrf_style),
    dbc.Collapse(
        id='cll_rerataPPP',
        is_open=False
    )
], style = cont_style)

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
        html.Div([rerata], style={'margin-bottom': '50px'}),
        dbc.Container([
                dcc.Link([
                    dbc.Button('^', style=buttonLink_style),
                ], href='#name'),
            ], style={'margin-left': '90%'})
], style = {'justify-content': 'center'})

# FILTER CALLBACK
@app.callback(
    Output('grf_pubMhs', 'figure'),
    Input('fltrPubMhsStart', 'value'),
    Input('fltrPubMhsEnd', 'value')
)
def graphPubMhs(tglstart, tglend):
    dfPubMhs = data.getDataFrameFromDBwithParams('''
    select  tahun_ajaran 'Tahun Ajaran', 
            count(distinct fp.id_publikasi) 'Jumlah Publikasi'
    from br_pub_mahasiswa bpm
             inner join dim_publikasi dp on bpm.id_publikasi = dp.id_penelitian_pkm
             inner join fact_publikasi fp on bpm.id_publikasi = fp.id_penelitian_pkm
             inner join dim_date dd on fp.id_tanggal_publikasi = dd.id_date
             inner join dim_semester ds on ds.kode_semester = concat(tahun, if(bulan >= 7, 2, 1))
    where fp.is_deleted != 1 and (tahun_ajaran between %(start)s and %(end)s)
    group by tahun_ajaran
    order by tahun_ajaran desc;
    ''', {'start': tglstart, 'end': tglend})
    figPubMhs = px.line(dfPubMhs, x=dfPubMhs['Tahun Ajaran'], y=dfPubMhs['Jumlah Publikasi'])
    figPubMhs.update_traces(mode='lines+markers')
    return figPubMhs


@app.callback(
    Output('grf_ttguMhs', 'figure'),
    Input('fltrTTGUMhsStart', 'value'),
    Input('fltrTTGUMhsEnd', 'value')
)
def graphPPMhs(tglstart, tglend):
    dfTTGUMhs = data.getDataFrameFromDBwithParams('''
    select tahun 'Tahun',
            count(distinct dll.id_penelitian_pkm) 'Jumlah Judul'
    from dim_luaran_lainnya dll
             inner join fact_luaran_lainnya fll on dll.id_penelitian_pkm = fll.id_penelitian_pkm
             inner join dim_jenis_luaran djl on dll.id_jenis_luaran = djl.id_jenis_luaran
             inner join br_ll_mahasiswa blm on dll.id_luaran_lainnya = blm.id_luaran_lainnya
             inner join dim_date dd on dd.id_date=dll.id_tanggal_luaran
    where keterangan_jenis_luaran='TEKNOLOGI TEPAT GUNA' 
        and (tahun between %(start)s and %(end)s)
    group by tahun
    order by tahun desc;
    ''', {'start': tglstart, 'end': tglend})
    figTTGUMhs = px.line(dfTTGUMhs, x=dfTTGUMhs['Tahun'], y=dfTTGUMhs['Jumlah Judul'])
    figTTGUMhs.update_traces(mode='lines+markers')
    return figTTGUMhs


@app.callback(
    Output('grf_hkiMhs', 'figure'),
    Input('fltrHKIMhsStart', 'value'),
    Input('fltrHKIMhsEnd', 'value')
)
def graphHKIMhs(tglstart, tglend):
    dfHKIMhs = data.getDataFrameFromDBwithParams('''
    select tahun 'Tahun', count(distinct fll.id_luaran_lainnya) 'Jumlah Judul'
    from br_ll_mahasiswa blm
             inner join fact_luaran_lainnya fll on blm.id_luaran_lainnya = fll.id_luaran_lainnya
             inner join dim_luaran_lainnya dll on blm.id_luaran_lainnya = dll.id_luaran_lainnya
             inner join dim_date dd on dd.id_date = fll.id_tanggal_luaran
    where no_haki is not null and (tahun between %(start)s and %(end)s)
    group by tahun
    order by tahun desc;
    ''',{'start':tglstart, 'end':tglend})
    fig = px.line(dfHKIMhs, x=dfHKIMhs['Tahun'], y=dfHKIMhs['Jumlah Judul'])
    fig.update_traces(mode='lines+markers')
    return fig

@app.callback(
    Output('grf_reTelitiDosen', 'figure'),
    Output('grf_rePubDosen', 'figure'),
    Input('fltrRerataStart', 'value'),
    Input('fltrRerataEnd', 'value')
)
def graphRerata(tglstart, tglend):
    dfPenDs = data.getDataFrameFromDBwithParams('''
    select pp.tahun Tahun, pp.jumlah 'Jumlah Judul', dosen.jumlah 'Jumlah Dosen', round(pp.jumlah/dosen.jumlah) Rerata
    from (select dd.tahun tahun, count(bpd.id_penelitian_pkm) jumlah
          from br_pp_dosen bpd
                   inner join dim_penelitian_pkm dpp on bpd.id_penelitian_pkm = dpp.id_penelitian_pkm
                   inner join dim_date dd on dpp.id_tanggal_selesai = dd.id_date
          where bpd.jenis = 'Penelitian'
          group by dd.tahun) pp,
         (select dd.tahun tahun, count(distinct bpd.id_dosen) jumlah
          from br_pp_dosen bpd
                inner join dim_penelitian_pkm dpp on bpd.id_penelitian_pkm = dpp.id_penelitian_pkm
                inner join dim_date dd on dpp.id_tanggal_selesai = dd.id_date
                inner join dim_dosen dd2 on bpd.id_dosen=dd2.id_dosen
          where bpd.jenis = 'Penelitian'
          group by dd.tahun)dosen
    where pp.tahun=dosen.tahun and (pp.tahun between %(Start)s and %(End)s)
    group by pp.tahun, pp.jumlah, dosen.jumlah, `Rerata`
    order by pp.tahun;''', {'Start': tglstart, 'End': tglend})
    figPenDs = px.line(dfPenDs, x=dfPenDs['Tahun'], y=dfPenDs['Rerata'], color=px.Constant('Penelitian /Dosen'))
    figPenDs.update_traces(mode='lines+markers')
    figPenDs.add_bar(x=dfPenDs['Tahun'], y=dfPenDs['Jumlah Judul'], name='Penelitian')

    dfPubDs = data.getDataFrameFromDBwithParams('''
    select dd.tahun Tahun, count(distinct dp.id_publikasi) 'Jumlah Judul'
    from br_pp_publikasi bpp
             inner join dim_publikasi dp on bpp.id_penelitian_pkm = dp.id_penelitian_pkm
             inner join dim_date dd on dp.tahun_publikasi = dd.tahun
    where dd.tahun and (dd.tahun between %(Start)s and %(End)s)
    group by dd.tahun''', {'Start': tglstart, 'End': tglend})
    figPubDs = px.bar(dfPubDs, x=dfPubDs['Tahun'], y=dfPubDs['Jumlah Judul'])
    figPubDs.update_yaxes(categoryorder='category descending')
    figPubDs.update_layout(barmode='group')

    return figPenDs, figPubDs


# COLLAPSE CALLBACK
@app.callback(
    Output('cll_luaranPPPDosen', 'is_open'),
    Output('cll_luaranPPPDosen', 'children'),
    [Input('cll_grfhkiDs', 'n_clicks'),
     Input('cll_grfttguDs', 'n_clicks'),
     Input('cll_grfbukuDs', 'n_clicks'),
     Input('tab_luaranDosen', 'value')],
    [State('cll_luaranPPPDosen', 'is_open')]
)
def toggle_collapse(nhkids, nttguds, nbukuds, luarands, is_open):
    isiHKIDosen = dbc.Card(
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
        ),style=cardtbl_style
    )
    isiTTGUDosen = dbc.Card(
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
        ),style=cardtbl_style
    )
    isiBukuDosen = dbc.Card(
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
        ),style=cardtbl_style
    )
    if nhkids and luarands == 'HKIDosen':
        return not is_open, isiHKIDosen
    if nttguds and luarands == 'TTGUDosen':
        return not is_open, isiTTGUDosen
    if nbukuds and luarands == 'BukuDosen':
        return not is_open, isiBukuDosen
    return is_open, None


@app.callback(
    Output('cll_luaranPPPMhs', 'is_open'),
    Output('cll_luaranPPPMhs', 'children'),
    [Input('cll_grfpubMhs', 'n_clicks'),
     Input('cll_grfttguMhs', 'n_clicks'),
     Input('cll_grfhkiMhs', 'n_clicks'),
     Input('tab_luaranMhs', 'value')],
    [State('cll_luaranPPPMhs', 'is_open')]
)
def toggle_collapse(npub, nttgu, nhki, luaran, is_open):
    isiPublikasiMhs = dbc.Card(
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
        ),style=cardtbl_style
    )
    isiTTGUMhs = dbc.Card(
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
        ),style=cardtbl_style
    )
    isiHKIMhs = dbc.Card(
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
        ),style=cardtbl_style
    )
    if npub and luaran == 'pubMhs':
        return not is_open, isiPublikasiMhs
    if nttgu and luaran == 'ttguMhs':
        return not is_open, isiTTGUMhs
    if nhki and luaran == 'hkiMhs':
        return not is_open, isiHKIMhs
    return is_open, None


@app.callback(
    Output('cll_rerataPPP', 'is_open'),
    Output('cll_rerataPPP', 'children'),
    [Input('cll_grfreTelitiDosen', 'n_clicks'),
     Input('cll_grfrePubDosen', 'n_clicks'),
     Input('tab_rerataPPP', 'value')],
    [State('cll_rerataPPP', 'is_open')])
def toggle_collapse(nneliti, npub, ppp, is_open):
    isiPenelitian = dbc.Card(
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
        ),style=cardtbl_style
    ),
    isiPublikasi = dbc.Card(
        dt.DataTable(
            id='rePubDosen',
            columns=[
                {'name': i, 'id': i} for i in dfratajumlpublikasidosen.columns
            ],
            data=dfratajumlpublikasidosen.to_dict('records'),
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
    if nneliti and ppp == 'reTelitiDosen':
        return not is_open, isiPenelitian
    if npub and ppp == 'rePubDosen':
        return not is_open, isiPublikasi
    return is_open, None


# GRAPH CALLBACK
@app.callback(
    Output('grf_hkiDs', 'figure'),
    Input('grf_hkiDs', 'id')
)
def grafPubDs(id):
    df = dfluaranhkidosen
    fig = px.bar(df, x=df['Tahun'], y=df['Jumlah Judul'], color=df['Nama Dosen'])
    fig.update_layout(barmode='group')
    return fig


@app.callback(
    Output('grf_ttguDs', 'figure'),
    Input('grf_ttguDs', 'id')
)
def grafTTGUDs(id):
    df = dfluaranttgudosen
    fig = px.bar(df, x=df['Tahun'], y=df['Jumlah Judul'], color=df['Nama Dosen'])
    fig.update_layout(barmode='group')
    return fig


@app.callback(
    Output('grf_bukuDs', 'figure'),
    Input('grf_bukuDs', 'id')
)
def grafBukuDs(id):
    df = dfluaranbukudosen
    fig = px.bar(df, x=df['Tahun'], y=df['Jumlah'], color=df['Nama Dosen'])
    fig.update_layout(barmode='group')
    return fig


# @app.callback(
#     Output('grf_pubMhs', 'figure'),
#     Input('grf_pubMhs', 'id')
# )
# def grafPubMhs(id):
#     df = dfpublikasimhs
#     fig = px.line(df, x=df['Tahun Ajaran'], y=df['Jumlah Publikasi'])
#     fig.update_traces(mode='lines+markers')
#     return fig


# @app.callback(
#     Output('grf_ttguMhs', 'figure'),
#     Input('grf_ttguMhs', 'id')
# )
# def grafTTGUMhs(id):
#     df = dfttguadopsimhs
#     fig = px.line(df, x=df['Tahun'], y=df['Jumlah Judul'])
#     fig.update_traces(mode='lines+markers')
#     return fig


# @app.callback(
#     Output('grf_hkiMhs', 'figure'),
#     Input('grf_hkiMhs', 'id')
# )
# def grafHKIMhs(id):
#     df = dfluaranhkimhs
#     fig = px.line(df, x=df['Tahun'], y=df['Jumlah Judul'])
#     fig.update_traces(mode='lines+markers')
#     return fig

# @app.callback(
#     Output('grf_reTelitiDosen', 'figure'),
#     Input('grf_reTelitiDosen', 'id')
# )
# def grafReTelitiDosen(id):
#     df = dfratajumlpenelitiandosen
#     fig = px.line(df, x=df['Tahun'], y=df['Rerata'], color=px.Constant('Penelitian /Dosen'))
#     fig.update_traces(mode='lines+markers')
#     fig.add_bar(x=df['Tahun'], y=df['Jumlah Judul'], name='Penelitian')
#     return fig


# @app.callback(
#     Output('grf_rePubDosen', 'figure'),
#     Input('grf_rePubDosen', 'id')
# )
# def grafRePubDosen(id):
#     df = dfratajumlpublikasidosen
#     fig = px.bar(df, x=df['Tahun'], y=df['Jumlah Judul'])
#     fig.update_yaxes(categoryorder='category descending')
#     fig.update_layout(barmode='group')
#     return fig

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
