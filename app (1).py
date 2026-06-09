import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="SentiKampus — Analisis Kepuasan Mahasiswa",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.main { background: #0f1117; }

.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    color: #ffffff;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}
.hero-sub {
    font-size: 1.1rem;
    color: #8b92a5;
    margin-bottom: 2rem;
}
.stat-card {
    background: #1a1d27;
    border: 1px solid #2a2d3a;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
}
.stat-number {
    font-size: 2.5rem;
    font-weight: 800;
    line-height: 1;
}
.stat-label {
    font-size: 0.85rem;
    color: #8b92a5;
    margin-top: 0.3rem;
}
.form-card {
    background: #1a1d27;
    border: 1px solid #2a2d3a;
    border-radius: 20px;
    padding: 2rem;
}
.result-pos {
    background: linear-gradient(135deg, #0d2b1a, #1a4d2e);
    border: 1px solid #2d7a4a;
    border-radius: 16px;
    padding: 1.5rem;
    color: #4ade80;
}
.result-neg {
    background: linear-gradient(135deg, #2b0d0d, #4d1a1a);
    border: 1px solid #7a2d2d;
    border-radius: 16px;
    padding: 1.5rem;
    color: #f87171;
}
.result-neu {
    background: linear-gradient(135deg, #1a1d27, #252836);
    border: 1px solid #3a3d4a;
    border-radius: 16px;
    padding: 1.5rem;
    color: #94a3b8;
}
.badge-pos { background: #166534; color: #4ade80; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }
.badge-neg { background: #7f1d1d; color: #f87171; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }
.badge-neu { background: #1e293b; color: #94a3b8; padding: 4px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem;
    color: #ffffff;
    margin-bottom: 1rem;
}
.divider { border: none; border-top: 1px solid #2a2d3a; margin: 2rem 0; }
.review-item {
    background: #1a1d27;
    border: 1px solid #2a2d3a;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}
</style>
""", unsafe_allow_html=True)

# ── Data persistence ─────────────────────────────────────────
DATA_FILE = "responses.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── Sentiment analysis ────────────────────────────────────────
POSITIVE_WORDS = {
    'bagus','baik','memuaskan','mantap','hebat','keren','cepat','responsif',
    'ramah','profesional','lengkap','nyaman','bersih','mudah','murah','stabil',
    'modern','membantu','luar biasa','canggih','update','transparan','beragam',
    'excellent','oke','sip','jos','mantul','kece','top','recommended'
}
NEGATIVE_WORDS = {
    'buruk','jelek','lambat','rusak','kotor','mahal','susah','kurang','error',
    'terlambat','rumit','penuh','parah','tidak','sering','antri','menjengkelkan',
    'kecewa','mengecewakan','payah','gagal','lemot','berantakan','semrawut','boros'
}

def analyze_sentiment(text):
    vader = SentimentIntensityAnalyzer()
    scores = vader.polarity_scores(text)
    compound = scores['compound']

    words = set(text.lower().split())
    pos_count = len(words & POSITIVE_WORDS)
    neg_count = len(words & NEGATIVE_WORDS)
    lexicon_score = (pos_count - neg_count) / max(len(words), 1)

    final_score = (compound * 0.6) + (lexicon_score * 0.4)

    if final_score > 0.05:
        label = "positif"
        emoji = "😊"
        confidence = min(95, int(50 + abs(final_score) * 200))
    elif final_score < -0.05:
        label = "negatif"
        emoji = "😞"
        confidence = min(95, int(50 + abs(final_score) * 200))
    else:
        label = "netral"
        emoji = "😐"
        confidence = int(40 + abs(final_score) * 100)

    return {
        "label": label,
        "emoji": emoji,
        "confidence": confidence,
        "compound": round(compound, 3),
        "pos_words": pos_count,
        "neg_words": neg_count
    }

# ── Load responses ────────────────────────────────────────────
responses = load_data()

# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div style="padding: 2rem 0 1rem;">
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:1rem;">
        <span style="font-size:2rem;">🎓</span>
        <span style="font-size:1rem; font-weight:600; color:#6366f1; letter-spacing:0.1em;">SENTIKAMPUS</span>
    </div>
    <div class="hero-title">Analisis Sentimen<br>Kepuasan Mahasiswa</div>
    <div class="hero-sub">Berikan ulasanmu tentang layanan kampus — AI kami akan menganalisis sentimennya secara otomatis</div>
</div>
""", unsafe_allow_html=True)

# Stats row
total = len(responses)
pos = sum(1 for r in responses if r['sentimen'] == 'positif')
neg = sum(1 for r in responses if r['sentimen'] == 'negatif')
neu = sum(1 for r in responses if r['sentimen'] == 'netral')

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="stat-card">
        <div class="stat-number" style="color:#6366f1">{total}</div>
        <div class="stat-label">Total Responden</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="stat-card">
        <div class="stat-number" style="color:#4ade80">{pos}</div>
        <div class="stat-label">Ulasan Positif</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="stat-card">
        <div class="stat-number" style="color:#f87171">{neg}</div>
        <div class="stat-label">Ulasan Negatif</div>
    </div>""", unsafe_allow_html=True)
with c4:
    pct = round(pos / total * 100) if total > 0 else 0
    st.markdown(f"""<div class="stat-card">
        <div class="stat-number" style="color:#fbbf24">{pct}%</div>
        <div class="stat-label">Tingkat Kepuasan</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# FORM INPUT
# ══════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>✍️ Isi Ulasanmu</div>", unsafe_allow_html=True)

with st.form("form_ulasan", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        nama = st.text_input("Nama (opsional)", placeholder="Nama kamu...")
        fakultas = st.selectbox("Fakultas", [
            "Pilih Fakultas",
            "Fakultas Keguruan dan Ilmu Pendidikan",
            "Fakultas Ekonomi dan Bisnis",
            "Fakultas Teknologi Industri dan Informatika",
            "Fakultas Ilmu-Ilmu Kesehatan",
            "Fakultas Ilmu Sosial dan Ilmu Politik",
            "Fakultas Farmasi dan Sains",
            "Fakultas Agama Islam",
            "Fakultas Psikologi",
            "Fakultas Kedokteran",
            "Fakultas Hukum",
        ])
    with col2:
        angkatan = st.selectbox("Angkatan", ["Pilih Angkatan", "2021", "2022", "2023", "2024", "2025"])
        layanan = st.selectbox("Kategori Layanan yang Dinilai", [
            "Pilih Kategori", "Akademik", "Dosen & Pengajaran",
            "Administrasi Akademik", "Perpustakaan", "Ruang Kelas",
            "Mushola", "Toilet", "Parkiran", "Laboratorium",
            "Wifi", "Teknologi Informasi", "Lainnya"
        ])

    rating = st.slider("Rating Kepuasan", 1, 5, 3,
                       help="1 = Sangat Tidak Puas, 5 = Sangat Puas")

    ulasan = st.text_area("Tuliskan ulasanmu di sini",
                          placeholder="Ceritakan pengalamanmu dengan layanan kampus ini...",
                          height=120)

    submitted = st.form_submit_button("🚀 Kirim & Analisis Sentimen", use_container_width=True)

if submitted:
    if not ulasan.strip():
        st.error("⚠️ Mohon isi ulasan terlebih dahulu!")
    elif len(ulasan.strip()) < 10:
        st.error("⚠️ Ulasan terlalu singkat, minimal 10 karakter ya!")
    else:
        with st.spinner("🤖 AI sedang menganalisis sentimen ulasanmu..."):
            result = analyze_sentiment(ulasan)

        label = result['label']
        css_class = f"result_{label[:3]}"
        badge_class = f"badge_{label[:3]}"

        st.markdown(f"""
        <div class="result_{label[:3]}" style="margin-top:1rem;">
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.75rem;">
                <div style="font-size:1.1rem; font-weight:700;">Hasil Analisis Sentimen</div>
                <span class="{badge_class}">{result['emoji']} {label.upper()}</span>
            </div>
            <div style="font-size:0.9rem; opacity:0.85; margin-bottom:0.5rem;">"{ulasan}"</div>
            <div style="display:flex; gap:1.5rem; font-size:0.82rem; opacity:0.7; margin-top:0.75rem;">
                <span>🎯 Keyakinan AI: {result['confidence']}%</span>
                <span>📊 Skor VADER: {result['compound']}</span>
                <span>✅ Kata positif: {result['pos_words']}</span>
                <span>❌ Kata negatif: {result['neg_words']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Save response
        new_entry = {
            "id": total + 1,
            "nama": nama if nama else "Anonim",
            "fakultas": fakultas if fakultas != "Pilih Fakultas" else "Tidak Disebutkan",
            "angkatan": angkatan if angkatan != "Pilih Angkatan" else "Tidak Disebutkan",
            "layanan": layanan if layanan != "Pilih Kategori" else "Umum",
            "rating": rating,
            "ulasan": ulasan,
            "sentimen": result['label'],
            "confidence": result['confidence'],
            "skor_vader": result['compound'],
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        responses.append(new_entry)
        save_data(responses)
        st.success("✅ Ulasanmu berhasil disimpan! Terima kasih sudah berpartisipasi 🙏")
        st.rerun()

# ══════════════════════════════════════════════════════════════
# DASHBOARD (hanya untuk admin dengan password)
# ══════════════════════════════════════════════════════════════
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📊 Dashboard Hasil Analisis</div>", unsafe_allow_html=True)

ADMIN_PASSWORD = "aapgtiga27"

if "dashboard_unlocked" not in st.session_state:
    st.session_state.dashboard_unlocked = False

if not st.session_state.dashboard_unlocked:
    st.markdown('''
    <div style="background:#1a1d27; border:1px solid #2a2d3a; border-radius:16px; padding:2rem; text-align:center; max-width:400px; margin:0 auto;">
        <div style="font-size:2rem; margin-bottom:0.5rem;">🔒</div>
        <div style="font-weight:600; color:#e2e8f0; margin-bottom:0.5rem;">Dashboard Admin</div>
        <div style="font-size:0.85rem; color:#8b92a5;">Masukkan password untuk melihat grafik dan data lengkap</div>
    </div>
    ''', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        pwd_input = st.text_input("Password", type="password", placeholder="Masukkan password...", label_visibility="collapsed")
        if st.button("🔓 Masuk Dashboard", use_container_width=True):
            if pwd_input == ADMIN_PASSWORD:
                st.session_state.dashboard_unlocked = True
                st.rerun()
            else:
                st.error("❌ Password salah!")

if st.session_state.dashboard_unlocked and len(responses) > 0:

    df = pd.DataFrame(responses)

    col1, col2 = st.columns(2)

    with col1:
        # Pie chart sentimen
        counts = df['sentimen'].value_counts()
        colors = {'positif': '#4ade80', 'negatif': '#f87171', 'netral': '#94a3b8'}
        fig_pie = px.pie(
            values=counts.values,
            names=counts.index,
            color=counts.index,
            color_discrete_map=colors,
            title="Distribusi Sentimen"
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            title_font_size=16,
            showlegend=True,
            legend=dict(font=dict(color='#8b92a5'))
        )
        fig_pie.update_traces(textfont_color='white')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Bar chart per layanan
        layanan_counts = df.groupby(['layanan', 'sentimen']).size().reset_index(name='count')
        fig_bar = px.bar(
            layanan_counts, x='layanan', y='count', color='sentimen',
            color_discrete_map=colors,
            title="Sentimen per Kategori Layanan",
            barmode='stack'
        )
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            title_font_size=16,
            xaxis=dict(tickangle=-30, gridcolor='#2a2d3a'),
            yaxis=dict(gridcolor='#2a2d3a'),
            legend=dict(font=dict(color='#8b92a5')),
            showlegend=True
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        # Rating distribution
        rating_counts = df['rating'].value_counts().sort_index()
        fig_rating = px.bar(
            x=rating_counts.index, y=rating_counts.values,
            title="Distribusi Rating",
            color=rating_counts.values,
            color_continuous_scale=['#f87171', '#fbbf24', '#4ade80']
        )
        fig_rating.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            title_font_size=16,
            xaxis=dict(title='Rating', gridcolor='#2a2d3a'),
            yaxis=dict(title='Jumlah', gridcolor='#2a2d3a'),
            showlegend=False, coloraxis_showscale=False
        )
        st.plotly_chart(fig_rating, use_container_width=True)

    with col4:
        # Rata-rata rating per layanan
        avg_rating = df.groupby('layanan')['rating'].mean().sort_values()
        fig_avg = px.bar(
            x=avg_rating.values, y=avg_rating.index,
            orientation='h',
            title="Rata-rata Rating per Layanan",
            color=avg_rating.values,
            color_continuous_scale=['#f87171', '#fbbf24', '#4ade80'],
            range_color=[1, 5]
        )
        fig_avg.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            title_font_size=16,
            xaxis=dict(range=[0, 5], gridcolor='#2a2d3a'),
            yaxis=dict(gridcolor='#2a2d3a'),
            showlegend=False, coloraxis_showscale=False
        )
        st.plotly_chart(fig_avg, use_container_width=True)

    # Recent reviews
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>💬 Ulasan Terbaru</div>", unsafe_allow_html=True)

    recent = list(reversed(responses[-10:]))
    for r in recent:
        badge = f"badge_{r['sentimen'][:3]}"
        emoji_map = {'positif': '😊', 'negatif': '😞', 'netral': '😐'}
        st.markdown(f"""
        <div class="review-item">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                <div style="font-weight:600; color:#e2e8f0; font-size:0.9rem;">
                    {r['nama']} · {r['layanan']} · ⭐ {r['rating']}/5
                </div>
                <span class="{badge}">{emoji_map[r['sentimen']]} {r['sentimen'].upper()}</span>
            </div>
            <div style="color:#8b92a5; font-size:0.88rem;">"{r['ulasan']}"</div>
            <div style="color:#4a4f62; font-size:0.75rem; margin-top:0.4rem;">{r['waktu']} · {r['fakultas']} · Angkatan {r['angkatan']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Download button
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📥 Export Data</div>", unsafe_allow_html=True)
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="⬇️ Download Data Lengkap (CSV)",
        data=csv,
        file_name=f"data_sentimen_kampus_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

elif st.session_state.dashboard_unlocked and len(responses) == 0:
    st.markdown("""
    <div style="text-align:center; padding:3rem; color:#4a4f62;">
        <div style="font-size:3rem; margin-bottom:1rem;">📭</div>
        <div style="font-size:1.1rem;">Belum ada data ulasan.</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<hr class='divider'>
<div style="text-align:center; color:#4a4f62; font-size:0.8rem; padding-bottom:2rem;">
    SentiKampus — Sistem Analisis Sentimen Kepuasan Mahasiswa · Powered by AI & NLP
</div>
""", unsafe_allow_html=True)
