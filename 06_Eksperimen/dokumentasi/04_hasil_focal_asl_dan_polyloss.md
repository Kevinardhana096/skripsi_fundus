# Hasil Focal Loss, ASL, dan PolyLoss

> Catatan status: angka rinci pada dokumen ini berasal dari studi pendahuluan resolusi 224. Ketiga loss telah memiliki run seed 42, 52, dan 62; ringkasan agregatnya terdapat pada `05_perbandingan_dan_kesimpulan.md`. Untuk protokol 512, ASL seed 42 sedang berjalan dan PolyLoss belum dijalankan.

## Hasil eksperimen Focal Loss

Focal Loss mengurangi pengaruh sampel yang sudah mudah diprediksi dan memusatkan pembelajaran pada sampel yang masih sulit. Eksperimen menggunakan `alpha=0,25` dan `gamma=2`.

| Ukuran | Hasil |
|---|---:|
| Epoch checkpoint | 30 |
| Validation Macro-F1, threshold 0,50 | 0,5329 |
| Validation Macro-F1, threshold per label | 0,5958 |
| Test Macro-F1 | 0,6012 |
| Test Micro-F1 | 0,5778 |
| Test Macro-AUROC | 0,8520 |
| Hamming loss | 0,1531 |
| Subset accuracy | 0,2514 |

Focal Loss menghasilkan rata-rata recall tujuh penyakit tertinggi, yaitu 0,6298. Model ini paling sensitif dalam menemukan kasus penyakit, terutama M dan O. Namun, sensitivitas tersebut juga meningkatkan false positive. Pada label O, model menemukan 116 dari 147 kasus positif, tetapi menghasilkan 203 false positive. Hal ini menurunkan Hamming loss dan subset accuracy.

## Hasil eksperimen Asymmetric Loss

Asymmetric Loss memberi tingkat fokus yang berbeda pada label positif dan negatif. Eksperimen menggunakan `gamma_neg=4`, `gamma_pos=1`, dan `clip=0,05`. Konfigurasi ini mengurangi pengaruh negatif yang mudah dan membantu model mempelajari label positif tanpa memberi tekanan yang sama pada seluruh contoh.

| Ukuran | Hasil |
|---|---:|
| Epoch checkpoint | 18 |
| Jumlah epoch yang dijalankan | 25 |
| Validation Macro-F1, threshold 0,50 | 0,5730 |
| Validation Macro-F1, threshold per label | 0,6156 |
| Test Macro-F1 | 0,6034 |
| Test Micro-F1 | 0,5867 |
| Test Macro-AUROC | 0,8511 |
| Hamming loss | 0,1395 |
| Subset accuracy | 0,3429 |

ASL memperoleh Test Macro-F1 tertinggi dan rata-rata F1 tujuh penyakit tertinggi. Keunggulannya berasal dari keseimbangan precision dan recall, bukan dari recall tertinggi pada setiap penyakit. ASL juga memperoleh F1 terbaik pada label H dan O.

## Hasil eksperimen PolyLoss

Eksperimen menggunakan Poly-1 Loss dengan `epsilon=1`. Fungsi ini menambahkan komponen koreksi polinomial pada BCE untuk mengubah tekanan pembelajaran terhadap probabilitas yang belum yakin.

| Ukuran | Hasil |
|---|---:|
| Epoch checkpoint | 13 |
| Jumlah epoch yang dijalankan | 20 |
| Validation Macro-F1, threshold 0,50 | 0,5416 |
| Validation Macro-F1, threshold per label | 0,5796 |
| Test Macro-F1 | 0,5788 |
| Test Micro-F1 | 0,5888 |
| Test Macro-AUROC | 0,8596 |
| Hamming loss | 0,1367 |
| Subset accuracy | 0,3562 |

PolyLoss memperoleh Test Micro-F1 dan Macro-AUROC tertinggi. Model ini juga hampir menyamai BCE pada Hamming loss dan subset accuracy. Namun, rata-rata F1 tujuh penyakit hanya 0,5715, terendah di antara lima loss. Hasil agregat PolyLoss baik, tetapi performanya belum merata pada G, A, H, dan O.
