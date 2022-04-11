import pandas as pd
from sqlalchemy import create_engine

con = create_engine('mysql+pymysql://admin:admin@localhost:3333/ftidw')
# con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')
# con = create_engine('mysql+pymysql://user1:Ul0HenorahF1oyeo@localhost:3333/datawarehouse_dev')


def getDataFrameFromDB(query):
    return pd.read_sql(query, con)


def getDataFrameFromDBwithParams(query, parameter):
    return pd.read_sql(query, con, params=parameter)

def getDosen(): return pd.read_sql('select nama from dim_dosen where id_prodi=9',con)

# jumlah judul
def getJumlahPPP(): return pd.read_sql('''
select Tahun, Nama, max(Penelitian) Penelitian, max(pkm) as PKM , max(publikasi) as "Publikasi Penelitan dan PKM", max(LuaranLainnya) as "Luaran Lainnya" from 
(
   ( select nama, dim_dosen.id_dosen, tahun, count(*) as Penelitian, null as pkm, null as publikasi, null as LuaranLainnya from fact_penelitian fact
        inner join dim_penelitian_pkm dim on dim.id_penelitian_pkm = fact.id_penelitian
        inner join br_pp_dosen on fact.id_penelitian = br_pp_dosen.id_penelitian_pkm
        inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen and id_prodi = 9 
        inner join dim_date on dim_date.id_date = dim.id_tanggal_mulai
        group by nama,dim_dosen.id_dosen, tahun
        order by nama, tahun)
        union 
    (select nama, dim_dosen.id_dosen, tahun, null as Penelitian, count(*) as pkm , null as publikasi, null as LuaranLainnya  from fact_pkm fact
        inner join dim_penelitian_pkm dim on dim.id_penelitian_pkm = fact.id_pkm
        inner join br_pp_dosen on fact.id_pkm = br_pp_dosen.id_penelitian_pkm
        inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen and id_prodi = 9 
        inner join dim_date on dim_date.id_date = dim.id_tanggal_mulai
        group by dim_dosen.id_dosen, nama, tahun
        order by nama, tahun)
    union
    (select nama, dimdos.id_dosen, tahun_publikasi as tahun, null as Penelitian, null as pkm, count(*) as publikasi, null as LuaranLainnya from fact_publikasi fact
        inner join dim_publikasi dimpub on fact.id_publikasi = dimpub.id_publikasi
        inner join br_pub_dosen brpub on fact.id_publikasi = brpub.id_publikasi
        inner join dim_dosen dimdos on brpub.id_dosen = dimdos.id_dosen and id_prodi = 9  
        group by nama, dimdos.id_dosen, tahun_publikasi
        order by nama)        
    union
    (select nama, dim_dosen.id_dosen, tahun, 
        null as Penelitian, null as pkm, null as publikasi ,  
        count(*) LuaranLainnya
        from fact_luaran_lainnya fatl
        inner join dim_luaran_lainnya diml on fatl.id_luaran_lainnya = diml.id_luaran_lainnya
        inner join br_pp_luaranlainnya brl on fatl.id_luaran_lainnya = brl.id_luaranlainnya
        inner join br_pp_dosen brpp on brpp.id_penelitian_pkm = brl.id_penelitian_pkm
        inner join dim_dosen on brpp.id_Dosen = dim_dosen.id_dosen and id_prodi = 9  
        inner join dim_date on dim_date.id_date = diml.id_tanggal_luaran
        group by  nama, dim_dosen.id_dosen, tahun)
) data
where tahun>year(now())-5
group by tahun, nama
order by tahun desc, nama''', con)


# pendanaan
def getPenelitianDana(): return pd.read_sql('''
select  Tahun, judul_penelitian as "Judul Penelitan", dim_penelitian_pkm.wilayah_nama "Nama Wilayah", 
        br_pp_dana.besaran_dana "Jumlah Dana", dim_sumber_dana.jenis_sumber_dana "Sumber Dana", dim_sumber_dana.status "Asal Sumber Dana"
from fact_penelitian fact
inner join dim_penelitian_pkm on fact.id_penelitian = dim_penelitian_pkm.id_penelitian_pkm
inner join br_pp_dana on dim_penelitian_pkm.id_penelitian_pkm = br_pp_dana.id_penelitian_pkm
inner join dim_sumber_dana on br_pp_dana.id_sumber_dana = dim_sumber_dana.id_sumber_dana
inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
order by tahun, judul_penelitian''', con)


