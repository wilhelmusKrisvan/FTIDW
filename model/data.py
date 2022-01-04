import pandas as pd
from sqlalchemy import create_engine


con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

def getDataFrameFromDB(query):
    return pd.read_sql(query,con)

def getDataFrameFromDBwithParams(query,parameter):
    return pd.read_sql(query,con,params=parameter)

def getSeleksi():
    return pd.read_sql('''select 
dataMahasiswa.tahun_aka as 'Tahun Ajaran', dy_tampung as 'Daya Tampung',jml_pendaftar as 'Pendaftar', 
lolos as 'Lolos Seleksi', baru as 'Baru Reguler', Barutransfer as 'Baru Transfer', 
aktif.jmlaktif as 'Aktif Reguler', 0 as 'Aktif Transfer' from (
    select dataPendaftar.*, count(id_tanggal_lolos_seleksi) as lolos, count(id_mahasiswa) as baru,  
    0 as Barutransfer
    from(
    select dy.id_semester, tahun_ajaran as tahun_aka, dy.jumlah as dy_tampung, count(fpmbDaftar.id_pmb)  as jml_pendaftar 
    from dim_daya_tampung dy
    inner join dim_semester smstr on dy.id_semester = smstr.id_semester
    inner join dim_prodi prodi on prodi.id_prodi = dy.id_prodi
    left join fact_pmb fpmbDaftar on dy.id_semester = fpmbDaftar.id_semester and (fpmbDaftar.id_prodi_pilihan_1 || fpmbDaftar.id_prodi_pilihan_3 || fpmbDaftar.id_prodi_pilihan_3 = 9)
    where kode_prodi = '71' and dy.id_semester <= (select id_semester from dim_semester where tahun_ajaran='2018/2019' limit 1)
    group by tahun_aka, dy_tampung, dy.id_semester
    ) dataPendaftar
    left join fact_pmb fpmbLolos on dataPendaftar.id_semester = fpmbLolos.id_semester and fpmbLolos.id_prodi_diterima = 9
    group by id_semester, tahun_aka,dy_tampung, jml_pendaftar
    order by id_semester asc
)dataMahasiswa
left join (
select count(*) as jmlaktif, tahun_ajaran from fact_mahasiswa_status
left join dim_semester on fact_mahasiswa_status.id_semester = dim_semester.id_semester
where status = 'AK' 
group by tahun_ajaran
)aktif on aktif.tahun_ajaran = tahun_aka''',con)

def getMahasiswaAsing():
    return pd.read_sql('''select data.nama_prodi as 'Program Studi', tahun_semster as 'Tahun Ajaran', jumlah as 'Jumlah', parttime as 'Parttime', (jumlah - parttime) as 'Fulltime'
from (
select dim_prodi.nama_prodi, concat(tahun_angkatan, '/', cast(tahun_angkatan+1 as char(4))) as tahun_semster, count(*) as jumlah,
SUM(if(substr(nim,3,3)= 'ASG', 1, 0)) AS parttime
from dim_mahasiswa
inner join dim_prodi on dim_mahasiswa.id_prodi = dim_prodi.id_prodi AND (dim_prodi.id_prodi = 9 || 10)
where warga_negara = 'WNA'
group by dim_prodi.nama_prodi,tahun_semster, tahun_angkatan
) data
inner join dim_semester on dim_semester.tahun_ajaran = data.tahun_semster AND semester = 1 and dim_semester.id_semester <= (select id_semester from dim_semester where tahun_ajaran = '2018/2019' limit 1)
order by nama_prodi, tahun_semster desc''',con)

def getJenisSekolahPendaftar():
    return pd.read_sql('''select
       (case
           when tipe_sekolah_asal=1 then "NEGERI"
           WHEN tipe_sekolah_asal=2 THEN "SWASTA"
           when tipe_sekolah_asal=3 then "N/A"
       END)
           as 'Tipe Sekolah Asal', ds.tahun_ajaran as 'Tahun Ajaran', count(kode_pendaftar) AS 'Jumlah Pendaftar'
from fact_pmb
inner join dim_semester ds on fact_pmb.id_semester = ds.id_semester
where fact_pmb.id_prodi_diterima = 9 and fact_pmb.id_tanggal_registrasi is not null
group by ds.tahun_ajaran,'Tipe Sekolah Asal'
order by ds.tahun_ajaran''',con)

