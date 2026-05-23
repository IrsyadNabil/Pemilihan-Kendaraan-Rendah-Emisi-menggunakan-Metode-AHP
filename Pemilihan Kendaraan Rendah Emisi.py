import numpy as np
import pandas as pd

data = pd.read_csv('CO2 Emissions_Canada.csv')
print(f"Total data: {len(data)} kendaraan")
print(f"Kolom: {data.columns.tolist()}")
data

kriteria = [
    'Emisi CO2 per km (g/km)', 
    'Konsumsi BBM Comb (L/100km)', 
    'Konsumsi BBM Hwy (L/100km)',
    'MPG (Miles Per Gallon)',
    'Ukuran Mesin (cc)', 
    'Jumlah Silinder', 
]

tipe_kriteria = [ 'cost', 'cost', 'cost', 'benefit', 'cost', 'cost' ]

print("Kriteria yang digunakan:")
for i, kriteria_name in enumerate(kriteria, start=1):
    print(f"{i}. {kriteria_name} ({tipe_kriteria[i-1]})")
    
    
matriks_perbandingan = np.array([
    [1,   2,   3,   3,   5,   7],
    [1/2, 1,   2,   2,   4,   5],
    [1/3, 1/2, 1,   2,   3,   4],
    [1/3, 1/2, 1/2, 1,   3,   4],
    [1/5, 1/4, 1/3, 1/3, 1,   2],
    [1/7, 1/5, 1/4, 1/4, 1/2, 1]
    
])

df_kriteria = pd.DataFrame(np.round(matriks_perbandingan, 2), columns=kriteria, index=kriteria)
df_kriteria

jumlah_kolom = matriks_perbandingan.sum(axis=0)
normalisasi_kriteria = matriks_perbandingan / jumlah_kolom

df_normalisasi = pd.DataFrame(
    np.round(normalisasi_kriteria, 4), 
    columns=kriteria, 
    index=kriteria
)

df_normalisasi

bobot_kriteria = normalisasi_kriteria.mean(axis=1)

df_bobot = pd.DataFrame(
    {'Bobot': np.round(bobot_kriteria, 4),
     'Bobot(%)': np.round(bobot_kriteria * 100, 2)},
    index=kriteria
)
df_bobot

n = len(kriteria)
hasil_kali = np.dot(matriks_perbandingan, bobot_kriteria)
lambda_max = np.mean(hasil_kali / bobot_kriteria)
ci = (lambda_max - n) / (n - 1)
ri = 1.24
cr = ci / ri

print(f"Lambda max             : {lambda_max:.4f}")
print(f"Consistency Index (CI) : {ci:.4f}")
print(f"Consistency Ratio (CR) : {cr:.4f}")

if cr < 0.1:
    print("Matriks perbandingan konsisten.")
else:
    print("Matriks perbandingan tidak konsisten. Perlu diperbaiki.")
    
    
## Persiapan Data Alternatif dari Dataset

# Mapping kolom dataset ke nama kriteria
kolom_dataset = [
    'CO2 Emissions(g/km)',
    'Fuel Consumption Comb (L/100 km)',
    'Fuel Consumption Hwy (L/100 km)',
    'Fuel Consumption Comb (mpg)',
    'Engine Size(L)',
    'Cylinders',
]

# Buat label unik tiap kendaraan (Make + Model + index)
data['Nama_Kendaraan'] = data['Make'] + ' ' + data['Model'] + ' (' + data.index.astype(str) + ')'

# Ambil kolom yang diperlukan dan rename sesuai nama kriteria
data_alternatif = data[['Nama_Kendaraan'] + kolom_dataset].copy()
data_alternatif = data_alternatif.set_index('Nama_Kendaraan')
data_alternatif.columns = kriteria

print(f"Total alternatif kendaraan: {len(data_alternatif)}")
data_alternatif.head()

## Normalisasi Data Alternatif (SAW)
# - cost    : min(kolom) / nilai  → nilai kecil = skor mendekati 1
# - benefit : nilai / max(kolom)  → nilai besar = skor mendekati 1
# Khusus BBM Hwy (benefit): tetap pakai min/x karena
#   nilai L/100km kecil = lebih hemat = lebih baik