def getPKMDana(): return pd.read_sql('''
select  
    Tahun, judul_pkm "Judul PkM",
    jumlah_Dosen "Jumlah Dosen", 
     jumlah_mahasiswa "Jumlah Mahasiswa"
from fact_pkm fact
inner join dim_penelitian_pkm on fact.id_pkm = dim_penelitian_pkm.id_penelitian_pkm
inner join br_pp_dosen on fact.id_pkm = br_pp_dosen.id_penelitian_pkm
inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen
inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
inner join br_pp_mahasiswa on fact.id_pkm = br_pp_mahasiswa.id_penelitian_pkm
inner join dim_mahasiswa on br_pp_mahasiswa.id_mahasiswa = dim_mahasiswa.id_mahasiswa 
group by fact.id_pkm, jumlah_Dosen,judul_pkm, jumlah_mahasiswa, tahun
order by tahun, judul_pkm''', con)


# mahasiswa
# def getPenelitianMhs(): return pd.read_sql('''
# select
#     tahun 'Tahun', fact.judul_penelitian 'Judul Penelitian',
#     jumlah_Dosen 'Jumlah Dosen', GROUP_CONCAT(distinct dim_dosen.nama  SEPARATOR', ') 'Nama Dosen',
#     jumlah_mahasiswa 'Jumlah Mahasiswa', GROUP_CONCAT(distinct dim_mahasiswa.nama  SEPARATOR', ') 'Nama Mahasiswa'
# from fact_penelitian fact
# inner join dim_penelitian_pkm on fact.id_penelitian = dim_penelitian_pkm.id_penelitian_pkm
# inner join dim_penelitian_pkm dim on dim.id_penelitian_pkm = fact.id_penelitian
#     inner join br_pp_dosen on fact.id_penelitian = br_pp_dosen.id_penelitian_pkm
#     inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen
#     inner join dim_date on dim_date.id_date = dim.id_tanggal_mulai
#     inner join br_pp_mahasiswa on fact.id_penelitian = br_pp_mahasiswa.id_penelitian_pkm
#     inner join dim_mahasiswa on br_pp_mahasiswa.id_mahasiswa = dim_mahasiswa.id_mahasiswa
#     group by fact.id_penelitian, jumlah_Dosen,judul_penelitian, jumlah_mahasiswa, tahun''', con)


def getPKMMhs(): return pd.read_sql('''
select 
    Tahun, judul_pkm "Judul PkM",
    jumlah_Dosen "Jumlah Dosen",
    jumlah_mahasiswa "Jumlah Mahasiswa"
from fact_pkm fact
inner join dim_penelitian_pkm on fact.id_pkm = dim_penelitian_pkm.id_penelitian_pkm
inner join br_pp_dosen on fact.id_pkm = br_pp_dosen.id_penelitian_pkm
inner join dim_dosen on br_pp_dosen.id_Dosen = dim_dosen.id_dosen
inner join dim_date on dim_date.id_date = dim_penelitian_pkm.id_tanggal_mulai
inner join br_pp_mahasiswa on fact.id_pkm = br_pp_mahasiswa.id_penelitian_pkm
inner join dim_mahasiswa on br_pp_mahasiswa.id_mahasiswa = dim_mahasiswa.id_mahasiswa 
group by fact.id_pkm, jumlah_Dosen,judul_pkm, jumlah_mahasiswa, tahun
order by tahun desc, judul_pkm''', con)


def getPublikasiMhs():
    return pd.read_sql('''
    select  tahun_ajaran 'Tahun Ajaran', 
            count(distinct fp.id_publikasi) 'Jumlah Publikasi'
    from br_pub_mahasiswa bpm
             inner join dim_publikasi dp on bpm.id_publikasi = dp.id_penelitian_pkm
             inner join fact_publikasi fp on bpm.id_publikasi = fp.id_penelitian_pkm
             inner join dim_date dd on fp.id_tanggal_publikasi = dd.id_date
             inner join dim_semester ds on ds.kode_semester = concat(tahun, if(bulan >= 7, 2, 1))
    where fp.is_deleted != 1
    group by tahun_ajaran
    order by tahun_ajaran desc;
    ''', con)


