# Catatan Tanya-Jawab Arah Penelitian LEBER

## 1. Apa arah penelitian sekarang?

Penelitian tidak lagi hanya membandingkan fungsi *loss*. Penelitian terdiri atas dua tahap yang saling berhubungan:

1. **Studi pendahuluan fungsi loss** untuk memilih aturan optimasi yang layak dan menetapkannya sebagai variabel kontrol.
2. **Pengembangan dan evaluasi arsitektur LEBER** sebagai kontribusi utama penelitian.

LEBER adalah singkatan dari **Label-wise Exchange-Equivariant Bilateral Evidence Routing**. Metode ini menerima citra fundus mata kiri dan kanan seorang pasien, kemudian menghasilkan delapan probabilitas diagnosis pada tingkat pasien.

Tujuan akhirnya adalah menghasilkan model yang:

- mempunyai performa klasifikasi yang kompetitif atau lebih baik;
- konsisten ketika urutan citra mata kiri dan kanan ditukar;
- memungkinkan sumber bukti keputusan model dianalisis untuk setiap label.

## 2. Apa research gap penelitian?

Research gap yang **tidak boleh** digunakan adalah klaim bahwa belum ada penelitian yang menggunakan kedua mata. Sejumlah penelitian terdahulu sudah menggunakan citra bilateral, attention, feature fusion, pixel-level fusion, cross-attention, dan gated fusion.

Research gap yang lebih tepat adalah:

> Berdasarkan literatur ODIR-5K yang ditelaah, belum ditemukan metode yang secara bersamaan memisahkan bukti mata kiri, mata kanan, dan hubungan bilateral untuk setiap label, serta menjamin dan menguji konsistensi diagnosis tingkat pasien ketika urutan kedua mata ditukar.

Klaim ini dibatasi dengan frasa **“berdasarkan literatur yang ditelaah”**. Klaim “pertama di dunia” belum dapat digunakan.

### Mengapa gap ini penting?

ODIR-5K memberikan pasangan citra kiri dan kanan, tetapi target akhirnya berupa diagnosis gabungan pada tingkat pasien. Dari target tersebut, tidak terlihat secara langsung apakah suatu prediksi didukung oleh:

- mata kiri;
- mata kanan;
- atau hubungan kondisi kedua mata.

Istilah yang benar adalah **kontribusi bukti visual terhadap keputusan model**, bukan kontribusi terhadap penyebab penyakit. LEBER tidak menentukan penyebab klinis penyakit.

## 3. Apa bukti masalah dari data?

Dataset kerja memiliki 2.450 pasien pada training set. Distribusi positifnya adalah:

| Label | Positif | Persentase |
|---|---:|---:|
| N | 796 | 32,49% |
| D | 790 | 32,24% |
| G | 151 | 6,16% |
| C | 148 | 6,04% |
| A | 115 | 4,69% |
| H | 72 | 2,94% |
| M | 122 | 4,98% |
| O | 685 | 27,96% |

Jumlah sampel positif label terbanyak sekitar sebelas kali label paling sedikit. Dengan demikian, model dapat lebih mudah mempelajari label umum daripada penyakit yang jarang muncul.

## 4. Mengapa eksperimen fungsi loss dilakukan?

Fungsi loss menentukan seberapa besar kesalahan model dan sinyal pembelajaran yang diterima setiap label. Loss diprioritaskan karena masalah multi-label dan ketimpangan kelas berhubungan langsung dengan pembentukan sinyal tersebut.

Lima fungsi loss yang diuji mewakili strategi berbeda:

- BCE sebagai baseline multi-label;
- Weighted BCE untuk memberikan penalti lebih besar pada kelas langka;
- Focal Loss untuk memusatkan pembelajaran pada contoh sulit;
- ASL untuk memperlakukan contoh positif dan negatif secara asimetris;
- PolyLoss untuk memodifikasi bentuk penalti klasifikasi.

Hasil studi pendahuluan resolusi 224 pada tiga seed:

| Fungsi loss | Rata-rata Test Macro-F1 ± SD |
|---|---:|
| BCE | 0,5877 ± 0,0071 |
| Weighted BCE | 0,5791 ± 0,0094 |
| Focal Loss | 0,5802 ± 0,0193 |
| ASL | **0,5909 ± 0,0115** |
| PolyLoss | 0,5868 ± 0,0111 |

ASL hanya unggul sekitar 0,0032 terhadap BCE dan 0,0041 terhadap PolyLoss pada rata-rata tiga seed. Hasil ini menunjukkan bahwa loss berpengaruh, tetapi perubahan loss saja belum menyelesaikan seluruh masalah. BCE, ASL, dan PolyLoss sedang dikonfirmasi pada baseline bilateral 512 sebelum satu loss dikunci untuk LEBER.

Parameter lain seperti learning rate, batch size, optimizer, augmentasi, backbone, dan jumlah epoch tidak diabaikan. Parameter tersebut dibuat tetap agar penyebab perubahan performa dapat diisolasi. Jika semua parameter diubah sekaligus, kontribusi masing-masing perubahan tidak dapat diketahui.

## 5. Mengapa menggunakan ODIR-5K?

ODIR-5K dipilih bukan karena merupakan dataset fundus paling baru, tetapi karena strukturnya paling sesuai dengan pertanyaan penelitian. Dataset ini menyediakan:

- pasangan citra fundus mata kiri dan kanan;
- identitas pasien;
- diagnosis multi-label berdasarkan kondisi kedua mata;
- delapan kategori diagnosis;
- data dari beberapa pusat dan perangkat pengambilan gambar.

Dataset yang lebih baru tidak otomatis lebih sesuai. RFMiD dan MuReD terutama menggunakan label tingkat citra. BRSET lebih baru dan lebih besar, tetapi label patologinya juga tercatat pada tingkat citra. Menggunakannya sebagai test set langsung akan mengubah unit tugas dan definisi target.

BRSET dapat dipertimbangkan sebagai validasi eksternal tambahan apabila:

1. pasangan kiri-kanan dibentuk secara valid pada tingkat pasien;
2. hanya label yang definisinya benar-benar setara yang digunakan;
3. aturan agregasi label tingkat citra menjadi tingkat pasien dibenarkan secara ilmiah.

Tanpa harmonisasi tersebut, performa rendah dapat disebabkan perbedaan label dan protokol, bukan kelemahan model.

## 6. Bagaimana cara kerja LEBER?

LEBER dapat dibayangkan sebagai tiga saksi dan satu ketua:

- saksi kiri membaca mata kiri;
- saksi kanan membaca mata kanan;
- saksi bilateral membandingkan kedua mata;
- router bertindak sebagai ketua yang membagi tingkat kepercayaan.

### Tahap 1: shared ResNet50

Kedua citra dibaca dengan ResNet50 yang sama:

$$
f_L=E(x_L), \qquad f_R=E(x_R)
$$

$f_L$ dan $f_R$ adalah ringkasan fitur mata kiri dan kanan. Bobot backbone dibagi agar kedua mata dibaca menggunakan aturan visual yang sama.

### Tahap 2: bukti bilateral

Hubungan kedua mata dibentuk dengan:

$$
f_B=[f_L+f_R,\ |f_L-f_R|,\ f_L\odot f_R]
$$

Maknanya:

- penjumlahan menangkap informasi keseluruhan;
- selisih mutlak menangkap perbedaan kedua mata;
- perkalian menangkap pola yang kuat pada keduanya.

### Tahap 3: tiga expert

Model menghasilkan tiga pendapat untuk setiap label:

- $z_{L,c}$ dari expert kiri;
- $z_{R,c}$ dari expert kanan;
- $z_{B,c}$ dari expert bilateral.

### Tahap 4: router per label

Router memberikan tiga bobot untuk label ke-$c$:

$$
w_{L,c}+w_{R,c}+w_{B,c}=1
$$

Prediksi gabungannya adalah:

$$
z_c=w_{L,c}z_{L,c}+w_{R,c}z_{R,c}+w_{B,c}z_{B,c}
$$

Pembagian bobot dapat berbeda untuk setiap label dan pasien. Angka tersebut dipelajari dari data, bukan ditentukan secara manual.

### Tahap 5: pertukaran mata

Diagnosis pasien seharusnya memenuhi:

$$
p(x_L,x_R)=p(x_R,x_L)
$$

Ketika urutan mata ditukar:

- expert dan bobot kiri-kanan mengikuti pertukaran;
- bukti bilateral tetap;
- prediksi akhir pasien tetap sama.

Selisih prediksi dapat diukur dengan:

$$
\Delta p=\operatorname{mean}|p(x_L,x_R)-p(x_R,x_L)|
$$

Semakin kecil nilai $\Delta p$, semakin konsisten model terhadap pertukaran mata.

## 7. Apa kebaruan yang dituju?

Kandidat kebaruan LEBER adalah kombinasi berikut:

