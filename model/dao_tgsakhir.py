import pandas as pd
from sqlalchemy import create_engine


con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

def getDataFrameFromDB(query):
    return pd.read_sql(query,con)

def getDataFrameFromDBwithParams(query,parameter):
    return pd.read_sql(query,con,params=parameter)

def getMahasiswaBimbinganSkripsi():
    return pd.read_sql('''select tahun_ajaran,semester_nama,count(id_mahasiswa) 'Jumlah Mahasiswa',nama from fact_skripsi fs
inner join dim_dosen dd on fs.id_dosen_pembimbing1=dd.id_dosen
inner join dim_semester ds on fs.id_semester = ds.id_semester
group by tahun_ajaran,semester_nama,nama
order by tahun_ajaran desc, semester_nama asc''',con)

def getIPK():
    return pd.read_sql('''select tahun_ajaran_yudisium as 'Tahun Lulus', count(id_mahasiswa) "Jumlah Lulusan",  min(ipk) "Min. IPK", avg(ipk) as 'Rata-rata IPK' ,  max(ipk) "Max. IPK"
from fact_yudisium
group by tahun_ajaran_yudisium
order by tahun_ajaran_yudisium''', con)

def getJmlLulusan():
    return pd.read_sql('''select count(*) as 'Jumlah Mahasiswa', tahun_ajaran_yudisium
from fact_yudisium
group by tahun_ajaran_yudisium
order by tahun_ajaran_yudisium''',con)

def getRateMasaStudi():
    return pd.read_sql('''
select 
    concat(round((masa_studi-mods)/12,0) ," tahun ", mods, " bulan")  as "Masa Studi" , 
    tahun_ajaran_yudisium as 'TA Yudisium'
from (
select  mod(masa_studi,12) as mods, masa_studi, tahun_ajaran_yudisium
from (
select round(avg(masa_studi_dalam_bulan),0) as "masa_studi", tahun_ajaran_yudisium from fact_yudisium
group by tahun_ajaran_yudisium) as data_mentah
) as data_ready
order by tahun_ajaran_yudisium
''', con)

def getMasaStudi():
    return pd.read_sql('''
select * from 
(select concat(dim_mahasiswa.tahun_angkatan,'/',cast(dim_mahasiswa.tahun_angkatan+1 as char(4))) as TahunMAsuk,
SUM(case when masa_studi_dalam_bulan < 36 then 1 else 0 end) as '< 3 Tahun',
SUM(case when masa_studi_dalam_bulan >= 36 AND masa_studi_dalam_bulan <42 then 1 else 0 end) as '3 - 3.5 Tahun',
SUM(case when masa_studi_dalam_bulan >= 42 AND masa_studi_dalam_bulan <54  then 1 else 0 end) as '3.5 - 4.5 Tahun',
SUM(case when masa_studi_dalam_bulan >= 54 AND masa_studi_dalam_bulan <=84 then 1 else 0 end) as '4.5 - 7 Tahun',
SUM(case when masa_studi_dalam_bulan >= 85 then 1 else 0 end) as '> 7 tahun'
from fact_yudisium
inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa=fact_yudisium.id_mahasiswa
group by TahunMAsuk
order by TahunMAsuk) lulusan
left join (
    select count(id_mahasiswa), tahun_ajaran from fact_pmb
    inner join dim_semester on dim_semester.id_semester=fact_pmb.id_semester AND id_prodi_diterima = 9
    group by tahun_ajaran
    order by tahun_ajaran
) mhsditerima on mhsditerima.tahun_ajaran = TahunMAsuk
''', con)

def getMahasiswaKP():
    return pd.read_sql('''
select count(*) as 'Jumlah KP', dim_semester.semester 'Semester',dim_semester.tahun_ajaran 'Tahun Ajaran' from fact_kp
inner join dim_semester on dim_semester.id_semester = fact_kp.id_semester
inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa = fact_kp.id_mahasiswa AND dim_mahasiswa.id_prodi = 9
group by dim_semester.tahun_ajaran, dim_semester.semester
order by  dim_semester.tahun_ajaran, dim_semester.semester
''', con)

def getMahasiswaKPpkm():
    return pd.read_sql('''select count(*) as 'Jumlah KP', dim_semester.tahun_ajaran 'Tahun Ajaran'
from fact_kp
inner join dim_semester on dim_semester.id_semester= fact_kp.id_semester 
inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa = fact_kp.id_mahasiswa AND dim_mahasiswa.id_prodi = 9
where fact_kp.is_pen_pkm = 1
group by dim_semester.tahun_ajaran
order by dim_semester.tahun_ajaran''', con)