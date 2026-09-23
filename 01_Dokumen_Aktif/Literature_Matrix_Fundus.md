# Literature Matrix: Multi-Label Klasifikasi Penyakit Mata pada Citra Fundus

## Tujuan

Matriks ini mendukung penyusunan proposal penelitian berjudul kerja:

> Klasifikasi Multi-Label Penyakit Mata dengan Routing Bukti Bilateral Ekuivarian pada ODIR-5K.

Fokus utama penelitian adalah pengembangan label-wise exchange-equivariant bilateral evidence routing. Perbandingan BCE, Weighted BCE, Focal Loss, ASL, dan PolyLoss dipertahankan sebagai studi pendahuluan unt uk memilih loss dan membentuk baseline. Layer-CAM digunakan untuk interpretasi kualitatif setiap cabang.

## Status verifikasi

- **Dibaca penuh dari folder lokal**: abstrak, metode/kesimpulan atau halaman penting telah ditinjau dari PDF lokal.
- **Terverifikasi dari laman abstrak/penerbit**: metadata dan abstrak telah dicek di laman primer; teks lengkap perlu ditelaah sebelum dipakai untuk klaim angka atau keterbatasan yang spesifik.
- **Perlu telaah penuh**: kandidat relevan yang tetap harus dibaca penuh sebelum dipakai sebagai bukti utama.

## Matriks penelitian terdahulu (2021-2026)

