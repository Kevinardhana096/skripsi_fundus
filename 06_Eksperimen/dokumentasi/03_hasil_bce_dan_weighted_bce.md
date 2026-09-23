# Hasil BCE dan Weighted BCE

> Catatan status: angka pada dokumen ini merupakan rincian eksperimen awal resolusi 224, terutama run seed 42. Ringkasan tiga seed terdapat pada `05_perbandingan_dan_kesimpulan.md`. Baseline bilateral BCE 512 seed 42 telah diuji terpisah dan menghasilkan Test Macro-F1 0,6122.

## Hasil eksperimen baseline BCE

Baseline menggunakan ResNet50 dengan fungsi loss Binary Cross-Entropy (BCE). Model menerima sepasang citra fundus, yaitu foto bagian belakang mata kiri dan kanan dari satu pasien. Model kemudian memprediksi kemungkinan munculnya satu atau beberapa dari delapan label: N, D, G, C, A, H, M, dan O.

BCE adalah fungsi yang mengukur kesalahan prediksi untuk setiap label. Jika prediksi model berbeda dari label sebenarnya, nilai kesalahannya membesar. Pada BCE standar, semua label diperlakukan dengan bobot yang sama, meskipun jumlah contoh setiap penyakit tidak seimbang.

### Ringkasan hasil

| Ukuran | Hasil | Arti sederhana |
|---|---:|---|
| Epoch terbaik | 27 | Checkpoint dengan Macro-F1 validasi tertinggi diperoleh pada putaran ke-27. |
| Validation Macro-F1, threshold 0,50 | 0,5566 | Performa rata-rata delapan label pada data validasi ketika semua label memakai batas keputusan 0,50. |
| Validation Macro-F1, threshold per label | 0,5943 | Performa validasi meningkat setelah setiap label memakai batas keputusan yang ditentukan hanya dari data validasi. |
| Test Macro-F1 | 0,5955 | Rata-rata F1 dari delapan label pada data test. Setiap label memiliki pengaruh yang sama terhadap nilai ini. |
| Test Micro-F1 | 0,5827 | F1 yang dihitung setelah seluruh keputusan label digabungkan. Nilainya lebih dipengaruhi label dengan jumlah contoh lebih banyak. |
| Test Macro-AUROC | 0,8544 | Model cukup baik dalam memberikan skor lebih tinggi kepada kasus positif daripada kasus negatif. |
| Hamming loss | 0,1357 | Sekitar 13,57 persen dari seluruh keputusan label pada data test salah. Nilai yang lebih kecil lebih baik. |
| Subset accuracy | 0,3638 | Sekitar 36,38 persen pasien memiliki seluruh kombinasi label yang diprediksi tepat. Ukuran ini ketat karena satu label yang salah membuat satu pasien dihitung salah. |

### Arti istilah penting

- **Epoch** adalah satu putaran ketika model mempelajari seluruh data training.
- **Training loss** adalah angka kesalahan model pada data yang dipakai untuk belajar. Nilai yang semakin kecil menunjukkan model semakin cocok dengan data training.
- **Validation set** adalah data pemeriksaan selama pengembangan. Data ini tidak dipakai untuk memperbarui bobot model.
- **Test set** adalah data untuk pengujian akhir. Data ini tidak digunakan untuk memilih model atau menentukan threshold.
- **Threshold** adalah batas untuk mengubah probabilitas menjadi keputusan positif atau negatif. Sebagai contoh, dengan threshold 0,50, probabilitas 0,70 menjadi positif dan probabilitas 0,30 menjadi negatif.
- **F1-score** menggabungkan kemampuan menemukan kasus positif dan kemampuan menjaga agar prediksi positif tidak banyak yang salah.
- **Macro-F1** menghitung F1 setiap label lalu mengambil rata-ratanya. Penyakit yang jarang muncul tetap memiliki kepentingan yang sama dengan label yang sering muncul.
- **Micro-F1** menggabungkan seluruh keputusan dari semua label sebelum menghitung F1. Hasilnya lebih dipengaruhi oleh label yang memiliki lebih banyak contoh.
- **AUROC** mengukur kemampuan model mengurutkan kasus positif lebih tinggi daripada kasus negatif. Nilai 0,50 setara dengan tebakan acak, sedangkan nilai yang mendekati 1,00 semakin baik.
- **Overfitting** adalah kondisi ketika model semakin baik menghafal data training, tetapi tidak semakin baik pada data baru.
- **Early stopping** menghentikan training ketika performa validasi tidak membaik selama beberapa epoch.
- **Checkpoint** adalah file yang menyimpan kondisi model pada epoch tertentu. Evaluasi akhir memakai checkpoint terbaik, bukan model dari epoch terakhir.
- **Class imbalance** adalah kondisi ketika jumlah contoh antarkelas tidak seimbang. Beberapa penyakit memiliki banyak contoh, sedangkan penyakit lainnya hanya memiliki sedikit contoh.

