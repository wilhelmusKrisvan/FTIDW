import dash
import pandas as pd
import dash_table as dt
import plotly.express as px
import dash_bootstrap_components as dbc
from apps import pmb, registrasi, kegiatan_kerjasama, tgsakhir, alumni, ppp
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from appConfig import app, server
from dash import html, dcc

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

dfmasatunggu = pd.read_sql('''
select data2.*, lulusan.jumlah as "Lulusan", terlacak.jumlah as "Lulusan Terlacak" from
 (
    select tahun_lulus,
    SUM(IF( waktu_tunggu = "KURANG 6 BULAN", data.jumlah, 0)) AS "<6 BULAN",
    SUM(IF( waktu_tunggu = "6 - 18 BULAN", data.jumlah, 0)) AS "6-18 BULAN",
    SUM(IF( waktu_tunggu = "LEBIH 18 BULAN", data.jumlah, 0)) AS ">18 BULAN",
    SUM(IF( waktu_tunggu = "LAINNYA", data.jumlah, 0)) AS "LAINNYA"
    from (
        select count(*) as jumlah, ifnull(waktu_tunggu,"LAINNYA") as waktu_tunggu,tahun_lulus
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
)lulusan on lulusan.tahun_lulus = data2.tahun_lulus
left join(
    select count(id_mahasiswa) as jumlah, tahun_lulus
    from dim_lulusan
    group by tahun_lulus
)terlacak on terlacak.tahun_lulus = data2.tahun_lulus
order by tahun_lulus;''', con)

dfbidangkerja = pd.read_sql('''
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
order by data2.tahun_lulus
''', con)

dftempatkerja = pd.read_sql('''
 select data2.tahun_lulus as 'Tahun Lulus', Lokal+Regional as 'Lokal/Regional', Nasional, Internasional, lulusan.jumlah as "Lulusan", terlacak.jumlah as "Lulusan Terlacak" from
 (
    select tahun_lulus,
    SUM(IF( wilayah = 1, data.jumlah, 0)) AS "Lokal",
    SUM(IF( wilayah = 2, data.jumlah, 0)) AS "Regional",
    SUM(IF( wilayah = 3, data.jumlah, 0)) AS "Nasional",
    SUM(IF( wilayah = 4, data.jumlah, 0)) AS "Internasional"
    from
    (
        select tahun_lulus,count(*) jumlah, wilayah
        from fact_tracer_study tracer
        inner join dim_lulusan on tracer.id_lulusan = dim_lulusan.id_lulusan
        inner join dim_organisasi_pengguna_lulusan org on dim_lulusan.id_organisasi_pengguna_lulusan = org.id_organisasi_pengguna_lulusan
        group by tahun_lulus,wilayah
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
    group by tahun_lulus
)terlacak on terlacak.tahun_lulus = data2.tahun_lulus
order by terlacak.tahun_lulus
''', con)

