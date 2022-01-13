import pandas as pd
from sqlalchemy import create_engine

con = create_engine('mysql+pymysql://sharon:TAhug0r3ng!@localhost:3333/datawarehouse')

def getDataFrameFromDB(query):
    return pd.read_sql(query, con)

def getDataFrameFromDBwithParams(query, parameter):
    return pd.read_sql(query, con, params=parameter)

def getMasaTunggu():
    return pd.read_sql('''select data2.*, lulusan.jumlah as "Lulusan", terlacak.jumlah as "Lulusan Terlacak" from
 (
    select tahun_lulus,
    SUM(IF( waktu_tunggu = "KURANG 6 BULAN", data.jumlah, 0)) AS "<6 BULAN",
    SUM(IF( waktu_tunggu = "6 - 18 BULAN", data.jumlah, 0)) AS "6-18 BULAN",
    SUM(IF( waktu_tunggu = "LEBIH 18 BULAN", data.jumlah, 0)) AS ">18 BULAN",
    SUM(IF( waktu_tunggu = "LAINNYA", data.jumlah, 0)) AS "LAINNYA"
    from (
        select count(*) as jumlah, ifnull(waktu_tunggu,"LAINNYA") as waktu_tunggu,tahun_lulus
        from fact_tracer_study fact
        inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
        group by waktu_tunggu ,tahun_lulus
        order by tahun_lulus desc
    ) data
    group by tahun_lulus
    order by tahun_lulus
) data2
left join (
    select count(id_mahasiswa) as jumlah, tahun_lulus
    from (select *, if(semester_yudisium = 'GENAP', substr(tahun_ajaran_yudisium,6,4),substr(tahun_ajaran_yudisium,1,4)) as tahun_lulus
    from fact_yudisium) data
    group by tahun_lulus
)lulusan on lulusan.tahun_lulus = data2.tahun_lulus
left join(
    select count(id_mahasiswa) as jumlah, tahun_lulus
    from dim_lulusan
    group by tahun_lulus
)terlacak on terlacak.tahun_lulus = data2.tahun_lulus
order by tahun_lulus;''', con)


def getBidangKerja():
    return pd.read_sql('''
select data2.tahun_lulus as "Tahun Lulus", 
        TINGGI as 'Tinggi', SEDANG as 'Sedang', RENDAH as 'Rendah', LAINNYA as 'Lainnya',
        lulusan.jumlah as "Lulusan", terlacak.jumlah as "Lulusan Terlacak" 
 from
 (
    select tahun_lulus,
        SUM(IF( tingkat_kesesuaian_bidang_kerja = "TINGGI", data.jumlah, 0)) AS "TINGGI",
        SUM(IF( tingkat_kesesuaian_bidang_kerja = "SEDANG", data.jumlah, 0)) AS "SEDANG",
        SUM(IF( tingkat_kesesuaian_bidang_kerja = "RENDAH", data.jumlah, 0)) AS "RENDAH",
        SUM(IF( tingkat_kesesuaian_bidang_kerja = "LAINNYA", data.jumlah, 0)) AS "LAINNYA"
    from (
        select count(*) as jumlah, ifnull(tingkat_kesesuaian_bidang_kerja,"LAINNYA") as tingkat_kesesuaian_bidang_kerja,tahun_lulus
        from fact_tracer_study fact
        inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
        group by tahun_lulus,tingkat_kesesuaian_bidang_kerja
        order by tahun_lulus asc
        )data
        group by tahun_lulus
) data2
left join (
    select count(id_mahasiswa) as jumlah, tahun_lulus
    from (select *, if(semester_yudisium = 'GENAP', substr(tahun_ajaran_yudisium,6,4),substr(tahun_ajaran_yudisium,1,4)) as tahun_lulus
    from fact_yudisium) data
    group by tahun_lulus
)lulusan on lulusan.tahun_lulus = data2.tahun_lulus
left join(
    select count(id_mahasiswa) as jumlah, tahun_lulus
    from dim_lulusan
    inner join fact_tracer_study on dim_lulusan.id_lulusan = fact_tracer_study.id_lulusan
    group by tahun_lulus
)terlacak on terlacak.tahun_lulus = data2.tahun_lulus
order by data2.tahun_lulus''', con)


