import pandas as pd
from sqlalchemy import create_engine


con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

def getDataFrameFromDB(query):
    return pd.read_sql(query,con)

def getDataFrameFromDBwithParams(query,parameter):
    return pd.read_sql(query,con,params=parameter)


def getMatkulKurikulumBaru():
    return pd.read_sql('''select kode_matakuliah Kode, kelompok_matakuliah 'Kelompok Matakuliah', 
    upper(nama_matakuliah) Matakuliah, sks SKS from fact_matakuliah_kurikulum
inner join dim_matakuliah on fact_matakuliah_kurikulum.id_matakuliah = dim_matakuliah.id_matakuliah
where id_kurikulum = 8''',con)

def getMatkulBatal():
    return pd.read_sql('''select ds.tahun_ajaran 'Tahun Ajaran', ds.semester_nama Semester, 
    dd.nik NIK, dd.nama Nama, dd.nama_gelar 'Nama Gelar', dm.kode_matakuliah Kode, dm.nama_matakuliah Matakuliah
from fact_dosen_mengajar
inner join dim_dosen dd on fact_dosen_mengajar.id_dosen = dd.id_dosen
inner join dim_semester ds on fact_dosen_mengajar.id_semester = ds.id_semester
inner join dim_matakuliah dm on dm.id_matakuliah = fact_dosen_mengajar.id_matakuliah
where is_batal = 1
order by ds.tahun_ajaran, ds.semester, dd.nama''',con)

def getMatkulTawar():
    return pd.read_sql('''select distinct ds.tahun_ajaran 'Tahun Ajaran', ds.semester_nama Semester
     , dm.kode_matakuliah Kode, dm.nama_matakuliah Matakuliah, dm.sks SKS, dm.kelompok_matakuliah 'Kelompok Matakuliah'
     -- , kapasitas_kelas
     -- , sifat_mengajar
     -- , total_pertemuan
from fact_registrasi_matakuliah
inner join dim_matakuliah dm on fact_registrasi_matakuliah.id_matakuliah = dm.id_matakuliah
inner join dim_semester ds on fact_registrasi_matakuliah.id_semester = ds.id_semester
order by ds.tahun_ajaran, ds.semester, kelompok_matakuliah, nama_matakuliah''',con)

def getMahasiswaAktif():
    return pd.read_sql('''select ds.tahun_ajaran 'Tahun Ajaran', ds.semester_nama Semester, count(*) as 'Jumlah Mahasiswa Aktif' from fact_mahasiswa_status fms
inner join dim_semester ds on ds.id_semester = fms.id_semester
where fms.status = 'AK' and 
ds.tahun_ajaran between concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
group by ds.tahun_ajaran, ds.semester_nama
order by ds.tahun_ajaran, ds.semester_nama''',con)

def getMahasiswaAsing():
    return pd.read_sql('''select ds.tahun_ajaran 'Tahun Ajaran', 
    count(*) as 'Jumlah Mahasiswa Asing' from fact_mahasiswa_status fms
inner join dim_semester ds on ds.id_semester = fms.id_semester
inner join dim_mahasiswa dm on dm.id_mahasiswa = fms.id_mahasiswa
where warga_negara ='WNA'and 
tahun_ajaran between concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
group by tahun_ajaran
order by tahun_ajaran ''',con)

def getDosenMengajar():
    return pd.read_sql('''select tahun_ajaran 'Tahun Ajaran',semester_nama 'Semester',
    count(distinct fdm.id_dosen) 'Jumlah' from fact_dosen_mengajar fdm
inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
inner join dim_semester ds on fdm.id_semester = ds.id_semester
where ds.tahun_ajaran between 
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
group by tahun_ajaran, semester_nama
order by tahun_ajaran desc,semester_nama asc''',con)

def getPersentaseDosenTidakTetap():
    return pd.read_sql('''select semua.tahun_ajaran 'Tahun Ajaran',semua.semester_nama 'Semester',
       tetap.jumlah 'Dosen Tidak Tetap',semua.jumlah 'Semua Dosen',(tetap.jumlah/semua.jumlah)*100 as 'Persentase' from
(select tahun_ajaran,semester_nama,count(distinct fdm.id_dosen) jumlah from fact_dosen_mengajar fdm
inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
inner join dim_semester ds on fdm.id_semester = ds.id_semester
where kode_semester>=20171 and status_dosen='Kontrak'
group by tahun_ajaran, semester_nama) tetap,
(select tahun_ajaran,semester_nama,count(distinct fdm.id_dosen) jumlah from fact_dosen_mengajar fdm
inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
inner join dim_semester ds on fdm.id_semester = ds.id_semester
where kode_semester>=20171
group by tahun_ajaran, semester_nama) semua
where semua.semester_nama=tetap.semester_nama and
      semua.tahun_ajaran=tetap.tahun_ajaran
order by semua.tahun_ajaran desc, semua.semester_nama asc''',con)

