import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

icnBrand = 'https://www.ukdw.ac.id/wp-content/uploads/2017/10/fti-ukdw.png'

menu = dbc.CardGroup([
    dbc.Row([
        dbc.Card(
            dbc.CardLink([
                html.H5('PMB', className='card-title',
                        style={'color': 'black', 'textAlign': 'center'}),
                html.P('Penerimaan Mahasiswa Baru, Daya Tampung, Mahasiswa Aktif',
                       style={'color': 'black', 'textAlign': 'center'})
            ], href='/dashboard/pmb')
            , outline=True
            , style={'padding': '10px', 'margin': '10px', 'width': '360px'}
            , className='card bg-light mb-3'
        ),
        dbc.Card(
            dbc.CardLink([
                html.H5('KP, Skripsi, Yudisium',
                        style={'color': 'black', 'textAlign': 'center'}),
                html.P('KP Penelitian Pengabdian, Masa Studi, Jumlah Kelulusan',
                       style={'color': 'black', 'textAlign': 'center'})
            ], href='/dashboard/kp-skripsi-yudisium')
            , outline=True
            , style={'padding': '10px', 'margin': '10px', 'width': '360px'}
            , className='card bg-light mb-3'
        ),
        dbc.Card(
            dbc.CardLink([
                html.H5('Alumni',
                        style={'color': 'black', 'textAlign': 'center'}),
                html.P('Tracer Study Alumni, Tingkat Kepuasan Pengguna Lulusan.',
                       style={'color': 'black', 'textAlign': 'center'})
            ], href='/dashboard/alumni')
            , outline=True
            , style={'padding': '10px', 'margin': '10px', 'width': '360px'}
            , className='card bg-light mb-3'
        )
    ]),
    dbc.Row([
        dbc.Card(
            dbc.CardLink([
                html.H5('Registrasi KBM',
                        style={'color': 'black', 'textAlign': 'center'}),
                html.P('Registrasi Mahasiswa, Dosen Mengajar',
                       style={'color': 'black', 'textAlign': 'center'})
            ], href='/dashboard/registrasi')
            , outline=True
            , style={'padding': '10px', 'margin': '10px', 'width': '360px'}
            , className='card bg-light mb-3'
        ),
        dbc.Card(
            dbc.CardLink([
                html.H5('Kegiatan Kerjasama',
                        style={'color': 'black', 'textAlign': 'center'}),
                html.P('Kegiatan (Mahasiswa & Dosen), Kerjasama, IPK Dosen',
                       style={'color': 'black', 'textAlign': 'center'})
            ], href='/dashboard/kegiatan-kerjasama')
            , outline=True
            , style={'padding': '10px', 'margin': '10px', 'width': '360px'}
            , className='card bg-light mb-3'
        ),
        dbc.Card(
            dbc.CardLink([
                html.H5('PPP',
                        style={'color': 'black', 'textAlign': 'center'}),
                html.P('Penelitian, Pengabdian kepada Masyarakat, Publikasi',
                       style={'color': 'black', 'textAlign': 'center'})
            ], href='/dashboard/ppp')
            , outline=True
            , style={'padding': '10px', 'margin': '10px', 'width': '360px'}
            , className='card bg-light mb-3'
        )
    ])
], style={'margin-top': '50px', 'justify-content': 'center'}
)

layout = html.Div([
    menu
])