def getTempatKerja():
    return pd.read_sql('''
select data2.tahun_lulus as 'Tahun Lulus', Lokal+Regional as 'Lokal/Regional', Nasional, Internasional, lulusan.jumlah as "Lulusan", terlacak.jumlah as "Lulusan Terlacak" from
 (
    select tahun_lulus,
    SUM(IF( wilayah = 1, data.jumlah, 0)) AS "Lokal",
    SUM(IF( wilayah = 2, data.jumlah, 0)) AS "Regional",
    SUM(IF( wilayah = 3, data.jumlah, 0)) AS "Nasional",
    SUM(IF( wilayah = 4, data.jumlah, 0)) AS "Internasional"
    from
    (
        select tahun_lulus,count(*) jumlah, wilayah
        from fact_tracer_study tracer
        inner join dim_lulusan on tracer.id_lulusan = dim_lulusan.id_lulusan
        inner join dim_organisasi_pengguna_lulusan org on dim_lulusan.id_organisasi_pengguna_lulusan = org.id_organisasi_pengguna_lulusan
        group by tahun_lulus,wilayah
    )data
    group by tahun_lulus
) data2
left join (
    select count(id_mahasiswa) as jumlah, tahun_lulus
    from (select *, if(semester_yudisium = 'GENAP', substr(tahun_ajaran_yudisium,6,4),substr(tahun_ajaran_yudisium,1,4)) as tahun_lulus
    from fact_yudisium) data
    group by tahun_lulus
)lulusan on lulusan.tahun_lulus = data2.tahun_lulus
left join(
    select count(id_mahasiswa) as jumlah, tahun_lulus
    from dim_lulusan
    group by tahun_lulus
)terlacak on terlacak.tahun_lulus = data2.tahun_lulus
order by terlacak.tahun_lulus''', con)