dfskill = pd.read_sql('''
select kriteria as Kriteria, 
    SANGATBAIK+BAIK+CUKUP+KURANG+LAINNYA as Jumlah, 
    concat(round(SANGATBAIK/(SANGATBAIK+BAIK+CUKUP+KURANG)*100,2),'%') as "Sangat Baik",
    concat(round(BAIK/(SANGATBAIK+BAIK+CUKUP+KURANG)*100,2),'%') as "Baik",
    concat(round(CUKUP/(SANGATBAIK+BAIK+CUKUP+KURANG)*100,2),'%') as "Cukup",
    concat(round(KURANG/(SANGATBAIK+BAIK+CUKUP+KURANG)*100,2),'%') as "Kurang"
    
    from (
    select "1" as nomor, "INTEGRITAS" as kriteria, 
    sum(case when integritas = "SANGAT BAIK" then jumlah end) as "SANGATBAIK",
    sum(case when integritas = "BAIK" then jumlah end) as "BAIK",
    sum(case when integritas = "CUKUP" then jumlah end) as "CUKUP",
    sum(case when integritas = "KURANG" then jumlah end) as "KURANG",
    sum(case when integritas = "LAINNYA" then jumlah end) as "LAINNYA"
    from(
        select ifnull(integritas, 'LAINNYA') as integritas, count(*) jumlah
        from fact_kepuasan_pengguna_lulusan fact
        inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
        group by integritas
    ) as data
    union all
    select  "2" as nomor, "KEAHLIAN BIDANG ILMU" as keahlian_bidang_ilmu, 
    sum(case when keahlian_bidang_ilmu = "SANGAT BAIK" then jumlah end) as "SANGATBAIK",
    sum(case when keahlian_bidang_ilmu = "BAIK" then jumlah end) as "BAIK",
    sum(case when keahlian_bidang_ilmu = "CUKUP" then jumlah end) as "CUKUP",
    sum(case when keahlian_bidang_ilmu = "KURANG" then jumlah end) as "KURANG",
    sum(case when keahlian_bidang_ilmu = "LAINNYA" then jumlah end) as "LAINNYA"
    from(
        select ifnull(keahlian_bidang_ilmu, 'LAINNYA') as keahlian_bidang_ilmu, count(*) jumlah
        from fact_kepuasan_pengguna_lulusan fact
        inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
        group by keahlian_bidang_ilmu
    ) as data
    union all
    select  "3" as nomor, "KEMAMPUAN BAHASA ASING" as Kriteria, 
    sum(case when kemampuan_bahasa_asing = "SANGAT BAIK" then jumlah end) as "SANGATBAIK",
    sum(case when kemampuan_bahasa_asing = "BAIK" then jumlah end) as "BAIK",
    sum(case when kemampuan_bahasa_asing = "CUKUP" then jumlah end) as "CUKUP",
    sum(case when kemampuan_bahasa_asing = "KURANG" then jumlah end) as "KURANG",
    sum(case when kemampuan_bahasa_asing = "LAINNYA" then jumlah end) as "LAINNYA"
    from(
        select ifnull(kemampuan_bahasa_asing, 'LAINNYA') as kemampuan_bahasa_asing, count(*) jumlah
        from fact_kepuasan_pengguna_lulusan fact
        inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
        group by kemampuan_bahasa_asing
    ) as data
    union all
    select  "4" as nomor,  "PENGGUNAAN TEKNOLOGI INFORMASI" as Kriteria, 
    sum(case when penggunaan_teknologi = "SANGAT BAIK" then jumlah end) as "SANGATBAIK",
    sum(case when penggunaan_teknologi = "BAIK" then jumlah end) as "BAIK",
    sum(case when penggunaan_teknologi = "CUKUP" then jumlah end) as "CUKUP",
    sum(case when penggunaan_teknologi = "KURANG" then jumlah end) as "KURANG",
    sum(case when penggunaan_teknologi = "LAINNYA" then jumlah end) as "LAINNYA"
    from(
        select ifnull(penggunaan_teknologi, 'LAINNYA') as penggunaan_teknologi, count(*) jumlah
        from fact_kepuasan_pengguna_lulusan fact
        inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
        group by penggunaan_teknologi
    ) as data
    union all
    select  "5" as nomor,  "KOMUNIKASI" as komunikasi, 
    sum(case when komunikasi = "SANGAT BAIK" then jumlah end) as "SANGATBAIK",
    sum(case when komunikasi = "BAIK" then jumlah end) as "BAIK",
    sum(case when komunikasi = "CUKUP" then jumlah end) as "CUKUP",
    sum(case when komunikasi = "KURANG" then jumlah end) as "KURANG",
    sum(case when komunikasi = "LAINNYA" then jumlah end) as "LAINNYA"
    from(
        select ifnull(komunikasi, 'LAINNYA') as komunikasi, count(*) jumlah
        from fact_kepuasan_pengguna_lulusan fact
        inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
        group by komunikasi
    ) as data
    union all
    select  "6" as nomor, "KERJASAMA TIM" as kerjasama_tim, 
    sum(case when kerjasama_tim = "SANGAT BAIK" then jumlah end) as "SANGATBAIK",
    sum(case when kerjasama_tim = "BAIK" then jumlah end) as "BAIK",
    sum(case when kerjasama_tim = "CUKUP" then jumlah end) as "CUKUP",
    sum(case when kerjasama_tim = "KURANG" then jumlah end) as "KURANG",
    sum(case when kerjasama_tim = "LAINNYA" then jumlah end) as "LAINNYA"
    from(
        select ifnull(kerjasama_tim, 'LAINNYA') as kerjasama_tim, count(*) jumlah
        from fact_kepuasan_pengguna_lulusan fact
        inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
        group by kerjasama_tim
    ) as data
    union all
    select "7" as nomor, "PENGEMBANGAN DIRI" as Kriteria, 
    sum(case when pengembangan_diri = "SANGAT BAIK" then jumlah end) as "SANGATBAIK",
    sum(case when pengembangan_diri = "BAIK" then jumlah end) as "BAIK",
    sum(case when pengembangan_diri = "CUKUP" then jumlah end) as "CUKUP",
    sum(case when pengembangan_diri = "KURANG" then jumlah end) as "KURANG",
    sum(case when pengembangan_diri = "LAINNYA" then jumlah end) as "LAINNYA"
    from(
        select ifnull(pengembangan_diri, 'LAINNYA') as pengembangan_diri, count(*) jumlah
        from fact_kepuasan_pengguna_lulusan fact
        inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
        group by pengembangan_diri
    ) as data
) dataJumlah
order by nomor
''', con)

