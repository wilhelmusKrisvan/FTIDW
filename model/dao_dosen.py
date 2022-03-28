import pandas as pd
from sqlalchemy import create_engine

con = create_engine('mysql+pymysql://admin:admin@localhost:3333/ftidw')
# con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')
# con = create_engine('mysql+pymysql://user1:Ul0HenorahF1oyeo@localhost:3333/datawarehouse_dev')


def getDataFrameFromDB(query):
    return pd.read_sql(query, con)


def getDataFrameFromDBwithParams(query, parameter):
    return pd.read_sql(query, con, params=parameter)


# def getDosenS3():
#     return pd.read_sql('''
#     select data.Jumlah 'S3',dosen.Jumlah 'Jumlah Dosen',(data.Jumlah/dosen.Jumlah)*100 'persentase' from
#     (select count(*) Jumlah,cast(2021 as char) tahun  from (
#         select dim_dosen.id_dosen, nama, max(tingkat_pendidikan) tingkat_pendidikan from fact_pendidikan_dosen
#         inner join dim_dosen on dim_dosen.id_dosen = fact_pendidikan_dosen.id_dosen
#         where id_prodi = 9 and status_Dosen = 'Tetap' and tingkat_pendidikan='S3'
#         group by dim_dosen.id_dosen, nama
#         order by nama
#     ) data) data,
#         (select sum(Jumlah) as Jumlah,cast(2021 as char) as tahun from
#         (select count(*) as Jumlah,year(tanggal_masuk) as tahun
#         from dim_dosen
#         where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
#         group by tahun) data
#         where data.tahun<=2020) dosen
#     where dosen.tahun=data.tahun''', con)

def getDosenS3():
    return pd.read_sql('''
    select dim_dosen.id_dosen, nama, max(tingkat_pendidikan) tingkat_pendidikan from fact_pendidikan_dosen
        inner join dim_dosen on dim_dosen.id_dosen = fact_pendidikan_dosen.id_dosen
        where id_prodi = 9 and status_Dosen = 'Tetap' and tanggal_keluar is null
        group by dim_dosen.id_dosen, nama
        order by nama''',con)


def getJabfungperTahun():
    return pd.read_sql('''
    select jabatan.tahun Tahun,jabatan.Jumlah 'Jumlah Pejabat', dosen.Jumlah 'Total Dosen',(jabatan.Jumlah/dosen.Jumlah)*100 'persentase' from
    (select sum(Jumlah) as Jumlah,cast(2021 as char) as tahun from
        (select count(*) as Jumlah,year(tanggal_masuk) as tahun
        from dim_dosen
        where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
        group by tahun) data
        where data.tahun<=2021
        union all
        select sum(Jumlah) as Jumlah,cast(2020 as char) as tahun from
        (select count(*) as Jumlah,year(tanggal_masuk) as tahun
        from dim_dosen
        where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
        group by tahun) data
        where data.tahun<=2020
        union all
        select sum(Jumlah) as Jumlah,cast(2019 as char) as tahun from
        (select count(*) as Jumlah,year(tanggal_masuk) as tahun
        from dim_dosen
        where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
        group by tahun) data
        where data.tahun<=2019) dosen,
    (select count(jabatan_dosen) Jumlah, tahun from dosen_jabfung_monev
    inner join dim_dosen dd on dd.id_dosen=dosen_jabfung_monev.id_dosen
    where ( jabatan_dosen like "L%%") and tahun>=2019 and id_prodi=9
    group by tahun) jabatan
    where jabatan.tahun=dosen.tahun
    order by tahun desc''', con)



