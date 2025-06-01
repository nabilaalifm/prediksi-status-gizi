import streamlit as st
import pickle
import numpy as np

# Fungsi load model sekali pakai @st.cache_resource
@st.cache_resource
def load_models():
    model_cb = pickle.load(open('modelCB_terbaik.sav', 'rb'))
    model_knn = pickle.load(open('modelKNN_terbaik.sav', 'rb'))
    return model_cb, model_knn

model_cb, model_knn = load_models()

# Mapping input
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

# Judul aplikasi
st.title("Prediksi Status Gizi Balita")

# Session state untuk menyimpan hasil prediksi dan form kosong
if 'hasil_prediksi' not in st.session_state:
    st.session_state.hasil_prediksi = None

if 'input_data' not in st.session_state:
    st.session_state.input_data = {}

def clear_data():
    st.session_state.hasil_prediksi = None
    st.session_state.input_data = {}
    # Clear juga input form (buat agar form kosong)
    for key in form_keys:
        st.session_state[key] = ''

form_keys = [
    'Jenis_Kelamin', 'Usia', 'Berat_Badan_Lahir', 'Tinggi_Badan_Lahir',
    'Berat_Badan', 'Tinggi_Badan', 'Status_Pemberian_ASI',
    'Status_Tinggi_Badan', 'Status_Berat_Badan'
]

# Isi form input (pakai session_state supaya bisa di-reset)
with st.form("form_prediksi"):
    Jenis_Kelamin = st.selectbox("Pilih Jenis Kelamin", ["", "Laki-laki", "Perempuan"], key='Jenis_Kelamin')
    Usia = st.text_input("Usia (bulan)", key='Usia')
    Berat_Badan_Lahir = st.text_input("Berat Badan Lahir (kg)", key='Berat_Badan_Lahir')
    Tinggi_Badan_Lahir = st.text_input("Tinggi Badan Lahir (cm)", key='Tinggi_Badan_Lahir')
    Berat_Badan = st.text_input("Berat Badan Saat Ini (kg)", key='Berat_Badan')
    Tinggi_Badan = st.text_input("Tinggi Badan Saat Ini (cm)", key='Tinggi_Badan')
    Status_Pemberian_ASI = st.selectbox("Status Pemberian ASI", ["", "Ya", "Tidak"], key='Status_Pemberian_ASI')
    Status_Tinggi_Badan = st.selectbox("Kondisi Tinggi Badan Saat Ini", ["", "Sangat pendek", "Pendek", "Normal", "Tinggi"], key='Status_Tinggi_Badan')
    Status_Berat_Badan = st.selectbox("Kondisi Berat Badan Saat Ini", ["", "Berat badan sangat kurang", "Berat badan kurang", "Berat badan normal", "Risiko berat badan lebih"], key='Status_Berat_Badan')

    model_choice = st.selectbox("Pilih Algoritma", ["CatBoost", "KNN"], key='model_choice')

    submitted = st.form_submit_button("Prediksi")

if submitted:
    # Validasi input kosong
    if "" in [Jenis_Kelamin, Usia, Berat_Badan_Lahir, Tinggi_Badan_Lahir,
              Berat_Badan, Tinggi_Badan, Status_Pemberian_ASI, Status_Tinggi_Badan, Status_Berat_Badan]:
        st.warning("Mohon lengkapi semua input terlebih dahulu.")
    else:
        try:
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
            # Prediksi sesuai pilihan model
            if model_choice == "CatBoost":
                hasil = model_cb.predict(input_data)
            else:
                hasil = model_knn.predict(input_data)

            st.session_state.hasil_prediksi = status_gizi_map[int(hasil[0])]
            st.success(f"Hasil Prediksi: {st.session_state.hasil_prediksi}")

        except Exception as e:
            st.error("Terjadi kesalahan saat memproses data. Pastikan semua input valid.")
            st.error(f"Detail error: {str(e)}")

if st.session_state.hasil_prediksi is not None:
    if st.button("Clear Input & Hasil"):
        clear_data()
        st.experimental_rerun()
