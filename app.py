import streamlit as st
import pandas as pd
import kModes_Model as kmodes

# CONFIG

st.set_page_config(
    page_title="K-Modes Diabetes",
    page_icon="🩺",
    layout="wide"
)

# CUSTOM CSS

st.markdown("""
<style>

.main {
    background-color: #eef4ff;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #0f172a;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #2563eb, #1e40af);
    padding: 20px;
    border-radius: 18px;
    color: white;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
}

[data-testid="stMetricLabel"] {
    color: white;
    font-weight: bold;
}

[data-testid="stMetricValue"] {
    color: white;
}

div[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 15px;
    padding: 10px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.08);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 15px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #dbeafe;
    border-radius: 10px;
    padding: 10px 20px;
    color: #1e3a8a;
    font-weight: bold;
}

.stTabs [aria-selected="true"] {
    background-color: #2563eb !important;
    color: white !important;
}

.stButton>button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px;
    font-size: 16px;
    font-weight: bold;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #1d4ed8, #1e40af);
    color: white;
}

.stAlert {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# HEADER

st.title("🩺 Dashboard K-Modes Clustering Diabetes")

st.markdown("""
### Analisis Clustering Pasien Diabetes Menggunakan Algoritma K-Modes
""")

st.divider()

# TAB
tab1, tab2 = st.tabs([
    "📊 Hasil Clustering",
    "🧠 Diagnosa & Cluster"
])

# TAB 1
with tab1:

    st.header("📊 Hasil Clustering")

    # METRIC
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Jumlah Data",
            len(kmodes.df)
        )

    with col2:
        st.metric(
            "Jumlah Cluster",
            kmodes.k_optimal
        )

    with col3:
        st.metric(
            "Silhouette Score",
            f"{kmodes.sil_score:.4f}"
        )

    st.divider()

    # DATASET
    st.subheader("🗂 Dataset Hasil Clustering")

    st.dataframe(
        kmodes.df,
        use_container_width=True,
        height=400
    )

    st.divider()

    # DISTRIBUSI CLUSTER
    st.subheader("📌 Distribusi Anggota Cluster")

    distribusi = kmodes.df[
        'Cluster'
    ].value_counts().sort_index()

    st.dataframe(
        distribusi.reset_index().rename(
            columns={
                'index': 'Cluster',
                'Cluster': 'Jumlah Pasien'
            }
        ),
        use_container_width=True
    )

    st.divider()

    # MODES
    st.subheader("🎯 Modes Tiap Cluster")

    st.dataframe(
        kmodes.modes_df,
        use_container_width=True
    )

    st.divider()

    # VISUALISASI
    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📈 Elbow Method")

        st.image(
            "elbow_kmodes.png",
            use_container_width=True
        )

    with col2:

        st.subheader("📊 Visualisasi Cluster")

        st.image(
            "visualisasi_cluster.png",
            use_container_width=True
        )

    st.divider()

    # INTERPRETASI
    st.subheader("📋 Karakteristik Tiap Cluster")

    for i in range(kmodes.k_optimal):

        subset = kmodes.df[
            kmodes.df['Cluster'] == i
        ][kmodes.kolom_cluster]

        with st.expander(
            f"Cluster {i} ({len(subset)} pasien)"
        ):

            for col in kmodes.kolom_cluster:

                top_val = subset[col].mode()[0]

                pct = (
                    (subset[col] == top_val).mean()
                ) * 100

                st.write(
                    f"✅ {col} → {top_val} ({pct:.1f}%)"
                )

# TAB 2
with tab2:

    st.header("🧠 Prediksi Diagnosa & Cluster")

    st.markdown("""
    Masukkan data pasien untuk mengetahui cluster dan diagnosa dominan.
    """)

    st.divider()

    # INPUT
    col1, col2 = st.columns(2)

    with col1:

        jenis_kelamin = st.selectbox(
            "👤 Jenis Kelamin",
            ["L", "P"]
        )

        umur = st.number_input(
            "🎂 Umur",
            min_value=1,
            max_value=120,
            value=40
        )

    with col2:

        imt = st.selectbox(
            "⚖️ Kategori IMT",
            ["KURUS", "NORMAL", "GEMUK"]
        )

        sistole = st.number_input(
            "🩸 Tekanan Sistole",
            min_value=50,
            max_value=300,
            value=120
        )

    st.divider()

    # KATEGORI UMUR

    if umur <= 40:
        kel_umur = "Muda"

    elif umur <= 60:
        kel_umur = "Dewasa"

    else:
        kel_umur = "Lansia"

    # KATEGORI SISTOLE
    if sistole <= 120:
        kel_sistole = "Normal"

    elif sistole <= 140:
        kel_sistole = "Pre-Hipertensi"

    else:
        kel_sistole = "Hipertensi"

    # PREDIKSI
    if st.button(
        "🔍 Prediksi Sekarang",
        use_container_width=True
    ):

        data_baru = pd.DataFrame([{
            'Jenis Kelamin': jenis_kelamin,
            'Kel_Umur': kel_umur,
            'Hasil_IMT': imt,
            'Kel_Sistole': kel_sistole,
            'Diagnosa': 'Unknown'
        }])

        pred_cluster = kmodes.km_final.predict(
            data_baru
        )[0]

        subset = kmodes.df[
            kmodes.df['Cluster'] == pred_cluster
        ]

        diagnosa_pred = subset[
            'Diagnosa'
        ].mode()[0]

        st.success(
            f"✅ Pasien masuk ke Cluster {pred_cluster}"
        )

        st.info(
            f"🩺 Prediksi Diagnosa Dominan: {diagnosa_pred}"
        )

        st.subheader("📋 Karakteristik Cluster")

        for col in kmodes.kolom_cluster:

            top_val = subset[col].mode()[0]

            pct = (
                (subset[col] == top_val).mean()
            ) * 100

            st.write(
                f"✅ {col} → {top_val} ({pct:.1f}%)"
            )