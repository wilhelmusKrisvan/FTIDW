import pandas as pd
from sqlalchemy import create_engine

#con = create_engine('mysql+pymysql://wilhelmus:TAhug0r3ng!@localhost:3333/datawarehouse')
#con = create_engine('mysql+pymysql://wilhelmus:TAhug0r3ng!@localhost:3333/datawarehouse_dev')
#con = create_engine('mysql+pymysql://user1:Ul0HenorahF1oyeo@localhost:3333/datawarehouse_dev')
con = create_engine('mysql+pymysql://admin:admin@localhost:3333/ftidw')

def getDataFrameFromDB(query):
    return pd.read_sql(query, con)


def getDataFrameFromDBwithParams(query, parameter):
    return pd.read_sql(query, con, params=parameter)


def getIpkMahasiswa():
    return pd.read_sql('''select ds.tahun_ajaran 'Tahun Ajaran', ds.semester_nama Semester, avg(ipk) as "Rata-Rata"
from fact_mahasiswa_status fms 
inner join dim_semester ds on ds.id_semester = fms.id_semester
where ds.tahun_ajaran between concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
group by ds.tahun_ajaran, ds.semester_nama
order by ds.tahun_ajaran, ds.semester_nama''', con)

def getIpkAngkatan():
    return pd.read_sql('''select 
    concat(ds.tahun_ajaran,' ',ds.semester_nama) 'Tahun Ajaran', 
    tahun_angkatan Angkatan,round(avg(ipk),2) as "Rata-Rata"
    from fact_mahasiswa_status fms 
    inner join dim_semester ds on ds.id_semester = fms.id_semester
    inner join dim_mahasiswa dm on fms.id_mahasiswa = dm.id_mahasiswa
    where tahun_angkatan>year(now())-7 and ds.tahun_ajaran between concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
     and (fms.status != 'UD' OR fms.status != 'DO')
    group by `Tahun Ajaran`,tahun_angkatan,ds.tahun_ajaran, ds.semester_nama
    order by ds.tahun_ajaran, tahun_angkatan''', con)

def getPersentaseMahasiswaTidakAktif():
    return pd.read_sql('''select mhs.`Tahun Ajaran`,mhs.tahun_angkatan,status,mhs.jumlah Mahasiswa,total.jumlah Total,
       round((mhs.jumlah/total.jumlah)*100,2) Persentase
from(select concat(ds.tahun_ajaran,' ', ds.semester_nama) 'Tahun Ajaran', dm.tahun_angkatan,
       status,count(distinct (dm.nim)) jumlah
      from fact_mahasiswa_status fms
               inner join dim_mahasiswa dm on fms.id_mahasiswa = dm.id_mahasiswa
               inner join dim_semester ds on fms.id_semester= ds.id_semester
      where tahun_angkatan > year(now())-7
        and ds.tahun_ajaran between
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
        and id_prodi=9
      group by `Tahun Ajaran`,dm.tahun_angkatan,status) mhs
inner join (select concat(ds.tahun_ajaran,' ', ds.semester_nama) 'Tahun Ajaran',
                tahun_angkatan,count(distinct (dm.nim)) jumlah
      from fact_mahasiswa_status fms
               inner join dim_mahasiswa dm on fms.id_mahasiswa = dm.id_mahasiswa
               inner join dim_semester ds on fms.id_semester= ds.id_semester
      where tahun_angkatan > year(now())-7
        and ds.tahun_ajaran between
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
        and id_prodi=9
      group by `Tahun Ajaran`,tahun_angkatan) total on total.`Tahun Ajaran`=mhs.`Tahun Ajaran`
order by `Tahun Ajaran`, tahun_angkatan
''', con)

