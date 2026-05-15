==============================================================
  INTERPRETASI HASIL K-MODES CLUSTERING - DATA DIABETES
==============================================================
  Metode    : K-Modes Clustering
  Dataset   : DataDiabetes1.xlsx
  Jumlah K  : 3 Cluster
  Bahasa    : Python
==============================================================


----------------------------------------------------------------
1. INFORMASI UMUM DATASET
----------------------------------------------------------------
  Jumlah data        : 1.163 baris, 17 kolom
  Duplikat           : 0 (tidak ada)
  Missing Value      :
    - Lingkar Perut  : 748 data kosong (~64%)
    - Diagnosa 2     : 583 data kosong (~50%)

  Catatan:
  Missing value pada dua kolom di atas dianggap wajar karena
  tidak semua pasien memiliki data lingkar perut yang diukur,
  dan tidak semua pasien memiliki diagnosa penyerta (Diagnosa 2).
  Kedua kolom tersebut tidak diikutsertakan dalam proses clustering.


----------------------------------------------------------------
2. KOLOM YANG DIGUNAKAN UNTUK CLUSTERING
----------------------------------------------------------------
  Setelah pre-processing, kolom yang digunakan adalah:

  No  Kolom Asli        Kolom Hasil             Keterangan
  --  ----------------  ----------------------  --------------------------
  1   Jenis Kelamin     Jenis Kelamin           Langsung dipakai (P / L)
  2   Umur Tahun        Kel_Umur                Dibin: Muda / Dewasa / Lansia
  3   Hasil IMT         Hasil_IMT               GEMUK & SANGAT GEMUK digabung
  4   Sistole           Kel_Sistole             Dibin: Normal / Pre-Hipertensi / Hipertensi
  5   Diagnosa 1        Diagnosa                Diambil kode ICD (misal E11.8)


----------------------------------------------------------------
3. EVALUASI MODEL
----------------------------------------------------------------
  Silhouette Score  : 0.2578
  Total Cost        : 1.417
  Jumlah Cluster    : 3

  Penjelasan Silhouette Score:
  Nilai 0.2578 termasuk kategori lemah-sedang. Hal ini umum
  terjadi pada data medis karena profil antar pasien diabetes
  cenderung mirip satu sama lain. Nilai positif tetap menunjukkan
  bahwa pengelompokan yang terbentuk lebih baik dibanding acak,
  artinya pola antar cluster masih dapat diidentifikasi.


----------------------------------------------------------------
4. DISTRIBUSI ANGGOTA CLUSTER
----------------------------------------------------------------
  Cluster 0  :  415 pasien  (35.7%)
  Cluster 1  :  493 pasien  (42.4%)  <- terbesar
  Cluster 2  :  255 pasien  (21.9%)  <- terkecil
  ----------------------------------------
  Total       : 1.163 pasien


