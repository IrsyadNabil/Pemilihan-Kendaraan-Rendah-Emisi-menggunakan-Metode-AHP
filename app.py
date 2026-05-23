import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="EcoRank — Pemilihan Kendaraan Rendah Emisi",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS — Industrial Dark Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=Outfit:wght@300;400;500;600&display=swap');

/* ── Root & Background ── */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    background: #0c0e12;
    color: #e8eaf0;
}
.stApp {
    background: #0c0e12;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #111318 !important;
    border-right: 1px solid #1e2130;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSlider label {
    color: #9da5b4 !important;
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.04em;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #e8eaf0 !important;
    font-family: 'Syne', sans-serif;
}

/* ── Typography ── */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.02em;
}
h1 { font-weight: 800; }
h2 { font-weight: 700; }
h3 { font-weight: 600; }

/* ── Metric Cards ── */
[data-testid="metric-container"] {
    background: #13151d !important;
    border: 1px solid #1e2130 !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
[data-testid="metric-container"] label {
    color: #6b7280 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #4ade80 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #1e2130 !important;
    border-radius: 10px !important;
    overflow: hidden;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(22, 163, 74, 0.3) !important;
}
.stButton > button:hover {
    box-shadow: 0 6px 28px rgba(22, 163, 74, 0.5) !important;
    transform: translateY(-1px) !important;
}

/* ── Sliders ── */
[data-testid="stSlider"] {
    padding: 0.3rem 0;
}

/* ── Number Input ── */
input[type="number"] {
    background: #13151d !important;
    color: #e8eaf0 !important;
    border: 1px solid #1e2130 !important;
    border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #111318 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid #1e2130;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    color: #6b7280 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.04em !important;
    border-radius: 7px !important;
    padding: 0.5rem 1.2rem !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #16a34a !important;
    color: #fff !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #13151d !important;
    border: 1px solid #1e2130 !important;
    border-radius: 10px !important;
}

/* ── Select / Multiselect ── */
[data-baseweb="select"] > div {
    background: #13151d !important;
    border-color: #1e2130 !important;
    color: #e8eaf0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}

/* ── Divider ── */
hr {
    border-color: #1e2130 !important;
}

/* ── Custom card class ── */
.eco-card {
    background: #13151d;
    border: 1px solid #1e2130;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.eco-badge {
    display: inline-block;
    background: rgba(74, 222, 128, 0.12);
    color: #4ade80;
    border: 1px solid rgba(74, 222, 128, 0.25);
    border-radius: 20px;
    padding: 2px 12px;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 8px;
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 0.85rem;
    background: #1e2130;
    color: #9da5b4;
}
.rank-1 { background: linear-gradient(135deg,#ca8a04,#a16207); color:#fff; }
.rank-2 { background: linear-gradient(135deg,#6b7280,#4b5563); color:#fff; }
.rank-3 { background: linear-gradient(135deg,#92400e,#78350f); color:#fff; }
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4ade80;
    margin-bottom: 0.5rem;
}
.cr-ok { color: #4ade80; font-weight: 700; font-family:'Syne',sans-serif; }
.cr-fail { color: #f87171; font-weight: 700; font-family:'Syne',sans-serif; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
KRITERIA = [
    'Emisi CO2 (g/km)',
    'Konsumsi BBM Kota (L/100km)',
    'Konsumsi BBM Hwy (L/100km)',
    'Konsumsi BBM Gabungan (L/100km)',
    'MPG (Miles Per Gallon)',
    'Ukuran Mesin (L)',
    'Jumlah Silinder',
]
TIPE = ['cost', 'cost', 'cost', 'cost', 'benefit', 'cost', 'cost']
KOLOM_CSV = [
    'CO2 Emissions(g/km)',
    'Fuel Consumption City (L/100 km)',
    'Fuel Consumption Hwy (L/100 km)',
    'Fuel Consumption Comb (L/100 km)',
    'Fuel Consumption Comb (mpg)',
    'Engine Size(L)',
    'Cylinders',
]
N = len(KRITERIA)
RI_TABLE = {1:0, 2:0, 3:0.58, 4:0.90, 5:1.12, 6:1.24, 7:1.32, 8:1.41, 9:1.45, 10:1.49}

DEFAULT_MATRIX = np.array([
    [1,    2,    2,    3,    4,    5,    7],
    [1/2,  1,    1,    2,    3,    4,    5],
    [1/2,  1,    1,    2,    3,    4,    5],
    [1/3,  1/2,  1/2,  1,    2,    3,    4],
    [1/4,  1/3,  1/3,  1/2,  1,    2,    3],
    [1/5,  1/4,  1/4,  1/3,  1/2,  1,    2],
    [1/7,  1/5,  1/5,  1/4,  1/3,  1/2,  1],
])

SAATY_SCALE = {
    "1 — Sama penting": 1,
    "2": 2,
    "3 — Sedikit lebih penting": 3,
    "4": 4,
    "5 — Lebih penting": 5,
    "6": 6,
    "7 — Jauh lebih penting": 7,
    "8": 8,
    "9 — Mutlak lebih penting": 9,
}

# ─────────────────────────────────────────────
# HELPERS / CORE AHP LOGIC
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("CO2 Emissions_Canada.csv")
    return df

def compute_ahp(matrix: np.ndarray):
    n = matrix.shape[0]
    col_sum = matrix.sum(axis=0)
    norm = matrix / col_sum
    weights = norm.mean(axis=1)
    aw = matrix @ weights
    lambda_max = np.mean(aw / weights)
    ci = (lambda_max - n) / (n - 1)
    ri = RI_TABLE.get(n, 1.49)
    cr = ci / ri if ri > 0 else 0
    return weights, lambda_max, ci, cr

def normalisasi_saw(df: pd.DataFrame, tipe: list) -> pd.DataFrame:
    df_norm = df.copy().astype(float)
    for i, col in enumerate(df.columns):
        if tipe[i] == 'cost':
            df_norm[col] = df[col].min() / df[col]
        else:
            df_norm[col] = df[col] / df[col].max()
    return df_norm

def set_matplotlib_dark():
    plt.rcParams.update({
        "figure.facecolor": "#13151d",
        "axes.facecolor":   "#13151d",
        "axes.edgecolor":   "#1e2130",
        "axes.labelcolor":  "#9da5b4",
        "xtick.color":      "#6b7280",
        "ytick.color":      "#6b7280",
        "text.color":       "#e8eaf0",
        "grid.color":       "#1e2130",
        "grid.linewidth":   0.6,
        "font.family":      "monospace",
    })

# ─────────────────────────────────────────────
# SESSION STATE DEFAULTS
# ─────────────────────────────────────────────
if "matrix" not in st.session_state:
    st.session_state["matrix"] = DEFAULT_MATRIX.copy()
if "hasil" not in st.session_state:
    st.session_state["hasil"] = None
if "weights" not in st.session_state:
    st.session_state["weights"] = None

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 0.5rem'>
        <p class='section-label'>Aplikasi SPK</p>
        <h2 style='font-family:Syne,sans-serif;font-size:1.4rem;margin:0;color:#e8eaf0'>
             EcoRank
        </h2>
        <p style='color:#6b7280;font-size:0.8rem;margin-top:4px;font-family:DM Mono,monospace'>
            Pemilihan Kendaraan Rendah Emisi
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p class='section-label'>Navigasi</p>", unsafe_allow_html=True)

    page = st.radio(
        "",
        ["  Dataset", "  Bobot Kriteria", "  Perhitungan AHP", "  Hasil Perangkingan", "  Profil Kelompok"],
        label_visibility="collapsed",
    )
    page = page.split("  ", 1)[1].strip()

    st.markdown("---")
    st.markdown("<p class='section-label'>Filter Hasil</p>", unsafe_allow_html=True)
    top_n = st.slider("Tampilkan Top N Kendaraan", 5, 50, 10, 1)
    filter_fuel = st.multiselect(
        "Filter Jenis Bahan Bakar",
        options=["X", "Z", "D", "E", "N"],
        default=["X", "Z", "D", "E", "N"],
        help="X=Regular, Z=Premium, D=Diesel, E=E85, N=Natural Gas"
    )

    st.markdown("---")
    st.caption("SCPK 2025/2026 · Metode AHP")

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
raw_data = load_data()

# apply fuel filter
if filter_fuel:
    filtered_data = raw_data[raw_data["Fuel Type"].isin(filter_fuel)].copy()
else:
    filtered_data = raw_data.copy()

# ═════════════════════════════════════════════
# PAGE: DATASET
# ═════════════════════════════════════════════
if page == "Dataset":
    st.markdown("<p class='section-label'>Overview</p>", unsafe_allow_html=True)
    st.markdown("##  Eksplorasi Dataset")
    st.markdown(
        "<p style='color:#6b7280;max-width:700px'>Dataset emisi CO₂ kendaraan di Kanada yang bersumber dari "
        "<a href='https://www.kaggle.com/datasets/debajyotipodder/co2-emission-by-vehicles' "
        "style='color:#4ade80'>Kaggle / Environment Canada</a>. "
        "Digunakan sebagai alternatif dalam sistem pendukung keputusan pemilihan kendaraan rendah emisi.</p>",
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Kendaraan", f"{len(raw_data):,}")
    c2.metric("Setelah Filter", f"{len(filtered_data):,}")
    c3.metric("Jumlah Merek", raw_data["Make"].nunique())
    c4.metric("Rata-rata CO₂", f"{raw_data['CO2 Emissions(g/km)'].mean():.0f} g/km")

    st.markdown("### Data Mentah")
    st.dataframe(
        filtered_data.reset_index(drop=True),
        use_container_width=True,
        height=420,
    )

    st.markdown("### Analitik Cepat")
    col_a, col_b = st.columns(2)

    set_matplotlib_dark()

    with col_a:
        st.markdown("**Distribusi Emisi CO₂**")
        fig, ax = plt.subplots(figsize=(5, 3))
        vals = filtered_data["CO2 Emissions(g/km)"].dropna()
        ax.hist(vals, bins=40, color="#16a34a", alpha=0.85, edgecolor="#0c0e12", linewidth=0.4)
        ax.axvline(vals.mean(), color="#4ade80", linewidth=1.5, linestyle="--", label=f"Rata-rata: {vals.mean():.0f}")
        ax.set_xlabel("CO₂ (g/km)")
        ax.set_ylabel("Frekuensi")
        ax.legend(fontsize=8)
        ax.grid(axis="y", alpha=0.4)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)

    with col_b:
        st.markdown("**Top 10 Merek — Rata-rata Emisi CO₂**")
        top_makes = (
            filtered_data.groupby("Make")["CO2 Emissions(g/km)"]
            .mean().sort_values().head(10)
        )
        fig2, ax2 = plt.subplots(figsize=(5, 3))
        colors = ["#4ade80" if v < 200 else "#fbbf24" if v < 250 else "#f87171" for v in top_makes.values]
        bars = ax2.barh(top_makes.index, top_makes.values, color=colors, edgecolor="#0c0e12", linewidth=0.4)
        ax2.set_xlabel("Rata-rata CO₂ (g/km)")
        ax2.grid(axis="x", alpha=0.4)
        fig2.tight_layout()
        st.pyplot(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown("**Konsumsi BBM vs Emisi CO₂**")
        fig3, ax3 = plt.subplots(figsize=(5, 3))
        sample = filtered_data.sample(min(800, len(filtered_data)), random_state=42)
        sc = ax3.scatter(
            sample["Fuel Consumption Comb (L/100 km)"],
            sample["CO2 Emissions(g/km)"],
            c=sample["CO2 Emissions(g/km)"],
            cmap=LinearSegmentedColormap.from_list("eco", ["#16a34a","#fbbf24","#f87171"]),
            alpha=0.55, s=12, linewidths=0,
        )
        ax3.set_xlabel("Konsumsi BBM Gabungan (L/100km)")
        ax3.set_ylabel("CO₂ (g/km)")
        ax3.grid(alpha=0.3)
        fig3.tight_layout()
        st.pyplot(fig3, use_container_width=True)

    with col_d:
        st.markdown("**Sebaran Kelas Kendaraan**")
        vc = filtered_data["Vehicle Class"].value_counts().head(8)
        fig4, ax4 = plt.subplots(figsize=(5, 3))
        palette = ["#16a34a","#4ade80","#86efac","#15803d","#166534","#14532d","#fbbf24","#f87171"]
        ax4.barh(vc.index[::-1], vc.values[::-1], color=palette[:len(vc)], edgecolor="#0c0e12", linewidth=0.4)
        ax4.set_xlabel("Jumlah Kendaraan")
        ax4.grid(axis="x", alpha=0.4)
        fig4.tight_layout()
        st.pyplot(fig4, use_container_width=True)

# ═════════════════════════════════════════════
# PAGE: BOBOT KRITERIA
# ═════════════════════════════════════════════
elif page == "Bobot Kriteria":
    st.markdown("<p class='section-label'>AHP — Langkah 1</p>", unsafe_allow_html=True)
    st.markdown("##  Matriks Perbandingan Berpasangan")
    st.markdown(
        "<p style='color:#6b7280;max-width:700px'>Isi nilai perbandingan antar kriteria menggunakan skala Saaty (1–9). "
        "Segitiga atas diisi manual; segitiga bawah otomatis menjadi nilai resiprokal.</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    short = ["CO₂", "Kota", "Hwy", "Gabung", "MPG", "Mesin", "Silinder"]

    mat = st.session_state["matrix"].copy()

    st.markdown("#### Input Nilai Perbandingan")
    st.caption("Isi sel di bawah ini (segitiga atas). 1 = sama penting, 9 = jauh lebih penting.")

    pairs = [(i, j) for i in range(N) for j in range(i+1, N)]
    cols_per_row = 2
    rows = [pairs[k:k+cols_per_row] for k in range(0, len(pairs), cols_per_row)]

    for row in rows:
        cols = st.columns(cols_per_row)
        for idx, (i, j) in enumerate(row):
            with cols[idx]:
                label = f"{short[i]} vs {short[j]}"
                val = st.number_input(
                    label,
                    min_value=0.111,
                    max_value=9.0,
                    value=float(round(mat[i, j], 3)),
                    step=0.5,
                    format="%.3f",
                    key=f"m_{i}_{j}",
                )
                mat[i, j] = val
                mat[j, i] = 1.0 / val

    st.session_state["matrix"] = mat

    st.markdown("---")
    st.markdown("#### Matriks Perbandingan (Preview)")
    df_mat = pd.DataFrame(
        np.round(mat, 4),
        columns=short,
        index=short,
    )
    st.dataframe(df_mat, use_container_width=True)

    st.markdown("---")
    st.markdown("""
    <div class='eco-card'>
        <p class='section-label'>Referensi Skala Saaty</p>
        <table style='width:100%;color:#9da5b4;font-family:DM Mono,monospace;font-size:0.78rem;border-collapse:collapse'>
            <tr style='color:#4ade80'>
                <th style='text-align:left;padding:4px 8px'>Nilai</th>
                <th style='text-align:left;padding:4px 8px'>Arti</th>
            </tr>
            <tr><td style='padding:3px 8px'>1</td><td style='padding:3px 8px'>Sama penting</td></tr>
            <tr><td style='padding:3px 8px'>3</td><td style='padding:3px 8px'>Sedikit lebih penting</td></tr>
            <tr><td style='padding:3px 8px'>5</td><td style='padding:3px 8px'>Lebih penting</td></tr>
            <tr><td style='padding:3px 8px'>7</td><td style='padding:3px 8px'>Jauh lebih penting</td></tr>
            <tr><td style='padding:3px 8px'>9</td><td style='padding:3px 8px'>Mutlak lebih penting</td></tr>
            <tr><td style='padding:3px 8px'>2,4,6,8</td><td style='padding:3px 8px'>Nilai antara</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# ═════════════════════════════════════════════
# PAGE: PERHITUNGAN AHP
# ═════════════════════════════════════════════
elif page == "Perhitungan AHP":
    st.markdown("<p class='section-label'>AHP — Langkah 2</p>", unsafe_allow_html=True)
    st.markdown("##  Perhitungan AHP")

    mat = st.session_state["matrix"]
    weights, lambda_max, ci, cr = compute_ahp(mat)
    st.session_state["weights"] = weights

    tab1, tab2, tab3 = st.tabs(["Normalisasi & Bobot", "Konsistensi (CR)", "Visualisasi Bobot"])

    with tab1:
        st.markdown("#### Matriks Perbandingan Asli")
        short = ["CO₂","Kota","Hwy","Gabung","MPG","Mesin","Silinder"]
        df_mat = pd.DataFrame(np.round(mat, 4), columns=short, index=short)
        st.dataframe(df_mat, use_container_width=True)

        st.markdown("#### Matriks Ternormalisasi (dibagi jumlah kolom)")
        col_sum = mat.sum(axis=0)
        norm_mat = mat / col_sum
        df_norm = pd.DataFrame(np.round(norm_mat, 4), columns=short, index=short)
        st.dataframe(df_norm, use_container_width=True)

        st.markdown("#### Bobot Prioritas Kriteria (rata-rata baris)")
        df_bobot = pd.DataFrame({
            "Kriteria": KRITERIA,
            "Bobot": np.round(weights, 5),
            "Bobot (%)": np.round(weights * 100, 2),
            "Tipe": TIPE,
        })
        st.dataframe(df_bobot, use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("#### Uji Konsistensi Matriks")

        c1, c2, c3 = st.columns(3)
        c1.metric("λ max", f"{lambda_max:.4f}")
        c2.metric("Consistency Index (CI)", f"{ci:.4f}")
        c3.metric("Consistency Ratio (CR)", f"{cr:.4f}")

        st.markdown("---")
        if cr < 0.1:
            st.markdown(f"""
            <div class='eco-card' style='border-color:rgba(74,222,128,0.3)'>
                <span class='eco-badge'>✓ Konsisten</span>
                <p style='margin-top:0.8rem;color:#9da5b4'>
                    Nilai CR = <span class='cr-ok'>{cr:.4f}</span> &lt; 0.10 — 
                    Matriks perbandingan <strong style='color:#4ade80'>dinyatakan konsisten</strong> 
                    dan bobot kriteria dapat digunakan untuk perhitungan selanjutnya.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='eco-card' style='border-color:rgba(248,113,113,0.3)'>
                <span style='background:rgba(248,113,113,0.12);color:#f87171;border:1px solid rgba(248,113,113,0.25);
                border-radius:20px;padding:2px 12px;font-family:DM Mono,monospace;font-size:0.72rem'>
                ✗ Tidak Konsisten</span>
                <p style='margin-top:0.8rem;color:#9da5b4'>
                    Nilai CR = <span class='cr-fail'>{cr:.4f}</span> ≥ 0.10 — 
                    Perbaiki nilai perbandingan pada halaman <strong>Bobot Kriteria</strong>.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### Tabel Nilai RI (Random Index)")
        ri_df = pd.DataFrame({
            "n": list(RI_TABLE.keys()),
            "RI": list(RI_TABLE.values()),
        })
        st.dataframe(ri_df.set_index("n").T, use_container_width=True)

    with tab3:
        set_matplotlib_dark()
        short_full = ["CO₂","BBM\nKota","BBM\nHwy","BBM\nGabung","MPG","Ukuran\nMesin","Silinder"]
        fig, axes = plt.subplots(1, 2, figsize=(11, 4))

        # Bar chart
        ax = axes[0]
        colors = ["#4ade80" if w == max(weights) else "#16a34a" if w >= np.percentile(weights,60) else "#166534" for w in weights]
        bars = ax.bar(short_full, weights * 100, color=colors, edgecolor="#0c0e12", linewidth=0.5, zorder=3)
        ax.set_ylabel("Bobot (%)")
        ax.set_title("Bobot Tiap Kriteria", color="#e8eaf0", fontsize=10)
        ax.grid(axis="y", alpha=0.35, zorder=0)
        for bar, w in zip(bars, weights):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    f"{w*100:.1f}%", ha="center", va="bottom", fontsize=7.5, color="#9da5b4")

        # Pie chart
        ax2 = axes[1]
        pie_colors = ["#4ade80","#16a34a","#15803d","#166534","#14532d","#fbbf24","#d97706"]
        wedges, texts, autotexts = ax2.pie(
            weights, labels=None, autopct="%1.1f%%",
            colors=pie_colors, startangle=140,
            wedgeprops={"edgecolor":"#0c0e12","linewidth":1.5},
            pctdistance=0.78,
        )
        for at in autotexts:
            at.set_fontsize(8); at.set_color("#e8eaf0")
        ax2.set_title("Proporsi Bobot", color="#e8eaf0", fontsize=10)
        ax2.legend(wedges, ["CO₂","Kota","Hwy","Gabung","MPG","Mesin","Silinder"],
                   loc="center left", bbox_to_anchor=(1,0.5),
                   fontsize=7.5, framealpha=0, labelcolor="#9da5b4")

        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)

# ═════════════════════════════════════════════
# PAGE: HASIL PERANGKINGAN
# ═════════════════════════════════════════════
elif page == "Hasil Perangkingan":
    st.markdown("<p class='section-label'>AHP — Hasil Akhir</p>", unsafe_allow_html=True)
    st.markdown("##  Hasil Perangkingan Kendaraan")

    if st.session_state["weights"] is None:
        st.warning(" Bobot belum dihitung. Silakan buka halaman **Perhitungan AHP** terlebih dahulu.")
    else:
        st.markdown(
            "<p style='color:#6b7280;max-width:700px'>Tekan tombol di bawah untuk menjalankan perhitungan "
            "SAW × AHP pada seluruh dataset yang sudah difilter.</p>",
            unsafe_allow_html=True,
        )

        col_btn, _ = st.columns([1, 3])
        with col_btn:
            run = st.button("  Jalankan Perhitungan SPK")

        if run:
            with st.spinner("Menghitung skor seluruh kendaraan..."):
                weights = st.session_state["weights"]

                kolom_csv_7 = [
                    'CO2 Emissions(g/km)',
                    'Fuel Consumption City (L/100 km)',
                    'Fuel Consumption Hwy (L/100 km)',
                    'Fuel Consumption Comb (L/100 km)',
                    'Fuel Consumption Comb (mpg)',
                    'Engine Size(L)',
                    'Cylinders',
                ]
                tipe_7 = ['cost','cost','cost','cost','benefit','cost','cost']

                data_work = filtered_data.copy()
                data_work["Nama_Kendaraan"] = (
                    data_work["Make"] + " " + data_work["Model"]
                    + " [" + data_work.index.astype(str) + "]"
                )
                alt = data_work[["Nama_Kendaraan"] + kolom_csv_7].set_index("Nama_Kendaraan")
                alt.columns = KRITERIA

                df_norm = normalisasi_saw(alt, tipe_7)
                skor = df_norm.dot(weights)

                df_out = pd.DataFrame({
                    "Nama Kendaraan": alt.index,
                    "Skor Akhir": skor,
                    "CO₂ (g/km)": alt["Emisi CO2 (g/km)"].values,
                    "BBM Kota": alt["Konsumsi BBM Kota (L/100km)"].values,
                    "BBM Hwy": alt["Konsumsi BBM Hwy (L/100km)"].values,
                    "BBM Gabung": alt["Konsumsi BBM Gabungan (L/100km)"].values,
                    "MPG": alt["MPG (Miles Per Gallon)"].values,
                    "Mesin (L)": alt["Ukuran Mesin (L)"].values,
                    "Silinder": alt["Jumlah Silinder"].values,
                }).sort_values("Skor Akhir", ascending=False).reset_index(drop=True)

                df_out.index = df_out.index + 1
                df_out.index.name = "Ranking"
                df_out["Nama Kendaraan"] = df_out["Nama Kendaraan"].str.rsplit(" [", n=1).str[0]
                st.session_state["hasil"] = df_out

        if st.session_state["hasil"] is not None:
            df_hasil = st.session_state["hasil"]
            top = df_hasil.head(top_n)

            # ── Top 3 podium cards ──
            st.markdown("### Podium Kendaraan Terbaik")
            podium_cols = st.columns(3)
            podium_colors = ["#ca8a04","#6b7280","#92400e"]
            podium_labels = [" Terbaik #1"," Terbaik #2"," Terbaik #3"]
            for idx, col in enumerate(podium_cols):
                row = df_hasil.iloc[idx]
                with col:
                    st.markdown(f"""
                    <div class='eco-card' style='border-color:{podium_colors[idx]}44;text-align:center'>
                        <p style='color:{podium_colors[idx]};font-family:Syne,sans-serif;font-weight:700;font-size:0.85rem;margin:0'>
                            {podium_labels[idx]}</p>
                        <p style='font-family:Syne,sans-serif;font-weight:700;font-size:1.05rem;
                        margin:0.5rem 0;color:#e8eaf0;line-height:1.3'>{row['Nama Kendaraan']}</p>
                        <p style='color:#4ade80;font-family:DM Mono,monospace;font-size:1.1rem;
                        font-weight:700;margin:0'>Skor: {row['Skor Akhir']:.5f}</p>
                        <p style='color:#6b7280;font-family:DM Mono,monospace;font-size:0.76rem;margin-top:0.5rem'>
                            CO₂: {row['CO₂ (g/km)']:.0f} g/km · {row['BBM Gabung']:.1f} L/100km · {row['MPG']:.0f} MPG
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown(f"### Tabel Perangkingan — Top {top_n}")
            display_cols = ["Nama Kendaraan","Skor Akhir","CO₂ (g/km)","BBM Kota","BBM Hwy","BBM Gabung","MPG","Mesin (L)","Silinder"]
            st.dataframe(
                top[display_cols].style.format({
                    "Skor Akhir": "{:.6f}",
                    "CO₂ (g/km)": "{:.0f}",
                    "BBM Kota": "{:.1f}",
                    "BBM Hwy": "{:.1f}",
                    "BBM Gabung": "{:.1f}",
                    "MPG": "{:.0f}",
                    "Mesin (L)": "{:.1f}",
                    "Silinder": "{:.0f}",
                }).background_gradient(subset=["Skor Akhir"], cmap="Greens"),
                use_container_width=True,
                height=450,
            )

            # Visualisasi skor top N
            st.markdown("### Visualisasi Skor Akhir")
            set_matplotlib_dark()
            fig, ax = plt.subplots(figsize=(10, max(4, top_n * 0.38)))
            names = [n[:35] + "…" if len(n) > 35 else n for n in top["Nama Kendaraan"]]
            scores = top["Skor Akhir"].values
            cmap_vals = scores / scores.max()
            bar_colors = [plt.cm.RdYlGn(v) for v in cmap_vals]
            bars = ax.barh(names[::-1], scores[::-1], color=bar_colors[::-1], edgecolor="#0c0e12", linewidth=0.4)
            ax.set_xlabel("Skor Akhir (AHP × SAW)")
            ax.set_title(f"Top {top_n} Kendaraan Rendah Emisi", color="#e8eaf0")
            ax.grid(axis="x", alpha=0.35)
            for bar, sc in zip(bars, scores[::-1]):
                ax.text(bar.get_width() + 0.0005, bar.get_y() + bar.get_height()/2,
                        f"{sc:.5f}", va="center", fontsize=7.5, color="#9da5b4")
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)

            # Export
            st.markdown("---")
            csv_export = df_hasil.to_csv(index=True).encode("utf-8")
            st.download_button(
                label="⬇  Unduh Hasil Lengkap (.csv)",
                data=csv_export,
                file_name="hasil_ranking_kendaraan_rendah_emisi.csv",
                mime="text/csv",
            )

# ═════════════════════════════════════════════
# PAGE: PROFIL KELOMPOK
# ═════════════════════════════════════════════
elif page == "Profil Kelompok":
    st.markdown("<p class='section-label'>Tentang Proyek</p>", unsafe_allow_html=True)
    st.markdown("## Profil Kelompok")

    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.markdown("""
        <div class='eco-card'>
            <p class='section-label'>Identitas Proyek</p>
            <table style='width:100%;color:#9da5b4;font-family:DM Mono,monospace;
            font-size:0.82rem;border-collapse:collapse'>
                <tr>
                    <td style='padding:6px 0;color:#6b7280;width:40%'>Judul</td>
                    <td style='color:#e8eaf0;font-weight:600'>Pemilihan Kendaraan Rendah Emisi</td>
                </tr>
                <tr>
                    <td style='padding:6px 0;color:#6b7280'>Metode SPK</td>
                    <td style='color:#4ade80;font-weight:700'>AHP (Analytical Hierarchy Process)</td>
                </tr>
                <tr>
                    <td style='padding:6px 0;color:#6b7280'>Dataset</td>
                    <td style='color:#e8eaf0'>CO₂ Emissions Canada (7.385 baris)</td>
                </tr>
                <tr>
                    <td style='padding:6px 0;color:#6b7280'>Jumlah Kriteria</td>
                    <td style='color:#e8eaf0'>7 Kriteria</td>
                </tr>
                <tr>
                    <td style='padding:6px 0;color:#6b7280'>Mata Kuliah</td>
                    <td style='color:#e8eaf0'>Sistem Pendukung Keputusan</td>
                </tr>
                <tr>
                    <td style='padding:6px 0;color:#6b7280'>Tahun Akademik</td>
                    <td style='color:#e8eaf0'>2025 / 2026</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown("""
        <div class='eco-card'>
            <p class='section-label'>Anggota Kelompok</p>
            <div style='margin-top:0.5rem'>
                <div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:1rem'>
                    <div style='width:42px;height:42px;border-radius:50%;background:linear-gradient(135deg,#16a34a,#4ade80);
                    display:flex;align-items:center;justify-content:center;font-family:Syne,sans-serif;
                    font-weight:800;color:#0c0e12;font-size:1rem;flex-shrink:0'>1</div>
                    <div>
                        <p style='margin:0;color:#e8eaf0;font-family:Syne,sans-serif;font-weight:700'>
                            Aushaf Fathin Irsyad Nabil</p>
                        <p style='margin:0;color:#6b7280;font-family:DM Mono,monospace;font-size:0.76rem'>
                            NIM: 123240092</p>
                    </div>
                </div>
                <div style='display:flex;align-items:center;gap:0.8rem'>
                    <div style='width:42px;height:42px;border-radius:50%;background:linear-gradient(135deg,#15803d,#86efac);
                    display:flex;align-items:center;justify-content:center;font-family:Syne,sans-serif;
                    font-weight:800;color:#0c0e12;font-size:1rem;flex-shrink:0'>2</div>
                    <div>
                        <p style='margin:0;color:#e8eaf0;font-family:Syne,sans-serif;font-weight:700'>
                            Ari Satya Dinata</p>
                        <p style='margin:0;color:#6b7280;font-family:DM Mono,monospace;font-size:0.76rem'>
                            NIM: 123240018</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Kriteria Penilaian")
    crit_data = {
        "No": list(range(1, 8)),
        "Kriteria": KRITERIA,
        "Tipe": TIPE,
        "Kolom Dataset": [
            "CO2 Emissions(g/km)",
            "Fuel Consumption City (L/100 km)",
            "Fuel Consumption Hwy (L/100 km)",
            "Fuel Consumption Comb (L/100 km)",
            "Fuel Consumption Comb (mpg)",
            "Engine Size(L)",
            "Cylinders",
        ],
        "Keterangan": [
            "Emisi gas CO₂ per kilometer (lebih kecil lebih baik)",
            "Konsumsi bahan bakar di dalam kota (lebih kecil lebih baik)",
            "Konsumsi bahan bakar di jalan bebas hambatan (lebih kecil lebih baik)",
            "Konsumsi bahan bakar gabungan (lebih kecil lebih baik)",
            "Efisiensi bahan bakar dalam MPG (lebih besar lebih baik)",
            "Ukuran mesin dalam liter (lebih kecil lebih baik)",
            "Jumlah silinder mesin (lebih kecil lebih baik)",
        ],
    }
    st.dataframe(pd.DataFrame(crit_data).set_index("No"), use_container_width=True)

    st.markdown("### Alur Kerja Sistem")
    st.markdown("""
    <div class='eco-card'>
        <div style='display:flex;gap:0.8rem;align-items:flex-start;flex-wrap:wrap'>
            <div style='text-align:center;min-width:90px'>
                <div style='background:#1e2130;border-radius:10px;padding:0.7rem;
                color:#4ade80;font-family:Syne,sans-serif;font-weight:700;font-size:0.8rem'>
                 Input Dataset</div>
            </div>
            <div style='padding-top:0.7rem;color:#4ade80;font-size:1.2rem'>→</div>
            <div style='text-align:center;min-width:120px'>
                <div style='background:#1e2130;border-radius:10px;padding:0.7rem;
                color:#4ade80;font-family:Syne,sans-serif;font-weight:700;font-size:0.8rem'>
                 Matriks Perbandingan</div>
            </div>
            <div style='padding-top:0.7rem;color:#4ade80;font-size:1.2rem'>→</div>
            <div style='text-align:center;min-width:100px'>
                <div style='background:#1e2130;border-radius:10px;padding:0.7rem;
                color:#4ade80;font-family:Syne,sans-serif;font-weight:700;font-size:0.8rem'>
                 Hitung Bobot (AHP)</div>
            </div>
            <div style='padding-top:0.7rem;color:#4ade80;font-size:1.2rem'>→</div>
            <div style='text-align:center;min-width:100px'>
                <div style='background:#1e2130;border-radius:10px;padding:0.7rem;
                color:#4ade80;font-family:Syne,sans-serif;font-weight:700;font-size:0.8rem'>
                 Normalisasi SAW</div>
            </div>
            <div style='padding-top:0.7rem;color:#4ade80;font-size:1.2rem'>→</div>
            <div style='text-align:center;min-width:100px'>
                <div style='background:#16a34a;border-radius:10px;padding:0.7rem;
                color:#fff;font-family:Syne,sans-serif;font-weight:700;font-size:0.8rem'>
                 Ranking Kendaraan</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)