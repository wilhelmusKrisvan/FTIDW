import pandas as pd
from sqlalchemy import create_engine

#con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')
#con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse_dev')
#con = create_engine('mysql+pymysql://user1:Ul0HenorahF1oyeo@localhost:3333/datawarehouse_dev')
con = create_engine('mysql+pymysql://admin:admin@localhost:3333/ftidw')


def getDataFrameFromDB(query):
    return pd.read_sql(query, con)


def getDataFrameFromDBwithParams(query, parameter):
    return pd.read_sql(query, con, params=parameter)


def getMahasiswaMBKMperSemester():
    return pd.read_sql('''
    select concat(ds.semester_nama,' ',ds.tahun_ajaran) Semester,
       (case
            when kode_bkp = 'PP' then 'Pertukaran Pelajar'
            when kode_bkp = 'PI' then 'Proyek Independen'
            when kode_bkp = 'PR' then 'Penelitian & Riset'
            when kode_bkp = 'PD' then 'Pembangunan Desa'
            when kode_bkp = 'PK' then 'Proyek Kemanusiaan'
            when kode_bkp = 'KP' then 'Kerja Praktik'
            when kode_bkp = 'KU' then 'Kewirausahaan'
            when kode_bkp = 'AM' then 'Asisten Mengajar'
            when kode_bkp = 'AK' then 'Ambil Kredit Unit'
            else kode_bkp
    end) as Bentuk,
       count(distinct id_mahasiswa) Jumlah
    from mbkm_matkul_monev
    inner join dim_semester ds on mbkm_matkul_monev.kode_semester = ds.kode_semester
    WHERE ds.tahun_ajaran between '2017/2018' and '2021/2022'
    group by ds.kode_semester, Bentuk , Semester
    order by ds.kode_semester desc;''', con)


def getMitraMBKM():
    return pd.read_sql('''
    select distinct mitra Mitra, kode_semester
    from mbkm_matkul_monev
    group by mitra, kode_semester;''', con)


def getJumlMitraMBKMperSemester():
    return pd.read_sql('''
    select CONCAT(semester_nama,' ',tahun_ajaran) Semester, count(distinct mitra) 'Jumlah Mitra'
    from mbkm_matkul_monev mmm
    inner join dim_semester ds on mmm.kode_semester = ds.kode_semester
    group by ds.kode_semester, Semester
    order by ds.kode_semester
    ''',con)


def getDosbingMBKMperSemester():
    return pd.read_sql('''
    select CONCAT(semester_nama,' ',tahun_ajaran) Semester, count(distinct dd.id_dosen) 'Jumlah Dosen'
    from mbkm_matkul_monev mbm
         inner join dim_semester ds on mbm.kode_semester = ds.kode_semester
         inner join dim_matakuliah dm on mbm.kode_matakuliah = dm.kode_matakuliah
         inner join fact_khs fk on dm.id_matakuliah = fk.id_matakuliah
         inner join fact_dosen_mengajar fdm on dm.id_matakuliah = fdm.id_matakuliah
         inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
    group by mbm.kode_semester, Semester
    order by mbm.kode_semester desc;''', con)


def getRerataSKSMBKMperSemester():
    return pd.read_sql('''
    select concat(ds.semester_nama,' ',ds.tahun_ajaran) Semester, count(sks) 'Jumlah SKS'
    from mbkm_matkul_monev mbm
         inner join dim_semester ds on mbm.kode_semester = ds.kode_semester
         inner join dim_matakuliah dm on mbm.kode_matakuliah = dm.kode_matakuliah
    group by mbm.kode_semester, Semester
    order by mbm.kode_semester desc;''', con)


def getTableMitraInternal():
    return pd.read_sql('''
    select CONCAT(semester_nama,' ',tahun_ajaran) Semester,
       nama_matakuliah,
       mitra
from mbkm_matkul_monev mmm
inner join dim_semester ds on mmm.kode_semester = ds.kode_semester
inner join dim_matakuliah mm on mmm.kode_matakuliah = mm.kode_matakuliah
where mmm.mitra LIKE 'Prodi%%' or mitra in('MKH','Informatika');''', con)

