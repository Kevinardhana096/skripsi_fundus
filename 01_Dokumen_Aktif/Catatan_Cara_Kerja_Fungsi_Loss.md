# Catatan Cara Kerja Fungsi Loss

## Ringkasan

Fungsi loss adalah aturan untuk menghitung seberapa jauh prediksi model dari label yang benar. Fungsi loss tidak melihat citra atau menentukan diagnosis secara langsung. Model menghasilkan prediksi, kemudian fungsi loss memberikan sinyal kesalahan agar bobot model dapat diperbaiki.

```text
Citra mata kiri dan kanan
          |
          v
Model menghasilkan delapan logit
          |
          v
Sigmoid mengubah logit menjadi probabilitas 0-1
          |
          v
Probabilitas dibandingkan dengan label asli
          |
          v
Fungsi loss menghitung kesalahan
          |
          v
Backpropagation menghitung gradient
          |
          v
AdamW memperbarui bobot model
```

Analogi sederhananya:

- model adalah murid yang menjawab soal;
- label asli adalah kunci jawaban;
- fungsi loss adalah guru yang menghitung kesalahan;
- gradient adalah petunjuk bagian yang perlu diperbaiki;
- AdamW adalah mekanisme yang mengubah bobot;
- satu epoch berarti seluruh data training telah dipelajari satu kali.

## Logit dan probabilitas

Logit merupakan nilai mentah keluaran model. Logit kemudian diubah menjadi probabilitas menggunakan sigmoid.

```text
p = 1 / (1 + exp(-z))
```

- `z`: logit;
- `p`: probabilitas prediksi.

Karena tugasnya multi-label, setiap label dihitung sebagai keputusan biner yang terpisah. Seorang pasien dapat memiliki lebih dari satu label positif secara bersamaan.

## Binary Cross-Entropy (BCE)

```text
BCE = -[y * log(p) + (1-y) * log(1-p)]
```

- `y`: label asli, yaitu 0 atau 1;
- `p`: probabilitas prediksi.

Jika label asli 1, model diharapkan menghasilkan probabilitas mendekati 1. Jika label asli 0, probabilitasnya diharapkan mendekati 0. Model yang sangat yakin pada jawaban yang salah memperoleh loss besar. BCE sederhana dan cocok sebagai baseline, tetapi memperlakukan semua label menggunakan aturan yang sama.

## Weighted BCE

```text
Weighted BCE = -[w * y * log(p) + (1-y) * log(1-p)]
```

`w` adalah bobot kelas positif. Label dengan contoh positif lebih sedikit memperoleh bobot lebih besar. Tujuannya agar penyakit langka tidak diabaikan. Namun, bobot terlalu besar dapat membuat model terlalu sering memberikan prediksi positif: recall dapat naik, sementara precision menurun.

## Focal Loss

```text
Focal Loss = -(1-p_t)^gamma * log(p_t)
```

- `p_t`: probabilitas terhadap jawaban yang benar;
- `gamma`: kekuatan fokus terhadap contoh sulit.

Contoh yang sudah diprediksi dengan mudah mendapat pengaruh kecil. Contoh yang masih salah atau meragukan mendapat pengaruh lebih besar. Dengan kata lain, model mengurangi waktu belajar pada soal mudah dan berfokus pada soal sulit.

## Asymmetric Loss (ASL)

ASL dirancang untuk klasifikasi multi-label yang memiliki jauh lebih banyak label negatif daripada positif. ASL menggunakan tingkat fokus berbeda untuk sisi positif dan negatif, serta dapat menggunakan probability clipping.

Negatif yang sangat mudah, misalnya label asli 0 dengan prediksi 0,01, dikurangi pengaruhnya. Negatif yang sulit, misalnya label asli 0 tetapi prediksi 0,80, tetap dihukum. Dengan demikian, banyaknya negatif mudah tidak menenggelamkan pembelajaran label positif.

## PolyLoss

```text
PolyLoss = loss dasar + epsilon * (1-p_t)
```

- `loss dasar`: fungsi loss utama yang digunakan;
- `p_t`: probabilitas terhadap jawaban yang benar;
- `epsilon`: besar koreksi tambahan.

Jika keyakinan terhadap jawaban benar masih rendah, koreksi menjadi lebih besar. Hasilnya bergantung pada loss dasar dan nilai parameter koreksi.

## Perbandingan

| Fungsi loss | Fokus utama | Penjelasan sederhana |
|---|---|---|
| BCE | Semua kesalahan | Semua kesalahan dinilai dengan aturan yang sama |
| Weighted BCE | Positif yang langka | Kesalahan pada penyakit langka diberi bobot lebih besar |
| Focal Loss | Contoh sulit | Contoh mudah dikurangi dan contoh sulit diperhatikan |
| ASL | Ketidakseimbangan positif-negatif | Gangguan negatif mudah dikurangi agar positif tidak tenggelam |
| PolyLoss | Koreksi loss dasar | Loss dasar diberi komponen koreksi tambahan |

## Dari loss menuju pembaruan model

Backpropagation menggunakan loss untuk menghitung gradient. Gradient menunjukkan arah dan besar perubahan yang dibutuhkan oleh bobot model. AdamW melakukan pembaruannya.

```text
bobot baru = bobot lama - learning_rate * gradient
```

Fungsi loss menentukan bentuk sinyal kesalahan, backpropagation membawa sinyal tersebut ke jaringan, dan optimizer melakukan perubahan bobot.

## Training loss dan validation loss

Training loss dihitung pada data yang digunakan untuk memperbarui bobot. Validation loss dihitung pada data yang tidak digunakan dalam pembaruan bobot.

Jika training loss terus turun tetapi validation loss naik, model kemungkinan mengalami overfitting: model semakin baik pada data training, tetapi kemampuannya menghadapi pasien baru menurun. Oleh karena itu, checkpoint terbaik dipilih berdasarkan performa validasi, terutama Macro-F1, bukan hanya training loss paling kecil atau epoch terakhir.

## Kesimpulan

Fungsi loss bukan pendeteksi penyakit. Fungsi loss menentukan kesalahan mana yang lebih penting selama proses belajar. Model dan dataset yang sama dapat menghasilkan performa berbeda karena setiap loss memberikan tekanan belajar yang berbeda.

Eksperimen fungsi loss pada penelitian ini merupakan studi pendahuluan untuk memilih konfigurasi optimasi bagi metode utama. Kesimpulan tetap harus mempertimbangkan Macro-F1, hasil per label, validation dan test set, serta kestabilan pada beberapa seed.
