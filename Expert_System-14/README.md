# Sistem Pakar Mesin Cuci - Metode Tsukamoto

## 📋 Deskripsi
Sistem pakar untuk menentukan kecepatan RPM mesin cuci berdasarkan berat cucian dan tingkat kekotoran menggunakan metode inferensi fuzzy Tsukamoto.

## 🎯 Fitur
- Perhitungan fuzzy dengan fungsi keanggotaan sederhana
- Implementasi metode Tsukamoto
- Input interaktif dan mode non-interaktif via CLI
- Mode debug untuk melihat detail perhitungan
- Contoh otomatis untuk testing

## 🛠️ Teknologi
- Python 3.x

## 📁 Struktur Proyek
Expert_System-14/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── tests/
    └── test_main.py

## 🚀 Cara Menjalankan

1. (Opsional) Buat virtualenv dan aktifkan
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
```

2. Install deps (opsional untuk testing)
```bash
python -m pip install -r requirements.txt
```

3. Jalankan program
```bash
python main.py
# Non-interaktif contoh
python main.py --examples
# Non-interaktif input langsung
python main.py --berat 2 --kotoran 20 --debug
```

## 📊 Variabel Fuzzy
- Berat Cucian (kg)
  - Ringan: 0–4 kg
  - Berat: 3–10 kg

- Tingkat Kekotoran (%)
  - Rendah: 0–50%
  - Tinggi: 30–100%

## RPM Output
- Lambat: 500–1000 RPM (menurun)
- Cepat: 500–1200 RPM (meningkat)

## 🎮 Rule Base (singkat)
- IF Berat Ringan AND Kotoran Rendah THEN RPM Lambat
- IF Berat Ringan AND Kotoran Tinggi THEN RPM Cepat
- IF Berat Berat AND Kotoran Rendah THEN RPM Cepat
- IF Berat Berat AND Kotoran Tinggi THEN RPM Cepat

## 🧪 Testing
Tes otomatis menggunakan `pytest`.
```bash
python -m pytest -q
```

## 👤 Author
Muhamad Miftahudin, M.Kom

## 📄 License
MIT License
