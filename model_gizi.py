import numpy as np
import streamlit as st
import pickle

# === Fungsi load model hanya sekali pakai cache_resource ===
@st.cache_resource
def load_models():
    model_cb = pickle.load(open('modelCB_terbaik.sav', 'rb'))
    model_knn = pickle.load(open('modelKNN_terbaik.sav', 'rb'))
    return model_cb, model_knn

model_cb, model_knn = load_models()

# Mapping input ke angka
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

# CSS kustom (optional)
st.markdown("""
<style>
    body {
        background: linear-gradient(to right, #e0f7fa, #ffffff);
    }
    .stApp {
        background: linear-gradient(to right, #e0f7fa, #ffffff);
    }
    h1 {
        color: #0d47a1 !important;
    }
    h2, h3, h4, h5, h6 {
        color: #0d47a1;
    }
    .stMarkdown {
        color: #0d47a1;
    }
    label {
        font-weight: bold;
        color: #0d47a1;
    }
    button {
        background-color: #0d47a1 !important;
        color: white !important;
    }
    button:hover {
        background-color: #1565c0 !important;
        color: #0d47a1 !important;
    }
</style>
""", unsafe_allow_html=True)

# Inisialisasi page session state
if "page" not in st.session_state:
    st.session_state.page = "form"

# Fungsi reset input form
def reset_form():
    keys = ["Jenis_Kelamin", "Usia", "Berat_Badan_Lahir", "Tinggi_Badan_Lahir",
            "Berat_Badan", "Tinggi_Badan", "Status_Pemberian_ASI",
            "Status_Tinggi_Badan", "Status_Berat_Badan"]
    for key in keys:
        if key in st.session_state:
            del st.session_state[key]

# Halaman Form Input
if st.session_state.page == "form":
    st.title("Prediksi Status Gizi Balita Menggunakan CatBoost dan KNN")
    st.markdown("Silakan pilih algoritma lalu isi data berikut untuk mengetahui prediksi status gizi balita.")

    model_choice = st.selectbox("Pilih Algoritma", ["CatBoost", "KNN"], key="model_choice")

    col1, col2 = st.columns(2)

    with col1:
        Jenis_Kelamin = st.selectbox("Pilih Jenis Kelamin", ["", "Laki-laki", "Perempuan"], key="Jenis_Kelamin")
        Usia = st.text_input("Masukkan Usia (bulan)", key="Usia")
        Berat_Badan_Lahir = st.text_input("Berat Badan Lahir (kg)", key="Berat_Badan_Lahir")
        Tinggi_Badan_Lahir = st.text_input("Tinggi Badan Lahir (cm)", key="Tinggi_Badan_Lahir")

    with col2:
        Berat_Badan = st.text_input("Berat Badan Saat Ini (kg)", key="Berat_Badan")
        Tinggi_Badan = st.text_input("Tinggi Badan Saat Ini (cm)", key="Tinggi_Badan")
        Status_Pemberian_ASI = st.selectbox("Status Pemberian ASI", ["", "Ya", "Tidak"], key="Status_Pemberian_ASI")
        Status_Tinggi_Badan = st.selectbox("Kondisi Tinggi Badan Saat Ini", ["", "Sangat pendek", "Pendek", "Normal", "Tinggi"], key="Status_Tinggi_Badan")
        Status_Berat_Badan = st.selectbox("Kondisi Berat Badan Saat Ini", ["", "Berat badan sangat kurang", "Berat badan kurang", "Berat badan normal", "Risiko berat badan lebih"], key="Status_Berat_Badan")

    if st.button("Tampilkan Hasil Prediksi"):
        # Cek input kosong
        if "" in (Jenis_Kelamin, Usia, Berat_Badan_Lahir, Tinggi_Badan_Lahir,
                  Berat_Badan, Tinggi_Badan, Status_Pemberian_ASI, Status_Tinggi_Badan, Status_Berat_Badan):
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

                if model_choice == "CatBoost":
                    hasil = model_cb.predict(input_data)
                else:
                    hasil = model_knn.predict(input_data)

                st.session_state.hasil_prediksi = status_gizi_map[int(hasil[0])]
                st.session_state.page = "hasil"
                st.experimental_rerun()

            except Exception as e:
                st.error("Terjadi kesalahan saat memproses data. Pastikan semua input valid.")
                st.error(f"Detail error: {str(e)}")

# Halaman hasil prediksi
elif st.session_state.page == "hasil":
    st.title("Hasil Prediksi Status Gizi Balita")
    st.markdown(f"""
        <div style="background-color: #d4edda; color: #000000; padding: 15px; border-radius: 5px; font-size: 18px;">
            <strong>Status Gizi:</strong> {st.session_state.hasil_prediksi}
        </div>
    """, unsafe_allow_html=True)

    st.markdown(" ")
    if st.button("Klik untuk mulai prediksi kembali"):
        reset_form()
        st.session_state.page = "form"
        st.experimental_rerun()
