import pandas as pd
from sqlalchemy import create_engine


#con = create_engine('mysql+pymysql://wilhelmus:TAhug0r3ng!@localhost:3333/datawarehouse')
#con = create_engine('mysql+pymysql://wilhelmus:TAhug0r3ng!@localhost:3333/datawarehouse_dev')
con = create_engine('mysql+pymysql://user1:Ul0HenorahF1oyeo@localhost:3333/datawarehouse_dev')

def getDataFrameFromDB(query):
    return pd.read_sql(query,con)

def getDataFrameFromDBwithParams(query,parameter):
    return pd.read_sql(query,con,params=parameter)

def getMahasiswaBimbinganSkripsi():
    return pd.read_sql('''select tahun_ajaran 'Tahun Ajaran',semester_nama 'Semester',count(id_mahasiswa) 'Jumlah Mahasiswa', nama 'Nama Dosen' 
    from fact_skripsi fs
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

def getJumlLulusSkripsiOntime():
    return ('''
    select count(*) as jumlah_mahasiswa, dim_semester.tahun_ajaran
    from fact_skripsi
        inner join(
            select count(*) as jumlah, id_mahasiswa from fact_skripsi
            group by id_mahasiswa
        ) data_skripsi on data_skripsi.id_mahasiswa = fact_skripsi.id_mahasiswa AND data_skripsi.jumlah=1
        inner join dim_semester on dim_semester.id_semester = fact_skripsi.id_semester
    where id_dosen_penguji1 <>''
    group by dim_semester.tahun_ajaran
    order by dim_semester.tahun_ajaran
    ''',con)

def getRateMasaStudi():
    return pd.read_sql('''
    select 
        concat(round((masa_studi-mods)/12,0) ," tahun ", mods, " bulan")  as "Masa Studi" , 
        tahun_ajaran_yudisium as 'TA Yudisium'
    from (
    select  mod(masa_studi,12) as mods, masa_studi, tahun_ajaran_yudisium
    from (
        select 
        round(avg(masa_studi_dalam_bulan),0) as "masa_studi", tahun_ajaran_yudisium from fact_yudisium
        group by tahun_ajaran_yudisium) as data_mentah
    ) as data_ready
    order by tahun_ajaran_yudisium
''', con)

def getMasaStudi():
    return pd.read_sql('''
select * from 
(select concat(dim_mahasiswa.tahun_angkatan,'/',cast(dim_mahasiswa.tahun_angkatan+1 as char(4))) as 'Tahun Masuk',
SUM(case when masa_studi_dalam_bulan < 36 then 1 else 0 end) as '< 3 Tahun',
SUM(case when masa_studi_dalam_bulan >= 36 AND masa_studi_dalam_bulan <42 then 1 else 0 end) as '3 - 3.5 Tahun',
SUM(case when masa_studi_dalam_bulan >= 42 AND masa_studi_dalam_bulan <54  then 1 else 0 end) as '3.5 - 4.5 Tahun',
SUM(case when masa_studi_dalam_bulan >= 54 AND masa_studi_dalam_bulan <=84 then 1 else 0 end) as '4.5 - 7 Tahun',
SUM(case when masa_studi_dalam_bulan >= 85 then 1 else 0 end) as '> 7 tahun'
from fact_yudisium
inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa=fact_yudisium.id_mahasiswa
group by `Tahun Masuk`
order by `Tahun Masuk`) lulusan
left join (
    select count(id_mahasiswa) 'Jumlah Mahasiswa', tahun_ajaran 'Tahun Ajaran' from fact_pmb
    inner join dim_semester on dim_semester.id_semester=fact_pmb.id_semester AND id_prodi_diterima = 9
    group by tahun_ajaran
    order by tahun_ajaran desc
) mhsditerima on mhsditerima.`Tahun Ajaran` = `Tahun Masuk`
''', con)

def getMahasiswaKP():
    return pd.read_sql('''
select dim_semester.tahun_ajaran 'Tahun Ajaran',  dim_semester.semester_nama 'Semester', count(*) as 'Jumlah KP' from fact_kp
inner join dim_semester on dim_semester.id_semester = fact_kp.id_semester
inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa = fact_kp.id_mahasiswa AND dim_mahasiswa.id_prodi = 9
group by dim_semester.tahun_ajaran, dim_semester.semester_nama
order by  dim_semester.tahun_ajaran, dim_semester.semester_nama
''', con)

def getMahasiswaKPpkm():
    return pd.read_sql('''
select dim_semester.tahun_ajaran 'Tahun Ajaran', count(*) as 'Jumlah KP'
from fact_kp 
inner join dim_semester on dim_semester.id_semester= fact_kp.id_semester 
inner join dim_mahasiswa on dim_mahasiswa.id_mahasiswa = fact_kp.id_mahasiswa AND dim_mahasiswa.id_prodi = 9
where fact_kp.is_pen_pkm = 1
group by dim_semester.tahun_ajaran
order by dim_semester.tahun_ajaran asc''', con)

def getMhahasiswaSkripsipkm():
    return pd.read_sql('''select semester_nama Semester, tahun_ajaran 'Tahun Ajaran', count(distinct fs.id_mahasiswa) as 'Jumlah Mahasiswa'
from fact_skripsi fs
inner join dim_semester ds on fs.id_semester = ds.id_semester
inner join br_pp_skripsi bps on fs.id_mahasiswa = bps.id_mahasiswa
group by semester_nama, tahun_ajaran
order by tahun_ajaran asc,semester_nama asc''',con)

def getMitraKP():
    return pd.read_sql('''select semester_nama Semester, tahun_ajaran 'Tahun Ajaran', wilayah 'Tingkat Wilayah', count(distinct fk.id_mitra) as 'Jumlah Mitra'
from fact_kp fk
inner join dim_mitra dm on fk.id_mitra = dm.id_mitra
inner join dim_semester ds on fk.id_semester = ds.id_semester
group by  semester_nama, tahun_ajaran, wilayah
order by tahun_ajaran asc,semester_nama asc''',con)

def getTTGU():
    return pd.read_sql('''select semester_nama Semester, tahun_ajaran 'Tahun Ajaran', count(distinct id_mahasiswa) as 'Jumlah Mahasiswa'
from fact_kp fk
inner join dim_semester ds on fk.id_semester = ds.id_semester
where is_pen_pkm='1'
group by semester_nama, tahun_ajaran
order by tahun_ajaran asc,semester_nama asc''',con)

def getMahasiswaLulus():
    return pd.read_sql('''select tahun_ajaran 'Tahun Ajaran',lls.tahun_angkatan 'Tahun Angkatan',lls.jml as 'Jumlah Lulusan',
    mhs.jml as 'Jumlah Mahasiswa',(lls.jml/mhs.jml) * 100 'Persentase' from
(select count(dm.id_mahasiswa) jml, tahun_ajaran_yudisium,semester_nama, tahun_angkatan from fact_yudisium fy
inner join dim_mahasiswa dm on fy.id_mahasiswa = dm.id_mahasiswa
inner join dim_semester_yudisium dsy on fy.id_semester_yudisium = dsy.id_semester_yudisium
where convert(substr(tahun_ajaran,6,4),int)-4=convert(tahun_angkatan,int) and semester_nama='GENAP'
group by tahun_ajaran_yudisium, tahun_angkatan, semester_nama
order by tahun_ajaran_yudisium desc, semester_nama desc) lls,
(select ds.tahun_ajaran, dm.tahun_angkatan,
       count(distinct dm.id_mahasiswa) jml
from fact_mahasiswa_status ms
inner join dim_mahasiswa dm on ms.id_mahasiswa = dm.id_mahasiswa
inner join dim_semester ds on ms.id_semester=ds.id_semester
where kode_semester>='20161' and (status='AK' or status='UD' or status='CS')
group by tahun_ajaran,tahun_angkatan
order by tahun_ajaran desc) mhs
where mhs.tahun_ajaran=lls.tahun_ajaran_yudisium and mhs.tahun_angkatan=lls.tahun_angkatan
order by tahun_ajaran asc''',con)

def getMahasiswaLulusBandingTotal():
    return pd.read_sql('''select lulus.tahun_angkatan 'Angkatan', lulus.jumlah 'Jumlah Lulusan', 
    total.jumlah 'Total Mahasiswa', (lulus.jumlah / total.jumlah)*100 "persentase"
from (
         select tahun_angkatan, count(distinct fy.id_mahasiswa) 'jumlah'
         from fact_yudisium fy
                  inner join dim_mahasiswa dm on dm.id_mahasiswa = fy.id_mahasiswa
                  inner join dim_semester_yudisium dsy on fy.id_semester_yudisium = dsy.id_semester_yudisium
         group by tahun_angkatan
     ) lulus,
     (
         select tahun_angkatan, count(distinct id_mahasiswa) 'jumlah'
         from dim_mahasiswa dm
         group by tahun_angkatan
     )total
where lulus.tahun_angkatan=total.tahun_angkatan
order by lulus.tahun_angkatan asc''',con)