#Jumlah Pendaftar Berdasarkan Provinsi
def getProvinsiDaftar():
    return pd.read_sql('''select
    dl.provinsi as 'Provinsi', ds.tahun_ajaran as 'Tahun Ajaran', count(kode_pendaftar) AS 'Jumlah Pendaftar'
from fact_pmb
inner join dim_semester ds on fact_pmb.id_semester = ds.id_semester
inner join dim_lokasi dl ON fact_pmb.id_lokasi_rumah = dl.id_lokasi
group by ds.tahun_ajaran, dl.provinsi
order by ds.tahun_ajaran, dl.provinsi''',con)

def getProvinsiLolos():
    return pd.read_sql('''select
    dl.provinsi as 'Provinsi', ds.tahun_ajaran as 'Tahun Ajaran', count(kode_pendaftar) AS 'Pendaftar Lolos Seleksi'
from fact_pmb
inner join dim_semester ds on fact_pmb.id_semester = ds.id_semester
inner join dim_lokasi dl ON fact_pmb.id_lokasi_rumah = dl.id_lokasi
where fact_pmb.id_tanggal_lolos_seleksi is not null and fact_pmb.id_prodi_diterima = 9
group by ds.tahun_ajaran, dl.provinsi
order by ds.tahun_ajaran, dl.provinsi''',con)

def getProvinsiRegis():
    return pd.read_sql('''select
    dl.provinsi as 'Provinsi', ds.tahun_ajaran as 'Tahun Ajaran', count(kode_pendaftar) AS 'Pendaftar Registrasi Ulang'
from fact_pmb
inner join dim_semester ds on fact_pmb.id_semester = ds.id_semester
inner join dim_lokasi dl ON fact_pmb.id_lokasi_rumah = dl.id_lokasi
where fact_pmb.id_prodi_diterima = 9 and fact_pmb.id_tanggal_registrasi is not null
group by ds.tahun_ajaran, dl.provinsi
order by ds.tahun_ajaran, dl.provinsi''',con)

def getRasioCalonMahasiswa():
    return pd.read_sql('''select tahun_ajaran as 'Tahun Ajaran', jumlah as 'Jumlah', pendaftar_regis as 'Pendaftar Registrasi',
concat(round(jumlah/jumlah,0) ,' : ', round(pendaftar_regis/jumlah,2)) as 'Rasio Daya Tampung : Pendaftar Registrasi'
from(
    SELECT ds.tahun_ajaran,ds.kode_semester,dt.jumlah,
        sum(case when id_tanggal_registrasi is not null and id_prodi_diterima = 9 then 1 else 0 end) as pendaftar_regis
    FROM fact_pmb
    inner join dim_semester ds on fact_pmb.id_semester = ds.id_semester
    inner join dim_daya_tampung dt on ds.id_semester = dt.id_semester and dt.id_prodi = 9
    group by ds.kode_semester, ds.tahun_ajaran,dt.jumlah
    order by ds.tahun_ajaran
) as DataMentah''',con)

def getPerkembanganJumlahMaba():
    return pd.read_sql('''select tahun_ajaran 'Tahun Ajaran', count(distinct fp.id_mahasiswa) 'Jumlah'
from fact_pmb fp
         inner join dim_date dd on dd.id_date = fp.id_tanggal_registrasi
         inner join dim_semester ds on ds.kode_semester = concat(tahun, if(bulan >= 7, 2, 1))
         inner join dim_mahasiswa dm on fp.id_mahasiswa = dm.id_mahasiswa
where nim like "71%"
group by tahun_ajaran
order by tahun_ajaran''',con)

def getPersentaseKenaikanMaba():
    return pd.read_sql('''select tahun_ajaran 'Tahun Ajaran',
       if(@last_entry = 0, 0, format(((entry-@last_entry)/entry)*100,2)) '% Pertumbuhan',
        @last_entry := entry 'Jumlah'
from
      (select @last_entry := 0) x,
      (select tahun_ajaran, count(distinct fp.id_mahasiswa) entry
       from   fact_pmb fp
         inner join dim_date dd on dd.id_date = fp.id_tanggal_registrasi
         inner join dim_semester ds on ds.kode_semester = concat(tahun, if(bulan >= 7, 2, 1))
         inner join dim_mahasiswa dm on fp.id_mahasiswa = dm.id_mahasiswa
       group by tahun_ajaran) y
order by tahun_ajaran''',con)

