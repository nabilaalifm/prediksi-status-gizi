import numpy as np
import streamlit as st
import pickle

# Load model sekali saat aplikasi mulai jalan
model_prediksi = pickle.load(open(r"D:\Prediksi Status Gizi\modelCB_terbaik.sav", "rb"))

# Fungsi reset input dengan session_state
def reset_input():
    st.session_state['jenis_kelamin'] = ""
    st.session_state['usia'] = 0
    st.session_state['berat_badan_lahir'] = 0.0
    st.session_state['tinggi_badan_lahir'] = 0.0
    st.session_state['berat_badan'] = 0.0
    st.session_state['tinggi_badan'] = 0.0
    st.session_state['status_asi'] = ""
    st.session_state['status_tinggi_badan'] = ""
    st.session_state['status_berat_badan'] = ""

# Judul
st.title("Prediksi Status Gizi Balita")
st.markdown("Isi data berikut untuk prediksi status gizi balita.")

# Input form dengan session_state key biar bisa di-reset
Jenis_Kelamin = st.selectbox("Pilih Jenis Kelamin", ["", "Laki-laki", "Perempuan"], key='jenis_kelamin')
Usia = st.number_input("Masukkan Usia (bulan)", min_value=0, step=1, format="%d", key='usia')
Berat_Badan_Lahir = st.number_input("Berat Badan Lahir (kg)", min_value=0.0, step=0.1, format="%.1f", key='berat_badan_lahir')
Tinggi_Badan_Lahir = st.number_input("Tinggi Badan Lahir (cm)", min_value=0.0, step=0.1, format="%.1f", key='tinggi_badan_lahir')
Berat_Badan = st.number_input("Berat Badan Saat Ini (kg)", min_value=0.0, step=0.1, format="%.1f", key='berat_badan')
Tinggi_Badan = st.number_input("Tinggi Badan Saat Ini (cm)", min_value=0.0, step=0.1, format="%.1f", key='tinggi_badan')
Status_Pemberian_ASI = st.selectbox("Status Pemberian ASI", ["", "Ya", "Tidak"], key='status_asi')
Status_Tinggi_Badan = st.selectbox("Kondisi Tinggi Badan Saat Ini", ["", "Sangat pendek", "Pendek", "Normal", "Tinggi"], key='status_tinggi_badan')
Status_Berat_Badan = st.selectbox("Kondisi Berat Badan Saat Ini", ["", "Berat badan sangat kurang", "Berat badan kurang", "Berat badan normal", "Risiko berat badan lebih"], key='status_berat_badan')

# Mapping nilai input ke numerik
jenis_kelamin_map = {'Laki-laki': 0, 'Perempuan': 1}
asi_map = {'Tidak': 0, 'Ya': 1}
berat_badan_map = {
    'Berat badan sangat kurang': 2,
    'Berat badan kurang': 0,
    'Berat badan normal': 1,
    'Risiko berat badan lebih': 3
}
tinggi_badan_map = {
    'Sangat pendek': 2,
    'Pendek': 1,
    'Normal': 0,
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
    # Cek input lengkap
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

# Tombol clear/reset input
if st.button("Clear Data"):
    reset_input()
    st.experimental_rerun()  # Refresh halaman agar form ikut reset
