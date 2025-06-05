import streamlit as st

# WAJIB PALING ATAS SETELAH import st
st.set_page_config(page_title="Student Dropout Predictor", page_icon=":mortar_board:")

import pandas as pd
import numpy as np
import joblib

# --- LOAD MODEL ---
@st.cache_resource
def load_model():
    return joblib.load('model_rf.pkl')  # Sesuaikan path model kamu

model = load_model()

st.title("🎓 Student Dropout Predictor")
st.write("""
Aplikasi ini membantu Jaya Jaya Institut memprediksi kemungkinan **dropout mahasiswa** berdasarkan data pendaftaran dan semester awal.  
Silakan **isi data mahasiswa** atau **upload file csv** untuk prediksi massal!
""")

# --- FORM INPUT DATA INDIVIDU ---
st.header("Input Data Mahasiswa (Individu)")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input('Age at Enrollment', 15, 60, 18)
    admission_grade = st.number_input('Admission Grade', 0.0, 200.0, 100.0)
    tuition_up_to_date = st.selectbox('Tuition Fees Up to Date', [1, 0], format_func=lambda x: "Ya" if x==1 else "Tidak")
    curr_1_approved = st.number_input('Curricular Units 1st Sem Approved', 0, 20, 0)
    curr_1_grade = st.number_input('Curricular Units 1st Sem Grade', 0.0, 20.0, 10.0)
with col2:
    curr_2_approved = st.number_input('Curricular Units 2nd Sem Approved', 0, 20, 0)
    curr_2_grade = st.number_input('Curricular Units 2nd Sem Grade', 0.0, 20.0, 10.0)
    previous_qualification_grade = st.number_input('Previous Qualification Grade', 0.0, 200.0, 120.0)
    evaluations_2nd = st.number_input('Curricular Units 2nd Sem Evaluations', 0, 20, 0)
    course = st.number_input('Course (kode, contoh: 9147)', 33, 9991, 9147)

# -- Siapkan dictionary input (harus sesuai nama fitur saat training model)
input_dict = {
    'Curricular_units_2nd_sem_approved': curr_2_approved,
    'Curricular_units_2nd_sem_grade': curr_2_grade,
    'Curricular_units_1st_sem_approved': curr_1_approved,
    'Curricular_units_1st_sem_grade': curr_1_grade,
    'Tuition_fees_up_to_date': tuition_up_to_date,
    'Age_at_enrollment': age,
    'Curricular_units_2nd_sem_evaluations': evaluations_2nd,
    'Admission_grade': admission_grade,
    'Previous_qualification_grade': previous_qualification_grade,
    'Course': course
}

# -- PREDIKSI DATA INDIVIDU
if st.button('Predict Dropout (Individu)'):
    all_features = model.feature_names_in_ if hasattr(model, 'feature_names_in_') else list(input_dict.keys())
    df_input = pd.DataFrame([{f: input_dict.get(f, 0) for f in all_features}])
    pred = model.predict(df_input)[0]
    prob = model.predict_proba(df_input)[0][1]

    st.markdown("---")
    st.write("### Hasil Prediksi:")
    st.success(f"**{'Dropout' if pred==1 else 'Tidak Dropout'}** (Probabilitas Dropout: {prob:.2%})")

    with st.expander("Lihat data input"):
        st.dataframe(df_input)

    # Tampilkan fitur penting model
    st.write("#### Faktor penting model (Top 5):")
    importances = model.feature_importances_
    features = all_features
    fi_df = pd.DataFrame({"Feature": features, "Importance": importances}).sort_values(by="Importance", ascending=False)
    st.table(fi_df.head(5))

# --- UPLOAD CSV UNTUK PREDIKSI MASSAL
st.header("Prediksi Dropout Banyak Mahasiswa (Upload CSV)")
st.write("Format kolom harus sesuai dengan data training (lihat [contoh data](https://github.com/Habibie1798/Project-Laskar-AI/blob/main/data.csv)).")

uploaded_file = st.file_uploader("Upload file CSV", type=['csv'])
if uploaded_file is not None:
    df_csv = pd.read_csv(uploaded_file)
    # Cek kolom, fill kolom yang tidak ada
    for col in model.feature_names_in_:
        if col not in df_csv.columns:
            df_csv[col] = 0  # atau isi default
    y_pred = model.predict(df_csv[model.feature_names_in_])
    df_csv['Dropout_Pred'] = y_pred
    st.success("Prediksi selesai! Lihat hasil di bawah atau download.")
    st.dataframe(df_csv.head())

    csv = df_csv.to_csv(index=False).encode('utf-8')
    st.download_button("Download hasil prediksi", csv, "hasil_prediksi.csv", "text/csv")

st.markdown("---")
st.write("**Contact:** adam.bagus@lintasarta.co.id")
