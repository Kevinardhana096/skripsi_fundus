# Perbandingan dan Kesimpulan Eksperimen

## Perbandingan final fungsi loss

Bagian rincian per label di bawah mempertahankan hasil seed 42 pada resolusi 224. Seluruh lima loss kemudian telah diulang pada seed 52 dan 62 dengan protokol 224 yang sama. Threshold setiap label ditentukan menggunakan validation set.

### Ringkasan tiga seed pada resolusi 224

| Fungsi loss | Macro-F1 | Micro-F1 | Macro-AUROC | Hamming loss | Subset accuracy |
|---|---:|---:|---:|---:|---:|
| BCE | 0,5877 ± 0,0071 | 0,5803 ± 0,0091 | 0,8454 ± 0,0170 | 0,1474 ± 0,0101 | 0,2971 ± 0,0587 |
| Weighted BCE | 0,5791 ± 0,0094 | 0,5519 ± 0,0057 | 0,8446 ± 0,0118 | 0,1746 ± 0,0150 | 0,1937 ± 0,0656 |
| Focal Loss | 0,5802 ± 0,0193 | 0,5643 ± 0,0118 | **0,8523 ± 0,0039** | 0,1610 ± 0,0093 | 0,2463 ± 0,0251 |
| ASL | **0,5909 ± 0,0115** | 0,5675 ± 0,0171 | 0,8435 ± 0,0085 | 0,1569 ± 0,0183 | 0,2508 ± 0,0850 |
| PolyLoss | 0,5868 ± 0,0111 | **0,5827 ± 0,0115** | 0,8460 ± 0,0142 | **0,1358 ± 0,0013** | **0,3670 ± 0,0115** |

ASL memiliki rata-rata Macro-F1 tertinggi, tetapi selisihnya terhadap BCE sekitar 0,0032 dan terhadap PolyLoss sekitar 0,0041. Selisih ini kecil dan variasi antarseed bertumpang tindih, sehingga belum ada dasar untuk menyatakan keunggulan mutlak atau signifikansi statistik.

### Perbandingan metrik keseluruhan

| Fungsi loss | Val. Macro-F1 setelah tuning | Test Macro-F1 | Test Micro-F1 | Macro-AUROC | Hamming loss | Subset accuracy |
|---|---:|---:|---:|---:|---:|---:|
| BCE | 0,5943 | 0,5955 | 0,5827 | 0,8544 | **0,1357** | **0,3638** |
| Weighted BCE | 0,6082 | 0,5802 | 0,5525 | 0,8374 | 0,1574 | 0,2686 |
| Focal Loss | 0,5958 | 0,6012 | 0,5778 | 0,8520 | 0,1531 | 0,2514 |
| ASL | **0,6156** | **0,6034** | 0,5867 | 0,8511 | 0,1395 | 0,3429 |
| PolyLoss | 0,5796 | 0,5788 | **0,5888** | **0,8596** | 0,1367 | 0,3562 |

Hamming loss lebih baik jika nilainya lebih rendah. ASL memperoleh Macro-F1 tertinggi, PolyLoss memperoleh Micro-F1 dan Macro-AUROC tertinggi, sedangkan BCE memperoleh Hamming loss terendah dan subset accuracy tertinggi.

### Performa khusus tujuh label penyakit

Perhitungan berikut tidak memasukkan label N karena N berarti normal.

| Fungsi loss | Rata-rata F1 penyakit | Rata-rata recall penyakit |
|---|---:|---:|
| BCE | 0,5943 | 0,5802 |
| Weighted BCE | 0,5771 | 0,5865 |
| Focal Loss | 0,5982 | **0,6298** |
| ASL | **0,6040** | 0,5860 |
| PolyLoss | 0,5715 | 0,5486 |

ASL memberikan keseimbangan precision dan recall terbaik pada tujuh penyakit. Focal Loss menemukan proporsi pasien sakit paling banyak, tetapi menghasilkan lebih banyak false positive.

### Analisis tambahan enam penyakit spesifik

Evaluasi utama tetap memakai delapan label resmi ODIR-5K. Analisis tambahan berikut hanya menghitung rata-rata F1 untuk enam penyakit dengan kategori spesifik, yaitu D, G, C, A, H, dan M. Label N dikeluarkan karena berarti normal. Label O dikeluarkan dari rata-rata tambahan karena menggabungkan berbagai penyakit atau abnormalitas lain dalam satu kategori yang heterogen. Model tidak dilatih ulang dan prediksi O tidak dibuang dari hasil utama.

| Fungsi loss | Test Macro-F1 D/G/C/A/H/M |
|---|---:|
| BCE | 0,6066 |
| Weighted BCE | 0,6033 |
| Focal Loss | **0,6149** |
| ASL | 0,6121 |
| PolyLoss | 0,5854 |

