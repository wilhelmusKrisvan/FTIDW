import pandas as pd
from sqlalchemy import create_engine


con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

def getDataFrameFromDB(query):
    return pd.read_sql(query,con)

def getDataFrameFromDBwithParams(query,parameter):
    return pd.read_sql(query,con,params=parameter)

def getKegiatanDosen():
    return pd.read_sql('''select tahun, nama,count(fkd.id_dosen) 'Jumlah Kegiatan' from fact_kegiatan_dosen fkd
inner join dim_kegiatan dk on fkd.id_kegiatan = dk.id_kegiatan
inner join dim_date dd on dd.id_date=dk.id_tanggal_mulai
inner join dim_dosen d on fkd.id_dosen = d.id_dosen
group by tahun,nama
order by tahun desc, nama asc''',con)

# def getKegiatanDosen():
#     return pd.read_sql('''select nama_gelar,
# max(case when tahun = "2003" then jumlah end) as 'Thn 2003',
# max(case when tahun = "2004" then jumlah end) as 'Thn 2004',
# max(case when tahun = "2005" then jumlah end) as 'Thn 2005',
# max(case when tahun = "2006" then jumlah end) as 'Thn 2006',
# max(case when tahun = "2007" then jumlah end) as 'Thn 2007',
# max(case when tahun = "2008" then jumlah end) as 'Thn 2008',
# max(case when tahun = "2009" then jumlah end) as 'Thn 2009',
# max(case when tahun = "2010" then jumlah end) as 'Thn 2010',
# max(case when tahun = "2011" then jumlah end) as 'Thn 2011',
# max(case when tahun = "2012" then jumlah end) as 'Thn 2012',
# max(case when tahun = "2013" then jumlah end) as 'Thn 2013',
# max(case when tahun = "2014" then jumlah end) as 'Thn 2014',
# max(case when tahun = "2015" then jumlah end) as 'Thn 2015',
# max(case when tahun = "2016" then jumlah end) as 'Thn 2016',
# max(case when tahun = "2017" then jumlah end) as 'Thn 2017',
# max(case when tahun = "2018" then jumlah end) as 'Thn 2018',
# max(case when tahun = "2019" then jumlah end) as 'Thn 2019',
# max(case when tahun = "2020" then jumlah end) as 'Thn 2020'
# from (
#     select nama_gelar, tahun, count(*) as jumlah
#     from fact_rekognisi_dosen
#     inner join dim_date on dim_date.id_date = fact_rekognisi_dosen.id_tanggal_mulai
#     inner join dim_dosen on dim_dosen.id_dosen = fact_rekognisi_dosen.id_dosen
#     where id_prodi = 9
#     group by nama_gelar, tahun
#     order by nama_gelar, tahun
# ) data
# group by nama_gelar
# order by nama_gelar''', con)

def getPrestasiRekognisiDosen():
    return pd.read_sql('''
    select nama,tahun,judul_rekognisi,
       case
           when wilayah=1 then 'Regional'
           when wilayah=2 then 'Nasional'
           when wilayah=3 then 'ASEAN'
           when wilayah=4 then 'Internasional'
       end as Wilayah
        from fact_rekognisi_dosen frd
inner join dim_date dd on dd.id_date=frd.id_tanggal_mulai
inner join dim_dosen d on frd.id_dosen = d.id_dosen
group by nama,tahun, judul_rekognisi, wilayah
order by tahun desc''',con)

def getPrestasiAkademik():
    return pd.read_sql('''select  nama_kegiatan, tahun, 
    if(wilayah_nama='LOKAL','v','') as Lokal,
    if(wilayah_nama='REGIONAL','v','') as Regional,
    if(wilayah_nama='NASIONAL','v','') as Nasional,
    if(wilayah_nama='INTERNASIONAL','v','') as Internasional,
prestasi from(
    select distinct nama_kegiatan, tahun, fact.wilayah_nama, replace(jenis_partisipasi, 'L', 'I') as prestasi
    from fact_kegiatan_mahasiswa fact
    inner join dim_kegiatan keg on keg.id_kegiatan = fact.id_kegiatan
    inner join dim_date dat on keg.id_tanggal_mulai = dat.id_date
    where sifat_partisipasi = 'PM' and is_akademis = 1
) data 
order by tahun, nama_kegiatan''',con)

