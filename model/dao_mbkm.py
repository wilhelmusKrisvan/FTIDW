import pandas as pd
from sqlalchemy import create_engine

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')


def getDataFrameFromDB(query):
    return pd.read_sql(query, con)


def getDataFrameFromDBwithParams(query, parameter):
    return pd.read_sql(query, con, params=parameter)


def getMahasiswaMBKMperSemester():
    return pd.read_sql('''
    select (case
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
       count(distinct id_mahasiswa) Jumlah,
       kode_semester Semester
    from mbkm_matkul_monev
    group by kode_semester, Bentuk;''', con)


def getMitraMBKM():
    return pd.read_sql('''
    select distinct mitra Mitra from mbkm_matkul_monev;''', con)


def getJumlMitraMBKMperSemester():
    return pd.read_sql('''
    select ds.kode_semester, count(distinct mitra)
    from mbkm_matkul_monev
    inner join dim_semester ds on mbkm_matkul_monev.kode_semester = ds.kode_semester
    group by ds.kode_semester;
    ''')


def getDosbingMBKMperSemester():
    return pd.read_sql('''
    select tahun_ajaran 'Tahun Ajaran', semester_nama 'Semester', count(distinct dd.id_dosen) 'Jumlah Dosen'
    from mbkm_matkul_monev mbm
         inner join dim_semester ds on mbm.kode_semester = ds.kode_semester
         inner join dim_matakuliah dm on mbm.kode_matakuliah = dm.kode_matakuliah
         inner join fact_khs fk on dm.id_matakuliah = fk.id_matakuliah
         inner join fact_dosen_mengajar fdm on dm.id_matakuliah = fdm.id_matakuliah
         inner join dim_dosen dd on fdm.id_dosen = dd.id_dosen
    group by mbm.kode_semester, Semester, `Tahun Ajaran`
    order by `Tahun Ajaran`;''', con)


def getRerataSKSMBKMperSemester():
    return pd.read_sql('''
    select tahun_ajaran 'Tahun Ajaran', semester_nama 'Semester', count(sks) 'Jumlah SKS'
    from mbkm_matkul_monev mbm
         inner join dim_semester ds on mbm.kode_semester = ds.kode_semester
         inner join dim_matakuliah dm on mbm.kode_matakuliah = dm.kode_matakuliah
    group by mbm.kode_semester, Semester, `Tahun Ajaran`
    order by `Tahun Ajaran`;''', con)
