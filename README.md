# 🎓 SentiKampus — Web App Analisis Sentimen

Web app untuk mengumpulkan dan menganalisis sentimen kepuasan mahasiswa terhadap layanan kampus.

## 🚀 Cara Deploy ke Internet (GRATIS) — Streamlit Cloud

### Langkah 1 — Upload ke GitHub
1. Buat akun di **github.com** (gratis)
2. Buat repository baru, nama: `sentikampus`
3. Upload semua file ini ke repository tersebut:
   - `app.py`
   - `requirements.txt`
   - `.streamlit/config.toml`

### Langkah 2 — Deploy ke Streamlit Cloud
1. Buka **share.streamlit.io**
2. Login dengan akun GitHub
3. Klik **"New app"**
4. Pilih repository `sentikampus`
5. Main file path: `app.py`
6. Klik **"Deploy"**
7. Tunggu 2-3 menit → dapat link seperti:
   `https://namakamu-sentikampus.streamlit.app`

### Langkah 3 — Share ke Mahasiswa
Kirim link tersebut ke 50+ mahasiswa via WhatsApp/Instagram!

---

## 💻 Cara Jalankan di Laptop (untuk testing)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Lalu buka browser: `http://localhost:8501`

---

## ✨ Fitur Web App
- Form input ulasan mahasiswa
- Analisis sentimen otomatis (AI + NLP)
- Dashboard grafik interaktif
- Export data ke CSV
- Responsive di HP & laptop
- Dark mode yang keren untuk presentasi