def getPersentaseMahasiswaDO():
    return pd.read_sql('''
    select mhs.`Tahun Ajaran`,status,mhs.jumlah Mahasiswa,total.jumlah Total,
       round((mhs.jumlah/total.jumlah)*100,2) Persentase
from(select concat(ds.tahun_ajaran,' ', ds.semester_nama) 'Tahun Ajaran',
       status,count(distinct (dm.nim)) jumlah
      from fact_mahasiswa_status fms
               inner join dim_mahasiswa dm on fms.id_mahasiswa = dm.id_mahasiswa
               inner join dim_semester ds on fms.id_semester= ds.id_semester
      where (status='DO' or status='UD')
        and ds.tahun_ajaran between
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
        and id_prodi=9
      group by `Tahun Ajaran`,status) mhs
inner join (select concat(ds.tahun_ajaran,' ', ds.semester_nama) 'Tahun Ajaran',
                count(distinct (dm.nim)) jumlah
      from fact_mahasiswa_status fms
               inner join dim_mahasiswa dm on fms.id_mahasiswa = dm.id_mahasiswa
               inner join dim_semester ds on fms.id_semester= ds.id_semester
      where ds.tahun_ajaran between
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
        and id_prodi=9
      group by `Tahun Ajaran`) total on total.`Tahun Ajaran`=mhs.`Tahun Ajaran`
order by `Tahun Ajaran`
''', con)

def getDosenMengajar():
    return pd.read_sql('''
    select tahun_ajaran 'Tahun Ajaran',semester_nama 'Semester','NON INFORMATIKA' as Prodi,
    count(distinct fdm.id_dosen) 'Jumlah' from fact_dosen_mengajar fdm
inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
inner join dim_semester ds on fdm.id_semester = ds.id_semester
where id_prodi!=9 and tahun_ajaran between 
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
group by tahun_ajaran, semester_nama
    union all
    select tahun_ajaran 'Tahun Ajaran',semester_nama 'Semester','INFORMATIKA' as Prodi,
    count(distinct fdm.id_dosen) 'Jumlah' from fact_dosen_mengajar fdm
inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
inner join dim_semester ds on fdm.id_semester = ds.id_semester
where id_prodi=9 and tahun_ajaran between 
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
group by tahun_ajaran, semester_nama
order by 1 asc,2 asc''', con)

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
order by semua.tahun_ajaran desc, semua.semester_nama asc''', con)

def getRasioDosenMahasiswa():
    return pd.read_sql('''select data.tahun Tahun, concat(data.semester_nama,' ',data.tahun_ajaran) as Semester,
       dosen.Jumlah 'Jumlah Dosen',data.jumlah 'Jumlah Mahasiswa', 
       concat('1 : ',(data.jumlah/dosen.Jumlah)) 'Rasio' from
(select sum(Jumlah) as Jumlah,cast(year(now())-1 as char) as tahun from
    (select count(*) as Jumlah,year(tanggal_masuk) as tahun
    from dim_dosen
    where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
    group by tahun) data
    where data.tahun<=year(now())-1
    union all
    select sum(Jumlah) as Jumlah,cast(year(now())-2 as char) as tahun from
    (select count(*) as Jumlah,year(tanggal_masuk) as tahun
    from dim_dosen
    where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
    group by tahun) data
    where data.tahun<=year(now())-2
    union all
    select sum(Jumlah) as Jumlah,cast(year(now())-3 as char) as tahun from
    (select count(*) as Jumlah,year(tanggal_masuk) as tahun
    from dim_dosen
    where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
    group by tahun) data
    where data.tahun<=year(now())-3
    union all
    select sum(Jumlah) as Jumlah,cast(year(now())-4 as char) as tahun from
    (select count(*) as Jumlah,year(tanggal_masuk) as tahun
    from dim_dosen
    where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
    group by tahun) data
    where data.tahun<=year(now())-4
    union all 
    select sum(Jumlah) as Jumlah,cast(year(now())-5 as char) as tahun from
    (select count(*) as Jumlah,year(tanggal_masuk) as tahun
    from dim_dosen
    where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
    group by tahun) data
    where data.tahun<=year(now())-5) dosen
inner join
    (select substr(ds.kode_semester,1,4) tahun,ds.tahun_ajaran,ds.semester_nama,
    count(distinct fms.id_mahasiswa_status) jumlah
      from fact_mahasiswa_status fms
               inner join dim_mahasiswa dm on fms.id_mahasiswa_status = dm.id_mahasiswa
               inner join dim_semester ds on fms.id_semester= ds.id_semester
      where (status = 'AK' or status='CS' or status='TA')
        and ds.tahun_ajaran between 
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
      group by ds.semester_nama,ds.tahun_ajaran,tahun) data