def normalisasi_saw(df, tipe_kriteria):
    df_norm = df.copy().astype(float)
    for i, col in enumerate(df.columns):
        if tipe_kriteria[i] == 'cost':
            df_norm[col] = df[col].min() / df[col]
        else:  # benefit
            if 'Hwy' in col or 'L/100' in col:
                # Benefit tapi satuan cost (L/100km): balik dengan min/x
                df_norm[col] = df[col].min() / df[col]
            else:
                df_norm[col] = df[col] / df[col].max()
    return df_norm

data_normalisasi = normalisasi_saw(data_alternatif, tipe_kriteria)

print("Data setelah normalisasi (nilai 0-1):")
print("Semua nilai harus berada di rentang 0 hingga 1:")
print(f"  Min: {data_normalisasi.min().min():.4f}")
print(f"  Max: {data_normalisasi.max().max():.4f}")
print()
data_normalisasi.head()

## hitung skor akhir dengan metode ahp

skor_akhir = data_normalisasi.dot(bobot_kriteria)

df_hasil = pd.DataFrame({
    'Nama Kendaraan': data_normalisasi.index,
    'Skor Akhir': skor_akhir
}).sort_values(by='Skor Akhir', ascending=False)

# tambahkan data asli untuk referensi
df_hasil['CO2 (g/km)'] = data_alternatif['Emisi CO2 per km (g/km)'].values
df_hasil['Konsumsi BBM Comb (L/100km)'] = data_alternatif['Konsumsi BBM Comb (L/100km)'].values
df_hasil['Konsumsi BBM Hwy (L/100km)'] = data_alternatif['Konsumsi BBM Hwy (L/100km)'].values
df_hasil['MPG (Miles Per Gallon)'] = data_alternatif['MPG (Miles Per Gallon)'].values
df_hasil['Ukuran Mesin (cc)'] = data_alternatif['Ukuran Mesin (cc)'].values
df_hasil['Jumlah Silinder'] = data_alternatif['Jumlah Silinder'].values

# ranking
df_hasil = df_hasil.sort_values(by='Skor Akhir', ascending=False).reset_index(drop=True)
df_hasil.index += 1  # mulai index dari 1 untuk ranking
df_hasil.index.name = 'Ranking'
df_hasil['Ranking'] = df_hasil['Skor Akhir'].rank(ascending=False).astype(int)

print(f"Total kendaraan yang diranking: {len(df_hasil)}")
print("\nTop 20 Kendaraan Rendah Emisi:")
df_hasil.head(20)

# tampilkan rekomendasi top 10

print("╔══════════════════════════════════════════════════════════════════════════╗")
print("║         REKOMENDASI TOP 10 KENDARAAN RENDAH EMISI (AHP)                  ║")
print("╚══════════════════════════════════════════════════════════════════════════╝")
print()

for i, row in df_hasil.head(10).iterrows():
    nama = row['Nama Kendaraan'].rsplit('(', 1)[0]
    print(f"Rank #{i:2d} | {nama}")
    print(f"           Skor Akhir: {row['Skor Akhir']:.4f}")
    print(f"           Emisi CO2: {row['CO2 (g/km)']} g/km")
    print(f"           Konsumsi BBM Comb: {row['Konsumsi BBM Comb (L/100km)']} L/100km")
    print(f"           Konsumsi BBM Hwy: {row['Konsumsi BBM Hwy (L/100km)']} L/100km")
    print(f"           MPG: {row['MPG (Miles Per Gallon)']} mpg")
    print(f"           Ukuran Mesin: {row['Ukuran Mesin (cc)']} cc")
    print(f"           Jumlah Silinder: {row['Jumlah Silinder']}")
    print("-" * 80)
    
    # simpan hasil ke file csv

df_export = df_hasil.copy()
df_export['Nama Kendaraan'] = df_export['Nama Kendaraan'].str.rsplit('(',n=1).str[0]
df_export.to_csv('hasil_ranking_kendaraan_rendah_emisi.csv')

print("Hasil ranking kendaraan rendah emisi telah disimpan ke 'hasil_ranking_kendaraan_rendah_emisi.csv'")