def getTingkatKepuasanDosen():
    return pd.read_sql('''select tahun_ajaran 'Tahun Ajaran', semester_nama Semester, nama 'Nama Dosen', 
    Rata2 'Rata-rata',
       case
        when round(Rata2)>=0 and round(Rata2)<=25 then 'KURANG BAIK'
        when round(Rata2)>=26 and round(Rata2)<=50 then 'CUKUP BAIK'
        when round(Rata2)>51 and round(Rata2)<=75 then 'BAIK'
        when round(Rata2)>=76 and round(Rata2)<=100 then 'SANGAT BAIK'
       END AS Predikat
from
(select tahun_ajaran,semester_nama, nama,((avg(q1)+avg(q2)+avg(q3)+avg(q4)+avg(q5)+avg(q6)+
       avg(q7)+avg(q8)+avg(q9)+avg(q10)+avg(q11)+avg(q12))/12) Rata2
from fact_dosen_mengajar fdm
inner join dim_semester ds on fdm.id_semester = ds.id_semester
inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
where ds.tahun_ajaran between 
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1) and id_prodi=9
group by tahun_ajaran,semester_nama,nama) kepuasan
order by nama asc,tahun_ajaran asc, semester_nama asc''',con)

def getRasioDosenMahasiswa():
    return pd.read_sql('''select data.tahun Tahun,if(substr(data.kode_semester,5,1)='1','GASAL','GENAP') as Semester,
       dosen.Jumlah 'Jumlah Dosen',data.jumlah 'Jumlah Mahasiswa', concat(1,' : ',(data.jumlah/dosen.Jumlah)) 'Rasio' from
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
    where data.tahun<=2019) dosen
inner join
    (select substr(ds.kode_semester,1,4) tahun,ds.kode_semester,count(distinct fms.nim) jumlah
      from mahasiswa_status_monev fms
               inner join dim_mahasiswa dm on fms.nim = dm.nim
               inner join dim_semester ds on fms.kode_semester= ds.kode_semester
      where (status = 'AK' or status='CS' or status='TA')
        and ds.kode_semester>='20191'
      group by ds.kode_semester,tahun) data
on data.tahun=dosen.tahun''', con)

def getRasioDosenMengajarMahasiswa():
    return pd.read_sql('''select substr(data.kode_semester,1,4) Tahun,if(substr(data.kode_semester,5,1)='1','GASAL','GENAP') AS Semester,
       dosen.jumlah 'Jumlah Dosen',data.jumlah 'Jumlah Mahasiswa', concat(1,' : ',(data.jumlah/dosen.jumlah)) 'Rasio' from
(select substr(kode_semester,1,4) 'tahun', kode_semester, count(distinct fdm.id_dosen) jumlah
     from fact_dosen_mengajar fdm
         inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
         inner join dim_semester ds on fdm.id_semester = ds.id_semester
     where substr(kode_semester,1,4)>=2019
     group by tahun,kode_semester) dosen
inner join
    (select substr(ds.kode_semester,1,4) tahun,ds.kode_semester,count(distinct fms.nim) jumlah
      from mahasiswa_status_monev fms
               inner join dim_mahasiswa dm on fms.nim = dm.nim
               inner join dim_semester ds on fms.kode_semester= ds.kode_semester
      where (status = 'AK' or status='CS' or status='TA')
        and ds.kode_semester>='20191'
      group by ds.kode_semester,tahun) data
on data.kode_semester=dosen.kode_semester''',con)

def getPersentaseMahasiswaTidakAktif():
    return pd.read_sql('''select ak.tahun_angkatan 'Tahun Angkatan', 
    ak.tahun_ajaran, 
    ak.jumlah 'Mahasiswa Aktif',
    concat(if(substr(ak.kode_semester,5,1)='1','Ganjil','Genap')) Semester,
    ifnull(ta.jumlah,0) 'Mahasiswa Tidak Aktif',IFNULL(ta.jumlah / ak.jumlah * 100,'0')"persen"
from (select ds.tahun_ajaran,tahun_angkatan, ds.kode_semester,count(distinct (dm.nim)) jumlah
      from fact_mahasiswa_status fms
               inner join dim_mahasiswa dm on fms.id_mahasiswa = dm.id_mahasiswa
               inner join dim_semester ds on fms.id_semester= ds.id_semester
      where tahun_angkatan >= year(now()) -7
        and (status = 'AK'or status='CS')
        and ds.tahun_ajaran between 
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
        and id_prodi=9
      group by ds.tahun_ajaran,tahun_angkatan,ds.kode_semester) ak
    left join
     (select ds.tahun_ajaran,tahun_angkatan, ds.kode_semester, count(distinct (dm.nim)) jumlah
      from fact_mahasiswa_status fms
               inner join dim_mahasiswa dm on fms.id_mahasiswa = dm.id_mahasiswa
               inner join dim_semester ds on fms.id_semester= ds.id_semester
      where tahun_angkatan >= year(now()) -7
        and status = 'TA'
        and ds.tahun_ajaran between 
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
        and id_prodi=9
      group by ds.tahun_ajaran,tahun_angkatan, ds.kode_semester) ta
on ak.tahun_angkatan = ta.tahun_angkatan
and ak.kode_semester=ta.kode_semester
order by ak.tahun_angkatan desc, Semester asc''',con)