def getSkill():
    return pd.read_sql('''
select kriteria as Kriteria, 
    SANGATBAIK+BAIK+CUKUP+KURANG+LAINNYA as Jumlah, 
    concat(round(SANGATBAIK/(SANGATBAIK+BAIK+CUKUP+KURANG)*100,2),'%') as "Sangat Baik",
    concat(round(BAIK/(SANGATBAIK+BAIK+CUKUP+KURANG)*100,2),'%') as "Baik",
    concat(round(CUKUP/(SANGATBAIK+BAIK+CUKUP+KURANG)*100,2),'%') as "Cukup",
    concat(round(KURANG/(SANGATBAIK+BAIK+CUKUP+KURANG)*100,2),'%') as "Kurang"
    from (
    select "1" as nomor, "INTEGRITAS" as kriteria, 
    sum(case when integritas = "SANGAT BAIK" then jumlah end) as "SANGATBAIK",
    sum(case when integritas = "BAIK" then jumlah end) as "BAIK",
    sum(case when integritas = "CUKUP" then jumlah end) as "CUKUP",
    sum(case when integritas = "KURANG" then jumlah end) as "KURANG",
    sum(case when integritas = "LAINNYA" then jumlah end) as "LAINNYA"
    from(
        select ifnull(integritas, 'LAINNYA') as integritas, count(*) jumlah
        from fact_kepuasan_pengguna_lulusan fact
        inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
        group by integritas
    ) as data
    union all
    select  "2" as nomor, "KEAHLIAN BIDANG ILMU" as keahlian_bidang_ilmu, 
    sum(case when keahlian_bidang_ilmu = "SANGAT BAIK" then jumlah end) as "SANGATBAIK",
    sum(case when keahlian_bidang_ilmu = "BAIK" then jumlah end) as "BAIK",
    sum(case when keahlian_bidang_ilmu = "CUKUP" then jumlah end) as "CUKUP",
    sum(case when keahlian_bidang_ilmu = "KURANG" then jumlah end) as "KURANG",
    sum(case when keahlian_bidang_ilmu = "LAINNYA" then jumlah end) as "LAINNYA"
    from(
        select ifnull(keahlian_bidang_ilmu, 'LAINNYA') as keahlian_bidang_ilmu, count(*) jumlah
        from fact_kepuasan_pengguna_lulusan fact
        inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
        group by keahlian_bidang_ilmu
    ) as data
    union all
    select  "3" as nomor, "KEMAMPUAN BAHASA ASING" as Kriteria, 
    sum(case when kemampuan_bahasa_asing = "SANGAT BAIK" then jumlah end) as "SANGATBAIK",
    sum(case when kemampuan_bahasa_asing = "BAIK" then jumlah end) as "BAIK",
    sum(case when kemampuan_bahasa_asing = "CUKUP" then jumlah end) as "CUKUP",
    sum(case when kemampuan_bahasa_asing = "KURANG" then jumlah end) as "KURANG",
    sum(case when kemampuan_bahasa_asing = "LAINNYA" then jumlah end) as "LAINNYA"
    from(
        select ifnull(kemampuan_bahasa_asing, 'LAINNYA') as kemampuan_bahasa_asing, count(*) jumlah
        from fact_kepuasan_pengguna_lulusan fact
        inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
        group by kemampuan_bahasa_asing
    ) as data
    union all
    select  "4" as nomor,  "PENGGUNAAN TEKNOLOGI INFORMASI" as Kriteria, 
    sum(case when penggunaan_teknologi = "SANGAT BAIK" then jumlah end) as "SANGATBAIK",
    sum(case when penggunaan_teknologi = "BAIK" then jumlah end) as "BAIK",
    sum(case when penggunaan_teknologi = "CUKUP" then jumlah end) as "CUKUP",
    sum(case when penggunaan_teknologi = "KURANG" then jumlah end) as "KURANG",
    sum(case when penggunaan_teknologi = "LAINNYA" then jumlah end) as "LAINNYA"
    from(
        select ifnull(penggunaan_teknologi, 'LAINNYA') as penggunaan_teknologi, count(*) jumlah
        from fact_kepuasan_pengguna_lulusan fact
        inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
        group by penggunaan_teknologi
    ) as data
    union all
    select  "5" as nomor,  "KOMUNIKASI" as komunikasi, 
    sum(case when komunikasi = "SANGAT BAIK" then jumlah end) as "SANGATBAIK",
    sum(case when komunikasi = "BAIK" then jumlah end) as "BAIK",
    sum(case when komunikasi = "CUKUP" then jumlah end) as "CUKUP",
    sum(case when komunikasi = "KURANG" then jumlah end) as "KURANG",
    sum(case when komunikasi = "LAINNYA" then jumlah end) as "LAINNYA"
    from(
        select ifnull(komunikasi, 'LAINNYA') as komunikasi, count(*) jumlah
        from fact_kepuasan_pengguna_lulusan fact
        inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
        group by komunikasi
    ) as data
    union all
    select  "6" as nomor, "KERJASAMA TIM" as kerjasama_tim, 
    sum(case when kerjasama_tim = "SANGAT BAIK" then jumlah end) as "SANGATBAIK",
    sum(case when kerjasama_tim = "BAIK" then jumlah end) as "BAIK",
    sum(case when kerjasama_tim = "CUKUP" then jumlah end) as "CUKUP",
    sum(case when kerjasama_tim = "KURANG" then jumlah end) as "KURANG",
    sum(case when kerjasama_tim = "LAINNYA" then jumlah end) as "LAINNYA"
    from(
        select ifnull(kerjasama_tim, 'LAINNYA') as kerjasama_tim, count(*) jumlah
        from fact_kepuasan_pengguna_lulusan fact
        inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
        group by kerjasama_tim
    ) as data
    union all
    select "7" as nomor, "PENGEMBANGAN DIRI" as Kriteria, 
    sum(case when pengembangan_diri = "SANGAT BAIK" then jumlah end) as "SANGATBAIK",
    sum(case when pengembangan_diri = "BAIK" then jumlah end) as "BAIK",
    sum(case when pengembangan_diri = "CUKUP" then jumlah end) as "CUKUP",
    sum(case when pengembangan_diri = "KURANG" then jumlah end) as "KURANG",
    sum(case when pengembangan_diri = "LAINNYA" then jumlah end) as "LAINNYA"
    from(
        select ifnull(pengembangan_diri, 'LAINNYA') as pengembangan_diri, count(*) jumlah
        from fact_kepuasan_pengguna_lulusan fact
        inner join dim_lulusan on dim_lulusan.id_lulusan = fact.id_lulusan
        group by pengembangan_diri
    ) as data
) dataJumlah
order by nomor''', con)


def getJabatan():
    return pd.read_sql('''
select 
count(*) as Jumlah, 
ifnull(posisi_jabatan_alumni,'LAINNYA') as Posisi, 
posisi_jabatan_alumni as 'Jabatan Alumni'
from fact_tracer_study tracer
inner join dim_lulusan on dim_lulusan.id_lulusan = tracer.id_lulusan
where dim_lulusan.tahun_lulus='2015'
group by posisi, posisi_jabatan_alumni
order by posisi_jabatan_alumni desc
''', con)

def getPerusahaan():
    return pd.read_sql('''
select nama_mapping_organisasi as 'Nama Perusahaan', count(*) as 'Jumlah Lulusan'
from fact_tracer_study tracer
inner join dim_lulusan on tracer.id_lulusan = dim_lulusan.id_lulusan
inner join dim_organisasi_pengguna_lulusan org on dim_lulusan.id_organisasi_pengguna_lulusan = org.id_organisasi_pengguna_lulusan
where dim_lulusan.tahun_lulus='2015'
group by nama_mapping_organisasi
order by 'Jumlah Lulusan' desc
limit 15''', con)