def getPrestasiNonAkademik():
    return pd.read_sql('''select nama_kegiatan, tahun, 
    if(wilayah_nama='LOKAL','v','') as Lokal,
    if(wilayah_nama='REGIONAL','v','') as Regional,
    if(wilayah_nama='NASIONAL','v','') as Nasional,
    if(wilayah_nama='INTERNASIONAL','v','') as Internasional,
prestasi from(
    select distinct nama_kegiatan, tahun, fact.wilayah_nama, replace(jenis_partisipasi, 'L', 'I') as prestasi
    from fact_kegiatan_mahasiswa fact
    inner join dim_kegiatan keg on keg.id_kegiatan = fact.id_kegiatan
    inner join dim_date dat on keg.id_tanggal_mulai = dat.id_date
    where sifat_partisipasi = 'PM' and is_akademis = 0
) data 
order by tahun''', con)

def getKegKulUmMOU():
    return pd.read_sql('''
    select ddselesai.tahun, count(dim_kegiatan.nama_kegiatan) as jumlah_kuliah_umum
     -- , ddmulai.tanggal as tanggal_mulai, ddselesai.tanggal as tanggal_selesai
        from dim_kegiatan
            inner join dim_perjanjian dp on dim_kegiatan.id_perjanjian = dp.id_perjanjian
            inner join dim_date ddmulai on ddmulai.id_date = dim_kegiatan.id_tanggal_mulai
            inner join dim_date ddselesai on ddselesai.id_date = dim_kegiatan.id_tanggal_selesai
    where jenis_kegiatan = 'KULIAH UMUM' and dim_kegiatan.id_perjanjian is not null
    group by ddselesai.tahun
    order by ddselesai.tahun desc
    ''',con)

def getRerataJumlPesertaKulUm():
    return pd.read_sql('''
    select tahun, nama_kegiatan,count(id_mahasiswa) jumlah from fact_kegiatan_mahasiswa fkm
inner join dim_kegiatan dk on fkm.id_kegiatan = dk.id_kegiatan
inner join dim_date dd on dd.id_date=dk.id_tanggal_mulai
where jenis_kegiatan='KULIAH UMUM'
group by tahun,dk.id_kegiatan,dk.nama_kegiatan
order by tahun desc''',con)

#REMOVE SOON
def getKerjasama():
    return pd.read_sql('''select kode_perjanjian "Kode Perjanjian", no_perjanjian "No Perjanjian", concat(mulai.hari_dalam_bulan," ", mulai.nama_bulan, " ", mulai.tahun) as tglMulai, concat(selesai.hari_dalam_bulan," ", selesai.nama_bulan, " ", selesai.tahun) as tglSelesai ,
max(Penelitian) "Jumlah Penelitan", max(pkm) "Jumlah PkM",  max(kp) "Jumlah KP" from (    
    
    select id_perjanjian, kode_perjanjian, tipe_perjanjian, no_perjanjian, id_tanggal_mulai,  id_tanggal_selesai,
    max(case when jenis = 'Penelitian' then jumlah end) Penelitian,
    max(case when jenis = 'Pkm' then jumlah end) Pkm, null as KP
    from (
        select dim_perjanjian.id_perjanjian, kode_perjanjian, tipe_perjanjian, no_perjanjian, wilayah, br_pp_perjanjian.jenis, dim_perjanjian.id_tanggal_mulai, dim_perjanjian.id_tanggal_selesai, count(*) as "jumlah"
        from dim_perjanjian
        inner join br_pp_perjanjian on dim_perjanjian.id_perjanjian = br_pp_perjanjian.id_perjanjian
        group by dim_perjanjian.id_perjanjian, kode_perjanjian, tipe_perjanjian, no_perjanjian, wilayah,dim_perjanjian.id_tanggal_mulai, dim_perjanjian.id_tanggal_selesai,br_pp_perjanjian.jenis
    ) ppp
    group by id_perjanjian, kode_perjanjian, tipe_perjanjian, no_perjanjian, id_tanggal_mulai, id_tanggal_selesai
    
    union
    
    select fact_kp.id_perjanjian, kode_perjanjian, tipe_perjanjian, no_perjanjian, dim_perjanjian.id_tanggal_mulai, dim_perjanjian.id_tanggal_selesai, null as Penelitian, null as KP, count(*) as KP
    from fact_kp
    inner join dim_perjanjian on fact_kp.id_perjanjian = dim_perjanjian.id_perjanjian
    group by fact_kp.id_perjanjian, kode_perjanjian, tipe_perjanjian, no_perjanjian, dim_perjanjian.id_tanggal_mulai, dim_perjanjian.id_tanggal_selesai
) data 
inner join dim_date mulai on mulai.id_date = data.id_tanggal_mulai
inner join dim_date selesai on selesai.id_date = data.id_tanggal_selesai
group by kode_perjanjian, no_perjanjian,  tglMulai, tglSelesai
order by tglMulai''', con)