on data.tahun=dosen.tahun
order by data.tahun asc, data.semester_nama asc''', con)


def getRasioDosenMengajarMahasiswa():
    return pd.read_sql('''select substr(data.tahun_ajaran,1,4) Tahun,
    concat(data.semester_nama,' ',data.tahun_ajaran) AS Semester,
       dosen.jumlah 'Jumlah Dosen',data.jumlah 'Jumlah Mahasiswa', 
       concat(1,' : ',(data.jumlah/dosen.jumlah)) 'Rasio' from
(select substr(kode_semester,1,4) 'tahun', kode_semester, count(distinct fdm.id_dosen) jumlah
     from fact_dosen_mengajar fdm
         inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
         inner join dim_semester ds on fdm.id_semester = ds.id_semester
     where substr(kode_semester,1,4)>=year(now())-5
     group by tahun,kode_semester) dosen
inner join
    (select substr(ds.kode_semester,1,4) tahun,ds.kode_semester,ds.semester_nama,ds.tahun_ajaran,count(distinct fms.id_mahasiswa) jumlah
      from fact_mahasiswa_status fms
               inner join dim_mahasiswa dm on fms.id_mahasiswa = dm.id_mahasiswa
               inner join dim_semester ds on fms.id_semester= ds.id_semester
      where (status = 'AK' or status='CS' or status='TA')
        and substr(ds.kode_semester,1,4)>=year(now())-5
      group by ds.kode_semester,ds.semester_nama,ds.tahun_ajaran,tahun) data
on data.kode_semester=dosen.kode_semester
order by tahun asc
''', con)

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
order by tahun_ajaran desc, semester_nama asc,nama asc''', con)

def getMatkulKurikulumBaru():
    return pd.read_sql('''
    select kode_matakuliah Kode, 
    kelompok_matakuliah 'Kelompok Matakuliah',
    dk.kode_kurikulum as Kurikulum, 
    upper(nama_matakuliah) Matakuliah, sks SKS 
    from fact_matakuliah_kurikulum fmk
inner join dim_matakuliah dm on fmk.id_matakuliah = dm.id_matakuliah
inner join dim_kurikulum dk on dk.id_kurikulum = fmk.id_kurikulum
order by kode_kurikulum desc,kelompok_matakuliah desc''', con)

def getMatkulTawar():
    return pd.read_sql('''select ds.semester_nama, ds.tahun_ajaran Semester
     , dm.kode_matakuliah Kode, dm.nama_matakuliah Matakuliah, dm.sks SKS, dm.kelompok_matakuliah 'Kelompok Matakuliah'
from fact_registrasi_matakuliah
inner join dim_matakuliah dm on fact_registrasi_matakuliah.id_matakuliah = dm.id_matakuliah
inner join dim_semester ds on fact_registrasi_matakuliah.id_semester = ds.id_semester
where ds.tahun_ajaran between concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
order by ds.tahun_ajaran desc, ds.semester, kelompok_matakuliah desc, nama_matakuliah''', con)

def getMatkulBatal():
    return pd.read_sql('''
    select concat(ds.semester_nama,' ',ds.tahun_ajaran) Semester, 
    dd.nama Nama, dm.nama_matakuliah Matakuliah,
    if(dm.kelompok_matakuliah is null,'-',dm.kelompok_matakuliah) Kelompok
from fact_dosen_mengajar
inner join dim_dosen dd on fact_dosen_mengajar.id_dosen = dd.id_dosen
inner join dim_semester ds on fact_dosen_mengajar.id_semester = ds.id_semester
inner join dim_matakuliah dm on dm.id_matakuliah = fact_dosen_mengajar.id_matakuliah
where is_batal = 1 and ds.tahun_ajaran between concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
order by ds.tahun_ajaran desc, ds.semester, 'Kelompok' asc''', con)


# def getMahasiswaAktif():
#     return pd.read_sql('''select ds.tahun_ajaran 'Tahun Ajaran', ds.semester_nama Semester, count(*) as 'Jumlah Mahasiswa Aktif' from fact_mahasiswa_status fms
# inner join dim_semester ds on ds.id_semester = fms.id_semester
# where fms.status = 'AK' and
# ds.tahun_ajaran between concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
# group by ds.tahun_ajaran, ds.semester_nama
# order by ds.tahun_ajaran, ds.semester_nama''', con)


