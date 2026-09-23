# OUTLINE PENELITIAN

Sistem Informasi Cerdas - Multi-Label Klasifikasi Penyakit Mata pada Citra Fundus

### Judul Sementara

Klasifikasi Multi-Label Penyakit Mata dengan Routing Bukti Bilateral Ekuivarian pada ODIR-5K

### Status dokumen

- Outline awal untuk pengembangan proposal penelitian.

- Research gap dan arah metode telah diperbarui. Eksperimen lima fungsi loss menjadi studi pendahuluan; LEBER dan Layer-CAM menjadi fokus pengembangan serta evaluasi utama.

## 1. POSISI DAN ARAH PENELITIAN

Fokus bidang: Sistem Informasi, peminatan Sistem Informasi Cerdas. Pendekatan teknis yang digunakan adalah deep learning, khususnya multi-label image classification pada citra fundus. Citra fundus diposisikan sebagai domain kasus, sedangkan fokus penelitian berada pada mekanisme intelligent information processing yang mengubah data visual menjadi informasi prediktif yang dapat dijelaskan.

## 2. BAB I - PENDAHULUAN

### 2.1 Latar Belakang

- Sistem Informasi Cerdas: kebutuhan mengolah data kompleks menjadi informasi yang mendukung pengambilan keputusan.

- Citra fundus sebagai sumber data visual yang kompleks untuk pengembangan sistem cerdas.

- Multi-label classification: satu data dapat berkaitan dengan lebih dari satu kondisi penyakit.

- Tantangan pembelajaran: ketidakseimbangan label dan positive-negative imbalance pada multi-label data.

- Keterbatasan loss standar seperti Binary Cross-Entropy untuk kondisi tertentu.

- Kebutuhan interpretabilitas: sistem sebaiknya tidak hanya menghasilkan probabilitas, tetapi juga membantu memahami dasar prediksi.

- Ringkasan penelitian terdahulu, terutama yang menggunakan ODIR-5K, multi-label learning, imbalance handling, loss function, dan XAI.

- Research gap: model bilateral terdahulu belum ditemukan memisahkan bukti kiri, kanan, dan interaksi bilateral secara per label sekaligus menjamin konsistensi diagnosis pasien terhadap pertukaran input.

- Arah penelitian: mengembangkan LEBER, mengujinya melalui ablation study dan beberapa seed, lalu menganalisis kontribusi cabang menggunakan bobot router dan Layer-CAM.

### Urgensi Penelitian

Urgensi klinis: gangguan penglihatan dan kebutaan merupakan masalah kesehatan global. Organisasi Kesehatan Dunia melaporkan sedikitnya 2,2 miliar orang mengalami gangguan penglihatan atau kebutaan, dan sedikitnya 1 miliar kasus berpotensi dapat dicegah atau belum tertangani (WHO, 2023). Kondisi ini menegaskan kebutuhan terhadap skrining yang lebih cepat, terjangkau, dan dapat menjangkau wilayah dengan keterbatasan tenaga ahli.

Urgensi data dan teknis: ODIR-5K memiliki label tidak seimbang dan target tingkat pasien yang berasal dari pasangan mata. Manfaat informasi bilateral berbeda antarpenyakit, sedangkan model dapat mempelajari ciri laterality. Sistem perlu mengatur kontribusi kiri, kanan, dan interaksi untuk setiap label serta menjaga hasil saat urutan input ditukar.

Urgensi kepercayaan: keluaran sistem kesehatan tidak cukup hanya berupa probabilitas. Pengguna perlu melihat bagian citra yang berkontribusi terhadap prediksi agar hasil dapat ditinjau secara kritis. Layer-CAM digunakan untuk menunjukkan dasar visual prediksi dengan detail spasial yang lebih rinci melalui informasi dari beberapa layer CNN. Peta ini berfungsi sebagai interpretasi pendukung, bukan pengganti validasi klinis atau penanda lokasi lesi dari dokter.

Urgensi akademik dan sistem informasi: penelitian bilateral telah menggunakan Siamese network, attention, cross-attention, dan gated fusion. Masih diperlukan mekanisme yang menguraikan sumber bukti per label dan mengikuti sifat target tingkat pasien. Studi fungsi loss mendukung pemilihan konfigurasi, sedangkan kontribusi utama berada pada modifikasi arsitektur LEBER.

### 2.2 Rumusan Masalah

1. Bagaimana merancang mekanisme yang memisahkan bukti mata kiri, mata kanan, dan interaksi bilateral untuk setiap label?

2. Apakah label-wise bilateral evidence routing meningkatkan performa dibandingkan feature concatenation dan global gate?

3. Apakah exchange-equivariant design menjaga diagnosis pasien tetap konsisten ketika urutan kedua mata ditukar?

4. Bagaimana bobot router dan Layer-CAM menjelaskan kontribusi setiap cabang untuk masing-masing label?

### 2.3 Tujuan Penelitian

1. Mengembangkan metode LEBER untuk klasifikasi multi-label tingkat pasien pada ODIR-5K.

2. Menguji kontribusi symmetric fusion, tiga expert, global gate, label-wise router, supervisi kualitas, dan exchange-equivariant design melalui ablation study.

3. Mengukur performa, kestabilan antar-seed, dan konsistensi pertukaran input.

4. Menganalisis kontribusi cabang menggunakan bobot router per label dan Layer-CAM.

### 2.4 Manfaat Penelitian

- Akademik: memperkaya kajian Sistem Informasi Cerdas dalam intelligent processing pada data citra dan multi-label learning.

- Praktis: menghasilkan mekanisme pengolahan citra yang dapat memberikan informasi prediktif multi-penyakit secara lebih informatif dan dapat dijelaskan.

### 2.5 Batasan Penelitian

- Dataset utama: ODIR-5K.

- Fokus: klasifikasi/prediksi multi-label pada tingkat pasien, bukan diagnosis klinis atau diagnosis terpisah untuk mata kiri dan kanan.

- Pendekatan model: deep learning.

- Studi pendahuluan: BCE, Weighted BCE, Focal Loss, Asymmetric Loss, dan PolyLoss dengan konfigurasi sama; hasil digunakan untuk memilih kandidat loss dan baseline.

- XAI: Layer-CAM pada layer konvolusi yang ditetapkan sebelum eksperimen; Grad-CAM dibahas sebagai pembanding konseptual di tinjauan pustaka.

- Evaluasi utama: Macro-F1 delapan label, Micro-F1, AUROC, precision, recall, F1 per kelas, dan Hamming Loss. Analisis sekunder menghitung Macro-F1 enam penyakit spesifik tanpa N dan O.

- Pembagian data dilakukan pada level pasien. Citra mata kiri dan kanan pasien yang sama selalu berada pada subset yang sama untuk mencegah data leakage.

## 3. BAB II - TINJAUAN PUSTAKA

### 3.1 Sistem Informasi Cerdas

- Konsep Sistem Informasi Cerdas

- Intelligent information processing

- Decision support / decision-support context

### 3.2 Citra Fundus Mata

- Konsep dan karakteristik fundus image

- Penyakit/label yang digunakan dalam dataset

### 3.3 Machine Learning dan Deep Learning

- Posisi deep learning dalam machine learning

- CNN

- Transfer learning

- Backbone ResNet50 pretrained ImageNet

### 3.4 Multi-Label Classification

- Single-label, multi-class, dan multi-label

- Sigmoid output

- Label co-occurrence

### 3.5 Class Imbalance

- Ketidakseimbangan antar kelas

- Positive-negative imbalance

- Dampak terhadap pembelajaran model

### 3.6 Fungsi Loss dan Studi Pendahuluan

- Binary Cross-Entropy

- Weighted BCE

- Focal Loss

- Asymmetric Loss

- PolyLoss

### 3.7 Bilateral Evidence Routing dan Explainable AI

- Konsep expert mata kiri, expert mata kanan, dan expert interaksi bilateral

- Global gate, label-wise router, exchange equivariance, dan prediction invariance

- Layer-CAM: konsep, mekanisme, dan keterbatasan

- Layer-CAM digunakan untuk meninjau area perhatian setiap cabang. Peta merupakan interpretasi kualitatif karena ODIR-5K tidak menyediakan anotasi lokasi lesi untuk validasi klinis.

### 3.8 Dataset ODIR-5K

- Karakteristik dataset

- Label penyakit

- Distribusi label

- Potensi isu pembagian data

### 3.9 Penelitian Terdahulu

- Pemetaan 15-20 paper relevan

- Perbandingan dataset, metode, loss, imbalance handling, XAI, metrik, hasil, keterbatasan

### 3.10 Research Gap

- Sintesis gap dari literature matrix

- Gap utama dan gap pendukung

### 3.11 Kerangka Konseptual

- Pasangan fundus -> shared ResNet50 -> expert kiri, kanan, dan interaksi -> router per label -> diagnosis pasien -> evaluasi swap -> Layer-CAM

## 4. BAB III - METODOLOGI PENELITIAN

### 4.1 Jenis Penelitian

- Penelitian eksperimental berbasis deep learning

### 4.2 Tahapan Penelitian

- Literature review -> audit prior art -> studi fungsi loss -> desain LEBER -> implementasi -> ablation study -> multi-seed -> test -> Layer-CAM -> analisis

### 4.3 Dataset

- ODIR-5K: data latih berlabel terdiri dari 3.500 pasien, citra fundus mata kiri dan kanan, serta delapan label penyakit/normal

### 4.4 Preprocessing

- Quality check

- Resize

- Normalization

- Augmentation

- Pembentukan input model

### 4.5 Pembagian Data

- Train/validation/test 70/15/15 dengan patient-level split dan iterative multilabel stratification

### 4.6 Arsitektur Model

- Citra mata kiri dan kanan -> shared ResNet50 -> fitur kiri dan kanan -> tiga expert -> label-wise exchange-equivariant router -> delapan probabilitas pasien

### 4.7 Skenario Eksperimen

Konfigurasi Eksperimen yang Ditetapkan

| Komponen | Konfigurasi yang ditetapkan |
|---|---|
| Unit data | Pasien ODIR-5K, menggunakan pasangan citra mata kiri dan kanan. |
| Split data | 70% train, 15% validation, 15% test pada level pasien dengan iterative multilabel stratification. |
| Input | Citra fundus di-resize 512 x 512 lalu dinormalisasi dengan statistik ImageNet. Crop fundus belum menjadi bagian protokol berjalan. |
| Augmentasi train | Horizontal flip, rotasi ringan hingga 15 derajat, dan color jitter ringan. Validation dan test tanpa augmentasi acak. |
| Backbone | ResNet50 pretrained ImageNet sebagai backbone tunggal bersama untuk mata kiri dan kanan. |
| Model | Dua fitur 2.048 dimensi dari backbone digabungkan (concatenate), dropout 0,30, lalu linear head delapan label dan sigmoid. |
| Optimizer | AdamW, learning rate 0,0001, weight decay 0,0001. |
| Pelatihan | Maksimum 30 epoch, batch size 16, early stopping patience 7, scheduler ReduceLROnPlateau berdasarkan validation Macro-F1. |
| Loss | BCE; Weighted BCE dengan pos_weight dari data latih; Focal Loss alpha 0,25 dan gamma 2; ASL gamma positif 1, gamma negatif 4, clipping 0,05; PolyLoss epsilon 1. |
| Replikasi dan threshold | Studi lima loss 224 menggunakan seed 42, 52, dan 62. Kandidat loss dikonfirmasi ulang pada 512. Threshold dipilih pada validation lalu dikunci untuk test. |
| Evaluasi | Macro-F1 sebagai metrik utama; Micro-F1, AUROC per kelas dan macro, precision, recall, F1 per kelas, Hamming Loss, serta ringkasan mayoritas-minoritas. |

Studi loss memakai arsitektur dan split yang sama. Eksperimen utama mengubah komponen fusion secara bertahap dari A0 sampai A6 agar kontribusi setiap modifikasi dapat diuji.

Pipeline Eksperimen BCE

| Tahap | Kegiatan | Keluaran atau pemeriksaan |
|---|---|---|
| 1. Manifest pasien | Membaca data.xlsx, membentuk satu baris per pasien, memasangkan citra kiri-kanan, dan membuat vektor delapan label. | Setiap pasien memiliki pasangan citra valid dan label N, D, G, C, A, H, M, O. |
| 2. Pemeriksaan data | Memastikan file citra tersedia, patient_id unik, dan tidak ada label di luar delapan kelas. | Laporan data hilang, duplikasi, serta distribusi label. |
| 3. Patient-level split | Membagi pasien 70% train, 15% validation, 15% test dengan iterative multilabel stratification. | Tidak ada pasien yang muncul pada lebih dari satu subset. |
| 4. Preprocessing | Resize 512 x 512, normalisasi ImageNet, dan color jitter ringan pada train. | Tensor citra siap dipakai ResNet50. |
| 5. Model baseline | Membangun shared ResNet50 pretrained ImageNet, menggabungkan fitur kiri-kanan, dropout 0,30, head delapan sigmoid. | Model baseline menghasilkan delapan probabilitas per pasien. |
| 6. Pelatihan BCE | Melatih dengan BCE, AdamW, batch 16, maksimum 30 epoch, dan early stopping. | Checkpoint terbaik berdasarkan validation Macro-F1. |
| 7. Validasi | Memantau loss dan Macro-F1; memilih threshold per label hanya dari validation set. | Konfigurasi dan threshold dikunci sebelum test. |
| 8. Evaluasi test | Menghitung Macro-F1, Micro-F1, AUROC, precision, recall, F1 per kelas, dan Hamming Loss. | Hasil baseline BCE bagi empat loss lain. |
| 9. Layer-CAM | Membuat peta Layer-CAM pada contoh prediksi benar dan salah yang representatif. | Interpretasi visual kualitatif, bukan validasi klinis. |

BCE dijalankan terlebih dahulu sebagai baseline. Pipeline baru siap ketika seluruh tahap selesai tanpa kebocoran pasien dan hasil test tersimpan bersama konfigurasi, seed, threshold, serta checkpoint.

- BCE sebagai baseline standar

- Weighted BCE sebagai baseline pembobotan kelas

- Focal Loss sebagai pembanding yang menekankan contoh sulit

- Asymmetric Loss sebagai pembanding untuk positive-negative imbalance

- PolyLoss sebagai pembanding loss fleksibel berbasis ekspansi polinomial

Tabel Rancangan Pengujian Fungsi Loss

| No. | Fungsi loss | Konfigurasi khusus | Tujuan pengujian |
|---|---|---|---|
| 1 | BCE | Baseline standar tanpa pembobotan kelas. | Menjadi acuan minimum kinerja. |
| 2 | Weighted BCE | Bobot positif dihitung dari frekuensi label pada data latih. | Menguji pembobotan kelas minoritas. |
| 3 | Focal Loss | Alpha 0,25 dan gamma 2. | Menguji penekanan pada contoh yang sulit. |
| 4 | ASL | Gamma positif 1, gamma negatif 4, dan clipping 0,05. | Menguji positive-negative imbalance. |
| 5 | PolyLoss | Epsilon 1. | Menguji loss fleksibel berbasis ekspansi polinomial. |

Kontrol keadilan: patient-level split, preprocessing, optimizer, scheduler, threshold, dan evaluasi dipertahankan. A0-A6 dibandingkan melalui ablation study; baseline utama dan metode lengkap diulang minimal dengan seed 42, 52, dan 62.

- Eksperimen lima loss 224 dengan tiga seed telah selesai. BCE, ASL, dan PolyLoss dikonfirmasi pada baseline bilateral 512 sebelum loss utama dikunci.

### 4.8 Evaluasi

- Macro-F1

- Micro-F1

- AUROC

- Precision

- Recall

- F1 per kelas

- Hamming Loss

- Perbandingan majority vs minority class

### 4.9 Explainable AI

- Prediksi per label → Layer-CAM per mata → analisis area perhatian model pada kasus representatif

### 4.10 Analisis Hasil

- Apakah LEBER meningkatkan Macro-F1 dibandingkan baseline concatenation?

- Komponen mana yang memberikan peningkatan berdasarkan ablation study?

- Apakah prediksi dan bobot router konsisten setelah input mata ditukar?

- Bagaimana kontribusi expert dan peta Layer-CAM berbeda antarlabel?

### 4.11 Posisi dalam Sistem Informasi Cerdas

- Model diposisikan sebagai intelligent information processing / decision-support mechanism, bukan pengganti diagnosis dokter

## 5. BAB IV - HASIL DAN PEMBAHASAN

- Karakteristik dan distribusi dataset

- Hasil preprocessing

- Hasil baseline

- Perbandingan loss function

- Performa per kelas

- Analisis kelas minoritas

- Hasil Layer-CAM

- Analisis visual Layer-CAM pada fungsi loss terpilih

- Pembahasan terhadap penelitian terdahulu

- Implikasi terhadap Sistem Informasi Cerdas

## 6. BAB V - KESIMPULAN DAN SARAN

- Kesimpulan berdasarkan rumusan masalah

- Keterbatasan penelitian

- Saran pengembangan dan penelitian lanjutan

## 7. RANCANGAN ALUR PENELITIAN

Literature Review -> Audit Prior Art -> Studi Fungsi Loss -> Desain LEBER -> Implementasi A0-A6 -> Ablation Study -> Multi-Seed -> Evaluasi Test -> Layer-CAM -> Kesimpulan

## 8. BAGIAN YANG HARUS DIKUNCI SETELAH LITERATURE REVIEW

- Research gap utama telah dikunci secara kondisional berdasarkan literatur yang ditinjau.

- Novelty utama: label-wise exchange-equivariant bilateral evidence routing.

- Backbone final: shared ResNet50; head dan fusion dikembangkan melalui konfigurasi A0-A6.

- Loss kandidat utama: ASL, dengan validasi beberapa seed dan tanpa menutup kemungkinan hasil berbeda.

- Metode XAI final: Layer-CAM dan analisis bobot router.

- Strategi evaluasi: ablation study, multi-seed, metrik per label, dan pengujian swap.

- Apakah perlu external validation menggunakan dataset lain

## 9. CATATAN AKADEMIK

- Judul saat ini adalah judul kerja, bukan judul final.

- Research gap tidak boleh ditetapkan hanya dari asumsi; harus diturunkan dari literature matrix dan dibuktikan dengan penelitian terdahulu.

- Perbandingan fungsi loss merupakan studi pendahuluan. Kontribusi utama penelitian adalah LEBER; keunggulannya hanya dapat dinyatakan setelah ablation study dan pengujian beberapa seed.

- Penggunaan domain kesehatan tidak mengubah positioning utama sebagai penelitian Sistem Informasi Cerdas; fokusnya adalah intelligent information processing dan interpretabilitas keluaran sistem.

## 10. ROADMAP KERJA PENELITIAN

| Tahap | Output | Status | Catatan |
|---|---|---|---|
| 1. Literature review | Daftar 15-20 paper + literature matrix | Berjalan | Cari penelitian 2022-2026 yang paling dekat |
| 2. Research gap | 1 gap utama + gap pendukung | Belum dikunci | Harus berbasis evidence |
| 3. Novelty | Kontribusi yang dapat diuji | Belum dikunci | Jangan dipaksakan sebelum gap jelas |
| 4. Metodologi | Pipeline + eksperimen | Kerangka awal | Disesuaikan dengan gap |
| 5. Implementasi | Model dan hasil eksperimen | Sebagian selesai | Training, validation, dan testing lima loss selesai; Layer-CAM belum dijalankan. |
| 6. XAI | Explanation map + analisis | Belum | Pilih metode sesuai arsitektur |
| 7. Penulisan | Proposal/skripsi/artikel | Belum | Dilakukan setelah hasil cukup kuat |

Status Eksperimen Aktual

Kelima fungsi loss telah menjalani training, validation, dan testing menggunakan patient-level split yang sama pada seed 42, 52, dan 62 dengan resolusi 224. Hasil menjadi studi pendahuluan untuk menyaring kandidat loss.

| Fungsi loss | Validation Macro-F1 | Test Macro-F1 delapan label | Test Macro-F1 enam penyakit |
|---|---|---|---|
| BCE (run 224 seed 42) | 0,5943 | 0,5955 | 0,6066 |
| Weighted BCE | 0,6082 | 0,5802 | 0,6033 |
| Focal Loss | 0,5958 | 0,6012 | 0,6149 |
| ASL (run 224 seed 42) | 0,6156 | 0,6034 | 0,6121 |
| PolyLoss | 0,5796 | 0,5788 | 0,5854 |

ASL menghasilkan Test Macro-F1 tertinggi pada evaluasi utama delapan label. Focal Loss menghasilkan Macro-F1 tertinggi pada analisis sekunder enam penyakit spesifik D, G, C, A, H, dan M. Analisis sekunder tidak mengubah output model dan tidak memerlukan training ulang.

Tahap aktif adalah konfirmasi loss pada baseline bilateral 512. Setelah loss dikunci, pekerjaan dilanjutkan dengan implementasi A0-A6, pengulangan seed, pengujian swap, dan Layer-CAM.
