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