def getTTGUMhsDiadopsi():
    return pd.read_sql('''
    select  tahun 'Tahun',
            count(distinct dll.id_penelitian_pkm) 'Jumlah Judul'
    from dim_luaran_lainnya dll
             inner join dim_jenis_luaran djl on dll.id_jenis_luaran = djl.id_jenis_luaran
             inner join br_ll_mahasiswa blm on dll.id_luaran_lainnya = blm.id_luaran_lainnya
             inner join dim_date dd on dd.id_date=dll.id_tanggal_luaran
    where keterangan_jenis_luaran='TEKNOLOGI TEPAT GUNA'
    group by tahun
    order by tahun desc;
    ''', con)


def getLuaranHKIMhsperTh():
    return pd.read_sql('''
    select tahun 'Tahun', count(distinct fll.id_luaran_lainnya) 'Jumlah Judul'
    from br_ll_mahasiswa blm
             inner join fact_luaran_lainnya fll on blm.id_luaran_lainnya = fll.id_luaran_lainnya
             inner join dim_luaran_lainnya dll on blm.id_luaran_lainnya = dll.id_luaran_lainnya
             inner join dim_date dd on dd.id_date = fll.id_tanggal_luaran
    where no_haki is not null
    group by tahun
    order by tahun desc;
    ''', con)


def getPPDosenKPSkripsiMhs():
    return pd.read_sql('''
    select tahun 'Tahun',count(id_mahasiswa) Jumlah from br_pp_kp
    inner join dim_penelitian_pkm dpp on br_pp_kp.id_penelitian_pkm = dpp.id_penelitian_pkm
    inner join dim_date dd on dd.id_date=dpp.id_tanggal_selesai
    group by tahun
    order by tahun desc
    ''', con)


# kerjasama
def getKerjasamaPenelitian(): return pd.read_sql('''
select ddselesai.tahun 'Tahun Selesai',
       br_pp_perjanjian.jenis 'Jenis', dpp.judul 'Judul Penelitian', 
       CASE WHEN dp.tipe_perjanjian = 'MO' THEN 'MOU' ELSE 'PERJANJIAN KERJASAMA' END AS 'Tipe Perjanjian', 
       dp.no_perjanjian 'No Penjanjian',
       CASE WHEN dm.wilayah = '1' THEN 'LOKAL'
            WHEN dm.wilayah = '2' THEN 'REGIONAL'
		    WHEN dm.wilayah = '3' THEN 'NASIONAL'
            WHEN dm.wilayah = '4' THEN 'INTERNASIONAL'
		    ELSE 'NONE' END AS 'Wilayah Mitra',
	   dm.jenis_mitra 'Jenis Mitra', dm.nama_mitra 'Nama Mitra'
from br_pp_perjanjian
inner join dim_penelitian_pkm dpp on br_pp_perjanjian.id_penelitian_pkm = dpp.id_penelitian_pkm
inner join dim_perjanjian dp on br_pp_perjanjian.id_perjanjian = dp.id_perjanjian
inner join br_mitra_perjanjian bmp on dp.id_perjanjian = bmp.id_perjanjian
inner join dim_mitra dm on bmp.id_mitra = dm.id_mitra
inner join dim_date ddselesai on ddselesai.id_date = dpp.id_tanggal_selesai
inner join dim_date ddmulai on ddmulai.id_date = dpp.id_tanggal_mulai
where br_pp_perjanjian.jenis="Penelitian"''', con)


def getKerjasamaPKM(): return pd.read_sql('''
select ddselesai.tahun as 'Tahun Selesai',
       br_pp_perjanjian.jenis 'Jenis', dpp.judul 'Judul Penelitian', 
       CASE WHEN dp.tipe_perjanjian = 'MO' THEN 'MOU' ELSE 'PERJANJIAN KERJASAMA' END AS 'Tipe Perjanjian', dp.no_perjanjian 'No Perjanjian', 
       CASE WHEN dm.wilayah = '1' THEN 'LOKAL'
		    WHEN dm.wilayah = '2' THEN 'REGIONAL'
		    WHEN dm.wilayah = '3' THEN 'NASIONAL'
            WHEN dm.wilayah = '3' THEN 'INTERNASIONAL'
		    ELSE 'NONE' END AS 'Wilayah Mitra',
       dm.jenis_mitra 'Jenis Mitra', dm.nama_mitra 'Nama Mitra'
from br_pp_perjanjian
inner join dim_penelitian_pkm dpp on br_pp_perjanjian.id_penelitian_pkm = dpp.id_penelitian_pkm
inner join dim_perjanjian dp on br_pp_perjanjian.id_perjanjian = dp.id_perjanjian
inner join br_mitra_perjanjian bmp on dp.id_perjanjian = bmp.id_perjanjian
inner join dim_mitra dm on bmp.id_mitra = dm.id_mitra
inner join dim_date ddselesai on ddselesai.id_date = dpp.id_tanggal_selesai
inner join dim_date ddmulai on ddmulai.id_date = dpp.id_tanggal_mulai
where br_pp_perjanjian.jenis="PKM"''', con)