### Hasil setiap label pada test set

| Label | F1-score | AUROC | Interpretasi singkat |
|---|---:|---:|---|
| N | 0,6037 | 0,7763 | Model menemukan banyak kasus positif, tetapi masih menghasilkan cukup banyak prediksi positif yang salah. |
| D | 0,5759 | 0,7745 | Kemampuan deteksi sedang. |
| G | 0,5143 | 0,8728 | Model cukup baik mengurutkan kasus positif, tetapi keputusan positif dan negatifnya masih dapat ditingkatkan. |
| C | 0,7742 | 0,9470 | Performa baik. |
| A | 0,6087 | 0,9267 | Performa cukup baik meskipun jumlah kasus positif terbatas. |
| H | 0,3158 | 0,8093 | Model masih lemah dalam menemukan kasus positif. |
| M | 0,8511 | 0,9961 | Performa paling baik di antara delapan label. |
| O | 0,5205 | 0,7324 | Model masih menghasilkan cukup banyak prediksi positif yang salah. |

Label H menjadi temuan penting. Dari 15 kasus positif H pada test set, model hanya menemukan 3 kasus dengan benar dan melewatkan 12 kasus. Nilai recall H hanya 0,20. Hasil ini menunjukkan bahwa BCE standar belum memberikan performa yang merata, terutama pada label dengan jumlah kasus positif yang sedikit.

Training loss terus menurun hingga sekitar 0,0151 pada epoch 27, sedangkan validation loss mencapai sekitar 0,5008. Pola ini menunjukkan kecenderungan overfitting karena model semakin cocok dengan data training tanpa perbaikan yang konsisten pada data validasi. Pemilihan checkpoint berdasarkan Macro-F1 sudah tepat karena checkpoint terbaik berasal dari epoch 27, bukan kondisi model pada epoch terakhir.

### Kesimpulan baseline

BCE standar sudah dapat digunakan sebagai baseline penelitian. Model cukup baik dalam membedakan kasus positif dan negatif, terlihat dari Macro-AUROC sebesar 0,8544. Namun, performanya belum merata untuk semua label. Kelemahan paling jelas terdapat pada label H yang jarang muncul. Temuan ini menjadi dasar untuk menguji Weighted BCE, Focal Loss, Asymmetric Loss, dan PolyLoss menggunakan pembagian data, arsitektur, serta konfigurasi eksperimen yang sama.

## Hasil eksperimen Weighted BCE

Weighted BCE menggunakan dasar perhitungan yang sama dengan BCE, tetapi memberikan bobot lebih besar pada kesalahan untuk kasus positif dari label yang jarang muncul. Bobot positif dihitung dari jumlah data negatif dibagi jumlah data positif pada data training. Sebagai contoh, label H memiliki 72 data positif dan 2.378 data negatif, sehingga memperoleh `pos_weight` sekitar 33,03. Kesalahan saat tidak mengenali kasus positif H mendapat tekanan lebih besar selama training.

### Bobot positif setiap label

| Label | Positif training | Negatif training | `pos_weight` |
|---|---:|---:|---:|
| N | 796 | 1.654 | 2,0779 |
| D | 790 | 1.660 | 2,1013 |
| G | 151 | 2.299 | 15,2252 |
| C | 148 | 2.302 | 15,5541 |
| A | 115 | 2.335 | 20,3043 |
| H | 72 | 2.378 | 33,0278 |
| M | 122 | 2.328 | 19,0820 |
| O | 685 | 1.765 | 2,5766 |

### Ringkasan hasil

