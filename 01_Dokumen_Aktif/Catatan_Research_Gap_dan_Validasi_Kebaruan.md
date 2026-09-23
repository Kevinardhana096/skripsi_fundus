# Catatan Research Gap dan Validasi Kebaruan

**Status arah penelitian:** fungsi loss menjadi studi pendahuluan; LEBER menjadi kontribusi metode utama.  
**Topik penelitian:** klasifikasi multi-label penyakit mata tingkat pasien menggunakan pasangan citra fundus mata kiri dan kanan pada ODIR-5K  
**Tanggal audit terakhir:** 15 September 2026  
**Rentang utama literatur fundus yang ditinjau:** 2021–2026  
**Catatan:** karya sebelum 2021 tetap diperiksa apabila merupakan prior art penting. Hal ini diperlukan agar unsur metode lama tidak keliru diklaim sebagai kebaruan.

## 1. Posisi penelitian saat ini

Penelitian menggunakan data tingkat pasien. Satu sampel terdiri atas dua citra fundus, yaitu citra mata kiri dan citra mata kanan, serta satu vektor target yang berisi delapan label:

| Kode | Label |
|---|---|
| N | Normal |
| D | Diabetes |
| G | Glaucoma |
| C | Cataract |
| A | Age-related Macular Degeneration |
| H | Hypertension |
| M | Pathological Myopia |
| O | Other diseases/abnormalities |

Model menerima kedua citra dan menghasilkan diagnosis pada tingkat pasien. Keluaran model bukan diagnosis terpisah untuk setiap mata. Kondisi ini penting karena label resmi ODIR-5K ditentukan berdasarkan informasi kedua mata dan usia pasien.

Eksperimen pendahuluan menggunakan shared ResNet50 pada resolusi 224 telah dilakukan dengan seed 42, 52, dan 62. Ringkasannya adalah:

| Fungsi loss | Rata-rata Test Macro-F1 ± SD |
|---|---:|
| BCE | 0,5877 ± 0,0071 |
| Weighted BCE | 0,5791 ± 0,0094 |
| Focal Loss | 0,5802 ± 0,0193 |
| Asymmetric Loss | **0,5909 ± 0,0115** |
| PolyLoss | 0,5868 ± 0,0111 |

ASL memperoleh rata-rata Macro-F1 tertinggi, tetapi selisihnya terhadap BCE dan PolyLoss kurang dari 0,005 dan belum diuji signifikansinya. Protokol utama kemudian beralih ke 512. BCE bilateral 512 seed 42 telah menghasilkan Test Macro-F1 0,6122; ASL sedang berjalan dan PolyLoss belum dijalankan. Pemilihan loss LEBER belum dikunci.

## 2. Mengapa evaluasi fungsi loss saja belum cukup sebagai kebaruan

Mengganti fungsi loss merupakan eksperimen yang sah karena loss mengatur besar dan arah koreksi kesalahan selama pelatihan. Pada data tidak seimbang, BCE, Weighted BCE, Focal Loss, ASL, dan PolyLoss dapat memberikan perhatian yang berbeda kepada contoh mudah, contoh sulit, label mayoritas, dan label minoritas.

Meskipun demikian, membandingkan beberapa fungsi loss saja lebih tepat disebut evaluasi empiris. Penelitian membutuhkan kontribusi metode dan modifikasi arsitektur. Oleh karena itu, hasil eksperimen loss dipertahankan sebagai dasar pemilihan loss untuk metode yang dikembangkan, bukan sebagai satu-satunya kebaruan.

## 3. Hasil audit penelitian terdahulu

### 3.1 Unsur yang sudah pernah dikerjakan

