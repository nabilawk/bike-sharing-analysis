import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit as st
import pathlib

# Menentukan direktori utama tempat file dashboard.py berada
BASE_DIR = pathlib.Path(__file__).resolve().parent

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Bike Sharing Analytics Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Custom CSS untuk mempercantik latar belakang, memperbesar teks, dan tema hijau elegan
st.markdown("""
    <style>
    /* Latar belakang utama aplikasi */
    .stApp {
        background-color: #0E1621;
        color: #E2E8F0;
    }
    
    /* Styling Header Utama */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #F8FAFC !important;
        letter-spacing: -0.5px;
    }
    
    h2, h3 {
        color: #34D399 !important;
        font-weight: 700 !important;
    }

    /* Styling Metric / KPI Card */
    div[data-testid="stMetric"] {
        background-color: #17212B;
        border: 1px solid #2B5278;
        padding: 18px 22px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="stMetric"] label {
        font-size: 1rem !important;
        color: #94A3B8 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        color: #34D399 !important;
        font-weight: 800 !important;
    }

    /* Styling Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111B27;
        border-right: 1px solid #1F2C3A;
    }
    section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] span {
        color: #E2E8F0 !important;
        font-size: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Load Dataset dengan Caching dan Pathlib
@st.cache_data
def load_data():
    data = pd.read_csv(BASE_DIR / "main_data.csv")
    data['dteday'] = pd.to_datetime(data['dteday'])
    data['year_label'] = data['yr'].map({0: 2011, 1: 2012})
    return data

df_main = load_data()

# ==========================================
# SIDEBAR (FILTER)
# ==========================================
st.sidebar.markdown("### ⚙️ Filter Dashboard")
st.sidebar.markdown("Sesuaikan parameter di bawah untuk memfilter data analisis.")

selected_years = st.sidebar.multiselect(
    "📅 Pilih Tahun:",
    options=[2011, 2012],
    default=[2011, 2012]
)

selected_seasons = st.sidebar.multiselect(
    "🌿 Pilih Musim:",
    options=df_main['season_label'].unique().tolist(),
    default=df_main['season_label'].unique().tolist()
)

selected_workingday = st.sidebar.multiselect(
    "📊 Pilih Jenis Hari:",
    options=df_main['workingday_label'].unique().tolist(),
    default=df_main['workingday_label'].unique().tolist()
)

# Terapkan Filter
filtered_df = df_main[
    (df_main['year_label'].isin(selected_years)) &
    (df_main['season_label'].isin(selected_seasons)) &
    (df_main['workingday_label'].isin(selected_workingday))
]

# ==========================================
# HEADER UTAMA
# ==========================================
st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("<p style='font-size: 1.15rem; color: #94A3B8; margin-top: -10px;'>Monitoring & Analisis Komprehensif Pola Penyewaan Sepeda (2011–2012)</p>", unsafe_allow_html=True)
st.markdown("---")

if filtered_df.empty:
    st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih. Silakan sesuaikan kembali filter di sidebar.")
else:
    # ==========================================
    # KPI CARDS (Pemanfaatan Ruang Atas)
    # ==========================================
    total_rentals = filtered_df['cnt'].sum()
    daily_avg = int(filtered_df.groupby('dteday')['cnt'].sum().mean())
    total_casual = filtered_df['casual'].sum()
    total_registered = filtered_df['registered'].sum()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📊 Total Penyewaan", value=f"{total_rentals:,}")
    with col2:
        st.metric(label="📈 Rata-rata Harian", value=f"{daily_avg:,}")
    with col3:
        st.metric(label="👤 Total Casual", value=f"{total_casual:,}")
    with col4:
        st.metric(label="👥 Total Registered", value=f"{total_registered:,}")

    st.markdown("---")

    # Palet warna hijau monokrom elegan untuk Plotly
    green_color_scale = ['#065F46', '#047857', '#059669', '#10B981', '#34D399']

    # ==========================================
    # BAGIAN A: ANALISIS MUSIMAN + INSIGHT BAR
    # ==========================================
    st.subheader("A. Analisis Performa Berdasarkan Musim")
    
    col_a1, col_a2 = st.columns([2, 1])

    with col_a1:
        season_df = filtered_df.groupby('season_label')['cnt'].mean().reset_index()
        season_order = ['Spring', 'Summer', 'Fall', 'Winter']
        
        fig_season = px.bar(
            season_df,
            x='season_label',
            y='cnt',
            category_orders={'season_label': season_order},
            labels={'season_label': 'Musim', 'cnt': 'Rata-rata Penyewaan per Hari'},
            title="Rata-rata Penyewaan Sepeda Berdasarkan Musim",
            color='cnt',
            color_continuous_scale='Greens',
            template="plotly_dark"
        )
        fig_season.update_layout(coloraxis_showscale=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(size=13))
        st.plotly_chart(fig_season, use_container_width=True)

    with col_a2:
        st.markdown(
            """
            <div style="background-color: #17212B; padding: 22px; border-radius: 12px; border: 1px solid #2B5278; height: 100%;">
                <h4 style="color: #34D399; margin-top: 0; font-size: 1.2rem;">💡 Insight Musiman:</h4>
                <ul style="color: #CBD5E1; font-size: 0.95rem; padding-left: 20px; line-height: 1.7;">
                    <li>Musim <b>Fall (Gugur)</b> mencatatkan rata-rata penyewaan tertinggi (>5,600/hari).</li>
                    <li>Musim <b>Spring (Semi)</b> memiliki angka terendah secara signifikan (~2,600/hari).</li>
                </ul>
                <hr style="border-color: #2B5278; margin: 12px 0;">
                <p style="color: #94A3B8; font-size: 0.85rem; font-style: italic; margin-bottom: 0;">
                   Rekomendasi: Alokasikan stok armada maksimum saat Fall dan lakukan pemeliharaan armada saat Spring.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ==========================================
    # BAGIAN B: ANALISIS POLA PER JAM + INSIGHT BAR
    # ==========================================
    st.subheader("B. Analisis Pola Penyewaan Berdasarkan Jam")

    col_b1, col_b2 = st.columns([2, 1])

    with col_b1:
        hour_df = filtered_df.groupby(['hr', 'workingday_label'])['cnt'].mean().reset_index()

        fig_hour = px.line(
            hour_df,
            x='hr',
            y='cnt',
            color='workingday_label',
            markers=True,
            labels={'hr': 'Jam (0 - 23)', 'cnt': 'Rata-rata Penyewaan', 'workingday_label': 'Jenis Hari'},
            title="Pola Penyewaan Sepeda Berdasarkan Jam & Jenis Hari",
            color_discrete_sequence=['#34D399', '#6EE7B7'],
            template="plotly_dark"
        )
        fig_hour.update_xaxes(dtick=1)
        fig_hour.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(size=13))
        st.plotly_chart(fig_hour, use_container_width=True)

    with col_b2:
        st.markdown(
            """
            <div style="background-color: #17212B; padding: 22px; border-radius: 12px; border: 1px solid #2B5278; height: 100%;">
                <h4 style="color: #34D399; margin-top: 0; font-size: 1.2rem;">💡 Insight Pola Jam:</h4>
                <ul style="color: #CBD5E1; font-size: 0.95rem; padding-left: 20px; line-height: 1.7;">
                    <li><b>Hari Kerja:</b> Lonjakan tajam (puncak) di jam 08.00 pagi dan 17.00 sore (aktivitas komuter).</li>
                    <li><b>Hari Libur:</b> Pola landai terkonsentrasi di siang hari (12.00–14.00) untuk rekreasi.</li>
                </ul>
                <hr style="border-color: #2B5278; margin: 12px 0;">
                <p style="color: #94A3B8; font-size: 0.85rem; font-style: italic; margin-bottom: 0;">
                   Rekomendasi: Siagakan armada di area perkantoran saat jam sibuk kerja dan taman rekreasi saat akhir pekan.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ==========================================
    # BAGIAN C: PERBANDINGAN PENGGUNA + INSIGHT BAR
    # ==========================================
    st.subheader("C. Perbandingan Pengguna Casual vs Registered")

    col_c1, col_c2 = st.columns([2, 1])

    with col_c1:
        user_df = filtered_df.groupby('hr')[['casual', 'registered']].mean().reset_index()
        user_melted = user_df.melt(id_vars='hr', value_vars=['casual', 'registered'], var_name='Tipe Pengguna', value_name='Rata-rata')

        fig_user = px.line(
            user_melted,
            x='hr',
            y='Rata-rata',
            color='Tipe Pengguna',
            markers=True,
            labels={'hr': 'Jam', 'Rata-rata': 'Jumlah Pengguna'},
            title="Perbandingan Rata-rata Pengguna Casual & Registered",
            color_discrete_sequence=['#10B981', '#FBBF24'],
            template="plotly_dark"
        )
        fig_user.update_xaxes(dtick=1)
        fig_user.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(size=13))
        st.plotly_chart(fig_user, use_container_width=True)

    with col_c2:
        st.markdown(
            """
            <div style="background-color: #17212B; padding: 22px; border-radius: 12px; border: 1px solid #2B5278; height: 100%;">
                <h4 style="color: #34D399; margin-top: 0; font-size: 1.2rem;">💡 Insight Pengguna:</h4>
                <ul style="color: #CBD5E1; font-size: 0.95rem; padding-left: 20px; line-height: 1.7;">
                    <li>Pengguna <b>Registered</b> mendominasi volume secara masif di seluruh jam operasional.</li>
                    <li>Pengguna <b>Casual</b> memiliki porsi lebih tinggi secara proporsional saat akhir pekan siang hari.</li>
                </ul>
                <hr style="border-color: #2B5278; margin: 12px 0;">
                <p style="color: #94A3B8; font-size: 0.85rem; font-style: italic; margin-bottom: 0;">
                Kesimpulan: Fokuskan layanan langganan dan kemudahan akses bagi pengguna terdaftar harian.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )