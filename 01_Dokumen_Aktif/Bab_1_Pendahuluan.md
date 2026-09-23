# BAB I

# PENDAHULUAN

## 1.1 Latar Belakang

Gangguan penglihatan masih menjadi masalah kesehatan yang luas. World Health Organization (WHO) melaporkan bahwa sedikitnya 2,2 miliar orang mengalami gangguan penglihatan jarak dekat atau jarak jauh. Sedikitnya 1 miliar dari kasus tersebut sebenarnya dapat dicegah atau belum memperoleh penanganan yang diperlukan (WHO, 2023). Kondisi seperti katarak, glaukoma, degenerasi makula terkait usia, dan retinopati diabetik membutuhkan deteksi serta pemantauan. Sistem berbasis kecerdasan buatan dapat membantu proses skrining, tetapi hasilnya tetap perlu ditinjau oleh tenaga kesehatan.

Citra fundus adalah foto bagian belakang mata yang memperlihatkan retina, pembuluh darah, makula, dan diskus optik. Perubahan pada struktur tersebut dapat berkaitan dengan penyakit tertentu. Citra fundus karena itu banyak digunakan sebagai masukan model deep learning untuk membantu klasifikasi penyakit mata.

Seorang pasien dapat memiliki lebih dari satu kondisi pada waktu yang sama. Penelitian ini menggunakan klasifikasi multi-label, yaitu model membuat keputusan positif atau negatif untuk setiap label dan tidak memilih hanya satu kelas. Seorang pasien, misalnya, dapat memiliki label diabetes dan katarak secara bersamaan.

Penelitian menggunakan Ocular Disease Intelligent Recognition atau ODIR-5K. Data kerja berisi 3.500 pasien berlabel. Setiap pasien memiliki citra fundus mata kiri dan kanan. Delapan label yang diprediksi adalah normal (N), diabetes (D), glaukoma (G), katarak (C), degenerasi makula terkait usia (A), hipertensi (H), miopia patologis (M), dan penyakit atau abnormalitas lainnya (O). Label resmi berada pada tingkat pasien dan ditentukan berdasarkan kedua mata serta usia. Oleh karena itu, pasangan mata kiri dan kanan diproses sebagai satu unit dan model menghasilkan diagnosis tingkat pasien, bukan diagnosis terpisah untuk setiap mata.

Karakter tingkat pasien tersebut menimbulkan persoalan penting. Bukti suatu penyakit dapat tampak lebih jelas pada salah satu mata, sedangkan penyakit lain dapat membutuhkan perbandingan kedua mata. Anatomy-Slot melaporkan bahwa informasi bilateral tidak sama pentingnya untuk semua kategori. Glaukoma banyak terbantu oleh perbandingan antarmata, sedangkan katarak dan miopia lebih bergantung pada ciri monokular (Zhang et al., 2026). Dengan demikian, satu mekanisme penggabungan global belum tentu sesuai untuk seluruh label.

Model juga dapat mempelajari ciri mata kiri dan kanan yang tidak selalu berkaitan langsung dengan penyakit. Kim et al. (2021) menunjukkan bahwa CNN dapat membedakan citra fundus kiri dan kanan, termasuk pada data ODIR setelah transformasi horizontal. Temuan ini menunjukkan potensi bias laterality atau posisi input. Karena target penelitian berada pada tingkat pasien, menukar urutan citra kiri dan kanan semestinya tidak mengubah diagnosis akhir pasien.

Penelitian ODIR-5K sebelumnya telah memanfaatkan kedua mata. BFPC-Net menggunakan attention dan feature fusion (Li et al., 2022). DMS-Net menggunakan shared Siamese backbone, fitur multiskala, dan bidirectional attention (Huo et al., 2025). DualCrossAttnNet menggunakan bilateral cross-attention dan gated fusion adaptif (2026). Penelitian tersebut menunjukkan manfaat pemodelan bilateral, tetapi berdasarkan literatur yang ditinjau belum ditemukan metode yang secara bersamaan memisahkan kontribusi mata kiri, mata kanan, dan interaksi bilateral untuk setiap label serta menjamin prediksi pasien tetap sama ketika urutan kedua mata ditukar.

ODIR-5K juga memiliki distribusi label yang tidak seimbang. Pada data training penelitian ini, label N dan D masing-masing memiliki sekitar 790 contoh positif, sedangkan label H hanya memiliki 72 contoh positif. Perbandingan awal menggunakan BCE, Weighted BCE, Focal Loss, Asymmetric Loss, dan PolyLoss telah dilakukan dengan shared ResNet50 serta split pasien yang sama. Eksperimen tersebut diposisikan sebagai studi pendahuluan untuk memahami pola kesalahan dan memilih loss bagi pengembangan metode, bukan sebagai kebaruan utama.

Hasil tiga seed pada studi pendahuluan resolusi 224 menunjukkan ASL memperoleh rata-rata Test Macro-F1 tertinggi sebesar 0,5909, diikuti BCE 0,5877 dan PolyLoss 0,5868. Selisih ketiganya kurang dari 0,005 sehingga belum menunjukkan keunggulan mutlak. Karena protokol utama menggunakan resolusi 512, BCE, ASL, dan PolyLoss dikonfirmasi kembali pada baseline bilateral sebelum loss LEBER dikunci. Pemilihan final didasarkan pada validation set dan kestabilan beberapa seed, bukan satu hasil test.

Berdasarkan masalah tersebut, penelitian mengusulkan Label-wise Exchange-Equivariant Bilateral Evidence Routing atau LEBER. Model menggunakan shared ResNet50 untuk mengekstrak fitur kedua mata. Tiga sumber bukti dibentuk dari cabang mata kiri, cabang mata kanan, dan cabang interaksi bilateral. Router menentukan kontribusi ketiga sumber secara terpisah untuk setiap label. Arsitektur dirancang agar bobot cabang kiri dan kanan ikut bertukar ketika posisi input ditukar, sedangkan probabilitas diagnosis pasien tetap sama.

Kebaruan yang diajukan tidak terletak pada penggunaan dua mata, Siamese backbone, attention, gating, atau loss tertentu secara terpisah karena unsur tersebut telah memiliki pendahulu. Kontribusi metode terletak pada penggabungan dekomposisi bukti kiri, kanan, dan bilateral secara per label dengan aturan pertukaran yang sesuai untuk target tingkat pasien. Klaim ini dibatasi menjadi “berdasarkan literatur yang ditinjau” dan akan diperiksa kembali sebelum naskah akhir.

Penelitian mengevaluasi metode melalui ablation study. Baseline shared ResNet50 dengan concatenation dibandingkan dengan symmetric bilateral fusion, tiga expert berbobot tetap, global gate, label-wise router, supervisi kualitas expert, dan metode lengkap exchange-equivariant. Macro-F1 menjadi metrik utama. Micro-F1, AUROC, Hamming Loss, precision, recall, dan F1 setiap label digunakan sebagai metrik pendukung. Konsistensi pertukaran diukur dari selisih probabilitas sebelum dan sesudah urutan mata ditukar.

Layer-CAM digunakan untuk meninjau area citra yang berkontribusi terhadap prediksi pada setiap cabang. Layer-CAM membentuk peta aktivasi kelas menggunakan informasi dari beberapa lapisan konvolusi sehingga detail spasial dapat ditinjau lebih baik daripada peta yang hanya memakai lapisan akhir (Jiang et al., 2021). Peta tersebut merupakan interpretasi kualitatif dan bukan bukti lokasi lesi secara klinis.

Arah penelitian ini menghasilkan dua keluaran. Pertama, bukti empiris dari studi fungsi loss pada baseline bilateral. Kedua, metode LEBER yang diuji melalui ablation study, pengulangan seed, pengujian konsistensi pertukaran, evaluasi per label, dan Layer-CAM. Penelitian diharapkan menjelaskan seberapa baik model menghasilkan diagnosis pasien serta bagaimana bukti dari kedua mata berkontribusi untuk setiap penyakit.

## 1.2 Rumusan Masalah

1. Bagaimana merancang mekanisme yang memisahkan bukti mata kiri, mata kanan, dan interaksi bilateral untuk setiap label penyakit pada ODIR-5K?
2. Apakah label-wise bilateral evidence routing meningkatkan performa dibandingkan penggabungan fitur bilateral konvensional?
3. Apakah rancangan exchange-equivariant menjaga diagnosis pasien tetap konsisten ketika urutan citra kiri dan kanan ditukar?
4. Bagaimana kontribusi setiap cabang dan area perhatian Layer-CAM berbeda antarlabel penyakit?

## 1.3 Tujuan Penelitian

1. Mengembangkan metode LEBER untuk klasifikasi multi-label tingkat pasien menggunakan pasangan citra fundus.
2. Menguji kontribusi symmetric fusion, tiga expert, global gate, label-wise router, supervisi kualitas expert, dan exchange-equivariant design melalui ablation study.
3. Mengukur performa klasifikasi, kestabilan antar-seed, serta konsistensi prediksi terhadap pertukaran urutan mata.
4. Menganalisis kontribusi cabang dan area perhatian model menggunakan bobot router serta Layer-CAM.

## 1.4 Batasan Penelitian

1. Dataset utama adalah ODIR-5K dengan delapan label resmi.
2. Unit analisis dan pembagian data berada pada tingkat pasien.
3. Backbone utama adalah shared ResNet50 pretrained ImageNet.
4. Eksperimen loss menjadi studi pendahuluan; pengembangan LEBER menjadi eksperimen utama.
5. Layer-CAM digunakan sebagai interpretasi kualitatif, bukan validasi klinis lokasi lesi.
6. Model merupakan alat pengolahan informasi pendukung dan bukan pengganti diagnosis dokter.

## Referensi yang digunakan pada Bab I

1. World Health Organization. (2023). *Increasing eye care interventions to address vision impairment*. https://www.who.int/publications/m/item/increasing-eye-care-interventions-to-address-vision-impairment
2. Ridnik, T., et al. (2021). *Asymmetric Loss for Multi-Label Classification*. ICCV 2021. https://openaccess.thecvf.com/content/ICCV2021/html/Ridnik_Asymmetric_Loss_for_Multi-Label_Classification_ICCV_2021_paper.html
3. Kim et al. (2021). *Asymmetry between right and left fundus images identified using convolutional neural networks*. Scientific Reports. https://www.nature.com/articles/s41598-021-04323-3
4. Li, Z., et al. (2022). *Multi-Label Fundus Image Classification Using Attention Mechanisms and Feature Fusion*. Micromachines, 13(6), 947. https://doi.org/10.3390/mi13060947
5. Huo, G., et al. (2025). *DMS-Net Dual-Modal Multi-Scale Siamese Network for Binocular Fundus Image Classification*. https://arxiv.org/abs/2504.18046
6. *A novel bilateral cross-attention network for multi-label fundus disease diagnosis*. (2026). Computers in Biology and Medicine. https://www.sciencedirect.com/science/article/pii/S0010482526003823
7. Zhang et al. (2026). *Anatomy-Slot Unsupervised Anatomical Factorization for Homologous Bilateral Reasoning in Retinal Diagnosis*. https://arxiv.org/abs/2605.12929
8. Jiang, P.-T., et al. (2021). *LayerCAM Exploring Hierarchical Class Activation Maps for Localization*. IEEE Transactions on Image Processing, 30, 5875-5888. https://doi.org/10.1109/TIP.2021.3089943
9. ODIR-2019. *Dataset*. https://odir2019.grand-challenge.org/dataset/

> Catatan penulisan: angka hasil eksperimen ditempatkan pada Bab IV. Bab I menjelaskan masalah, gap, metode yang diusulkan, dan rencana pembuktian tanpa menyatakan metode baru telah terbukti lebih baik.
