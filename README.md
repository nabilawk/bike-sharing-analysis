# Bike Sharing Analysis Dashboard

Proyek ini merupakan analisis data penyewaan sepeda (*Bike Sharing*) menggunakan Python. Analisis dilakukan untuk mengetahui pola penyewaan sepeda berdasarkan musim, jam penyewaan, serta jenis pengguna (*casual* dan *registered*).

Proyek ini juga dilengkapi dengan dashboard interaktif menggunakan Streamlit untuk menyajikan hasil analisis data secara lebih informatif.

## Struktur Proyek

```text
bike-sharing-analysis/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── data/
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── requirements.txt
├── README.md
└── url.txt
```

## Setup Environment - Anaconda

```bash
conda create --name bike-sharing python=3.13.0
conda activate bike-sharing
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

Masuk ke direktori proyek:

```bash
cd bike-sharing-analysis
```

Buat virtual environment:

```bash
python -m venv .venv
```

Aktifkan virtual environment.

**Windows:**

```bash
.venv\Scripts\activate
```

**Mac/Linux:**

```bash
source .venv/bin/activate
```

Instal library yang dibutuhkan:

```bash
pip install -r requirements.txt
```

## Run Streamlit App

Pastikan terminal berada di direktori utama proyek `bike-sharing-analysis`, kemudian jalankan:

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka secara otomatis di browser. Jika tidak terbuka, akses alamat berikut:

```text
http://localhost:8501
```

## Tools and Libraries

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- Plotly

## Dataset

Dataset yang digunakan adalah **Bike Sharing Dataset**, yang terdiri dari:

- `day.csv`: data penyewaan sepeda berdasarkan hari.
- `hour.csv`: data penyewaan sepeda berdasarkan jam.