def getMatkulBaru():
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
where fms.status = 'AK' and ds.tahun_ajaran in ('2015/2016','2016/2017','2017/2018','2018/2019','2019/2020')
group by ds.tahun_ajaran, ds.semester_nama
order by ds.tahun_ajaran, ds.semester_nama''',con)

def getMahasiswaAsing():
    return pd.read_sql('''select tahun_angkatan 'Tahun Angkatan', count(*) as 'Jumlah Mahasiswa Asing' from dim_mahasiswa 
where warga_negara ='WNA' and tahun_angkatan >= 2015 group by tahun_angkatan order by tahun_angkatan''',con)

def getDosenMengajar():
    return pd.read_sql('''select tahun_ajaran 'Tahun Ajaran',semester_nama 'Semester',
    count(distinct fdm.id_dosen) 'Jumlah' from fact_dosen_mengajar fdm
inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
inner join dim_semester ds on fdm.id_semester = ds.id_semester
where kode_semester>=20171
group by tahun_ajaran, semester_nama
order by tahun_ajaran desc,semester_nama asc''',con)

def getPersentaseDosenTidakTetap():
    return pd.read_sql('''select semua.tahun_ajaran 'Tahun Ajaran',semua.semester_nama 'Semester',
       tetap.jumlah 'Dosen Tidak Tetap',semua.jumlah 'Semua Dosen',(tetap.jumlah/semua.jumlah)*100 '%' from
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
        when Rata2>=0 and Rata2<=25 then 'KURANG BAIK'
        when Rata2>=26 and Rata2<=50 then 'CUKUP BAIK'
        when Rata2>51 and Rata2<=75 then 'BAIK'
        when Rata2>=76 and Rata2<=100 then 'SANGAT BAIK'
       END AS Predikat
from
(select tahun_ajaran,semester_nama, nama,((avg(q1)+avg(q2)+avg(q3)+avg(q4)+avg(q5)+avg(q6)+
       avg(q7)+avg(q8)+avg(q9)+avg(q10)+avg(q11)+avg(q12))/12) Rata2
from fact_dosen_mengajar fdm
inner join dim_semester ds on fdm.id_semester = ds.id_semester
inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
where kode_semester>='20191' and id_prodi=9
group by tahun_ajaran,semester_nama,nama) kepuasan
order by tahun_ajaran asc, semester_nama asc''',con)

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
    concat(substr(ak.kode_semester,1,4),' ',if(substr(ak.kode_semester,5,1)='1','Ganjil','Genap')) Semester, 
    ak.jumlah 'Mahasiswa Aktif',
    ifnull(ta.jumlah,0) 'Mahasiswa Tidak Aktif',IFNULL(ta.jumlah / ak.jumlah * 100,'0')'%'
from (select tahun_angkatan, ds.kode_semester,count(distinct (fms.nim)) jumlah
      from mahasiswa_status_monev fms
               inner join dim_mahasiswa dm on fms.nim = dm.nim
               inner join dim_semester ds on fms.kode_semester= ds.kode_semester
      where tahun_angkatan >= 2015
        and (status = 'AK'or status='CS')
        and ds.kode_semester>='20191'
      group by tahun_angkatan,ds.kode_semester) ak
    left join
     (select tahun_angkatan, ds.kode_semester, count(distinct (fms.nim)) jumlah
      from mahasiswa_status_monev fms
               inner join dim_mahasiswa dm on fms.nim = dm.nim
               inner join dim_semester ds on fms.kode_semester= ds.kode_semester
      where tahun_angkatan >= 2015
        and status = 'TA'
        and ds.kode_semester>='20191'
      group by tahun_angkatan, ds.kode_semester) ta
on ak.tahun_angkatan = ta.tahun_angkatan
and ak.kode_semester=ta.kode_semester
order by ak.tahun_angkatan desc, Semester asc''',con)