def getKerjasamaKegiatan():
    return pd.read_sql('''select ddselesai.tahun as tahun_selesai,
       dk.jenis_kegiatan,dk.nama_kegiatan,  dk.is_akademis,
       CASE WHEN dp.tipe_perjanjian = 'MO' THEN 'MOU'
		WHEN dp.tipe_perjanjian = 'PK' THEN 'PERJANJIAN KERJASAMA'
		ELSE 'NONE' END AS tipe_perjanjian,       
		dp.no_perjanjian,
		CASE WHEN dm.wilayah = '1' THEN 'LOKAL'
		WHEN dm.wilayah = '2' THEN 'REGIONAL'
		WHEN dm.wilayah = '3' THEN 'NASIONAL'
        WHEN dm.wilayah = '4' THEN 'INTERNASIONAL'
		ELSE 'NONE' END AS wilayah_mitra,  dm.jenis_mitra,
       dm.nama_mitra
from dim_kegiatan dk
inner join dim_perjanjian dp on dp.id_perjanjian = dk.id_perjanjian
inner join br_mitra_perjanjian bmp on bmp.id_perjanjian = dk.id_perjanjian
inner join dim_mitra dm on bmp.id_mitra = dm.id_mitra
inner join dim_date ddselesai on ddselesai.id_date = dk.id_tanggal_selesai
inner join dim_date ddmulai on ddmulai.id_date = dk.id_tanggal_mulai
where dk.id_perjanjian is not null
''', con)

def getKerjasamaKP():
    return pd.read_sql('''select distinct tahun_ajaran, ds.semester_nama, ddselesai.tahun as tahun_selesai,
       fact_kp.jenis_kp, CASE WHEN dp.tipe_perjanjian = 'MO' THEN 'MOU' ELSE 'PERJANJIAN KERJASAMA' END AS tipe_perjanjian
       , dp.no_perjanjian
       , CASE   
            WHEN dm.wilayah = '1' THEN 'LOKAL'
            WHEN dm.wilayah = '2' THEN 'REGIONAL'
            WHEN dm.wilayah = '3' THEN 'NASIONAL'
            WHEN dm.wilayah = '3' THEN 'INTERNASIONAL'
            ELSE 'NONE' END AS wilayah_mitra
       , dm.jenis_mitra, dm.nama_mitra
       from fact_kp
        inner join dim_perjanjian dp on fact_kp.id_perjanjian = dp.id_perjanjian
        inner join br_mitra_perjanjian bmp on dp.id_perjanjian = bmp.id_perjanjian
        inner join dim_mitra dm on bmp.id_mitra = dm.id_mitra
        inner join dim_semester ds on fact_kp.id_semester = ds.id_semester
        inner join dim_date ddselesai on ddselesai.id_date = fact_kp.id_tanggal_selesai
        where fact_kp.id_perjanjian is not null''', con)

def getKerjasamaPP():
    return pd.read_sql('''select ddselesai.tahun as tahun_selesai,
       br_pp_perjanjian.jenis, dpp.judul , CASE WHEN dp.tipe_perjanjian = 'MO' THEN 'MOU' ELSE 'PERJANJIAN KERJASAMA' END AS tipe_perjanjian
       , dp.no_perjanjian
       , CASE 
            WHEN dm.wilayah = '1' THEN 'LOKAL'
            WHEN dm.wilayah = '2' THEN 'REGIONAL'
            WHEN dm.wilayah = '3' THEN 'NASIONAL'
            WHEN dm.wilayah = '3' THEN 'INTERNASIONAL'
            ELSE 'NONE' END AS wilayah_mitra
       , dm.jenis_mitra, dm.nama_mitra
from br_pp_perjanjian
inner join dim_penelitian_pkm dpp on br_pp_perjanjian.id_penelitian_pkm = dpp.id_penelitian_pkm
inner join dim_perjanjian dp on br_pp_perjanjian.id_perjanjian = dp.id_perjanjian
inner join br_mitra_perjanjian bmp on dp.id_perjanjian = bmp.id_perjanjian
inner join dim_mitra dm on bmp.id_mitra = dm.id_mitra
inner join dim_date ddselesai on ddselesai.id_date = dpp.id_tanggal_selesai
inner join dim_date ddmulai on ddmulai.id_date = dpp.id_tanggal_mulai''', con)
