import numpy as np
import pandas as pd
import streamlit as st
import pickle

# Load model
model_prediksi = pickle.load(open('modelCB_terbaik.sav', 'rb'))

# Custom CSS untuk latar belakang dan elemen UI
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #e0f7fa, #ffffff);
        }
        .stApp {
            background: linear-gradient(to right, #e0f7fa, #ffffff);
        }
        h1 {
            color: #0d47a1 !important;  /* Menambahkan warna biru gelap untuk judul */
        }
        h2, h3, h4, h5, h6 {
            color: #0d47a1;  /* Menambahkan warna biru gelap untuk sub-judul */
        }
        .stMarkdown {
            color: #0d47a1;  /* Ubah warna teks markdown */
        }
        .stSelectbox label, .stNumberInput label, .stTextInput label {
            font-weight: bold;
            color: #0d47a1;  /* Ubah warna label input */
        }
        .stButton button {
            background-color: #0d47a1;
            color: white;
        }
        .stButton button:hover {
            background-color: #1565c0;
        }
    </style>
""", unsafe_allow_html=True)

# Judul
st.title("Prediksi Status Gizi Balita")
st.markdown("Silakan isi data berikut untuk mengetahui prediksi status gizi balita.")

# Kolom input (2 kolom)
col1, col2 = st.columns(2)

import re

# Fungsi validasi untuk input angka desimal seperti 97.2, 56.0, 2.3, dll.
def validate_input(value):
    pattern = r"^\d+(\.\d+)?$"  # Memastikan formatnya angka atau angka desimal
    if re.match(pattern, value):
        return True
    else:
        return False

with col1:
    Jenis_Kelamin = st.selectbox("Pilih Jenis Kelamin", ["", "Laki-laki", "Perempuan"])
    Usia = st.text_input("Masukkan Usia (bulan)", help="Masukkan usia dalam bulan, misalnya 6, 12, 24.")
    if Usia and not validate_integer(Usia):
        st.error("Harap masukkan usia yang valid dalam bulan (angka bulat).")
    
    Berat_Badan_Lahir = st.text_input("Berat Badan Lahir (kg)", help="Contoh: 2.5, 3.0, 3.2")
    if Berat_Badan_Lahir and not validate_input(Berat_Badan_Lahir):
        st.error("Harap masukkan nilai yang valid untuk Berat Badan Lahir, misalnya 2.5, 3.0, 3.2.")
    
    Tinggi_Badan_Lahir = st.text_input("Tinggi Badan Lahir (cm)", help="Contoh: 48.0, 49.1, 50.0")
    if Tinggi_Badan_Lahir and not validate_input(Tinggi_Badan_Lahir):
        st.error("Harap masukkan nilai yang valid untuk Tinggi Badan Lahir, misalnya 48.0, 49.1, 50.0.")

with col2:
    Berat_Badan = st.text_input("Berat Badan Saat Ini (kg)", help="Contoh: 8.0, 9.2, 10.5")
    if Berat_Badan and not validate_input(Berat_Badan):
        st.error("Harap masukkan nilai yang valid untuk Berat Badan, misalnya 8.0, 9.2, 10.5.")
    
    Tinggi_Badan = st.text_input("Tinggi Badan Saat Ini (cm)", help="Contoh: 70.0, 72.5, 75.1")
    if Tinggi_Badan and not validate_input(Tinggi_Badan):
        st.error("Harap masukkan nilai yang valid untuk Tinggi Badan, misalnya 70.0, 72.5, 75.1.")
    Status_Pemberian_ASI = st.selectbox("Status Pemberian ASI", ["", "Ya", "Tidak"])
    Status_Tinggi_Badan = st.selectbox("Kondisi Tinggi Badan Saat Ini", ["", "Sangat pendek", "Pendek", "Normal", "Tinggi"])
    Status_Berat_Badan = st.selectbox("Kondisi Berat Badan Saat Ini", ["", "Berat badan sangat kurang", "Berat badan kurang", "Berat badan normal", "Risiko berat badan lebih"])


# Mapping
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

# Tombol Prediksi
if st.button("Tampilkan Hasil Prediksi"):
    if "" in (Jenis_Kelamin, Status_Pemberian_ASI, Status_Tinggi_Badan, Status_Berat_Badan):
        st.warning("Mohon lengkapi semua pilihan terlebih dahulu.")
    else:
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
