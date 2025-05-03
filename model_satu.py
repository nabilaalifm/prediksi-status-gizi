import pickle
import numpy as np
import pandas as pd
import streamlit as st

# Membaca model
model_prediksi = pickle.load(open(r"D:\Prediksi Status Gizi\modelCB_terbaik.sav", "rb"))

# Judul Website
st.title('Prediksi Status Gizi Balita')

st.markdown('Silakan isi data berikut:')

# Inputan pengguna
Jenis_Kelamin = st.selectbox('Pilih Jenis Kelamin', ['Laki-laki', 'Perempuan'])

Usia = st.number_input('Masukkan Nilai Usia (bulan)', min_value=0)

Berat_Badan_Lahir = st.number_input('Masukkan Nilai Berat Badan Lahir (kg)',min_value=0.0, step=0.1, format="%.1f")

Tinggi_Badan_Lahir = st.number_input('Masukkan Nilai Tinggi Badan Lahir (cm)', min_value=0.0, step=0.1, format="%.1f")

Berat_Badan = st.number_input('Masukkan Nilai Berat Badan Saat Ini (kg)', min_value=0.0, step=0.1, format="%.1f")

Tinggi_Badan = st.number_input('Masukkan Nilai Tinggi Badan Saat Ini (cm)', min_value=0.0, step=0.1, format="%.1f")

Status_Pemberian_ASI = st.selectbox('Pilih Status Pemberian ASI', ['Ya', 'Tidak'])

Status_Tinggi_Badan = st.selectbox('Pilih Kondisi Tinggi Badan Balita Saat Ini', ['Sangat pendek', 'Pendek', 'Normal', 'Tinggi'])

Status_Berat_Badan = st.selectbox('Pilih Kondisi Berat Badan Balita Saat Ini', ['Berat badan sangat kurang', 'Berat badan kurang', 'Berat badan normal', 'Risiko berat badan lebih'])

# Mapping input ke angka sesuai model training
jenis_kelamin_map = {'Laki-laki': 0, 'Perempuan': 1}
asi_map = {'Tidak': 0, 'Ya': 1}
berat_badan_map = {
    'Berat badan kurang': 0,
    'Berat badan normal': 1,
    'Berat badan sangat kurang': 2,
    'Risiko berat badan lebih': 3
}
tinggi_badan_map = {
    'Normal': 0,
    'Pendek': 1,
    'Sangat pendek': 2,
    'Tinggi': 3
}
status_gizi_map = {
    0: 'Berisiko gizi lebih',
    1: 'Gizi baik',
    2: 'Gizi buruk',
    3: 'Gizi kurang',
    4: 'Gizi lebih',
    5: 'Obesitas'
}

# Tombol prediksi
if st.button('Tampilkan Hasil Prediksi'):
    input_data = [[
        jenis_kelamin_map[Jenis_Kelamin],
        Usia,
        Berat_Badan_Lahir,
        Tinggi_Badan_Lahir,
        Berat_Badan,
        Tinggi_Badan,
        asi_map[Status_Pemberian_ASI],
        tinggi_badan_map[Status_Tinggi_Badan],
        berat_badan_map[Status_Berat_Badan]
    ]]

    hasil = model_prediksi.predict(input_data)
    gizi_diagnosis = status_gizi_map[int(hasil[0])]
    
    st.success(f"Hasil Prediksi Status Gizi Balita: **{gizi_diagnosis}**")
