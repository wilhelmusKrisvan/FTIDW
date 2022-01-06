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