| Ukuran | Hasil | Arti sederhana |
|---|---:|---|
| Epoch terbaik | 21 | Checkpoint dengan Macro-F1 validasi tertinggi diperoleh pada putaran ke-21. |
| Validation Macro-F1, threshold 0,50 | 0,5653 | Performa validasi ketika seluruh label memakai batas keputusan 0,50. |
| Validation Macro-F1, threshold per label | 0,6082 | Performa validasi setelah threshold setiap label ditentukan dari data validasi. |
| Test Macro-F1 | 0,5802 | Rata-rata F1 delapan label pada data test. |
| Test Micro-F1 | 0,5525 | F1 setelah seluruh keputusan label digabungkan. |
| Test Macro-AUROC | 0,8374 | Kemampuan rata-rata model dalam mengurutkan kasus positif di atas kasus negatif. |
| Hamming loss | 0,1574 | Sekitar 15,74 persen dari seluruh keputusan label pada data test salah. |
| Subset accuracy | 0,2686 | Sekitar 26,86 persen pasien memiliki seluruh kombinasi label yang diprediksi tepat. |

### Hasil setiap label pada test set

| Label | Precision | Recall | F1-score | AUROC | Interpretasi singkat |
|---|---:|---:|---:|---:|---|
| N | 0,4522 | 0,9017 | 0,6023 | 0,7645 | Hampir semua kasus positif ditemukan, tetapi terdapat banyak prediksi positif yang salah. |
| D | 0,4534 | 0,6627 | 0,5385 | 0,7268 | Recall meningkat dengan konsekuensi precision yang rendah. |
| G | 0,4737 | 0,5625 | 0,5143 | 0,9069 | Kemampuan pengurutan kasus baik, tetapi keputusan akhirnya masih sedang. |
| C | 0,8400 | 0,6563 | 0,7368 | 0,9239 | Performa baik dengan sedikit prediksi positif yang salah. |
| A | 0,6842 | 0,5417 | 0,6047 | 0,9414 | Kemampuan membedakan kasus baik, tetapi beberapa kasus positif masih terlewat. |
| H | 0,3043 | 0,4667 | 0,3684 | 0,7722 | Model menemukan lebih banyak kasus positif H, tetapi menghasilkan lebih banyak prediksi positif yang salah. |
| M | 0,9130 | 0,8077 | 0,8571 | 0,9967 | Performa paling baik di antara delapan label. |
| O | 0,4317 | 0,4082 | 0,4196 | 0,6665 | Performa masih lemah untuk kelompok penyakit lain yang beragam. |

Pada label H, Weighted BCE menemukan 7 dari 15 kasus positif dan melewatkan 8 kasus. BCE standar hanya menemukan 3 dari 15 kasus. Recall H meningkat dari 0,20 menjadi 0,4667, tetapi precision turun dari 0,75 menjadi 0,3043 karena Weighted BCE menghasilkan 16 prediksi positif H yang salah. Hasil ini menunjukkan bahwa pemberian bobot membantu model lebih peka terhadap kelas langka, tetapi dapat membuat model terlalu sering memberikan prediksi positif.

### Perbandingan dengan BCE standar

| Metrik test | BCE | Weighted BCE | Hasil lebih baik |
|---|---:|---:|---|
| Macro-F1 | 0,5955 | 0,5802 | BCE |
| Micro-F1 | 0,5827 | 0,5525 | BCE |
| Macro-AUROC | 0,8544 | 0,8374 | BCE |
| Hamming loss | 0,1357 | 0,1574 | BCE, karena lebih rendah |
| Subset accuracy | 0,3638 | 0,2686 | BCE |
| F1 label H | 0,3158 | 0,3684 | Weighted BCE |
| Recall label H | 0,2000 | 0,4667 | Weighted BCE |

Training loss Weighted BCE turun dari sekitar 1,0139 pada epoch pertama menjadi 0,0923 pada epoch 28, sedangkan validation loss meningkat hingga sekitar 1,4883. Nilai loss Weighted BCE tidak boleh dibandingkan langsung dengan nilai loss BCE karena keduanya memakai skala pembobotan yang berbeda. Pola training dan validation menunjukkan kecenderungan overfitting setelah checkpoint terbaik pada epoch 21.

### Kesimpulan Weighted BCE

Weighted BCE belum mengungguli BCE standar pada metrik test keseluruhan. Keunggulannya terlihat pada sensitivitas terhadap label H yang langka. Model menemukan lebih banyak kasus H, tetapi juga menghasilkan lebih banyak false positive. Hasil ini membuktikan bahwa penambahan bobot tidak otomatis meningkatkan seluruh metrik. Weighted BCE memberikan trade-off antara menemukan lebih banyak kasus langka dan menjaga ketepatan prediksi positif.