# def getMahasiswaAsing():
#     return pd.read_sql('''select ds.tahun_ajaran 'Tahun Ajaran',
#     count(*) as 'Jumlah Mahasiswa Asing' from fact_mahasiswa_status fms
# inner join dim_semester ds on ds.id_semester = fms.id_semester
# inner join dim_mahasiswa dm on dm.id_mahasiswa = fms.id_mahasiswa
# where warga_negara ='WNA'and
# tahun_ajaran between concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
# group by tahun_ajaran
# order by tahun_ajaran ''', con)





#--------------df for graph----------------------#
def dfRasioDosenBar(tahun,smt):
    return pd.read_sql('''
    select dosen.tahun Tahun, concat(smt.semester_nama,' ',smt.tahun_ajaran) as Semester,
       dosen.Jumlah, 'Dosen' as Tipe from
(select sum(Jumlah) as Jumlah,cast(year(now())-1 as char) as tahun from
    (select count(*) as Jumlah,year(tanggal_masuk) as tahun
    from dim_dosen
    where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
    group by tahun) data
    where data.tahun<=year(now())-1
    union all
    select sum(Jumlah) as Jumlah,cast(year(now())-2 as char) as tahun from
    (select count(*) as Jumlah,year(tanggal_masuk) as tahun
    from dim_dosen
    where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
    group by tahun) data
    where data.tahun<=year(now())-2
    union all
    select sum(Jumlah) as Jumlah,cast(year(now())-3 as char) as tahun from
    (select count(*) as Jumlah,year(tanggal_masuk) as tahun
    from dim_dosen
    where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
    group by tahun) data
    where data.tahun<=year(now())-3
    union all
    select sum(Jumlah) as Jumlah,cast(year(now())-4 as char) as tahun from
    (select count(*) as Jumlah,year(tanggal_masuk) as tahun
    from dim_dosen
    where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
    group by tahun) data
    where data.tahun<=year(now())-4
    union all 
    select sum(Jumlah) as Jumlah,cast(year(now())-5 as char) as tahun from
    (select count(*) as Jumlah,year(tanggal_masuk) as tahun
    from dim_dosen
    where id_prodi=9 and status_dosen='Tetap' and tanggal_keluar is null
    group by tahun) data
    where data.tahun<=year(now())-5) dosen
inner join
    (select substr(ds.tahun_ajaran,1,4) sahun,ds.semester_nama,ds.tahun_ajaran
      from dim_semester ds
      where ds.tahun_ajaran between 
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1) and 
        ds.tahun_ajaran=%(year)s and semester_nama=%(smt)s) smt
on smt.sahun=dosen.tahun
UNION ALL
select substr(ds.tahun_ajaran,1,4) as sahun,concat(ds.semester_nama,' ',ds.tahun_ajaran),
    count(distinct fms.id_mahasiswa_status) jumlah,
    'Mahasiswa' Tipe
      from fact_mahasiswa_status fms
               inner join dim_mahasiswa dm on fms.id_mahasiswa_status = dm.id_mahasiswa
               inner join dim_semester ds on fms.id_semester= ds.id_semester
      where (status = 'AK' or status='CS' or status='TA')
        and ds.tahun_ajaran between 
concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1) and 
        ds.tahun_ajaran=%(year)s and semester_nama=%(smt)s
      group by ds.semester_nama,ds.tahun_ajaran,sahun
    ''',con,params={'year': tahun, 'smt': smt})