def getTableMitraEksternal():
    return pd.read_sql('''
    select CONCAT(semester_nama,' ',tahun_ajaran) Semester,
       nama_matakuliah,
       mitra
from mbkm_matkul_monev mmm
inner join dim_semester ds on mmm.kode_semester = ds.kode_semester
inner join dim_matakuliah mm on mmm.kode_matakuliah = mm.kode_matakuliah
where mmm.mitra not in
          (select distinct mitra from mbkm_matkul_monev
              where mitra LIKE 'Prodi%%' or mitra in('MKH','Informatika'))
order by semester ASC''', con)


def getTotalMhsMbkm():
    return pd.read_sql('''
    select distinct concat(ds.semester_nama,' ',ds.tahun_ajaran) Semester,
                mbkm_matkul_monev.kode_semester,
                count(distinct id_mahasiswa) as jumlah_mhs_mbkm
from mbkm_matkul_monev
inner join dim_semester ds on mbkm_matkul_monev.kode_semester = ds.kode_semester
group by mbkm_matkul_monev.kode_semester, semester,tahun_ajaran
order by kode_semester asc ''', con)

def getTotalMhsAktifPerSemester():
    return pd.read_sql('''
    select ds.tahun_ajaran 'Tahun Ajaran', ds.semester_nama Semester,ds.kode_semester,
       dmhs.tahun_angkatan,
    count(*) as 'Jumlah Mahasiswa Aktif' from fact_mahasiswa_status fms
inner join dim_mahasiswa dmhs on fms.id_mahasiswa = dmhs.id_mahasiswa
inner join dim_semester ds on ds.id_semester = fms.id_semester
where fms.status = 'AK'
group by ds.tahun_ajaran, ds.semester_nama,dmhs.tahun_angkatan,kode_semester
order by ds.tahun_ajaran, ds.semester_nama''', con)

def getListSemester():
    return pd.read_sql('''select distinct concat(ds.semester_nama,' ',ds.tahun_ajaran) Semester, ds.kode_semester
from mbkm_matkul_monev
inner join dim_semester ds on mbkm_matkul_monev.kode_semester = ds.kode_semester
group by mbkm_matkul_monev.kode_semester, semester,tahun_ajaran,ds.kode_semester
order by tahun_ajaran asc
    ''', con)


def getRawDataMBKM():
    return pd.read_sql('''select kode_matakuliah,mitra,id_mahasiswa,concat(ds.semester_nama,' ',ds.tahun_ajaran) Semester,ds.kode_semester
from mbkm_matkul_monev
inner join dim_semester ds on mbkm_matkul_monev.kode_semester = ds.kode_semester
group by Semester,kode_matakuliah,mitra,id_mahasiswa,tahun_ajaran,ds.kode_semester
order by tahun_ajaran
        ''', con)


def getRawDataMhsAktif():
    return pd.read_sql('''select concat(ds.semester_nama,' ',ds.tahun_ajaran) Semester,ds.kode_semester,
    count(*) as 'Jumlah Mahasiswa Aktif' from fact_mahasiswa_status fms
inner join dim_mahasiswa dmhs on fms.id_mahasiswa = dmhs.id_mahasiswa
inner join dim_semester ds on ds.id_semester = fms.id_semester
where fms.status = 'AK'
group by ds.tahun_ajaran, ds.semester_nama,Semester,kode_semester
order by ds.tahun_ajaran, ds.semester_nama''', con)


def getRawDataRerataMBKM():
    return pd.read_sql('''select mbm.kode_matakuliah,
       dm.sks,
       mitra,
       id_mahasiswa,
       mbm.kode_semester,
       concat(ds.semester_nama,' ',ds.tahun_ajaran) Semester
    from mbkm_matkul_monev mbm
         inner join dim_semester ds on mbm.kode_semester = ds.kode_semester
         inner join dim_matakuliah dm on mbm.kode_matakuliah = dm.kode_matakuliah
    where ds.tahun_ajaran between
    '2019/2020' and '2021/2022'
    group by mbm.kode_semester, Semester,mbm.kode_matakuliah,sks,mitra,id_mahasiswa
    order by mbm.kode_semester''', con)
