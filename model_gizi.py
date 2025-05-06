import numpy as np
import pandas as pd
import streamlit as st
import pickle
import re

# Load model
model_prediksi = pickle.load(open('modelCB_terbaik.sav', 'rb'))

# Custom CSS
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to right, #e0f7fa, #ffffff);
        }
        h1, h2, h3, h4, h5, h6, .stMarkdown {
            color: #0d47a1;
        }
        .stSelectbox label, .stTextInput label {
            font-weight: bold;
            color: #0d47a1;
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

# Fungsi validasi angka desimal dengan koma
def validate_input(value):
    return re.match(r"^\d+,\d+$", value)

# Fungsi konversi koma ke titik
def format_decimal(angka_str):
    return float(angka_str.replace(",", "."))

# Judul dan Instruksi
st.title("Prediksi Status Gizi Balita")
st.markdown("""
Silakan isi data berikut untuk mengetahui prediksi status gizi balita.  
**Catatan:** Untuk pengisian nilai berat dan tinggi badan, gunakan format **angka desimal dengan koma (,).**  
Contoh: `3,4`, `45,0`, `72,3`
""")

col1, col2 = st.columns(2)

with col1:
    Jenis_Kelamin = st.selectbox("Pilih Jenis Kelamin", ["", "Laki-laki", "Perempuan"])
    Usia = st.text_input("Masukkan Usia (bulan)")
    if Usia and not Usia.isdigit():
        st.error("Usia harus berupa angka bulat, misalnya: 12")

    Berat_Badan_Lahir = st.text_input("Berat Badan Lahir (kg)")
    if Berat_Badan_Lahir and not validate_input(Berat_Badan_Lahir):
        st.error("Contoh input valid: 3,2")

    Tinggi_Badan_Lahir = st.text_input("Tinggi Badan Lahir (cm)")
    if Tinggi_Badan_Lahir and not validate_input(Tinggi_Badan_Lahir):
        st.error("Contoh input valid: 48,5")

with col2:
    Berat_Badan = st.text_input("Berat Badan Saat Ini (kg)")
    if Berat_Badan and not validate_input(Berat_Badan):
        st.error("Contoh input valid: 8,5")

    Tinggi_Badan = st.text_input("Tinggi Badan Saat Ini (cm)")
    if Tinggi_Badan and not validate_input(Tinggi_Badan):
        st.error("Contoh input valid: 72,3")

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

# Tombol prediksi
if st.button("Tampilkan Hasil Prediksi"):
    if "" in (Jenis_Kelamin, Usia, Berat_Badan_Lahir, Tinggi_Badan_Lahir, Berat_Badan, Tinggi_Badan, Status_Pemberian_ASI, Status_Tinggi_Badan, Status_Berat_Badan):
        st.warning("Mohon lengkapi semua input terlebih dahulu.")
    else:
        try:
            input_data = [[
                jenis_kelamin_map[Jenis_Kelamin],
                int(Usia),
                format_decimal(Berat_Badan_Lahir),
                format_decimal(Tinggi_Badan_Lahir),
                format_decimal(Berat_Badan),
                format_decimal(Tinggi_Badan),
                asi_map[Status_Pemberian_ASI],
                tinggi_badan_map[Status_Tinggi_Badan],
                berat_badan_map[Status_Berat_Badan]
            ]]
            hasil = model_prediksi.predict(input_data)
            gizi_diagnosis = status_gizi_map[int(hasil[0])]
            st.success(f"Hasil Prediksi Status Gizi Balita: **{gizi_diagnosis}**")
        except Exception as e:
            st.error("Terjadi kesalahan saat memproses data. Pastikan semua input valid.")