def dfRasioDosenMengajarBar(tahun,smt):
    return pd.read_sql('''
select substr(ds.tahun_ajaran,1,4) 'Tahun', concat(ds.semester_nama,' ',ds.tahun_ajaran) Semester,
    count(distinct fdm.id_dosen) Jumlah,'Dosen' as Tipe
    from fact_dosen_mengajar fdm
        inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
        inner join dim_semester ds on fdm.id_semester = ds.id_semester
    where substr(kode_semester,1,4)>=year(now())-5 and ds.tahun_ajaran=%(year)s and ds.semester_nama=%(smt)s
    group by tahun,semester,semester_nama,tahun_ajaran
UNION ALL
select substr(ds.tahun_ajaran,1,4) tahun, 
    concat(ds.semester_nama,' ',ds.tahun_ajaran) semester,
    count(distinct fms.id_mahasiswa) jumlah,
    'Mahasiswa' Tipe
      from fact_mahasiswa_status fms
               inner join dim_mahasiswa dm on fms.id_mahasiswa = dm.id_mahasiswa
               inner join dim_semester ds on fms.id_semester= ds.id_semester
      where (status = 'AK' or status='CS' or status='TA')
        and substr(ds.kode_semester,1,4)>=year(now())-5 and ds.tahun_ajaran=%(year)s and ds.semester_nama=%(smt)s
      group by ds.semester_nama,ds.tahun_ajaran,tahun,semester
    ''',con,params={'year': tahun, 'smt': smt})

def getKurikulum():
    return pd.read_sql('select kode_kurikulum from dim_kurikulum '
                       'where id_kurikulum in (select id_kurikulum from fact_matakuliah_kurikulum)',con)

def dfBatalTawar(tahun,smt):
    return pd.read_sql('''
select data.Semester, kode_semester, sum(Jumlah) 'Jumlah Matakuliah Yang Ditawarkan', Tipe from
    (select concat(ds.semester_nama, ' ',ds.tahun_ajaran) Semester,
    ds.kode_semester,
    count(dm.kode_matakuliah) Jumlah,
    'Kelas Yang Diambil Mahasiswa' Tipe
    from fact_registrasi_matakuliah
    inner join dim_matakuliah dm on fact_registrasi_matakuliah.id_matakuliah = dm.id_matakuliah
    inner join dim_semester ds on fact_registrasi_matakuliah.id_semester = ds.id_semester
    where ds.tahun_ajaran between concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
    and dm.id_matakuliah not in (280,242,245,5,3,189,188,371,513,512,514,516,283,523,525,519,520,522,524,216)
    and dm.id_prodi=9
    and ds.tahun_ajaran between %(From)s and %(To)s and id_prodi=9 
    group by Semester,ds.kode_semester
union all
    select concat(ds.semester_nama, ' ',ds.tahun_ajaran) Semester,
    ds.kode_semester,
    count(distinct dm.kode_matakuliah) Jumlah,
    'Kelas Yang Diambil Mahasiswa' Tipe
    from fact_registrasi_matakuliah
    inner join dim_matakuliah dm on fact_registrasi_matakuliah.id_matakuliah = dm.id_matakuliah
    inner join dim_semester ds on fact_registrasi_matakuliah.id_semester = ds.id_semester
    where ds.tahun_ajaran between concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
    and dm.id_matakuliah = 280 and dm.id_prodi=9
    and ds.tahun_ajaran between %(From)s and %(To)s and id_prodi=9 
    group by Semester,ds.kode_semester
union all
    select batal.* from
    (select concat(ds.semester_nama, ' ',ds.tahun_ajaran) Semester, 
    ds.kode_semester,
    count(dm.kode_matakuliah) Jumlah, 
    'Kelas Yang Dibatalkan' Tipe
    from fact_dosen_mengajar
    inner join dim_dosen dd on fact_dosen_mengajar.id_dosen = dd.id_dosen
    inner join dim_semester ds on fact_dosen_mengajar.id_semester = ds.id_semester
    inner join dim_matakuliah dm on dm.id_matakuliah = fact_dosen_mengajar.id_matakuliah
    where is_batal = 1 and dm.id_matakuliah not in (242,245,5,3,189,188,371,513,512,514,516,283,523,525,519,520,522,524,216)
    and ds.tahun_ajaran between concat(year(now())-5,'/',year(now())-4) and concat(year(now()),'/',year(now())+1)
    and ds.tahun_ajaran between %(From)s and %(To)s
    group by Semester,ds.kode_semester) batal    
    )data
    group by data.kode_semester,data.Tipe,data.Semester
order by 1,4
    ''',con,params={'From': tahun, 'To': smt})