ASL memperoleh Macro-F1 tertinggi pada evaluasi utama delapan label, yaitu 0,6034. Ketika rata-rata dibatasi pada enam penyakit spesifik, Focal Loss menjadi yang tertinggi dengan nilai 0,6149. Selisih Focal Loss terhadap ASL hanya 0,0028. Hasil ini menunjukkan bahwa peringkat fungsi loss dipengaruhi oleh cakupan label yang dievaluasi.

Analisis enam penyakit digunakan sebagai analisis sekunder, bukan pengganti hasil utama. Kedua hasil dilaporkan bersama agar pengaruh kategori N dan O terlihat jelas serta kesimpulan tidak menyatakan satu fungsi loss unggul untuk seluruh tujuan.
### F1 setiap label

| Label | BCE | Weighted BCE | Focal Loss | ASL | PolyLoss | Hasil tertinggi |
|---|---:|---:|---:|---:|---:|---|
| N | 0,6037 | 0,6023 | 0,6227 | 0,5992 | **0,6295** | PolyLoss |
| D | 0,5759 | 0,5385 | 0,5714 | 0,5625 | **0,5976** | PolyLoss |
| G | 0,5143 | 0,5143 | **0,5373** | 0,5075 | 0,4400 | Focal Loss |
| C | 0,7742 | 0,7368 | 0,7812 | **0,7931** | **0,7931** | ASL dan PolyLoss |
| A | **0,6087** | 0,6047 | 0,5366 | 0,5641 | 0,4878 | BCE |
| H | 0,3158 | 0,3684 | 0,3429 | **0,3704** | 0,3478 | ASL |
| M | 0,8511 | 0,8571 | **0,9200** | 0,8750 | 0,8462 | Focal Loss |
| O | 0,5205 | 0,4196 | 0,4979 | **0,5552** | 0,4883 | ASL |

Tidak ada satu fungsi loss yang unggul pada semua label. PolyLoss unggul pada N dan D, Focal Loss unggul pada G dan M, ASL unggul pada H dan O, sedangkan BCE unggul pada A. ASL dan PolyLoss menghasilkan F1 yang sama pada C.

### Analisis label H

Label H hanya memiliki 15 kasus positif pada test set.

| Fungsi loss | True positive | False negative | False positive | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| BCE | 3 | 12 | 1 | 0,7500 | 0,2000 | 0,3158 |
| Weighted BCE | **7** | **8** | 16 | 0,3043 | **0,4667** | 0,3684 |
| Focal Loss | 6 | 9 | 14 | 0,3000 | 0,4000 | 0,3429 |
| ASL | 5 | 10 | 7 | 0,4167 | 0,3333 | **0,3704** |
| PolyLoss | 4 | 11 | 4 | 0,5000 | 0,2667 | 0,3478 |

Weighted BCE menemukan kasus H paling banyak, tetapi menghasilkan false positive paling banyak. BCE menghasilkan false positive paling sedikit, tetapi melewatkan 12 dari 15 kasus. ASL memperoleh F1 H tertinggi karena keseimbangan precision dan recall-nya lebih baik. Karena test set hanya memiliki 15 kasus H, satu pasien dapat mengubah recall sekitar 0,0667. Selisih kecil pada label ini harus ditafsirkan dengan hati-hati.

### Kesimpulan studi pendahuluan

Pada run seed 42, ASL menghasilkan Test Macro-F1 tertinggi sebesar 0,6034. Setelah tiga seed, ASL tetap memiliki rata-rata Macro-F1 tertinggi sebesar 0,5909, tetapi BCE dan PolyLoss sangat dekat.

Keunggulan ASL terhadap Focal Loss hanya 0,0021 dan terhadap BCE hanya 0,0079. Selisih tersebut kecil. ASL tidak boleh dinyatakan unggul pada seluruh aspek. Focal Loss lebih sensitif dalam menemukan penyakit, BCE membuat kesalahan label paling sedikit, dan PolyLoss menghasilkan Micro-F1 serta Macro-AUROC tertinggi.

Kesimpulan yang digunakan adalah bahwa fungsi loss mengubah pola kesalahan model. ASL unggul tipis pada rata-rata Macro-F1, BCE stabil, dan PolyLoss unggul pada beberapa metrik keseluruhan. Kestabilan telah diperiksa melalui tiga seed, tetapi signifikansi statistik belum diuji.

## Implikasi terhadap eksperimen utama

Hasil lima loss tidak menjadi kebaruan utama. Karena protokol utama berubah ke 512, BCE, ASL, dan PolyLoss dikonfirmasi kembali pada baseline bilateral. BCE 512 seed 42 selesai dengan Test Macro-F1 0,6122; ASL sedang berjalan dan PolyLoss menunggu. Loss LEBER belum dikunci dan pemilihannya harus memakai validation set.

Eksperimen utama selanjutnya membandingkan concatenation dengan symmetric bilateral fusion, tiga expert berbobot tetap, global gate, label-wise router, supervisi kualitas expert, dan exchange-equivariant design. Dengan urutan ini, peningkatan dapat dikaitkan dengan komponen arsitektur yang diuji, bukan hanya dengan bertambahnya parameter.