----------------------------------------------------------------
5. PROFIL DAN INTERPRETASI TIAP CLUSTER
----------------------------------------------------------------

  ============================================================
  CLUSTER 0 - "Pria Lansia Berisiko Tinggi"
  Jumlah: 415 pasien (35.7%)
  ============================================================

  Atribut         Nilai Dominan       Persentase
  --------------  ------------------  ----------
  Jenis Kelamin   Laki-laki (L)          69.6%
  Kelompok Umur   Lansia (>60 th)        76.4%
  Hasil IMT       Ideal                  92.3%
  Tekanan Darah   Pre-Hipertensi         65.8%
  Diagnosa        E11.8 (DM tipe 2
                  + komplikasi)          54.7%

  Interpretasi:
  Cluster ini didominasi oleh pasien pria berusia lanjut (>60 tahun).
  Meskipun berat badan mayoritas masih dalam kategori ideal, kondisi
  tekanan darah sudah masuk pre-hipertensi dan diagnosa yang paling
  banyak adalah E11.8 yaitu DM tipe 2 dengan komplikasi tidak spesifik.
  Hal ini menunjukkan bahwa pada cluster ini, faktor usia menjadi
  pemicu utama komplikasi, bukan berat badan.

  Tingkat Risiko : TINGGI
  Rekomendasi    : Perlu pengawasan klinis intensif, pemantauan
                   tekanan darah rutin, dan manajemen komplikasi
                   yang lebih ketat.


  ============================================================
  CLUSTER 1 - "Wanita Dewasa Diabetes Tanpa Komplikasi"
  Jumlah: 493 pasien (42.4%) -- TERBESAR
  ============================================================

  Atribut         Nilai Dominan       Persentase
  --------------  ------------------  ----------
  Jenis Kelamin   Perempuan (P)          87.6%
  Kelompok Umur   Dewasa (40-60 th)      84.6%
  Hasil IMT       Ideal                  92.9%
  Tekanan Darah   Pre-Hipertensi         65.9%
  Diagnosa        E11.9 (DM tipe 2
                  tanpa komplikasi)      63.1%

  Interpretasi:
  Cluster terbesar ini didominasi wanita usia produktif (40-60 tahun)
  dengan berat badan ideal. Diagnosa yang mendominasi adalah E11.9
  yaitu DM tipe 2 tanpa komplikasi, yang berarti kelompok ini masih
  berada di tahap awal atau penyakitnya masih terkontrol dengan baik.
  Meski begitu, tekanan darah sudah menunjukkan tanda pre-hipertensi
  yang perlu diwaspadai.

  Tingkat Risiko : SEDANG
  Rekomendasi    : Target utama program edukasi kesehatan dan
                   pencegahan komplikasi sejak dini. Pemantauan
                   tekanan darah secara berkala sangat dianjurkan
                   agar tidak berkembang ke E11.8.


  ============================================================
  CLUSTER 2 - "Wanita Dewasa Diabetes Terkontrol"
  Jumlah: 255 pasien (21.9%) -- TERKECIL
  ============================================================

  Atribut         Nilai Dominan       Persentase
  --------------  ------------------  ----------
  Jenis Kelamin   Perempuan (P)          78.4%
  Kelompok Umur   Dewasa (40-60 th)      71.8%
  Hasil IMT       Ideal                  84.7%
  Tekanan Darah   Normal                 96.5%
  Diagnosa        E11.8 (DM tipe 2
                  + komplikasi)          47.5%

  Interpretasi:
  Secara demografi, cluster ini mirip dengan Cluster 1 (wanita, dewasa,
  IMT ideal). Perbedaan utama terletak pada tekanan darah yang Normal
  dengan persentase sangat tinggi (96.5%), menjadikan cluster ini yang
  paling stabil secara kardiovaskular. Meskipun sebagian sudah memiliki
  komplikasi (E11.8), kondisi fisik secara umum lebih terkontrol
  dibanding dua cluster lainnya.

  Tingkat Risiko : RELATIF RENDAH / TERKONTROL
  Rekomendasi    : Pertahankan pola hidup yang sudah baik, khususnya
                   kontrol tekanan darah. Tetap lakukan pemantauan
                   rutin untuk mencegah perkembangan komplikasi lebih
                   lanjut.


----------------------------------------------------------------
6. PERBANDINGAN ANTAR CLUSTER
----------------------------------------------------------------

  Aspek             Cluster 0        Cluster 1        Cluster 2
  ----------------  ---------------  ---------------  ---------------
  Dominasi Gender   Pria             Wanita           Wanita
  Usia              Lansia (>60 th)  Dewasa (40-60)   Dewasa (40-60)
  IMT               Ideal            Ideal            Ideal
  Tekanan Darah     Pre-Hipertensi   Pre-Hipertensi   Normal (96.5%)
  Komplikasi        Ada (E11.8)      Belum (E11.9)    Ada (E11.8)
  Jumlah Pasien     415 (35.7%)      493 (42.4%)      255 (21.9%)
  Tingkat Risiko    TINGGI           SEDANG           TERKONTROL


----------------------------------------------------------------
7. KESIMPULAN UMUM
----------------------------------------------------------------
  Dari hasil K-Modes Clustering dengan K=3, diperoleh tiga kelompok
  pasien diabetes dengan karakteristik yang berbeda secara klinis:

  1. Cluster 0 merepresentasikan pasien paling berisiko, yaitu pria
     lanjut usia dengan tekanan darah tinggi dan komplikasi diabetes.
     Kelompok ini membutuhkan penanganan medis yang paling intensif.

  2. Cluster 1 merupakan kelompok terbesar dan masih dalam kondisi
     tanpa komplikasi. Kelompok ini adalah target terbaik untuk
     program edukasi dan pencegahan dini agar kondisi tidak memburuk.

  3. Cluster 2 adalah kelompok dengan kondisi paling terkontrol,
     ditandai dengan tekanan darah normal yang sangat konsisten.
     Fokus utama adalah mempertahankan kondisi yang sudah baik ini.

  Secara keseluruhan, hasil clustering menunjukkan bahwa GENDER dan
  USIA adalah dua faktor pembeda utama antar kelompok pasien, sementara
  IMT (berat badan) tidak menjadi pembeda karena mayoritas pasien di
  semua cluster memiliki IMT ideal.


==============================================================
  Dibuat menggunakan Python - K-Modes Clustering
  Library : kmodes, pandas, scikit-learn, matplotlib, seaborn
==============================================================