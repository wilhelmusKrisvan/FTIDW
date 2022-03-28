from dash import html
import dash_bootstrap_components as dbc

icnBrand = 'https://www.ukdw.ac.id/wp-content/uploads/2017/10/fti-ukdw.png'

title_style = {
    'font-family': 'Nunito',
    'font-weight':'600',
    'color': 'black',
    'textAlign': 'center'
}

desc_style = {
    'color': 'black',
    'textAlign': 'center'
}

# menuu = dbc.CardGroup([
#     dbc.Row([
#         dbc.Card(
#             dbc.CardLink([
#                 html.H5('PMB', className='card-title',
#                         style=title_style),
#                 html.P('Penerimaan Mahasiswa Baru, Daya Tampung, Mahasiswa Aktif',
#                        style=desc_style)
#             ], href='/dashboard/pmb')
#             , outline=True
#             , id='card_menu'
#         ),
#         dbc.Card(
#             dbc.CardLink([
#                 html.H5('KP, Skripsi, Yudisium',
#                         style=title_style),
#                 html.P('KP Penelitian Pengabdian, Masa Studi, Jumlah Kelulusan',
#                        style=desc_style)
#             ], href='/dashboard/kp-skripsi-yudisium')
#             , outline=True
#             , id='card_menu'
#         ),
#         dbc.Card(
#             dbc.CardLink([
#                 html.H5('Alumni',
#                         style=title_style),
#                 html.P('Tracer Study Alumni, Tingkat Kepuasan Pengguna Lulusan.',
#                        style=desc_style)
#             ], href='/dashboard/alumni')
#             , outline=True
#             , id='card_menu'
#         )
#     ]),
#     dbc.Row([
#         dbc.Card(
#             dbc.CardLink([
#                 html.H5('Registrasi KBM',
#                         style=title_style),
#                 html.P('Registrasi Mahasiswa, Dosen Mengajar',
#                        style=desc_style)
#             ], href='/dashboard/registrasi')
#             , outline=True
#             , id='card_menu'
#         ),
#         dbc.Card(
#             dbc.CardLink([
#                 html.H5('Kegiatan Kerjasama',
#                         style=title_style),
#                 html.P('Kegiatan (Mahasiswa & Dosen), Kerjasama, IPK Dosen',
#                        style=desc_style)
#             ], href='/dashboard/kegiatan-kerjasama')
#             , outline=True
#             , id='card_menu'
#         ),
#         dbc.Card(
#             dbc.CardLink([
#                 html.H5('PPP',
#                         style=title_style),
#                 html.P('Penelitian, Pengabdian kepada Masyarakat, Publikasi',
#                        style=desc_style)
#             ], href='/dashboard/ppp')
#             , outline=True
#             , id='card_menu'
#         ),
#         dbc.Card(
#             dbc.CardLink([
#                 html.H5('PPP',
#                         style=title_style),
#                 html.P('Penelitian, Pengabdian kepada Masyarakat, Publikasi',
#                        style=desc_style)
#             ], href='/dashboard/ppp')
#             , outline=True
#             , id='card_menu'
#         )
#     ])
# ], style={'justify-content': 'center'})

menu = dbc.CardGroup([
    dbc.Row([
        dbc.Card(
            dbc.CardLink([
                html.H5('PMB', className='card-title',
                        style=title_style),
                html.P('Penerimaan Mahasiswa Baru, Daya Tampung, Mahasiswa Aktif',
                       style=desc_style)
            ], href='/dashboard/pmb')
            , outline=True
            , id='card_menu'
        ),
        dbc.Card(
            dbc.CardLink([
                html.H5('Registrasi KBM',
                        style=title_style),
                html.P('Registrasi Mahasiswa, Dosen Mengajar',
                       style=desc_style)
            ], href='/dashboard/registrasi')
            , outline=True
            , id='card_menu'
        ),
        dbc.Card(
            dbc.CardLink([
                html.H5('MBKM',
                        style=title_style),
                html.P('Merdeka Belajar Kampus Merdeka',
                       style=desc_style)
            ], href='/dashboard/mbkm')
            , outline=True
            , id='card_menu'
        ),
        dbc.Card(
            dbc.CardLink([
                html.H5('KP, Skripsi, Yudisium',
                        style=title_style),
                html.P('KP Penelitian Pengabdian, Masa Studi, Jumlah Kelulusan',
                       style=desc_style)
            ], href='/dashboard/kp-skripsi-yudisium')
            , outline=True
            , id='card_menu'
        )
    ]),
    dbc.Row([
        dbc.Card(
            dbc.CardLink([
                html.H5('Kegiatan Kerjasama',
                        style=title_style),
                html.P('Kegiatan (Mahasiswa & Dosen), Kerjasama, IPK Dosen',
                       style=desc_style)
            ], href='/dashboard/kegiatan-kerjasama')
            , outline=True
            , id='card_menu'
        ),
        dbc.Card(
            dbc.CardLink([
                html.H5('PPP & Luaran',
                        style=title_style),
                html.P('Penelitian, Pengabdian kepada Masyarakat, Publikasi dan Luaran',
                       style=desc_style)
            ], href='/dashboard/ppp')
            , outline=True
            , id='card_menu'
        ),
        dbc.Card(
            dbc.CardLink([
                html.H5('Dosen',
                        style=title_style),
                html.P('Profil Dosen Fakultas Teknologi Informasi',
                       style=desc_style)
            ], href='/dashboard/profil-dosen')
            , outline=True
            , id='card_menu'
        ),
        dbc.Card(
            dbc.CardLink([
                html.H5('Alumni',
                        style=title_style),
                html.P('Tracer Study Alumni, Tingkat Kepuasan Pengguna Lulusan.',
                       style=desc_style)
            ], href='/dashboard/alumni')
            , outline=True
            , id='card_menu'
        )
    ])
], style={'justify-content': 'center'})

layout = html.Div([
    menu
], style={'height': '75vh', 'align-items': 'center', 'display': 'flex', 'justify-content': 'center'})
