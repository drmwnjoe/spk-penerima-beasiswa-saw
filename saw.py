import pandas as pd

# =========================
# MEMBACA FILE CSV
# =========================

df = pd.read_csv(
    r"D:\tugas kuliah joe\SPK\Tabel Tugas 2 Daftar Usulan Penerima Beasiswa.csv",
    header=None
)

# =========================
# MEMBERI NAMA KOLOM
# =========================

df.columns = [
    'No',
    'NIM',
    'Nama Mahasiswa',
    'Alamat',
    'IPK',
    'Semester',
    'Pekerjaan Orang Tua',
    'Penghasilan Orang Tua',
    'Jumlah Tanggungan Orang Tua'
]

# =========================
# HAPUS BARIS TIDAK VALID
# =========================

# hapus judul tabel
df = df[df['No'] != 'Tabel Data Usulan Penerima Beasiswa']

# hapus header yang muncul di bawah
df = df[df['No'] != 'No']

# reset index
df = df.reset_index(drop=True)

# =========================
# MEMBERSIHKAN PENGHASILAN
# =========================

df['Penghasilan Orang Tua'] = (
    df['Penghasilan Orang Tua']
    .astype(str)
    .str.replace('Rp.', '', regex=False)
    .str.replace('.', '', regex=False)
    .str.replace(',', '', regex=False)
    .str.strip()
)

# =========================
# KONVERSI NUMERIK
# =========================

df['Penghasilan Orang Tua'] = pd.to_numeric(
    df['Penghasilan Orang Tua'],
    errors='coerce'
)

df['IPK'] = pd.to_numeric(
    df['IPK'],
    errors='coerce'
)

df['Jumlah Tanggungan Orang Tua'] = pd.to_numeric(
    df['Jumlah Tanggungan Orang Tua'],
    errors='coerce'
)

# hapus data kosong
df = df.dropna()

# =========================
# NORMALISASI BENEFIT
# =========================

# IPK
df['N_IPK'] = (
    df['IPK'] / df['IPK'].max()
)

# Tanggungan
df['N_Tanggungan'] = (
    df['Jumlah Tanggungan Orang Tua'] /
    df['Jumlah Tanggungan Orang Tua'].max()
)

# =========================
# NORMALISASI COST
# =========================

# Penghasilan
df['N_Penghasilan'] = (
    df['Penghasilan Orang Tua'].min() /
    df['Penghasilan Orang Tua']
)

# =========================
# BOBOT KRITERIA
# =========================

w_ipk = 0.50
w_penghasilan = 0.30
w_tanggungan = 0.20

# =========================
# HITUNG SKOR SAW
# =========================

df['Skor_SAW'] = (
    (w_ipk * df['N_IPK']) +
    (w_penghasilan * df['N_Penghasilan']) +
    (w_tanggungan * df['N_Tanggungan'])
)

# =========================
# SORTING RANKING
# =========================

df = df.sort_values(
    by='Skor_SAW',
    ascending=False
)

# ranking
df['Ranking'] = range(1, len(df) + 1)

# =========================
# TAMPILKAN HASIL
# =========================

hasil = df[[
    'Ranking',
    'NIM',
    'Nama Mahasiswa',
    'IPK',
    'Penghasilan Orang Tua',
    'Jumlah Tanggungan Orang Tua',
    'Skor_SAW'
]]

# menampilkan semua kolom
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print("\nHASIL RANKING PENERIMA BEASISWA")
print(hasil)

print("\nTOP 5 PRIORITAS PENERIMA BEASISWA")
print(hasil.head(5))