# 🚲 Bike Sharing Dashboard

Proyek ini merupakan bagian dari kelas **Belajar Analisis Data dengan Python** di Dicoding.  
Dashboard ini menampilkan analisis interaktif terhadap data peminjaman sepeda di Washington DC tahun 2011–2012.

---

## 🔧 Setup Environment

### 💻 Menggunakan Anaconda
```bash
conda create --name bike-sharing python=3.9
conda activate bike-sharing
pip install -r requirements.txt
```

### 🐚 Menggunakan Shell / Terminal
```bash
mkdir bike_sharing_dashboard
cd bike_sharing_dashboard
pip install pipenv
pipenv install
pipenv shell
pip install -r requirements.txt
```

---

## ▶️ Menjalankan Dashboard

Pastikan Anda sudah berada di folder yang berisi `app.py` dan `day.csv`.

```bash
streamlit run app.py
```

Dashboard akan terbuka di browser Anda secara otomatis.

---

## 🧩 Isi Folder Proyek

```
submission
├───dashboard
| ├───main_data.csv
| └───dashboard.py
├───data
| ├───data_1.csv
| └───data_2.csv
├───notebook.ipynb
├───README.md
└───requirements.txt
└───url.txt
```

---

## 📈 Fitur Dashboard

- Filter interaktif: tanggal, musim, cuaca
- Visualisasi total peminjaman per musim
- Analisis pengaruh cuaca terhadap jumlah peminjaman
- Tren peminjaman sepeda bulanan
- Perbandingan hari kerja vs hari libur

---

## 📝 Dataset

Dataset yang digunakan adalah **Bike Sharing Dataset** dari UCI Machine Learning Repository:  
https://drive.google.com/file/d/1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ/view

---

## 📌 Dibuat Oleh

- **Nama:** Adam Bagus Habibie Al Rasyid  
- **Email:** adam.bagus@lintasarta.co.id  
- **ID Dicoding:** habibiealrasyid17