def getPersenJabfungAkumulasiperTahun():
    return pd.read_sql('''
    select jabatan.tahun Tahun,jabatan.Jumlah 'Jumlah Jabatan', 
    dosen.Jumlah 'Jumlah Dosen',(jabatan.Jumlah/dosen.Jumlah)*100 'persentase' from
    (select sum(Jumlah) as Jumlah,cast(2021 as char) as tahun from
        (select count(*) as Jumlah,year(tanggal_masuk) as tahun
        from dim_dosen
        where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
        group by tahun) data
        where data.tahun<=2021
        union all
        select sum(Jumlah) as Jumlah,cast(2020 as char) as tahun from
        (select count(*) as Jumlah,year(tanggal_masuk) as tahun
        from dim_dosen
        where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
        group by tahun) data
        where data.tahun<=2020
        union all
        select sum(Jumlah) as Jumlah,cast(2019 as char) as tahun from
        (select count(*) as Jumlah,year(tanggal_masuk) as tahun
        from dim_dosen
        where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
        group by tahun) data
        where data.tahun<=2019) dosen,
    (select count(jabatan_dosen) Jumlah, tahun from dosen_jabfung_monev
    inner join dim_dosen dd on dd.id_dosen=dosen_jabfung_monev.id_dosen
    where ( jabatan_dosen like 'L%%') and tahun>=2019 and id_prodi=9
    group by tahun) jabatan
    where jabatan.tahun=dosen.tahun
    order by tahun asc''', con)

def getPersenJabfungperTahun():
    return pd.read_sql('''
    select jabatan.tahun                         Tahun,
       jabatan.jabatan_dosen                 'Jabatan',
       jabatan.Jumlah                        'Jumlah Jabatan',
       dosen.Jumlah                          'Jumlah Dosen',
       (jabatan.Jumlah / dosen.Jumlah) * 100 'persentase'
    from (select sum(Jumlah) as Jumlah, cast(2021 as char) as tahun
          from (select count(distinct fdm.id_dosen) as Jumlah, year(tanggal_masuk) as tahun
                from dim_dosen
                         inner join fact_dosen_mengajar fdm on dim_dosen.id_dosen = fdm.id_dosen
                where status_dosen = 'Tetap'
                  and tanggal_keluar is null
                group by tahun) data
          where data.tahun <= 2021
          union all
          select sum(Jumlah) as Jumlah, cast(2020 as char) as tahun
          from (select count(distinct fdm.id_dosen) as Jumlah, year(tanggal_masuk) as tahun
                from dim_dosen
                         inner join fact_dosen_mengajar fdm on dim_dosen.id_dosen = fdm.id_dosen
                where status_dosen = 'Tetap'
                  and tanggal_keluar is null
                group by tahun) data
          where data.tahun <= 2020
          union all
          select sum(Jumlah) as Jumlah, cast(2019 as char) as tahun
          from (select count(distinct fdm.id_dosen) as Jumlah, year(tanggal_masuk) as tahun
                from dim_dosen
                         inner join fact_dosen_mengajar fdm on dim_dosen.id_dosen = fdm.id_dosen
                where status_dosen = 'Tetap'
                  and tanggal_keluar is null
                group by tahun) data
          where data.tahun <= 2019) dosen,
         (select jabatan_dosen,count(jabatan_dosen) Jumlah, tahun
          from dosen_jabfung_monev
                   inner join dim_dosen dd on dd.id_dosen = dosen_jabfung_monev.id_dosen
          where (jabatan_dosen like 'L%%')
            and tahun >= 2019
            and id_prodi = 9
          group by jabatan_dosen,tahun) jabatan
    where jabatan.tahun = dosen.tahun
    group by Tahun, Jabatan, `Jumlah Jabatan`, `Jumlah Dosen`, `persentase`
    order by Tahun desc;
    ''',con)


def getDosenTetapINF():
    return pd.read_sql('''
    select nama, nik, nomor_induk,
    tipe_nomor_induk,jenis_kelamin,
    no_sertifikat, status_yayasan from dim_dosen
    where id_prodi = 9 and status_dosen = "TETAP" and tanggal_keluar is null
    order by nama''', con)

# keknya ini belom bener
def getDosenIndustriPraktisi():
    return pd.read_sql(''' select nama, nik, kode_dosen, 
    jenis_kelamin,no_sertifikat,status_dosen,
    status_dikti,status_yayasan
    from dim_dosen
    where is_praktisi="1"
    order by nama''',con)