| No. | Referensi | Dataset / cakupan | Metode utama | Loss / penanganan imbalance | XAI | Temuan relevan | Keterbatasan / catatan untuk gap | Status |
|---:|---|---|---|---|---|---|---|---|
| 1 | Ridnik et al. (2021), [Asymmetric Loss for Multi-Label Classification](https://openaccess.thecvf.com/content/ICCV2021/papers/Ridnik_Asymmetric_Loss_for_Multi-Label_Classification_ICCV_2021_paper.pdf) | Benchmark multi-label umum | Asymmetric Loss (ASL) | Memisahkan perlakuan positif dan negatif; menurunkan bobot easy negatives | Tidak | ASL dirancang khusus untuk positive-negative imbalance pada multi-label classification | Bukan data fundus; perlu pembuktian empiris pada ODIR-5K | Terverifikasi dari paper primer |
| 2 | Gour & Khanna (2021), [Multi-class multi-label ophthalmological disease detection using transfer learning based CNN](https://www.sciencedirect.com/science/article/pii/S1746809420304432) | ODIR; delapan kategori penyakit/normal | Transfer learning CNN, membandingkan beberapa backbone | Tidak berfokus pada loss imbalance | Tidak | VGG16 dengan SGD dilaporkan sebagai konfigurasi terbaik di studi tersebut | Dapat menjadi baseline historis; tidak mengisolasi pengaruh ASL | Terverifikasi dari laman penerbit |
| 3 | He et al. (2021), [Self-speculation of clinical features based on knowledge distillation for accurate ocular disease classification](https://www.sciencedirect.com/science/article/pii/S1746809421000884) | ODIR-5K | Knowledge distillation dan clinical-feature speculation | Bukan fokus utama | Tidak | Memakai data ODIR pada level kasus/pasien | Metodenya lebih kompleks dari rancangan eksperimen inti; berguna sebagai pembanding state-of-the-art | Terverifikasi dari laman penerbit |
| 4 | Li et al. (2022), *Multi-Label Fundus Image Classification Using Attention Mechanisms and Feature Fusion* | ODIR fundus binokular | ResNet50, attention, feature fusion mata kiri-kanan | Menyoroti keterbatasan data | Tidak | BFPC-Net melaporkan peningkatan atas baseline melalui feature fusion dan attention | Berfokus pada arsitektur, bukan studi loss yang terkontrol | Dibaca penuh dari folder lokal |
| 5 | Bhati et al. (2023), *Discriminative Kernel Convolution Network for Multi-Label Ophthalmic Disease Detection on Imbalanced Fundus Image Dataset* | ODIR-5K; juga pengujian pada data lain | DKCNet: attention block + squeeze-and-excitation | Over-sampling dan/atau under-sampling | Tidak | Melaporkan AUC 96,08%, F1 94,28%, dan kappa 0,81 pada konfigurasi terbaik | Menangani imbalance melalui resampling; belum menjawab dampak ASL dengan protokol sama | Dibaca penuh dari folder lokal |
| 6 | Rodriguez et al. (2023), [Multi-Label Retinal Disease Classification Using Transformers](https://pubmed.ncbi.nlm.nih.gov/36223359/) | MuReD, fundus multi-label dari beberapa sumber | Transformer untuk multi-label disease classification | Membandingkan WBCE, Focal Loss, ASL, BCE, dan PolyLoss | Tidak | PolyLoss dan BCE termasuk hasil terbaik secara agregat, sementara ASL juga kompetitif pada metrik tertentu | Bukan ODIR-5K; menjadi dasar bahwa PolyLoss layak diuji, bukan bukti bahwa ia pasti terbaik pada ODIR | Terverifikasi dari artikel dan abstrak PubMed |
| 7 | [A Multi-Label Detection Deep Learning Model with Attention-Guided Image Enhancement for Retinal Images](https://pubmed.ncbi.nlm.nih.gov/36985112/) (2023) | RFMiD | VGG19 + ResNet50 dan attention-guided enhancement | Tidak menjadi fokus utama | Grad-CAM | Grad-CAM dipakai untuk menunjukkan area perhatian dan mendukung proses enhancement | Berbeda dataset dan strategi XAI; relevan sebagai landasan analisis Grad-CAM | Terverifikasi dari abstrak PubMed |
| 8 | [A fundus image classification framework for learning with noisy labels](https://www.sciencedirect.com/science/article/pii/S0895611123000964) (2023) | ODIR dan dataset klinis | Data cleansing, adaptive negative learning, SAM | Negative-learning loss untuk label yang salah/noisy | Tidak | Kualitas label dapat memengaruhi hasil klasifikasi fundus | Noise label adalah faktor pengganggu yang perlu disebut sebagai keterbatasan penelitian | Terverifikasi dari laman penerbit |
| 9 | Sivaz & Aykut (2024), *Combining EfficientNet with ML-Decoder Classification Head for Multi-Label Retinal Disease Classification* | ODIR-5K | EfficientNet-B5 + ML-Decoder, fusion mata kiri-kanan, SAM | Augmentasi; imbalance disebut sebagai isu | Grad-CAM | F1 92,48% dan AUC 94,80% pada skenario three-fold CV terbaik yang dilaporkan | Arsitektur dan optimisasi terdiri dari banyak komponen; sulit mengatribusikan hasil hanya pada satu komponen | Dibaca penuh dari folder lokal |
| 10 | Zhao et al. (2024), [Multi-label Classification of Retinal Diseases Based on Fundus Images Using ResNet and Transformer](https://pubmed.ncbi.nlm.nih.gov/38871856/) | ODIR-5K | ResNet + Transformer + learnable label embedding | Tidak menjadi fokus utama | Tidak | Melaporkan mAP 92,86%, AUC 97,27%, dan recall 90,62% | Menjadi pembanding pendekatan hubungan antar-label, bukan pembanding loss langsung | Terverifikasi dari abstrak PubMed |
| 11 | Wang, Lian & Jiao (2024), [Multi-label Classification of Retinal Disease via a Novel Vision Transformer Model](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2023.1290803/full) | ODIR-2019 | Vision Transformer | Tidak menjadi fokus utama | Tidak | Menggunakan delapan label ODIR dan pembagian train/validation/test | Perlu telaah protokol split secara penuh sebelum membandingkan metrik | Terverifikasi dari laman jurnal |
| 12 | Zhou, Wang & Li (2024), [A Multi-class Fundus Disease Classification System Based on an Adaptive Scale Discriminator and Hybrid Loss](https://www.sciencedirect.com/science/article/pii/S1476927124002299) | ODIR-5K | ResNet50, attention, adaptive scale discriminator | Hybrid BCE + Focal Loss | Tidak | Hybrid loss diusulkan untuk data tidak seimbang; laporan hasil mencantumkan AUC 98,53 dan F1 89,73 | Pembanding penting bila Focal Loss dimasukkan ke eksperimen; arsitektur juga berubah sehingga efek loss tidak terisolasi | Terverifikasi dari laman penerbit |
| 13 | [TL-CCL: Two-level Causal Contrastive Learning for Multi-label Ocular Disease Diagnosis with Fundus Images](https://www.sciencedirect.com/science/article/pii/S1746809424003665) (2024) | OIA-ODIR | Causal contrastive learning | Masked entropy regularization | Tidak | Memodelkan fitur kausal untuk mengurangi spurious correlation | Kompleks; menunjukkan bahwa korelasi label adalah tantangan tambahan di luar imbalance | Terverifikasi dari laman penerbit |
| 14 | Jian et al. (2026), *Long-tailed Multi-label Retinal Disease Classification Using Alternate Group Training and Gradient-based Re-weighting* | ODIR-5K dan dataset fundus publik lain | Alternate group training, teacher-student, knowledge distillation | Relational grouping dan gradient-based re-weighting untuk long-tail | Tidak | Pada ODIR-5K, melaporkan kappa 0,707 ± 0,014 dengan ResNet-50; kombinasi RIDE meningkatkan kappa | Sangat kompleks; menjadi bukti bahwa long-tail penting, sekaligus alasan memilih eksperimen ASL yang lebih terukur | Dibaca penuh dari folder lokal |
| 15 | Li & Tao (2026), *A Vessel-guided Multi-task Deep Learning Framework with Visual Interpretability for Simultaneous Retinal Vessel Segmentation and Multi-disease Classification from Fundus Images* | ODIR-5K, RFMiD, DRIVE, EyePACS-light-v2 | V-MNet: shared encoder, vessel segmentation, disease classification | BCE untuk klasifikasi dan Dice loss untuk segmentasi | Grad-CAM | Menggabungkan klasifikasi dan transparansi visual; rata-rata AUC 0,978 dan F1 0,935 untuk klasifikasi yang dilaporkan | Scope multi-task dan multi-dataset lebih luas dari proposal; dipakai sebagai landasan XAI, bukan baseline langsung | Dibaca penuh dari folder lokal |
| 16 | Chen et al. (2025), [ViResGF-Net](https://pubmed.ncbi.nlm.nih.gov/41284448/) | ODIR | CNN-ViT, feature pyramid, dan gated fusion | Enhanced asymmetric loss + Dice loss | Tidak | Loss asimetris digunakan bersama banyak komponen arsitektur dan loss lain | Tidak mengisolasi ASL standar terhadap BCE standar | Terverifikasi dari abstrak dan naskah penulis |
| 17 | Jiang et al. (2021), [LayerCAM](https://pubmed.ncbi.nlm.nih.gov/34156941/) | Benchmark lokalisasi | Layer-CAM | Peta aktivasi dari beberapa layer CNN | Ya, Layer-CAM | Memberi peta aktivasi lebih rinci secara spasial | Bukan data fundus dan bukan bukti validitas klinis heatmap pada ODIR-5K | Terverifikasi dari paper primer |

| 18 | Kim et al. (2021), [Asymmetry between right and left fundus images identified using CNN](https://www.nature.com/articles/s41598-021-04323-3) | ODIR dan data fundus lain | Klasifikasi laterality kiri-kanan | Bukan fokus | CAM | CNN dapat membedakan mata kiri dan kanan; pada eksperimen ODIR dilaporkan akurasi 91,13% | Menguatkan risiko model mempelajari ciri laterality atau urutan input | Terverifikasi dari artikel penuh |
| 19 | Huo et al. (2025), [DMS-Net](https://arxiv.org/abs/2504.18046) | ODIR-5K bilateral | Shared Siamese ResNet-152, multiscale context, bidirectional attention | Bukan fokus utama | Tidak | Memodelkan interaksi kedua mata | Bilateral Siamese dan interaksi fitur bukan kebaruan; tidak ditemukan dekomposisi tiga sumber per label | Terverifikasi dari naskah primer |
| 20 | [DualCrossAttnNet](https://www.sciencedirect.com/science/article/pii/S0010482526003823) (2026) | ODIR-2019 bilateral | EfficientNet-B2, bilateral cross-attention, gated fusion, GeM | Bukan fokus utama | Grad-CAM | Gated fusion adaptif sudah digunakan untuk menyeimbangkan informasi kedua mata | Gating bilateral secara umum bukan kebaruan | Terverifikasi dari laman artikel primer |
| 21 | Zhang et al. (2026), [Anatomy-Slot](https://arxiv.org/abs/2605.12929) | ODIR-5K dan validasi eksternal | Anatomical factorization dan homologous bilateral reasoning | Bukan fokus utama | Analisis cross-attention | Manfaat bilateral berbeda per label; glaukoma banyak menggunakan asimetri antarmata | Menjadi dasar routing per label; belum ditemukan dekomposisi kiri-kanan-interaksi dengan exchange-equivariant router | Terverifikasi dari naskah primer |
| 22 | [Multimodal Ocular Disease Recognition](https://dspace.cuni.cz/bitstream/handle/20.500.11956/207010/120534995.pdf?sequence=1) (2026) | ODIR-5K | Single-eye, dual-image, metadata, dan fusion | Beberapa konfigurasi | Tidak | Menggunakan left-right swap 50% sebelum concatenation | Swap augmentation sudah ada, tetapi tidak sama dengan jaminan struktural invariance | Terverifikasi dari tesis penuh |
| 23 | Shim et al. (2019), [ARGate](https://arxiv.org/abs/1901.10610) | Multimodal sensor fusion | Auxiliary unimodal branches dan fusion-weight regularization | Auxiliary loss membentuk target bobot fusion | Tidak | Loss cabang dapat mengarahkan bobot gate | Prior art sebelum 2021 tetap wajib dicatat; target berbasis loss bukan kebaruan | Terverifikasi dari paper primer |
| 24 | Wang et al. (2026), [C²Net: A Co-Occurrence and Consistency-Aware Framework for Structured Multi-Label Fundus Diagnosis](https://pubmed.ncbi.nlm.nih.gov/42048017/) | ODIR-5K dan MuReD | Co-occurrence-aware supervised contrastive learning, Auto-MLFocal, dan diagnostic consistency mechanism | Auto-adaptive focal loss untuk long-tail imbalance | Tidak | Melaporkan Macro-F1 72,1% dan mAP 74,4% pada ODIR-5K dengan five-fold cross-validation | Konsistensi yang dimodelkan adalah logika antarl­abel, misalnya konflik Normal dan penyakit, bukan konsistensi pertukaran mata | Terverifikasi dari abstrak PubMed dan DOI primer |
| 25 | Kim, Han & Iqbal (2026), [Bilateral Lesion-Guided Transformers with Patient-Level Graph Reasoning for Multi-Label Retinal Disease Diagnosis](https://www.researchgate.net/publication/408446161_Bilateral_Lesion-Guided_Transformers_with_Patient-Level_Graph_Reasoning_for_Multi-label_Retinal_Disease_Diagnosis) | OIA-ODIR bilateral | High-resolution encoder, lesion-aware gating, Local-Global Transformer, bilateral cross-attention, class-wise query pooling, dan graph-regularized patient head | Focal loss pada output mata dan pasien serta consistency term | Analisis attention | Sudah menghasilkan bukti tingkat mata per label dan memakai interaksi $[p_L,p_R,\lvert p_L-p_R\rvert,p_L\odot p_R]$ untuk prediksi pasien | Pembanding terdekat LEBER; deskripsi yang diakses belum menunjukkan convex routing tiga expert atau jaminan struktural swap equivariance | Metadata konferensi terverifikasi; naskah metode perlu diaudit penuh sebelum klaim final |
| 26 | Nakayama et al. (2024; versi data 2026), [BRSET: A Brazilian Multilabel Ophthalmological Dataset](https://physionet.org/content/brazilian-ophthalmological/1.0.2/) | 16.266 citra dari 8.524 pasien Brasil | Dataset fundus multi-label dengan metadata pasien, kualitas, anatomi, dan sisi mata | Bukan studi loss | Tidak | Menyediakan 13 label patologis tingkat citra serta identitas pasien dan sisi mata | Lebih baru dan besar daripada data kerja ODIR-5K, tetapi unit labelnya tingkat citra sehingga tidak dapat langsung menjadi test set diagnosis bilateral tingkat pasien | Terverifikasi dari dokumentasi PhysioNet dan publikasi PLOS Digital Health |
| 27 | Pachade et al. (2024), [RFMiD: Retinal Image Analysis for Multi-Disease Detection Challenge](https://www.sciencedirect.com/science/article/pii/S1361841524002901) | 3.200 citra fundus | Benchmark screening dan klasifikasi multi-label penyakit fundus | Beragam strategi peserta untuk kelas langka | Tidak menjadi fokus dataset paper | Menyediakan anotasi 45 kelainan dan tugas klasifikasi 28 kelas pada challenge | Kaya penyakit langka, tetapi unit analisisnya citra tunggal dan tidak menyediakan tugas pasangan mata tingkat pasien seperti ODIR-5K | Terverifikasi dari laman artikel primer |

## Pembanding arsitektur yang paling dekat

| Aspek | DualCrossAttnNet (2026) | Bi-LGT (2026) | LEBER yang diusulkan |
|---|---|---|---|
| Backbone | EfficientNet-B2 | Convolutional encoder dan Local-Global Transformer | Shared ResNet50 |
| Interaksi kedua mata | Bilateral cross-attention pada fitur spasial dan kanal | Pertukaran token dengan bilateral cross-attention | Interaksi simetris dari jumlah, selisih mutlak, dan perkalian fitur |
| Bentuk fusion | Gated fusion adaptif | Bukti tingkat mata dan graph-regularized patient head | Tiga expert dengan bobot router per label yang berjumlah satu |
| Informasi per label | Multi-label classifier; gate per label belum dinyatakan pada sumber yang ditelaah | Class-wise query pooling menghasilkan bukti per label | Router secara eksplisit menggabungkan logit kiri, kanan, dan bilateral untuk setiap label |
| Pertukaran kiri-kanan | Jaminan struktural dan metrik swap belum ditemukan pada sumber yang ditelaah | Jaminan struktural belum ditemukan; vektor fusion masih memuat $p_L$ dan $p_R$ secara berurutan | Bobot kiri-kanan dirancang bertukar, bukti bilateral tetap, dan prediksi pasien invariant |
| Fokus | Akurasi melalui cross-attention dan gated fusion | Interaksi bilateral serta hubungan antarl­abel | Keterlacakan sumber bukti dan konsistensi pertukaran mata dengan performa kompetitif |
| Status sebagai pembanding | Pembanding dekat | Pembanding paling dekat | Metode yang masih harus dibuktikan |

## Sintesis research gap

Penelitian ODIR-5K telah menggunakan attention, feature fusion, Siamese backbone, bidirectional attention, cross-attention, gated fusion, class-wise query, bukti tingkat mata, hubungan antarl­abel, resampling, dan berbagai fungsi loss. DualCrossAttnNet dan Bi-LGT mempersempit ruang kebaruan karena keduanya sudah mengolah interaksi bilateral secara adaptif. Bi-LGT bahkan sudah menghasilkan bukti per label dari setiap mata. Oleh karena itu, kebaruan tidak dapat diletakkan pada penggunaan dua mata, gating, attention, bukti per mata, class query, tiga cabang, atau target router berbasis loss secara terpisah.

Gap kerja berasal dari tiga temuan. Pertama, label ODIR-5K berada pada tingkat pasien dan ditentukan berdasarkan kedua mata. Kedua, manfaat informasi bilateral dapat berbeda antarpenyakit. Ketiga, CNN dapat mengenali ciri laterality kiri-kanan sehingga fusion berurutan dapat mempelajari posisi input. Berdasarkan sumber yang ditelaah sampai 9 September 2026, belum ditemukan metode ODIR-5K yang secara bersamaan menggunakan tiga logit expert kiri, kanan, dan bilateral dengan convex routing per label, menerapkan aturan exchange equivariance pada bobot internal, serta menguji invariance prediksi pasien dengan metrik swap.

Gap tersebut bersifat sempit dan sementara. Naskah lengkap DualCrossAttnNet dan Bi-LGT harus diperiksa sampai persamaan, objective function, dan ablation study sebelum klaim kebaruan dikunci. Jika salah satu paper telah menerapkan kombinasi yang sama, rancangan LEBER harus diubah.

## Gap kerja dan kebaruan sementara

### Gap kerja

> Model bilateral pada ODIR-5K telah memakai feature fusion, cross-attention, gating adaptif, dan bukti per label. Berdasarkan sumber yang ditelaah, belum ditemukan formulasi yang menggabungkan tiga expert kiri, kanan, dan bilateral melalui convex routing per label sekaligus menjamin dan mengukur konsistensi diagnosis pasien terhadap pertukaran urutan mata.

### Kontribusi metode yang diusulkan

1. Tiga sumber bukti berupa expert mata kiri, expert mata kanan, dan expert interaksi bilateral.
2. Label-wise router yang memberikan bobot berbeda untuk setiap label penyakit.
3. Exchange-equivariant construction: bobot kiri dan kanan bertukar mengikuti input, sedangkan prediksi pasien tetap invariant.
4. Ablation study yang memisahkan manfaat symmetric fusion, expert, global gate, label-wise routing, supervisi kualitas, dan aturan pertukaran.
5. Layer-CAM pada setiap cabang sebagai interpretasi kualitatif.

### Batas klaim

Klaim yang digunakan adalah “berdasarkan literatur yang ditinjau sampai 9 September 2026, belum ditemukan”, bukan “pertama di dunia”. Bilateral fusion, Siamese backbone, attention, gated fusion, class-wise query, bukti per mata, mixture-of-experts, target gate berbasis loss, dan swap augmentation telah memiliki prior art. Bobot router hanya boleh disebut sebagai kontribusi terhadap keputusan model, bukan penyebab klinis penyakit.

## Rujukan dan kesesuaian dataset

| Dataset | Struktur | Kesesuaian dengan penelitian |
|---|---|---|
| [ODIR-2019 / ODIR-5K](https://odir2019.grand-challenge.org/dataset/) | 5.000 pasien, pasangan citra kiri-kanan, delapan label yang ditetapkan berdasarkan kedua mata dan usia | Dataset utama karena sesuai dengan diagnosis multi-label tingkat pasien dan pengujian pertukaran mata |
| [RFMiD](https://www.sciencedirect.com/science/article/pii/S1361841524002901) | 3.200 citra, 45 kelainan, tugas challenge 28 kelas | Berguna untuk penyakit langka, tetapi bukan benchmark pasangan mata tingkat pasien |
| [MuReD](https://pubmed.ncbi.nlm.nih.gov/36223359/) | 2.208 citra hasil penggabungan beberapa sumber dengan label multi-penyakit | Relevan untuk studi loss dan transformer, tetapi unitnya citra tunggal |
| [BRSET v1.0.2](https://physionet.org/content/brazilian-ophthalmological/1.0.2/) | 16.266 citra dari 8.524 pasien dengan 13 label patologis tingkat citra | Kandidat validasi eksternal terbatas setelah pemetaan label dan pembentukan pasangan yang valid; tidak dapat dipakai langsung sebagai test delapan label ODIR-5K |

Usia dataset bukan satu-satunya dasar pemilihan. ODIR-5K dipilih karena struktur bilateral dan unit label tingkat pasien sesuai dengan pertanyaan penelitian. Kesimpulan tetap dibatasi pada populasi dan protokol ODIR-5K.

## Rancangan penelitian terkini

Penelitian dibagi menjadi tiga tahap. Tahap pertama adalah studi lima fungsi loss pada shared ResNet50 resolusi 224 dengan seed 42, 52, dan 62. Tahap kedua mengonfirmasi BCE, ASL, dan PolyLoss pada baseline bilateral 512. Tahap ketiga mengembangkan dan mengevaluasi LEBER sebagai kontribusi utama setelah loss dikunci.

| Komponen | Rancangan terkini |
|---|---|
| Dataset | ODIR-5K, 3.500 pasien berlabel, citra mata kiri dan kanan, delapan label |
| Unit analisis | Pasien; split 70/15/15 dengan iterative multilabel stratification |
| Backbone | Shared ResNet50 pretrained ImageNet |
| Studi pendahuluan | Lima fungsi loss pada baseline concatenation |
| Metode utama | Expert kiri, expert kanan, expert interaksi bilateral, dan label-wise exchange-equivariant router |
| Kandidat loss | ASL, dikonfirmasi melalui validation dan pengulangan seed |
| Ablation | Concatenation, symmetric fusion, tiga expert berbobot tetap, global gate, label-wise router, supervisi kualitas, metode lengkap |
| Metrik utama | Macro-F1 delapan label |
| Uji konsistensi | Selisih probabilitas dan bobot router sebelum serta sesudah pertukaran input |
| Interpretabilitas | Bobot router per label dan Layer-CAM per cabang |
| Replikasi | Minimal seed 42, 52, dan 62 untuk baseline utama dan metode lengkap |

## Konfigurasi eksperimen pendahuluan yang dikunci

Penelitian menggunakan **shared ResNet50 pretrained ImageNet** sebagai satu-satunya backbone. Satu citra mata kiri dan satu citra mata kanan dari pasien yang sama diproses oleh backbone dengan bobot yang sama. Kedua vektor fitur kemudian digabungkan, diberi dropout 0,30, dan diteruskan ke linear classification head dengan delapan keluaran sigmoid.

Data dibagi pada level pasien dengan rasio 70% train, 15% validation, dan 15% test menggunakan iterative multilabel stratification. Studi pendahuluan memakai 224 x 224. Protokol utama terbaru memakai resize 512 x 512, normalisasi ImageNet, dan color jitter ringan pada train; crop fundus dan augmentasi geometris independen tidak diterapkan. Optimizer adalah AdamW dengan learning rate 0,0001 dan weight decay 0,0001; pelatihan maksimum 30 epoch dengan batch size 16, early stopping patience 7, serta scheduler ReduceLROnPlateau berdasarkan validation Macro-F1.

Setiap loss pada studi 224 telah dijalankan menggunakan seed 42, 52, dan 62. Rata-rata Test Macro-F1 adalah ASL 0,5909, BCE 0,5877, PolyLoss 0,5868, Focal Loss 0,5802, dan Weighted BCE 0,5791. Selisih tiga teratas kecil dan signifikansi statistik belum diuji. BCE, ASL, dan PolyLoss dikonfirmasi ulang pada 512 sebelum loss LEBER dikunci.

## Pipeline eksperimen BCE

Pipeline BCE adalah jalur eksperimen pertama untuk memastikan sistem dasar benar sebelum empat loss lain diuji. Tahapnya: (1) membaca data.xlsx dan membentuk manifest satu baris per pasien dengan citra kiri dan kanan serta delapan label; (2) memeriksa keberadaan citra, duplikasi pasien, dan distribusi label; (3) membuat patient-level split 70/15/15 menggunakan iterative multilabel stratification; (4) melakukan preprocessing dan augmentasi train; (5) membangun shared ResNet50 pretrained ImageNet dengan feature fusion, dropout 0,30, dan delapan output sigmoid; (6) melatih model memakai BCE dan AdamW; (7) memilih threshold tiap label dari validation set; (8) mengevaluasi test set satu kali; dan (9) membuat Layer-CAM untuk kasus representatif.

Pipeline dinyatakan valid jika tidak ada patient leakage, konfigurasi dan seed tersimpan, checkpoint terbaik tersedia, serta Macro-F1, Micro-F1, AUROC, metrik per kelas, dan Hamming Loss tercatat. Hasil BCE menjadi baseline bagi Weighted BCE, Focal Loss, ASL, dan PolyLoss.

## Tabel rancangan pengujian fungsi loss

| No. | Fungsi loss | Konfigurasi khusus | Tujuan pengujian |
|---:|---|---|---|
| 1 | BCE | Tanpa pembobotan kelas | Menjadi baseline standar. |
| 2 | Weighted BCE | Bobot positif dihitung dari frekuensi label data latih | Mengukur manfaat pembobotan kelas minoritas. |
| 3 | Focal Loss | Alpha 0,25 dan gamma 2 | Mengukur manfaat penekanan pada contoh sulit. |
| 4 | ASL | Gamma positif 1, gamma negatif 4, dan clipping 0,05 | Mengukur penanganan positive-negative imbalance. |
| 5 | PolyLoss | Epsilon 1 | Mengukur manfaat modifikasi polinomial yang fleksibel pada loss. |

Kontrol keadilan eksperimen: semua loss memakai patient-level split, backbone, preprocessing, augmentasi, optimizer, scheduler, maksimum epoch, seed 42, dan prosedur threshold yang sama. Data test dipakai hanya untuk evaluasi akhir.

## Status eksperimen aktual

Training, validation, dan testing telah selesai untuk lima fungsi loss. Seluruh hasil berasal dari checkpoint terbaik dan threshold per label yang ditentukan melalui validation set.

| Fungsi loss | Validation Macro-F1 | Test Macro-F1 delapan label | Test Macro-F1 enam penyakit |
|---|---:|---:|---:|
| BCE (run 224 seed 42) | 0,5943 | 0,5955 | 0,6066 |
| Weighted BCE | 0,6082 | 0,5802 | 0,6033 |
| Focal Loss | 0,5958 | 0,6012 | **0,6149** |
| ASL (run 224 seed 42) | **0,6156** | **0,6034** | 0,6121 |
| PolyLoss | 0,5796 | 0,5788 | 0,5854 |

ASL memperoleh Test Macro-F1 tertinggi pada evaluasi utama delapan label ODIR-5K. Focal Loss memperoleh Macro-F1 tertinggi pada analisis sekunder enam penyakit spesifik D, G, C, A, H, dan M. Analisis sekunder tidak mengubah output model dan tidak memerlukan training ulang. Layer-CAM masih menjadi tahap berikutnya karena belum ditemukan artefak hasilnya.
## Arah penelitian setelah studi fungsi loss

Perbandingan loss tetap dilaporkan sebagai hasil pendahuluan. ASL memperoleh rata-rata Test Macro-F1 tiga seed tertinggi pada resolusi 224 sebesar 0,5909, tetapi selisihnya terhadap BCE dan PolyLoss kurang dari 0,005. Protokol 512 kini dikonfirmasi sebelum LEBER dikembangkan. Efektivitas LEBER belum boleh dinyatakan sebelum ablation study, pengujian beberapa seed, dan pembandingan dengan setidaknya satu strong bilateral baseline selesai.

## Urgensi penelitian (bahan penguatan Bab I)

### Urgensi klinis

Gangguan penglihatan dan kebutaan merupakan masalah kesehatan global. Organisasi Kesehatan Dunia melaporkan sedikitnya 2,2 miliar orang mengalami gangguan penglihatan atau kebutaan, dan sedikitnya 1 miliar kasus berpotensi dapat dicegah atau belum tertangani ([WHO, 2023](https://www.who.int/publications/m/item/increasing-eye-care-interventions-to-address-vision-impairment)). Kondisi ini menegaskan kebutuhan terhadap skrining yang lebih cepat, terjangkau, dan dapat menjangkau wilayah dengan keterbatasan tenaga ahli.

### Urgensi data dan teknis

Citra fundus dapat memuat lebih dari satu penyakit, sedangkan distribusi label pada ODIR-5K tidak seimbang. Model yang dilatih dengan Binary Cross-Entropy berisiko menerima lebih banyak sinyal dari label negatif yang dominan, sehingga penyakit yang jarang muncul dapat kurang terdeteksi. Oleh karena itu, BCE, Weighted BCE, Focal Loss, ASL, dan PolyLoss perlu diuji secara langsung dan terkontrol, bukan diasumsikan memiliki kinerja terbaik.

### Urgensi kepercayaan dan sistem informasi

Keluaran sistem kesehatan tidak cukup hanya berupa probabilitas. Pengguna perlu melihat bagian citra yang berkontribusi terhadap prediksi agar hasil dapat ditinjau secara kritis. Layer-CAM dapat menampilkan peta perhatian yang lebih rinci dengan memanfaatkan informasi dari beberapa layer CNN. Peta ini tetap merupakan interpretasi pendukung dan bukan pengganti validasi klinis.

### Paragraf siap pakai untuk latar belakang

Kebutuhan terhadap sistem skrining penyakit mata yang cepat dan dapat ditinjau semakin penting karena gangguan penglihatan masih menjadi beban kesehatan global dan sebagian kasusnya berpotensi dapat dicegah atau belum tertangani. ODIR-5K menyediakan dua citra fundus untuk setiap pasien, sedangkan targetnya berupa diagnosis multi-label yang ditentukan dari kondisi kedua mata. Distribusi label yang tidak seimbang memengaruhi sinyal pembelajaran, sehingga BCE, Weighted BCE, Focal Loss, ASL, dan PolyLoss diuji sebagai studi pendahuluan. Hasil awal menunjukkan perbedaan antarloss relatif kecil. Penelitian kemudian berfokus pada cara model menggabungkan bukti visual dari mata kiri, mata kanan, dan hubungan bilateral. LEBER diusulkan untuk menghasilkan bobot tiga sumber per label dan menjaga prediksi pasien tetap konsisten ketika urutan mata ditukar. Penelitian ini tidak ditujukan untuk menggantikan dokter. Hasilnya digunakan untuk menilai apakah routing bilateral yang terstruktur dapat menghasilkan performa yang kompetitif, konsistensi yang lebih baik, dan keputusan model yang lebih mudah dianalisis.
