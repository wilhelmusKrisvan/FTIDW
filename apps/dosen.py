import dash
import pandas as pd
import dash_table as dt
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from apps import pmb, kbm, kegiatan_kerjasama, tgsakhir, alumni, ppp
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from appConfig import app, server
from dash import html, dcc
import model.dao_dosen as data

dfpersendosens3 = data.getDosenS3()

dfpersenjabfungAkumulasi = data.getPersenJabfungAkumulasiperTahun()
dfpersenjabfung = data.getPersenJabfungperTahun()
dfdosentetapinf = data.getDosenTetapINF()
dfdosenindustri = data.getDosenIndustriPraktisi()

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

DosenInduk = dbc.Container([
    dbc.Card([
        html.H5('Dosen Informatika Nomor Induk',
                style=ttlgrf_style),
        dbc.CardBody([
            dcc.Loading([
                dcc.Graph(id='grf_DosenTetapInfInduk'),
            ], type='default'),
            dbc.Button('Lihat Semua Data', id='cll_grfDosenTetapInfInduk', n_clicks=0,
                       style=button_style),
        ]),
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_tblDosenTetapInfInduk',
        is_open=False,
    )
], style=cont_style)

DosenSertif = dbc.Container([
    dbc.Card([
        html.H5('Dosen Informatika Bersertifikat',
                style=ttlgrf_style),
        dbc.CardBody([
            dcc.Loading([
                dcc.Graph(id='grf_DosenTetapInfSertif'),
            ], type='default'),
            dbc.Button('Lihat Semua Data', id='cll_grfDosenTetapInfSertif', n_clicks=0,
                       style=button_style),
        ]),
    ], style=cardgrf_style),
    dbc.Collapse(
        id='cll_tblDosenTetapInfSertif',
        is_open=False,
    )
], style=cont_style)


dosentetapindustri = dbc.Container([
    dbc.Card([
        html.H5('Daftar Dosen Industri Praktisi',
                style=ttlgrf_style),
        dbc.Card([
            dt.DataTable(
                id='tbl_dosenindustriinf',
                columns=[{"name": i, "id": i} for i in dfdosenindustri.columns],
                data=dfdosenindustri.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                page_size=10,
                export_format='xlsx'
            ),
        ], style=cardtbl_style),
    ], style=cardgrf_style),
], style=cont_style)

jumljabfungDosen = dbc.Container([
    dbc.Card([
        html.H5('Perbandingan Dosen Jabatan Fungsi dengan Dosen Non Jabatan Fungsi per Tahun',
                style=ttlgrf_style),
        dbc.CardBody([
            dcc.Loading([
                dcc.Graph(id='grf_jabfungth'),
            ], type='default'),
            dbc.Button('Lihat Semua Data',
                       id='cll_grfjabfungth',
                       n_clicks=0, style=button_style
                       ),
        ]),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_jabfungth',
                columns=[{"name": i, "id": i} for i in dfpersenjabfungAkumulasi.columns],
                data=dfpersenjabfungAkumulasi.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                page_size=10,
                export_format='xlsx'
            ), style=cardtbl_style
        ),
        id='cll_tbljabfungth',
        is_open=False
    )
], style=cont_style)