1. dekomposisi eksplisit tiga sumber bukti: kiri, kanan, dan bilateral;
2. *convex routing* khusus untuk setiap label, dengan tiga bobot berjumlah satu;
3. aturan *exchange-equivariant* pada expert dan bobot internal;
4. prediksi pasien yang *exchange-invariant*;
5. evaluasi khusus terhadap selisih prediksi dan konsistensi bobot setelah pertukaran mata.

Backbone ResNet50, ASL, attention, bilateral fusion, dan Layer-CAM bukan kebaruan utama.

## 8. Apa yang sudah dilakukan paper terdahulu?

### BFPC-Net, 2022

Menggunakan ResNet50, residual attention, dan feature fusion untuk citra bilateral. Paper ini membuktikan bahwa kedua mata dapat digunakan bersama, tetapi tidak menjelaskan routing tiga sumber per label dan pengujian swap.

### EfficientNet–ML-Decoder, 2024

Menggunakan EfficientNet, pixel-level bilateral fusion, ML-Decoder, dan SAM. Paper ini menunjukkan peningkatan melalui penggabungan citra kedua mata, tetapi tidak memisahkan kontribusi kiri, kanan, dan bilateral dengan bobot per label.

### DualCrossAttnNet, 2026

Menggunakan EfficientNet-B2, bilateral spatial/channel cross-attention, gated fusion, SE attention, GeM pooling, dan classifier multi-label. Ini merupakan pembanding dekat karena sudah melakukan penggabungan bilateral adaptif.

### Bi-LGT, 2026

Menggunakan convolutional encoder, attention bergaya CBAM, Local-Global Transformer, bilateral cross-attention, class query per label, dan patient-level graph head. Paper ini merupakan pembanding paling dekat karena sudah memiliki bukti tingkat mata, pemodelan per label, dan interaksi bilateral.

Perbedaan yang masih tampak adalah bahwa LEBER merumuskan tiga logit expert yang digabungkan dengan bobot eksplisit per label serta aturan pertukaran dan metrik swap. Namun, gap ini sempit dan harus diperiksa terhadap metode, persamaan, serta ablation study lengkap kedua paper 2026 tersebut.

## 9. Apa yang ingin diselesaikan dari penelitian terdahulu?

LEBER mencoba menyelesaikan tiga keterbatasan:

1. **Fusion yang sulit ditelusuri.** Model terdahulu dapat menggabungkan kedua mata, tetapi sumber keputusan kiri, kanan, dan bilateral tidak selalu terlihat secara eksplisit.
2. **Pola fusion yang belum eksplisit per sumber dan per label.** Setiap penyakit mungkin membutuhkan pembagian bukti berbeda.
3. **Konsistensi urutan yang belum dijamin dan diuji.** Diagnosis pasien tidak seharusnya berubah hanya karena posisi input ditukar.

Penelitian ini memperluas metode bilateral agar sumber keputusan per label lebih terlacak dan prediksinya konsisten terhadap pertukaran mata.

## 10. Apakah penelitian mengejar keakuratan?

Ya. LEBER dirancang dan diuji untuk meningkatkan atau setidaknya mempertahankan performa klasifikasi. Namun, peningkatan belum boleh dijanjikan sebelum eksperimen.

Keberhasilan dinilai berdasarkan tiga aspek:

1. **Performa:** Macro-F1, Micro-F1, precision, recall, F1 per label, AUROC, dan mAP.
2. **Konsistensi:** selisih probabilitas dan bobot setelah pertukaran mata.
3. **Keterlacakan:** distribusi bobot expert per label serta Layer-CAM pada cabang model.

Accuracy bukan satu-satunya metrik karena dataset tidak seimbang. Model dapat memperoleh accuracy tinggi dengan sering memprediksi negatif pada label langka. Macro-F1 dipilih sebagai metrik utama karena memberi kepentingan yang sama kepada setiap label.

Interpretasi hasil:

- apabila Macro-F1 naik dan selisih swap turun, bukti mendukung LEBER dengan kuat;
- apabila Macro-F1 tetap kompetitif tetapi konsistensi membaik secara besar, terdapat trade-off yang dapat dipertanggungjawabkan;
- apabila performa turun besar dan konsistensi tidak membaik, hipotesis LEBER tidak didukung.

## 11. Bagaimana pengujian arsitektur dilakukan?