dfjabatan = pd.read_sql('''
select 
count(*) as Jumlah, 
ifnull(posisi_jabatan_alumni,'LAINNYA') as Posisi, 
posisi_jabatan_alumni as 'Jabatan Alumni'
from fact_tracer_study tracer
inner join dim_lulusan on dim_lulusan.id_lulusan = tracer.id_lulusan
where dim_lulusan.tahun_lulus='2015'
group by posisi, posisi_jabatan_alumni
order by posisi_jabatan_alumni desc
''', con)

dfperusahaan = pd.read_sql('''
select nama_mapping_organisasi as 'Nama Perusahaan', count(*) as 'Jumlah Lulusan'
from fact_tracer_study tracer
inner join dim_lulusan on tracer.id_lulusan = dim_lulusan.id_lulusan
inner join dim_organisasi_pengguna_lulusan org on dim_lulusan.id_organisasi_pengguna_lulusan = org.id_organisasi_pengguna_lulusan
where dim_lulusan.tahun_lulus='2015'
group by nama_mapping_organisasi
order by 'Jumlah Lulusan' desc
limit 15
''',con)

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

tab_alumni = html.Div([
    html.Div(
        html.H5(
            'Analisis Lulusan dan Tracer Study Prodi Informatika',
            style={'margin-top': '30px', 'text-align': 'center'}
        )
    ),
    masatunggu,
    bidangkerja,
    tempatkerja,
    kemampuan,
    jabatan,
    perusahaan
])

tab_fasilitas = html.Div([
    html.Div(
        html.H5(
            'Analisis Kepuasan Lulusan terhadap Fasilitas dan Layanan Prodi Informatika',
            style={'margin-top': '30px', 'text-align': 'center'}
        )
    ),
])

layout = html.Div([
    dbc.Container([
        html.Div(html.H4('Analisis Lulusan, Tracer Study, Kepuasan Fasilitas dan Layanan',
                         style={'margin-top': '30px', 'textAlign': 'center'}
                         )
                 ),
        dbc.Tabs([
            dbc.Tab(label='Alumni', tab_id='alumni', style=tabs_styles),
            dbc.Tab(label='Fasilitas & Layanan', tab_id='fasilitas',style=tabs_styles)
        ], active_tab='alumni', id='cardTabsAlumni',style=tabs_styles),
        html.Div([], id='cardContentAlumni')
    ], fluid=True, style=cardgrf_style),
])


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
    Output('cardContentAlumni', 'children'),
    [Input("cardTabsAlumni", "active_tab")]
)
def tab_contentRegistrasi(active_tab):
    if active_tab == 'alumni':
        return tab_alumni
    if active_tab == 'fasilitas':
        return tab_fasilitas