persenjabfungthDosen = dbc.Container([
    dbc.Card([
        html.H5('Jumlah Jabatan Fungsi Dosen per Tahun',
                style=ttlgrf_style),
        dbc.CardBody([
            dcc.Loading([
                dcc.Graph(id='grf_persenjabfungth'),
            ], type='default'),
            dbc.Button('Lihat Semua Data',
                       id='cll_grfpersenjabfungth',
                       n_clicks=0, style=button_style
                       ),
        ]),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card([
            dt.DataTable(
                id='tbl_persenjabfungth',
                columns=[{"name": i, "id": i} for i in dfpersenjabfung.columns],
                data=dfpersenjabfung.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                page_size=10,
                export_format='xlsx'
            ),
        ], style=cardgrf_style),
        id='cll_tblpersenjabfungth',
        is_open=False
    )
], style=cont_style)

dosens3 = dbc.Container([
    dbc.Card([
        html.H5('Dosen S3',
                style=ttlgrf_style),
        dbc.CardBody([
            dcc.Loading([
                dcc.Graph(id='grf_dosens3'),
            ], type='default'),
            dbc.Button('Lihat Semua Data',
                       id='cll_grfdosens3',
                       n_clicks=0, style=button_style
                       ),
        ]),
    ], style=cardgrf_style),
    dbc.Collapse(
        dbc.Card(
            dt.DataTable(
                id='tbl_dosens3',
                columns=[{"name": i, "id": i} for i in dfpersendosens3.columns],
                data=dfpersendosens3.to_dict('records'),
                sort_action='native',
                sort_mode='multi',
                style_table={'width': '100%', 'padding': '10px', 'overflowX': 'auto', 'margin-top': '25px'},
                style_header={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                style_data={'border': 'none', 'font-size': '80%', 'textAlign': 'center'},
                page_size=10,
                export_format='xlsx'
            ), style=cardgrf_style
        ),
        id='cll_tbldosens3',
        is_open=False
    )
], style=cont_style)




layout = html.Div([
    html.Div(html.H1('Analisis Profil Dosen Prodi Informatika',
                     style={'margin-top': '30px', 'textAlign': 'center'}
                     )
             ),
    html.A(className='name'),
    html.Div([DosenInduk]),
    html.Div([DosenSertif]),
    html.Div([dosentetapindustri]),
    html.Div([jumljabfungDosen]),
    html.Div([persenjabfungthDosen]),
    html.Div([dosens3], style={'margin-bottom': '50px'}),
    dbc.Container([
        dcc.Link([
            dbc.Button('^', style=buttonLink_style),
        ], href='#name'),
    ], style={'margin-left': '90%'}),
], style={'justify-content': 'center'})


# CONTROL COLLAPSE
@app.callback(
    Output("cll_tblDosenTetapInfInduk", "is_open"),
    Output("cll_tblDosenTetapInfInduk", "children"),
    [Input("cll_grfDosenTetapInfInduk", "n_clicks"), ],
    [State("cll_tblDosenTetapInfInduk", "is_open")])
def toggle_collapse(ninduk, is_open):
    isiDosenTetap = dbc.Card(
        dt.DataTable(
            id='tbl_dosentetapinf',
            columns=[
                {'name': i, 'id': i} for i in dfdosentetapinf.columns
            ],
            data=dfdosentetapinf.to_dict('records'),
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
    if ninduk:
        return not is_open, isiDosenTetap
    return is_open, None


@app.callback(
    Output("cll_tblDosenTetapInfSertif", "is_open"),
    Output("cll_tblDosenTetapInfSertif", "children"),
    Input("cll_grfDosenTetapInfSertif", "n_clicks"),
    [State("cll_tblDosenTetapInfSertif", "is_open")])
def toggle_collapse(nsertif, is_open):
    isiDosenTetap = dbc.Card(
        dt.DataTable(
            id='tbl_dosentetapinf',
            columns=[
                {'name': i, 'id': i} for i in dfdosentetapinf.columns
            ],
            data=dfdosentetapinf.to_dict('records'),
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
    if nsertif:
        return not is_open, isiDosenTetap
    return is_open, None

@app.callback(
    Output("cll_tbljabfungth", "is_open"),
    [Input("cll_grfjabfungth", "n_clicks")],
    [State("cll_tbljabfungth", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tblpersenjabfungth", "is_open"),
    [Input("cll_grfpersenjabfungth", "n_clicks")],
    [State("cll_tblpersenjabfungth", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("cll_tbldosens3", "is_open"),
    [Input("cll_grfdosens3", "n_clicks")],
    [State("cll_tbldosens3", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# GRAPH COLLAPSE
@app.callback(
    Output('grf_DosenTetapInfInduk', 'figure'),
    Input('grf_DosenTetapInfInduk', 'id')
)
def graphDosenInfInduk(id):
    df = data.getDataFrameFromDB('''
    select count(nomor_induk) Jumlah,
    tipe_nomor_induk 'Tipe Nomor Induk' from dim_dosen
    where id_prodi = 9 and status_dosen = "TETAP" and tanggal_keluar is null
    group by tipe_nomor_induk
    ''')
    if (len(df['Jumlah']) != 0):
        fig = px.bar(df, y=df['Jumlah'], x=df['Tipe Nomor Induk'], color=df['Tipe Nomor Induk'])
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


@app.callback(
    Output('grf_DosenTetapInfSertif', 'figure'),
    Input('grf_DosenTetapInfSertif', 'id')
)
def graphDosenInfSertif(id):
    df = data.getDataFrameFromDB('''
    select count(no_sertifikat) Jumlah, 'Sertifikat' as 'Tipe Sertifikat'
    from dim_dosen
    where id_prodi = 9 and status_dosen = "TETAP" and tanggal_keluar is null
    and no_sertifikat is not null
    union all 
    select sum(if(no_sertifikat is null,1,0)) Jumlah, 'Non Sertifikat' as 'Tipe Sertifikat'
    from dim_dosen
    where id_prodi = 9 and status_dosen = "TETAP" and tanggal_keluar is null
    and no_sertifikat is null
    ''')
    if (len(df['Jumlah']) != 0):
        fig = px.bar(df, y=df['Jumlah'], x=df['Tipe Sertifikat'], color=df['Tipe Sertifikat'])
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig

# Jumlah Jabfung L LK per Tahun
@app.callback(
    Output('grf_jabfungth', 'figure'),
    Input('grf_jabfungth', 'id')
)
def grafJumlJabfungth(id):
    df = dfpersenjabfungAkumulasi
    count =df['Jumlah Non Jabatan'].value_counts().reset_index()
    if (len(df['Tahun']) != 0):
        fig = px.bar(df, x=df['Tahun'], y=df['Jumlah Jabatan'], color=px.Constant('Jabatan'),
                     labels=dict(x='Tahun', y='Jumlah Dosen', color='Jenis Jabatan'),
                     )
        # fig.update_traces(mode='lines+markers')
        fig.add_bar(x=df['Tahun'], y=df['Jumlah Non Jabatan'], name='Non Jabatan',
                    )
        fig.update_traces(hovertemplate="<br> Jumlah Dosen=%{y} </br> Tahun= %{x}")
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig


# Persentase Jabfung L LK per Tahun
@app.callback(
    Output('grf_persenjabfungth', 'figure'),
    Input('grf_persenjabfungth', 'id')
)
def grafPersenJabfungth(id):
    df = dfpersenjabfung
    if (len(df['Tahun']) != 0):
        fig = px.bar(df, x=df['Tahun'], y=df['persentase'], color=df['Jabatan'],
                     barmode='stack',)
        fig.update_xaxes(categoryorder='category ascending')
        fig.update_layout(yaxis_title="Persentase (%)")
        fig.update_traces(hovertemplate="<br> Persentase=%{y} </br> Tahun= %{x}")
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig

@app.callback(
    Output('grf_dosens3', 'figure'),
    Input('grf_dosens3', 'id')
)
def grafDosenS3(id):
    df = data.getDataFrameFromDB('''
    select count(data.id_dosen) Jumlah, data.tingkat_pendidikan "Tingkat Pendidikan" from
    (select dim_dosen.id_dosen,nama, max(tingkat_pendidikan) tingkat_pendidikan from fact_pendidikan_dosen
        inner join dim_dosen on dim_dosen.id_dosen = fact_pendidikan_dosen.id_dosen
        where id_prodi = 9 and status_Dosen = 'Tetap' and tanggal_keluar is null 
        and year(tanggal_masuk)<=year(now())
        group by dim_dosen.id_dosen, nama
        order by nama) data
        group by tingkat_pendidikan
        ''')
    if (len(df['Jumlah']) != 0):
        fig = px.pie(df, values=df['Jumlah'], names=df['Tingkat Pendidikan'])
        return fig
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig