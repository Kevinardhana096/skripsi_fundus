# Intelligent Fundus Screening

# Klasifikasi Multi-Label Penyakit Mata dengan Routing Bukti Bilateral Ekuivarian pada ODIR-5K

| STATUS / Draft penelitian |  | OWNER / Peneliti |  | LAST UPDATED / September 1, 2026 |
|---|---|---|---|---|

| Authors | Peneliti |
|---|---|
| Reviewers | Pembimbing |
| Related docs | Outline + Literature Matrix |
| Scope | Desain metode LEBER untuk klasifikasi multi-label tingkat pasien, didukung studi pendahuluan lima loss dan analisis Layer-CAM. |

## 1. Abstract

Desain ini menetapkan LEBER sebagai metode utama klasifikasi multi-label tingkat pasien pada ODIR-5K. Sistem memisahkan bukti mata kiri, mata kanan, dan interaksi bilateral, kemudian mengatur kontribusinya untuk setiap label melalui router yang mengikuti pertukaran input. Perbandingan lima fungsi loss tetap menjadi studi pendahuluan. Layer-CAM dan bobot router digunakan untuk interpretasi.

Desain mendukung pelatihan dan evaluasi eksperimen offline pada citra fundus berpasangan. Sistem tidak dimaksudkan untuk menggantikan diagnosis dokter, memberikan keputusan klinis otomatis, atau membuktikan validitas klinis melalui dataset retrospektif saja. Hasil eksperimen bergantung pada kualitas label ODIR-5K, patient-level split, sumber daya komputasi, dan pemilihan threshold yang didokumentasikan.

## 2. Goals and Non-Goals

| Goals | Non-goals |
|---|---|
| Mengembangkan dan menguji LEBER melalui ablation study yang dapat direproduksi. | Bukan sistem diagnosis klinis otonom. |
| Mengukur performa per label dan konsistensi pertukaran input. | Tidak membangun arsitektur multi-task segmentasi pembuluh. |
| Mencegah leakage melalui patient-level split. | Tidak mencakup deployment rumah sakit atau aplikasi pasien. |
| Menyediakan log, versi model, dan hasil yang dapat diaudit. | Tidak menyatakan satu fungsi loss sebagai yang terbaik sebelum eksperimen. |

## 3. Background and Problem Statement

ODIR-5K memberikan satu vektor label pasien untuk sepasang citra mata. Informasi bilateral tidak sama pentingnya untuk semua penyakit, dan CNN dapat mempelajari ciri laterality kiri-kanan. Penggabungan global atau concatenation berurutan tidak menjelaskan sumber bukti setiap label dan tidak menjamin hasil diagnosis tetap sama ketika posisi input ditukar.

Batas sistem dimulai dari manifest pasien dan pasangan citra fundus, lalu mencakup preprocessing, shared ResNet50, tiga expert, label-wise router, ablation study, evaluasi swap, dan Layer-CAM. Keluaran berada pada tingkat pasien. Sistem tidak menentukan mata mana yang mengalami penyakit dan tidak digunakan sebagai diagnosis klinis otonom.

### Rancangan Pengujian Fungsi Loss

| Loss | Posisi | Parameter yang dikunci | Pertanyaan yang diuji |
|---|---|---|---|
| BCE | Baseline | Tidak ada parameter khusus | Acuan kinerja standar |
| Weighted BCE | Pembobotan kelas | Bobot dari frekuensi label data latih | Meningkatkan perhatian pada label jarang |
| Focal Loss | Contoh sulit | Alpha 0,25 dan gamma 2 | Mengurangi dominasi contoh mudah |
| ASL | Positive-negative imbalance | Gamma positif 1, gamma negatif 4, dan clipping 0,05 | Mengurangi pengaruh easy negatives |
| PolyLoss | Loss fleksibel | Epsilon 1 | Menguji modifikasi polinomial pada loss |

Studi pendahuluan mempertahankan seluruh konfigurasi kecuali loss. Eksperimen utama mempertahankan data dan protokol evaluasi, tetapi mengubah fusion secara bertahap dari A0 sampai A6 agar kontribusi arsitektur dapat diisolasi.

### Konfigurasi Model dan Pelatihan yang Ditetapkan

| Komponen | Konfigurasi |
|---|---|
| Unit data | Pasien ODIR-5K, menggunakan pasangan citra mata kiri dan kanan. |
| Split data | 70% train, 15% validation, 15% test pada level pasien dengan iterative multilabel stratification. |
| Input | Citra fundus di-resize 512 x 512 lalu dinormalisasi dengan statistik ImageNet. Crop fundus belum diterapkan pada protokol berjalan. |
| Augmentasi train | Horizontal flip, rotasi ringan hingga 15 derajat, dan color jitter ringan. Validation dan test tanpa augmentasi acak. |
| Backbone | ResNet50 pretrained ImageNet sebagai backbone tunggal bersama untuk mata kiri dan kanan. |
| Model | Dua fitur 2.048 dimensi dari backbone digabungkan (concatenate), dropout 0,30, lalu linear head delapan label dan sigmoid. |
| Optimizer | AdamW, learning rate 0,0001, weight decay 0,0001. |
| Pelatihan | Maksimum 30 epoch, batch size 16, early stopping patience 7, scheduler ReduceLROnPlateau berdasarkan validation Macro-F1. |
| Loss | BCE; Weighted BCE dengan pos_weight dari data latih; Focal Loss alpha 0,25 dan gamma 2; ASL gamma positif 1, gamma negatif 4, clipping 0,05; PolyLoss epsilon 1. |
| Replikasi dan threshold | Studi lima loss 224 telah memakai seed 42, 52, dan 62. BCE, ASL, dan PolyLoss dikonfirmasi ulang pada 512. Threshold dipilih pada validation lalu dikunci untuk test. |
| Evaluasi | Macro-F1 sebagai metrik utama; Micro-F1, AUROC per kelas dan macro, precision, recall, F1 per kelas, Hamming Loss, serta ringkasan mayoritas-minoritas. |

Lima loss telah dijalankan satu kali dengan seed 42. Baseline utama dan metode lengkap akan diulang minimal dengan seed 42, 52, dan 62. Test set tidak digunakan untuk memilih arsitektur, threshold, atau hyperparameter.

### BCE Baseline Experiment Pipeline

| Stage | Activity | Output or gate |
|---|---|---|
| 1. Manifest pasien | Membaca data.xlsx, membentuk satu baris per pasien, memasangkan citra kiri-kanan, dan membuat vektor delapan label. | Setiap pasien memiliki pasangan citra valid dan label N, D, G, C, A, H, M, O. |
| 2. Pemeriksaan data | Memastikan file citra tersedia, patient_id unik, dan tidak ada label di luar delapan kelas. | Laporan data hilang, duplikasi, serta distribusi label. |
| 3. Patient-level split | Membagi pasien 70% train, 15% validation, 15% test dengan iterative multilabel stratification. | Tidak ada pasien yang muncul pada lebih dari satu subset. |
| 4. Preprocessing | Resize 512 x 512, normalisasi ImageNet, dan color jitter ringan hanya pada train. Augmentasi geometris independen tidak dipakai. | Tensor citra siap dipakai ResNet50. |
| 5. Model baseline | Membangun shared ResNet50 pretrained ImageNet, menggabungkan fitur kiri-kanan, dropout 0,30, head delapan sigmoid. | Model baseline menghasilkan delapan probabilitas per pasien. |
| 6. Pelatihan BCE | Melatih dengan BCE, AdamW, batch 16, maksimum 30 epoch, dan early stopping. | Checkpoint terbaik berdasarkan validation Macro-F1. |
| 7. Validasi | Memantau loss dan Macro-F1; memilih threshold per label hanya dari validation set. | Konfigurasi dan threshold dikunci sebelum test. |
| 8. Evaluasi test | Menghitung Macro-F1, Micro-F1, AUROC, precision, recall, F1 per kelas, dan Hamming Loss. | Hasil baseline BCE bagi empat loss lain. |
| 9. Layer-CAM | Membuat peta Layer-CAM pada contoh prediksi benar dan salah yang representatif. | Interpretasi visual kualitatif, bukan validasi klinis. |

Baseline A0 menggunakan shared ResNet50, concatenation, dan kandidat loss terpilih. Baseline menjadi acuan bagi symmetric fusion, tiga expert, global gate, label-wise router, supervisi kualitas, dan exchange-equivariant construction.

## 4. Proposed Architecture

Figure 1. ODIR-5K multi-label fundus classification architecture.

#### Core components

| Component | Responsibility | Primary storage | Failure behavior |
|---|---|---|---|
| Data and preprocessing | Memeriksa kualitas citra, resize, normalisasi, augmentasi, serta membentuk label multi-label. | ODIR-5K manifest and image files | Mencatat citra/label bermasalah dan menghentikan proses bila input wajib tidak lengkap. |
| Controlled model trainer | Melatih baseline dan varian A0-A6 dengan protokol data yang sama; perubahan arsitektur dicatat per ablation. | Experiment configuration and seed | Fail-closed: eksperimen tidak dipublikasikan bila konfigurasi atau seed tidak tercatat. |
| Inference and Layer-CAM | Menghasilkan probabilitas delapan label dan peta Layer-CAM untuk label yang dipilih. | Versioned model checkpoint | Jika checkpoint tidak cocok atau inference gagal, hasil ditandai tidak valid dan tidak dipakai dalam agregasi. |
| Evaluation and audit | Menyimpan metrik, threshold, confusion summary, dan hasil per kelas untuk perbandingan lima fungsi loss. | Versioned experiment results | Kegagalan penulisan menghentikan publikasi hasil; eksperimen dapat dijalankan ulang dari checkpoint. |
| Telemetry and reporting | Mencatat seed, versi kode, durasi, loss curve, metrik, dan sampel Layer-CAM. | Experiment log and report files | Eksperimen tanpa log lengkap diberi status tidak lengkap dan memerlukan review manual. |

## 5. Request Lifecycle

Job eksperimen masuk dengan manifest ODIR-5K, folder citra, label, konfigurasi model, seed, dan daftar split pasien.

Validasi memeriksa keberadaan citra, kesesuaian patient ID, rentang label, ukuran input, dan normalisasi yang sama untuk train/validation/test.

Sistem memuat konfigurasi backbone, loss, hyperparameter setiap loss, threshold, seed, versi preprocessing, dan daftar pasien tiap split.

Shared ResNet50 mengekstraksi fitur kedua mata. Expert kiri dan kanan menghasilkan bukti monokular, sedangkan expert bilateral memproses jumlah fitur, selisih absolut, dan perkalian elemen. Router menghasilkan tiga bobot per label dan menggabungkan logit expert menjadi delapan probabilitas pasien.

Sebelum evaluasi, sistem menyimpan checkpoint, konfigurasi, seed, daftar indeks pasien, dan hash manifest.

Evaluasi dan Layer-CAM dijalankan setelah checkpoint valid. Job gagal diulang dengan konfigurasi sama; hasil berhenti jika input atau checkpoint berubah.

Output akhir mencakup metrik agregat dan per label, hasil ablation, rata-rata serta standar deviasi antar-seed, nilai konsistensi swap, bobot router per label, peta Layer-CAM, checkpoint, dan log reproduksibilitas.

## 6. API and Data Contracts

#### Primary data contract

| Field | Type | Required | Description |
|---|---|---|---|
| patient_id | string | Yes | ID pasien untuk memastikan split dilakukan pada level pasien; tidak ditampilkan dalam visual publik. |
| image_id | string | Yes | ID unik citra mata kiri/kanan dari manifest ODIR-5K. |
| image_tensor | string | Yes | Tensor citra setelah resize dan normalisasi; preprocessing version wajib dicatat. |
| label_vector | string | Yes | Vektor delapan label biner yang terkait dengan patient_id dan image_id. |
| split | string | Yes | Nilai train/validation/test; harus konsisten dengan patient-level manifest. |
| model_version | string | Yes | Identitas backbone, loss, seed, dan versi kode yang menghasilkan checkpoint. |
| prediction_and_xai | string | Yes | Probabilitas per label, threshold, dan lokasi file Layer-CAM untuk audit analisis. |

#### Contract guarantees

Evaluasi hanya berjalan setelah manifest, split pasien, konfigurasi, dan checkpoint lolos validasi.

Setiap run memiliki run_id berdasarkan timestamp, seed, hash konfigurasi, dan model version.

Simpan patient split, preprocessing version, loss parameters, threshold, checkpoint hash, dan versi kode.

Hasil adalah bukti evaluasi eksperimental; bukan sumber kebenaran diagnosis klinis.

The versioned schema or interface definition is published at

ODIR-5K manifest and experiment schema and update it with each contract release.

## 7. Consistency, Idempotency, and Replay

Run eksperimen harus dapat diulang dengan seed dan konfigurasi yang sama. Hasil identik diberi run_id berbeda tetapi tetap dapat dibandingkan. Duplikasi job tidak boleh menggabungkan hasil ke laporan utama sebelum validasi konfigurasi.

| Scenario | Expected behavior | Reasoning |
|---|---|---|
| Run dengan hash konfigurasi sama dicatat sebagai pengulangan terpisah. | Menghasilkan checkpoint dan laporan baru tanpa menimpa hasil sebelumnya. | run_id dan checkpoint hash mencegah hasil berbeda tertukar. |
| Jika manifest, checkpoint, atau hasil tidak dapat disimpan, run berstatus gagal. | Kegagalan dapat diulang; tidak ada hasil parsial yang dipromosikan. | Status gagal dan pesan error disimpan dalam log. |
| Job dihentikan atau diulang sesuai tahap kegagalan. | Tidak ada fallback ke model lain; retry menggunakan konfigurasi dan checkpoint yang sama. | Log dan hash artefak memungkinkan penelusuran ulang. |
| Perubahan konfigurasi selama run tidak diizinkan. | Konfigurasi yang disimpan bersama run_id tetap menjadi versi otoritatif. | Konfigurasi dibekukan sebelum training dimulai. |

## 8. Security and Privacy Considerations

Akses ke citra dan manifest dibatasi pada peneliti/pembimbing; ID pasien dipakai untuk split dan tidak ditampilkan dalam laporan publik.

Simpan hanya identifier dan artefak yang diperlukan; jangan menulis informasi identitas langsung ke log atau gambar Layer-CAM.

Dataset dan kredensial penyimpanan tidak dimasukkan ke repository publik; konfigurasi rahasia dipisahkan dari laporan.

Mode default adalah offline dan read-only terhadap dataset; debugging menggunakan salinan terkontrol.

Pertahankan manifest, split, konfigurasi, checkpoint, dan log sesuai kebutuhan audit penelitian; hapus salinan yang tidak diperlukan.

## 9. Operational Readiness

| Signal | SLO or alert | Owner | Launch gate |
|---|---|---|---|
| Run completion | 100% tahap utama selesai tanpa input invalid | Peneliti | Required |
| Training/evaluation duration | Catat durasi per run; alarm bila menyimpang dari baseline | Peneliti | Required |
| Failed run rate | Tidak ada hasil dipromosikan dari run gagal | Peneliti | Required |
| Configuration drift | Hash konfigurasi/checkpoint berbeda dari run yang direferensikan | Peneliti | Required |
| Reproducibility check | Ulangi seluruh loss pada seed 52 dan 62 sebagai analisis penguatan | Peneliti | Recommended |
| Batas penerapan | Tidak ada deployment produksi sebelum validasi split, ablation, multi-seed, metrik, dan review Layer-CAM selesai. | - | Wajib |

## 10. Alternatives Considered

| Alternative | Why it was considered | Why it was not selected |
|---|---|---|
| BCE | Sederhana, stabil, dan menjadi baseline umum. | Menjadi baseline standar, tetapi tidak cukup untuk menentukan loss terbaik tanpa pembanding. |
| Weighted BCE | Mudah diterapkan dengan bobot berdasarkan frekuensi kelas. | Hasil sensitif terhadap cara memilih bobot dan belum memisahkan positive-negative imbalance seperti ASL. |
| Hybrid BCE-Focal | Dapat mengurangi pengaruh contoh mudah dan telah digunakan dalam studi fundus. | Menambah pembanding tetapi dapat memperlebar scope dan membuat kontribusi loss lebih sulit dibaca. |
| Arsitektur Transformer/multi-task | Berpotensi menangkap hubungan global atau informasi pembuluh. | Kompleksitas dan banyak komponen mengurangi kemampuan mengisolasi pengaruh fungsi loss. |
| PolyLoss | Memberi modifikasi fleksibel pada loss klasifikasi dan telah kompetitif pada studi retinal multi-label. | Eksperimen aktual menggunakan epsilon 1; pengaruh nilai epsilon lain belum diuji. |

## 11. Open Questions

Backbone tetap menggunakan shared ResNet50 pretrained ImageNet. Komponen fusion dan routing dikembangkan melalui A0-A6.

Apakah ASL tetap menjadi loss terbaik ketika baseline utama dan LEBER diuji pada beberapa seed?

Berapa nilai supervisi kualitas expert yang memberi kestabilan router tanpa mendominasi objective utama?

Bagaimana sampel Layer-CAM dan ringkasan bobot router dipilih secara konsisten untuk setiap label?

## 12. Decision and Next Steps

Keputusan terkini adalah mempertahankan studi lima loss 224 sebagai tahap pendahuluan dan menggunakan protokol 512 untuk eksperimen utama. Sebelum A0-A6, BCE, ASL, dan PolyLoss dikonfirmasi pada baseline bilateral 512. BCE seed 42 telah selesai, ASL seed 42 sedang berjalan, dan PolyLoss menunggu.

| Milestone | Deliverable | Exit criteria |
|---|---|---|
| M1 | Pipeline ODIR-5K + baseline BCE | Split pasien tervalidasi; training, evaluasi, dan log selesai tanpa error. |
| M2 | Eksperimen lima fungsi loss dan laporan per kelas | Training, validation, testing, threshold, checkpoint, dan hasil per kelas telah tersimpan untuk seluruh loss. |
| M3 | Analisis Layer-CAM pada sampel representatif | Belum selesai; artefak Layer-CAM belum tersedia. |
| M4 | Penyusunan proposal dan pembahasan | Metrik, keterbatasan, dan keputusan pembimbing terdokumentasi. |

### Status Eksperimen Aktual

Kelima fungsi loss telah menjalani training, validation, dan testing menggunakan patient-level split yang sama pada seed 42, 52, dan 62 dengan resolusi 224. Hasil run seed 42 berikut dipertahankan sebagai rincian historis, sedangkan ringkasan tiga seed menjadi dasar yang lebih kuat.

| Fungsi loss | Validation Macro-F1 | Test Macro-F1 delapan label | Test Macro-F1 enam penyakit |
|---|---|---|---|
| BCE (run 224 seed 42) | 0,5943 | 0,5955 | 0,6066 |
| Weighted BCE | 0,6082 | 0,5802 | 0,6033 |
| Focal Loss | 0,5958 | 0,6012 | 0,6149 |
| ASL (run 224 seed 42) | 0,6156 | 0,6034 | 0,6121 |
| PolyLoss | 0,5796 | 0,5788 | 0,5854 |

ASL menghasilkan Test Macro-F1 tertinggi pada evaluasi utama delapan label. Focal Loss menghasilkan Macro-F1 tertinggi pada analisis sekunder enam penyakit spesifik D, G, C, A, H, dan M. Analisis sekunder tidak mengubah output model dan tidak memerlukan training ulang.

Setiap loss pendahuluan telah dijalankan tiga kali. Selisih rata-rata ASL, BCE, dan PolyLoss tetap kecil sehingga konfirmasi pada protokol 512 diperlukan. Efektivitas LEBER belum diuji dan tidak boleh dinyatakan lebih baik sebelum ablation study serta pengulangan seed selesai.

Prioritas berikutnya adalah menyelesaikan konfirmasi BCE, ASL, dan PolyLoss pada 512, mengunci loss berdasarkan validation, lalu membangun A0 dan menambahkan symmetric fusion, expert, router, supervisi kualitas, serta aturan exchange-equivariant secara bertahap.

## 13. LEBER Architecture Specification

LEBER menggunakan satu shared ResNet50 untuk kedua mata. Tiga head ringan mewakili bukti mata kiri, mata kanan, dan interaksi bilateral simetris. Router menghasilkan tiga bobot ternormalisasi untuk setiap label. Eye scorer berbagi bobot sehingga pertukaran input menukar bobot mata, sedangkan representasi bilateral dan diagnosis pasien tetap sama.

| ID | Konfigurasi | Tujuan | Status |
|---|---|---|---|
| A0 | Concatenation dan loss 512 terpilih | Baseline | Reproduksi |
| A1 | Symmetric bilateral features | Uji interaksi simetris | Rencana |
| A2 | Tiga expert, bobot tetap | Kontrol kapasitas | Rencana |
| A3 | Tiga expert, global gate | Uji global fusion | Rencana |
| A4 | Label-wise router | Uji routing per label | Rencana |
| A5 | A4 dan supervisi kualitas | Uji supervisi router | Rencana |
| A6 | Konstruksi exchange-equivariant | Metode lengkap | Rencana |

## 14. Validation Rules

- Diagnosis pasien harus tetap sama ketika input kiri dan kanan ditukar.

- Bobot kiri dan kanan harus bertukar setelah input ditukar; bobot bilateral harus tetap sama.

- A0 dan A6 dijalankan minimal dengan seed 42, 52, dan 62 serta dilaporkan sebagai rata-rata dan standar deviasi.

- Pemilihan arsitektur dan threshold hanya menggunakan validation set; test dilakukan setelah konfigurasi dikunci.

- Layer-CAM menjadi interpretasi kualitatif dan bukan validasi klinis lokasi lesi.