| Unsur rancangan | Status dalam literatur | Implikasi untuk klaim |
|---|---|---|
| Mengolah citra kedua mata secara bersamaan | Sudah ada pada BFPC-Net, BFENet, DMS-Net, Anatomy-Slot, dan DualCrossAttnNet | Tidak boleh diklaim sebagai kebaruan |
| Shared/Siamese backbone untuk kedua mata | Sudah digunakan pada penelitian bilateral | Tidak boleh diklaim sebagai kebaruan |
| Interaksi fitur kiri dan kanan | Sudah ada melalui attention, bidirectional attention, dan cross-attention | Tidak boleh diklaim sebagai kebaruan |
| Gated bilateral fusion | Sudah digunakan oleh DualCrossAttnNet | Gating secara umum bukan kebaruan |
| Tiga ahli berupa dua cabang unimodal dan satu cabang cross-modal | Konsep sangat mirip sudah ada pada multimodal mixture-of-experts | Susunan tiga ahli saja bukan kebaruan yang kuat |
| Mengarahkan bobot fusion menggunakan loss cabang | Sudah diperkenalkan oleh ARGate dalam multimodal sensor fusion | Target `softmax(-loss)` bukan kebaruan |
| Pertukaran input kiri dan kanan sebagai augmentasi | Sudah digunakan pada tesis multimodal ODIR tahun 2026 | Swap augmentation saja bukan kebaruan |
| Diagnosis eye-level dan patient-level secara bersamaan | Sudah dibahas oleh MMW-Net | Tidak boleh mengklaim pertama menghubungkan kedua tingkat diagnosis |

### 3.2 Literatur ODIR-5K yang relevan

1. **Official ODIR-2019/ODIR-5K.** Dataset berisi 5.000 pasien, citra fundus mata kiri dan kanan, usia, serta kata kunci diagnosis. Delapan label pasien ditentukan berdasarkan kedua mata dan usia.  
   Sumber: https://odir2019.grand-challenge.org/dataset/

2. **BFPC-Net (2022).** Menggunakan informasi fundus binocular, attention, dan feature fusion untuk diagnosis multi-label tingkat pasien.  
   Sumber: https://pmc.ncbi.nlm.nih.gov/articles/PMC9230753/

3. **BFENet (2022).** Menggunakan two-stream interaction CNN, multiscale representation, serta feature enhancement untuk diagnosis multi-label tingkat pasien.  
   Sumber: https://doi.org/10.1016/j.cmpb.2022.106739

4. **MMW-Net (2021).** Melakukan diagnosis multi-label pada tingkat mata dan pasien secara bersamaan melalui weak supervision. Naskah lengkap tidak tersedia secara bebas sehingga persamaan dan seluruh detail implementasinya belum dapat diaudit secara penuh.  
   Sumber: https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/login?o=dnclcdr&s=id%3D%22110NYCU5394031%22.&searchmode=basic

5. **Fundus-DeepNet (2023).** Menggunakan HRNet, attention, squeeze-and-excitation, perkalian elemen, dan penggabungan akhir informasi mata kiri dan kanan.  
   Sumber: https://doi.org/10.1016/j.inffus.2023.102059

6. **DMS-Net (2025).** Menggunakan shared Siamese ResNet-152, fitur multiskala, spatial-semantic recalibration, dan bidirectional attention untuk menggabungkan informasi bilateral.  
   Sumber: https://arxiv.org/abs/2504.18046

7. **DualCrossAttnNet (2026).** Menggunakan EfficientNet-B2, bilateral cross-attention, gated fusion, dan GeM pooling. Penelitian ini menunjukkan bahwa adaptive bilateral gating sudah digunakan pada ODIR.  
   Sumber: https://www.sciencedirect.com/science/article/pii/S0010482526003823

8. **Anatomy-Slot (2026).** Menggunakan anatomical factorization dan homologous bilateral reasoning. Penelitian ini menunjukkan bahwa manfaat informasi bilateral berbeda antarpenyakit: glaukoma sangat terbantu oleh perbandingan antarmata, sedangkan katarak dan miopia lebih banyak bergantung pada ciri monokular. Evaluasinya menggunakan sepuluh seed dan uji statistik.  
   Sumber: https://arxiv.org/abs/2605.12929

9. **C²Net (2026).** Memodelkan hubungan ko-occurence antarlabel, class imbalance, dan konsistensi logis diagnosis pada ODIR-5K dan MuReD.  
   Sumber: https://pubmed.ncbi.nlm.nih.gov/42048017/

10. **Multimodal Ocular Disease Recognition (2026).** Menggunakan evaluasi tingkat pasien, single-eye dan dual-image heads, metadata, serta probabilitas 50% untuk menukar posisi citra kiri dan kanan sebelum concatenation. Pertukaran tersebut dimaksudkan untuk mendorong permutation symmetry, tetapi bukan jaminan struktural bahwa keluaran model selalu invariant.  
    Sumber: https://dspace.cuni.cz/bitstream/handle/20.500.11956/207010/120534995.pdf?sequence=1

### 3.3 Prior art umum yang membatasi klaim kebaruan

1. **ARGate (2019).** Auxiliary loss dari setiap modalitas digunakan untuk membentuk target bobot fusion. Modalitas dengan loss lebih tinggi diarahkan memperoleh bobot lebih kecil. Karena itu, penggunaan target seperti `softmax(-loss/T)` tidak dapat diklaim sebagai metode baru. Karya ini lebih lama dari batas utama 2021, tetapi wajib diperiksa sebagai prior art.  
   Sumber: https://arxiv.org/abs/1901.10610

2. **Multi-gate Mixture-of-Experts.** Task-specific gate yang memilih kontribusi sejumlah expert telah digunakan dalam pembelajaran multi-task. Oleh karena itu, penggunaan gate per label tidak otomatis menjadi kebaruan global.  
   Sumber: https://doi.org/10.1145/3219819.3220007

3. **Adaptive multimodal expert fusion.** Literatur multimodal telah menggunakan cabang unimodal, cross-modal expert, dan adaptive gate. Dengan demikian, tiga cabang kiri–kanan–bilateral harus dibedakan melalui masalah dan aturan khusus diagnosis bilateral, bukan sekadar melalui jumlah cabang.

## 4. Temuan penting mengenai mata kiri dan kanan

Penelitian Scientific Reports tahun 2021 menunjukkan bahwa CNN dapat membedakan citra mata kiri dan kanan. Pada bagian eksperimen ODIR, DenseNet121 masih dapat membedakan citra kanan dan citra kiri yang telah dibalik horizontal dengan akurasi sekitar 91,13% dan AUC 0,912.

Temuan tersebut menunjukkan bahwa model dapat mempelajari ciri laterality atau ciri khas kiri–kanan yang tidak selalu merupakan bukti penyakit. Jika model menggunakan concatenation dalam urutan tetap, ada risiko posisi input menjadi jalan pintas. Padahal, target ODIR berada pada tingkat pasien; diagnosis pasien semestinya tidak berubah hanya karena urutan dua citra ditukar.

Sumber: https://www.nature.com/articles/s41598-021-04323-3

## 5. Research gap yang dipilih

### 5.1 Versi singkat

> Model bilateral pada ODIR-5K telah menggabungkan citra mata kiri dan kanan, tetapi belum secara eksplisit menentukan kontribusi mata kiri, mata kanan, dan hubungan bilateral untuk setiap label penyakit, serta belum menjamin bahwa diagnosis tingkat pasien tetap konsisten ketika urutan kedua citra mata ditukar.

### 5.2 Versi untuk latar belakang

> ODIR-5K menyediakan sepasang citra fundus mata kiri dan kanan dengan label diagnosis pada tingkat pasien. Sejumlah penelitian telah memanfaatkan informasi bilateral melalui Siamese network, feature fusion, cross-attention, dan gated fusion. Namun, mekanisme tersebut umumnya menggabungkan fitur kedua mata menjadi satu representasi global tanpa menjelaskan sumber bukti untuk setiap label penyakit. Padahal, kebutuhan terhadap informasi bilateral dapat berbeda antarpenyakit. Selain itu, model berbasis penggabungan berurutan berpotensi menghasilkan prediksi yang dipengaruhi oleh posisi input mata kiri dan kanan, meskipun pertukaran urutan kedua mata seharusnya tidak mengubah diagnosis pasien. Oleh karena itu, diperlukan mekanisme yang mampu mengatur kontribusi mata kiri, mata kanan, dan interaksi bilateral secara khusus untuk setiap label, sekaligus menjaga konsistensi prediksi terhadap pertukaran urutan citra.

### 5.3 Dasar kekuatan gap

Gap tersebut dibangun dari empat bukti yang saling berhubungan:

1. Label resmi ODIR-5K berada pada tingkat pasien dan ditentukan berdasarkan kedua mata.
2. Informasi bilateral tidak sama pentingnya untuk seluruh penyakit.
3. CNN dapat mempelajari perbedaan kiri–kanan yang tidak selalu berkaitan dengan penyakit.
4. Metode bilateral terdahulu telah memakai fusion dan gating, tetapi belum ditemukan dekomposisi bukti per label dengan jaminan struktural terhadap pertukaran urutan input.

## 6. Rancangan metode yang diusulkan

Nama kerja metode:

> **Label-wise Exchange-Equivariant Bilateral Evidence Routing (LEBER)**

Nama tersebut masih bersifat sementara dan dapat diubah setelah rancangan final ditetapkan.

### 6.1 Alur konseptual

```text
Citra mata kiri  ──> Shared ResNet50 ──> Expert kiri ──────┐
                                                           │
Citra mata kanan ──> Shared ResNet50 ──> Expert kanan ─────┼─> Router per label
                                                           │        │
Fitur kiri + kanan ──> Expert interaksi bilateral ─────────┘        ▼
                                                        Diagnosis tingkat pasien
```

Model menghasilkan tiga sumber bukti untuk setiap label:

1. bukti yang diperoleh dari mata kiri;
2. bukti yang diperoleh dari mata kanan;
3. bukti yang diperoleh dari hubungan atau interaksi kedua mata.

Router menghasilkan bobot yang berbeda untuk setiap label. Sebagai ilustrasi, untuk glaukoma model dapat memberikan bobot besar kepada interaksi bilateral, sedangkan untuk katarak model dapat memberikan bobot lebih besar kepada salah satu mata.

### 6.2 Encoder kedua mata

Kedua citra diproses oleh ResNet50 dengan bobot bersama:

$$
f_L=E(x_L), \qquad f_R=E(x_R)
$$

`E` adalah encoder yang sama. Shared encoder membuat kedua mata diproses dengan aturan yang sama dan menghindari penggandaan seluruh parameter backbone.

### 6.3 Representasi interaksi simetris

Representasi bilateral dibuat dari operasi yang tidak berubah ketika urutan input ditukar:

$$
f_B=[f_L+f_R,\ |f_L-f_R|,\ f_L\odot f_R]
$$

Keterangan:

- `f_L + f_R` merangkum informasi bersama dari kedua mata;
- `|f_L - f_R|` menangkap besar perbedaan kedua mata tanpa menetapkan salah satu mata sebagai yang utama;
- `f_L ⊙ f_R` menangkap ciri yang muncul bersama pada kedua mata.

Karena seluruh operasi tersebut simetris:

$$
f_B(f_L,f_R)=f_B(f_R,f_L)
$$

### 6.4 Expert dan router per label

Untuk label ke-`c`, model menghasilkan:

$$
z_{L,c},\quad z_{R,c},\quad z_{B,c}
$$

Router menghasilkan bobot:

$$
w_{L,c}+w_{R,c}+w_{B,c}=1
$$

Logit akhir pasien dihitung dengan:

$$
z_c=w_{L,c}z_{L,c}+w_{R,c}z_{R,c}+w_{B,c}z_{B,c}
$$

Berbeda dari global gate, bobot tersebut dihitung secara khusus untuk setiap label penyakit.

### 6.5 Sifat exchange-equivariant dan invariant

Jika posisi kedua mata ditukar, bobot mata kiri dan kanan harus ikut bertukar:

$$
w_L(x_L,x_R)=w_R(x_R,x_L)
$$

$$
w_R(x_L,x_R)=w_L(x_R,x_L)
$$

Bobot interaksi bilateral harus tetap sama:

$$
w_B(x_L,x_R)=w_B(x_R,x_L)
$$

Dengan susunan tersebut, prediksi pasien harus tetap sama:

$$
p(x_L,x_R)=p(x_R,x_L)
$$

Istilah **equivariant** berarti bagian yang memang mewakili kiri dan kanan ikut bertukar secara teratur ketika input ditukar. Istilah **invariant** berarti diagnosis akhir pasien tidak berubah.

Perbedaannya dengan swap augmentation adalah sebagai berikut:

- swap augmentation hanya memberikan contoh pertukaran selama pelatihan dan mendorong model belajar konsisten;
- exchange-equivariant architecture membuat perilaku pertukaran menjadi bagian dari konstruksi model sehingga tidak hanya bergantung pada keberhasilan pelatihan.

## 7. Klaim kebaruan yang boleh dan tidak boleh digunakan

### 7.1 Klaim yang tidak boleh digunakan

- “Penelitian pertama yang menggunakan kedua mata pada ODIR-5K.”
- “Penelitian pertama yang menggunakan Siamese network untuk citra fundus bilateral.”
- “Penelitian pertama yang menggunakan attention atau gated fusion pada ODIR-5K.”
- “Penelitian pertama yang menggunakan mixture-of-experts.”
- “Penelitian pertama yang mengarahkan bobot fusion menggunakan loss cabang.”
- “Penelitian pertama yang menukar citra kiri dan kanan saat training.”

Semua klaim tersebut telah memiliki pendahulu atau konsep yang sangat dekat.

### 7.2 Klaim yang lebih aman

> Penelitian ini mengusulkan mekanisme label-wise bilateral evidence routing yang memisahkan kontribusi bukti mata kiri, mata kanan, dan interaksi bilateral untuk setiap label penyakit serta menjaga konsistensi diagnosis tingkat pasien terhadap pertukaran urutan citra.

Versi yang lebih berhati-hati untuk naskah ilmiah:

> Berdasarkan literatur yang ditinjau, belum ditemukan penelitian pada ODIR-5K yang secara bersamaan menerapkan dekomposisi bukti mata kiri, mata kanan, dan interaksi bilateral pada setiap label serta router exchange-equivariant untuk menghasilkan diagnosis multi-label tingkat pasien yang invariant terhadap pertukaran urutan input.

Klaim “berdasarkan literatur yang ditinjau” harus dipertahankan. Audit literatur dapat memberikan keyakinan yang kuat, tetapi tidak dapat membuktikan secara mutlak bahwa tidak ada karya serupa di seluruh dunia, termasuk karya yang tidak terindeks, tidak berbahasa Inggris, belum dipublikasikan, atau tidak dapat diakses.

## 8. Hipotesis penelitian

Hipotesis utama:

> Pengaturan kontribusi bukti mata kiri, mata kanan, dan interaksi bilateral secara khusus untuk setiap label, disertai konsistensi terhadap pertukaran urutan input, dapat meningkatkan Macro-F1 dan kemampuan mendeteksi label penyakit dibandingkan penggabungan fitur bilateral konvensional.

Hipotesis pendukung:

1. Manfaat interaction expert berbeda antarlabel.
2. Label-wise router lebih efektif daripada satu global gate untuk semua label.
3. Konstruksi exchange-equivariant menurunkan perubahan prediksi akibat pertukaran urutan input.
4. Peningkatan metode lengkap tidak hanya disebabkan oleh bertambahnya parameter model.

## 9. Rencana pembuktian melalui eksperimen

Validasi literatur hanya membuktikan bahwa masalah dan ruang kontribusi tersedia. Efektivitas metode harus dibuktikan melalui eksperimen terkontrol.

### 9.1 Ablation study

| ID | Konfigurasi | Tujuan |
|---|---|---|
| A0 | Shared ResNet50 + concatenation + loss 512 terpilih | Baseline arsitektur |
| A1 | Shared ResNet50 + symmetric interaction features | Menguji manfaat representasi simetris |
| A2 | Tiga expert + rata-rata bobot tetap | Menguji apakah penambahan expert saja membantu |
| A3 | Tiga expert + satu global gate | Membandingkan global gate dengan label-wise gate |
| A4 | Tiga expert + label-wise router | Menguji manfaat routing per label |
| A5 | A4 + target kualitas expert | Menguji manfaat supervisi router |
| A6 | A5 + exchange-equivariant construction/consistency | Metode lengkap yang diusulkan |

Jika A6 lebih baik daripada A0 sampai A5, hasil tersebut menunjukkan bahwa peningkatan bukan sekadar akibat penambahan cabang atau parameter.

### 9.2 Pengujian konsistensi pertukaran

Prediksi dihitung dua kali menggunakan pasangan yang sama:

1. urutan asli `(mata kiri, mata kanan)`;
2. urutan terbalik `(mata kanan, mata kiri)`.

Perbedaan prediksi dihitung dengan:

$$
\Delta_p=\operatorname{mean}|p(x_L,x_R)-p(x_R,x_L)|
$$

Nilai `Δp` yang mendekati nol menunjukkan bahwa diagnosis tidak dipengaruhi urutan input.

Konsistensi router dihitung dengan:

$$
\Delta_w=\operatorname{mean}|w_L(x_L,x_R)-w_R(x_R,x_L)|
$$

Nilai `Δw` yang mendekati nol menunjukkan bahwa bobot kiri dan kanan bertukar dengan benar.

Untuk model yang invariant secara konstruksi dan dijalankan dalam mode evaluasi deterministik, selisih ideal hanya berupa error numerik yang sangat kecil. Batas praktis seperti `10^-6` dapat digunakan untuk unit test, tetapi perlu disesuaikan dengan presisi komputasi yang digunakan.

### 9.3 Metrik performa

Metrik yang perlu dilaporkan:

- Macro-F1 sebagai metrik utama;
- F1 setiap label;
- recall setiap label;
- precision setiap label;
- AUC dan/atau mAP;
- performa khusus label minoritas;
- nilai `Δp` dan `Δw`;
- jumlah parameter;
- durasi training dan inference;
- visualisasi Layer-CAM untuk masing-masing cabang.

Macro-F1 tetap menjadi metrik utama karena memberikan bobot yang setara kepada seluruh label, sehingga label dengan jumlah data sedikit tidak tertutup oleh label mayoritas.

### 9.4 Pengulangan dan uji statistik

Eksperimen utama sebaiknya dijalankan dengan minimal tiga seed, misalnya 42, 52, dan 62. Hasil dilaporkan sebagai rata-rata dan standar deviasi:

$$
\text{Macro-F1}=\text{mean}\pm\text{standard deviation}
$$

Jika sumber daya memungkinkan, gunakan lima seed. Selain itu, confidence interval dapat dihitung melalui bootstrap pada prediksi pasien dalam test set. Perbandingan statistik harus memakai prediksi pasien yang sama dari metode berbeda agar pengujian bersifat berpasangan.

Test set tidak boleh digunakan untuk memilih hyperparameter, threshold, atau versi arsitektur. Seluruh pemilihan dilakukan menggunakan validation set; test set dipakai satu kali untuk evaluasi akhir.

## 10. Batas validasi saat ini

Status validasi dibedakan menjadi dua:

1. **Validasi gap melalui literatur:** cukup kuat secara kondisional. Penelitian terdahulu membuktikan kebutuhan informasi bilateral, variasi manfaat bilateral antarlabel, dan potensi perbedaan kiri–kanan. Belum ditemukan kombinasi metode yang sama persis pada ODIR-5K.
2. **Validasi efektivitas metode:** belum dilakukan. Belum boleh menyatakan LEBER meningkatkan performa sebelum implementasi, ablation study, pengulangan seed, dan evaluasi test set selesai.

Karena publikasi baru dapat muncul, audit literatur perlu diperbarui sekali lagi sebelum proposal final atau sidang. Pencarian lanjutan perlu memakai istilah berikut:

- `ODIR-5K label-wise bilateral fusion`;
- `per-class left right eye gating`;
- `exchange-equivariant bilateral fundus`;
- `permutation-invariant paired fundus classification`;
- `bilateral evidence routing retinal disease`;
- `patient-level multi-label paired fundus mixture of experts`.

## 11. Kesimpulan yang dikunci sementara

Rancangan awal yang hanya menggabungkan tiga expert dan loss-guided router tidak cukup kuat sebagai kebaruan karena komponen-komponen tersebut sudah mempunyai pendahulu. Research gap yang lebih kuat terletak pada ketidaksesuaian antara karakter target tingkat pasien dan mekanisme fusion bilateral yang belum memberikan dekomposisi bukti per label serta belum menjamin konsistensi terhadap pertukaran urutan mata.

Kontribusi yang diusulkan adalah modifikasi arsitektur berupa label-wise exchange-equivariant bilateral evidence routing. Metode memisahkan bukti mata kiri, mata kanan, dan interaksi bilateral untuk setiap label, lalu menghasilkan diagnosis pasien yang tidak berubah ketika posisi kedua citra ditukar.

Klaim tersebut telah lolos audit literatur awal dengan tingkat keyakinan yang lebih kuat daripada rancangan sebelumnya, tetapi masih bersifat kondisional. Kebaruan final baru dapat dikunci setelah audit terakhir terhadap publikasi terkait dan efektivitasnya dibuktikan melalui eksperimen terkontrol.