# sitasi
def getKISitasi3th():
    return pd.read_sql('''
    select  tahun_sitasi       'Tahun Sitasi',
            dp.judul_karya     'Judul Publikasi',
            sum(jumlah_sitasi) 'Jumlah Sitasi'
    from fact_publikasi_sitasi fps
             inner join dim_publikasi dp on fps.id_publikasi = dp.id_publikasi
    where tahun_sitasi >= year(now()) - 5
    group by tahun_sitasi, fps.id_publikasi, dp.judul_karya
    order by tahun_sitasi desc, 'Jumlah Sitasi' desc;
    ''', con)


# luaran
def getLuaranHKIDosenperTh():
    return pd.read_sql('''
    select  tahun Tahun, nama 'Nama Dosen',
            count(dpp.id_penelitian_pkm) 'Jumlah Judul' 
    from dim_penelitian_pkm dpp
    inner join br_pp_luaranlainnya bpl on dpp.id_penelitian_pkm = bpl.id_penelitian_pkm
    inner join br_pp_dosen bpd on bpl.id_penelitian_pkm = bpd.id_penelitian_pkm
    inner join dim_dosen dd on bpd.id_dosen = dd.id_dosen
    INNER JOIN dim_date dt on dpp.id_tanggal_selesai = dt.id_date
    where jenis_luaran like 'HAK ATAS KEKAYAAN INTELEKTUAL'
    group by tahun, nama,jenis_luaran
    order by tahun desc
    ''', con)


def getLuaranTTGUDosenperTh():
    return pd.read_sql('''
    select  tahun 'Tahun', 
            nama 'Nama Dosen',
            count(dpp.id_penelitian_pkm) 'Jumlah Judul' 
    from dim_penelitian_pkm dpp
    inner join br_pp_luaranlainnya bpl on dpp.id_penelitian_pkm = bpl.id_penelitian_pkm
    inner join br_pp_dosen bpd on bpl.id_penelitian_pkm = bpd.id_penelitian_pkm
    inner join dim_dosen dd on bpd.id_dosen = dd.id_dosen
    INNER JOIN dim_date dt on dpp.id_tanggal_selesai = dt.id_date
    where jenis_luaran like 'TEKNOLOGI TEPAT GUNA'
    group by tahun, nama,jenis_luaran
    order by tahun desc
    ''', con)


def getLuaranBukuDosenperTh():
    return pd.read_sql('''
    select  tahun Tahun, 
            nama 'Nama Dosen',
            count(dpp.id_penelitian_pkm) Jumlah 
    from dim_penelitian_pkm dpp
    inner join br_pp_luaranlainnya bpl on dpp.id_penelitian_pkm = bpl.id_penelitian_pkm
    inner join br_pp_dosen bpd on bpl.id_penelitian_pkm = bpd.id_penelitian_pkm
    inner join dim_dosen dd on bpd.id_dosen = dd.id_dosen
    INNER JOIN dim_date dt on dpp.id_tanggal_selesai = dt.id_date
    where not(jenis_luaran like 'HAK ATAS KEKAYAAN INTELEKTUAL' or jenis_luaran like 'TEKNOLOGI TEPAT GUNA')
    group by tahun, nama,jenis_luaran
    order by tahun desc
    ''', con)


def getRerataJumlPenelitianDosenperTh():
    return pd.read_sql('''
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
          group by dd.tahun) dosen
    where pp.tahun=dosen.tahun
    group by pp.tahun, pp.jumlah, dosen.jumlah, `Rerata`
    order by pp.tahun desc;
    ''', con)


def getRerataJumlPublikasiDosenperTh():
    return pd.read_sql('''
    select dd.tahun Tahun, count(distinct dp.id_publikasi) 'Jumlah Judul'
    from br_pp_publikasi bpp
             inner join dim_publikasi dp on bpp.id_penelitian_pkm = dp.id_penelitian_pkm
             inner join dim_date dd on dp.tahun_publikasi = dd.tahun
    where dd.tahun
    group by dd.tahun
    order by dd.tahun desc
    ''', con)