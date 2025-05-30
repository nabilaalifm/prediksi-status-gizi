import numpy as np
import pandas as pd
import streamlit as st
import pickle

# Load model
model_prediksi = pickle.load(open('modelCB_terbaik.sav', 'rb'))
model_knn = pickle.load(open('modelKNN_terbaik.sav', 'rb'))

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
            color: #0d47a1; 
        }
    </style>
""", unsafe_allow_html=True)

# Judul dan Instruksi
st.title("Prediksi Status Gizi Balita Menggunakan CatBoost dan KNN")
st.markdown("""Silakan pilih algoritma lalu isi data berikut untuk mengetahui prediksi status gizi balita.""")

model_choice = st.selectbox("Pilih Algoritma", ["CatBoost", "KNN"])

col1, col2 = st.columns(2)

with col1:
    Jenis_Kelamin = st.selectbox("Pilih Jenis Kelamin", ["", "Laki-laki", "Perempuan"])
    Usia = st.text_input("Masukkan Usia (bulan)")
    Berat_Badan_Lahir = st.text_input("Berat Badan Lahir (kg)")
    Tinggi_Badan_Lahir = st.text_input("Tinggi Badan Lahir (cm)")

with col2:
    Berat_Badan = st.text_input("Berat Badan Saat Ini (kg)")
    Tinggi_Badan = st.text_input("Tinggi Badan Saat Ini (cm)")
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
            # Kita tetap memproses data sebagai string, dan konversi angka dengan replace koma ke titik
            input_data = [[
                jenis_kelamin_map[Jenis_Kelamin],
                int(Usia),
                float(Berat_Badan_Lahir.replace(",", ".")),
                float(Tinggi_Badan_Lahir.replace(",", ".")),
                float(Berat_Badan.replace(",", ".")),
                float(Tinggi_Badan.replace(",", ".")),
                asi_map[Status_Pemberian_ASI],
                tinggi_badan_map[Status_Tinggi_Badan],
                berat_badan_map[Status_Berat_Badan]
            ]]

            # Pilih model sesuai input user
            if model_choice == "CatBoost":
                hasil = model_cb.predict(input_data)
            else:
                hasil = model_knn.predict(input_data)

            gizi_diagnosis = status_gizi_map[int(hasil[0])]
            
            # Menggunakan st.markdown dengan CSS untuk mengubah warna
            st.markdown(f"""
                <div style="background-color: #d4edda; color: #000000; padding: 10px; border-radius: 5px;">
                    <strong>Hasil Prediksi Status Gizi Balita:</strong> {gizi_diagnosis}
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error("Terjadi kesalahan saat memproses data. Pastikan semua input valid.")
            st.error(f"Error detail: {str(e)}")
