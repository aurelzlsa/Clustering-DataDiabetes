# ============================================================
# K-MODES CLUSTERING - DATA DIABETES
# ============================================================

# ── 1. IMPORT LIBRARY ────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from kmodes.kmodes import KModes
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import LabelEncoder

# ── 2. LOAD DATASET ──────────────────────────────────────────
df = pd.read_excel("DataDiabetes1.xlsx")

print("=== INFORMASI UMUM DATASET ===")
print(f"Jumlah baris & kolom : {df.shape}")
print(f"\nTipe data tiap kolom :")
print(df.dtypes)
print(f"\nMissing value per kolom :")
print(df.isnull().sum())
print(f"\nDuplikat : {df.duplicated().sum()} baris")

# ── 3. PRE-PROCESSING ────────────────────────────────────────

# Hapus duplikat
df.drop_duplicates(inplace=True)

# Ekstrak angka dari kolom bertipe string
df['Umur']    = df['Umur Tahun'].str.extract(r'(\d+)').astype(int)
df['Sistole'] = df['Sistole'].str.extract(r'(\d+)').astype(int)

# Bin Umur → kategori
df['Kel_Umur'] = pd.cut(
    df['Umur'],
    bins=[0, 40, 60, 200],
    labels=['Muda', 'Dewasa', 'Lansia']
).astype(str)

# Bin Sistole → kategori tekanan darah
df['Kel_Sistole'] = pd.cut(
    df['Sistole'],
    bins=[0, 120, 140, 300],
    labels=['Normal', 'Pre-Hipertensi', 'Hipertensi']
).astype(str)

# IMT: gabungkan nilai yang sangat sedikit
imt_map = {'SANGAT GEMUK': 'GEMUK', 'GEMUK': 'GEMUK'}
df['Hasil_IMT'] = df['Hasil IMT'].replace(imt_map)

# Sederhanakan label Diagnosa 1 (ambil kode ICD saja)
df['Diagnosa'] = df['Diagnosa 1'].str.extract(r'\((\w+[\.\d]*)\)')

# Pilih kolom kategorikal untuk clustering
kolom_cluster = ['Jenis Kelamin', 'Kel_Umur', 'Hasil_IMT', 'Kel_Sistole', 'Diagnosa']
df_cluster = df[kolom_cluster].astype(str)

print("\n=== DATA SIAP CLUSTERING ===")
print(df_cluster.head())
print(f"\nShape data cluster : {df_cluster.shape}")

# ── 4. ENCODING ──────────────────────────────────────────────
# K-Modes tidak butuh One-Hot Encoding
# LabelEncoder hanya untuk keperluan Silhouette Score
le = LabelEncoder()
df_encoded = df_cluster.apply(le.fit_transform)

# ── 5. ELBOW METHOD → TENTUKAN K OPTIMAL ─────────────────────
cost = []
K_range = range(2, 9)

for k in K_range:
    km = KModes(n_clusters=k, init='Huang', n_init=10, verbose=0, random_state=42)
    km.fit(df_cluster)
    cost.append(km.cost_)

plt.figure(figsize=(8, 4))
plt.plot(K_range, cost, 'bo-', linewidth=2, markersize=8)
plt.xlabel('Jumlah Cluster (k)')
plt.ylabel('Cost (Dissimilarity)')
plt.title('Elbow Method - K-Modes Clustering')
plt.xticks(K_range)
plt.tight_layout()
plt.savefig('elbow_kmodes.png', dpi=150)
plt.show()
print("\nGrafik Elbow disimpan → elbow_kmodes.png")

# ── 6. FIT MODEL K-MODES ─────────────────────────────────────
k_optimal = 3   # sesuai hasil elbow

km_final = KModes(n_clusters=k_optimal, init='Huang', n_init=10, verbose=0, random_state=42)
clusters = km_final.fit_predict(df_cluster)

df['Cluster'] = clusters
print(f"\n=== MODEL SELESAI | K = {k_optimal} ===")

# ── 7. EVALUASI ───────────────────────────────────────────────
sil_score = silhouette_score(df_encoded, clusters, metric='hamming')
print(f"Silhouette Score  : {sil_score:.4f}")
print(f"Total Cost        : {km_final.cost_:.0f}")

print("\nDistribusi anggota tiap cluster :")
print(df['Cluster'].value_counts().sort_index())

print("\nModes tiap cluster :")
modes_df = pd.DataFrame(km_final.cluster_centroids_, columns=kolom_cluster)
modes_df.index.name = 'Cluster'
print(modes_df)

# ── 8. VISUALISASI ────────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(16, 9))
axes = axes.flatten()

for i, col in enumerate(kolom_cluster):
    sns.countplot(data=df, x=col, hue='Cluster', palette='Set2', ax=axes[i])
    axes[i].set_title(f'Distribusi {col} per Cluster')
    axes[i].tick_params(axis='x', rotation=30)
    axes[i].legend(title='Cluster')

# Pie chart distribusi cluster
axes[5].pie(
    df['Cluster'].value_counts().sort_index(),
    labels=[f'Cluster {i}' for i in range(k_optimal)],
    autopct='%1.1f%%',
    colors=sns.color_palette('Set2', k_optimal)
)
axes[5].set_title('Proporsi Cluster')

plt.suptitle('K-Modes Clustering - Data Diabetes', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('visualisasi_cluster.png', dpi=150)
plt.show()
print("Visualisasi disimpan → visualisasi_cluster.png")

# ── 9. INTERPRETASI CLUSTER ───────────────────────────────────
print("\n=== KARAKTERISTIK TIAP CLUSTER ===")
for i in range(k_optimal):
    subset = df[df['Cluster'] == i][kolom_cluster]
    print(f"\n--- Cluster {i} ({len(subset)} pasien) ---")
    for col in kolom_cluster:
        top_val = subset[col].mode()[0]
        pct     = (subset[col] == top_val).mean() * 100
        print(f"  {col:<15} → {top_val} ({pct:.1f}%)")