| Kode | Konfigurasi | Pertanyaan yang dijawab |
|---|---|---|
| A0 | Shared ResNet50 dan fusion biasa | Seberapa baik baseline pada protokol yang sama? |
| A1 | Interaksi bilateral simetris | Apakah perbandingan kedua mata membantu? |
| A2 | Tiga expert dengan bobot tetap | Apakah peningkatan hanya berasal dari kapasitas tambahan? |
| A3 | Router global | Apakah bobot yang dipelajari membantu? |
| A4 | Router per label | Apakah kebutuhan fusion berbeda untuk setiap penyakit? |
| A5 | Router per label dan pengawasan expert | Apakah setiap expert mempelajari sumber buktinya? |
| A6 | Konstruksi LEBER lengkap | Apakah exchange equivariance memperbaiki konsistensi dan performa? |

Semua konfigurasi harus memakai split pasien, preprocessing, loss, optimizer, threshold, dan metrik yang sama. A0 dan A6 minimal dijalankan dengan seed 42, 52, dan 62, kemudian hasil dilaporkan sebagai rata-rata dan simpangan baku.

## 12. Bagaimana posisi hasil paper terdahulu?

Paper terdahulu harus digunakan sebagai dasar dan pembanding. Angka publikasinya tidak boleh langsung dibandingkan dengan hasil lokal jika protokol berbeda. Perbedaan dapat mencakup:

- pembagian data;
- level label pasien atau citra;
- pembuangan kelas atau sampel;
- definisi Macro-F1, Micro-F1, atau sample-averaged F1;
- threshold prediksi;
- pemilihan checkpoint dan preprocessing.

Jika kode dan sumber daya memungkinkan, satu model bilateral terdekat sebaiknya direplikasi menggunakan protokol kita sebagai *strong baseline*. Jika tidak memungkinkan, hasil publikasi tetap dicantumkan sebagai perbandingan tidak langsung dengan penjelasan batasannya.

## 13. Rumusan kesimpulan penelitian

> Penelitian ini mengembangkan dan mengevaluasi LEBER untuk klasifikasi multi-label tingkat pasien pada pasangan citra fundus ODIR-5K. Eksperimen lima fungsi loss digunakan sebagai studi pendahuluan dan kontrol optimasi. Kontribusi utamanya adalah pemisahan sumber bukti mata kiri, mata kanan, dan hubungan bilateral untuk setiap label, serta konstruksi yang menjaga konsistensi prediksi ketika urutan kedua mata ditukar. Metode dinilai berdasarkan performa klasifikasi, konsistensi swap, keterlacakan sumber bukti, efisiensi, ablation study, dan kestabilan pada beberapa seed.

## Referensi utama

1. ODIR-2019 Grand Challenge. *ODIR-5K Dataset*. https://odir2019.grand-challenge.org/dataset/
2. Aggarwal et al. (2022). *Multi-Label Fundus Image Classification Using Attention Mechanisms and Feature Fusion*. https://pmc.ncbi.nlm.nih.gov/articles/PMC9230753/
3. Bhati et al. (2023). *Discriminative Kernel Convolution Network for Multi-Label Ophthalmic Disease Detection on Imbalanced Fundus Image Dataset*. https://pubmed.ncbi.nlm.nih.gov/36608462/
4. Gündel et al. (2024). *Combining EfficientNet with ML-Decoder Classification Head for Multi-Label Retinal Disease Classification*. https://doi.org/10.1007/s00521-024-09820-w
5. Wang et al. (2026). *C²Net: A Co-Occurrence and Consistency-Aware Framework for Structured Multi-Label Fundus Diagnosis*. https://pubmed.ncbi.nlm.nih.gov/42048017/
6. Zhou et al. (2026). *A Novel Bilateral Cross-Attention Network for Multi-Label Fundus Disease Diagnosis*. https://doi.org/10.1016/j.compbiomed.2026.111818
7. Nakayama et al. (2024; dataset version 2026). *BRSET: A Brazilian Multilabel Ophthalmological Dataset*. https://physionet.org/content/brazilian-ophthalmological/1.0.2/

## Catatan kehati-hatian

- Klaim kebaruan LEBER belum final sebelum audit metode lengkap DualCrossAttnNet dan Bi-LGT selesai.
- Bobot router menjelaskan kontribusi terhadap keputusan model, bukan kausalitas penyakit.
- Layer-CAM tidak boleh disebut sebagai lokasi lesi klinis tanpa anotasi lesi.
- Kesimpulan utama dibatasi pada protokol dan populasi ODIR-5K.
- Hasil eksperimen yang tidak mendukung hipotesis harus dilaporkan dan tidak boleh dipaksakan menjadi klaim positif.
