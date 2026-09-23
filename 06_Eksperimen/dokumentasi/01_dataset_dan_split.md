# Dataset dan Pembagian Data

## Penjelasan dataset dan delapan label ODIR-5K

ODIR-5K merupakan dataset citra fundus untuk mengenali kondisi kesehatan mata. Citra fundus adalah foto bagian belakang mata yang memperlihatkan retina, pembuluh darah, makula, dan saraf optik. Bagian-bagian tersebut dapat menunjukkan tanda suatu penyakit.

Satu data pasien terdiri dari citra fundus mata kiri, citra fundus mata kanan, dan label kondisi mata pasien. Kedua citra digunakan bersama karena kondisi pada mata kiri dan kanan dapat berbeda, tetapi tetap berasal dari pasien yang sama.

Model memprediksi delapan label berikut:

| Kode | Nama label | Arti sederhana |
|---|---|---|
| N | Normal | Tidak ditemukan tanda penyakit mata yang termasuk kategori dataset. |
| D | Diabetes | Terdapat tanda gangguan mata akibat diabetes, terutama retinopati diabetik. |
| G | Glaucoma | Terdapat tanda kerusakan saraf optik yang berkaitan dengan glaukoma. |
| C | Cataract | Lensa mata mengalami kekeruhan atau katarak. |
| A | Age-related Macular Degeneration | Terdapat gangguan pada makula yang berkaitan dengan pertambahan usia. |
| H | Hypertension | Terdapat perubahan pada pembuluh darah retina yang berkaitan dengan tekanan darah tinggi. |
| M | Pathological Myopia | Rabun jauh berat telah menyebabkan perubahan atau kerusakan pada struktur mata. |
| O | Other diseases | Terdapat penyakit atau kelainan mata lain yang tidak termasuk enam kelompok penyakit utama. |

Penelitian ini merupakan klasifikasi multi-label. Artinya, model tidak hanya memilih satu kelas untuk seorang pasien. Model membuat delapan keputusan terpisah, yaitu menentukan apakah setiap label ada atau tidak ada. Nilai 1 berarti label tersebut ada, sedangkan nilai 0 berarti tidak ada.

Sebagai contoh, target `[0, 1, 0, 1, 0, 0, 0, 0]` berarti pasien memiliki label D dan C secara bersamaan, yaitu gangguan mata akibat diabetes dan katarak. Kondisi seperti ini dapat terjadi karena satu pasien dapat mengalami lebih dari satu penyakit.

Label N menunjukkan kondisi normal, sehingga secara konsep label ini tidak seharusnya aktif bersamaan dengan label penyakit. Sementara itu, beberapa label penyakit dapat aktif secara bersamaan. Karena itu, keluaran model terdiri dari delapan nilai probabilitas, bukan satu pilihan kelas saja.

Kalimat yang dapat digunakan saat presentasi:

> Delapan label pada ODIR-5K mewakili kondisi normal, diabetes, glaukoma, katarak, degenerasi makula terkait usia, hipertensi, miopia patologis, dan penyakit lainnya. Karena seorang pasien dapat mengalami lebih dari satu kondisi sekaligus, model membuat keputusan positif atau negatif untuk setiap label.

## Unit data dan keluaran tingkat pasien

Satu unit data dalam penelitian ini adalah satu pasien, bukan satu citra. Setiap pasien memiliki satu citra fundus mata kiri, satu citra fundus mata kanan, dan satu vektor berisi delapan label.

| Komponen | Contoh | Fungsi |
|---|---|---|
| `patient_id` | `4` | Identitas untuk memasangkan citra dan mencegah kebocoran antar-subset; tidak masuk ke model |
| `left_image` | `4_left.jpg` | Masukan citra fundus mata kiri |
| `right_image` | `4_right.jpg` | Masukan citra fundus mata kanan |
| Target | `[0,1,0,0,0,0,0,1]` | Jawaban benar untuk urutan N, D, G, C, A, H, M, O |

Target contoh tersebut berarti pasien memiliki D dan O secara bersamaan. Bentuk ini disebut multi-label karena model membuat keputusan positif atau negatif untuk setiap label. Berbeda dengan klasifikasi multi-class, model tidak dipaksa memilih tepat satu kelas.

Label N menunjukkan kondisi normal dan secara konsep tidak aktif bersama label penyakit. Label O menampung penyakit atau abnormalitas lain yang tidak termasuk enam penyakit spesifik. O dapat berdiri sendiri atau muncul bersama label penyakit lain.

Model menerima kedua citra dan menghasilkan prediksi pada tingkat pasien. Keluaran model bukan diagnosis terpisah untuk mata kiri dan mata kanan. Model dapat memprediksi bahwa seorang pasien memiliki D dan C, tetapi keluarannya tidak menentukan apakah D terdapat pada mata kiri, mata kanan, atau keduanya. Hal yang sama berlaku untuk C dan label lain. Ini merupakan batasan penting penelitian dan harus dinyatakan ketika menjelaskan hasil.

Kolom yang menjadi masukan model adalah `left_image` dan `right_image`. Delapan kolom label digunakan sebagai target saat training. `patient_id`, `split`, `label_count`, `is_multilabel`, `left_exists`, dan `right_exists` membantu pengelolaan serta pemeriksaan data, tetapi tidak diberikan sebagai fitur kepada ResNet50.

Pada studi pendahuluan 224, bentuk satu data adalah `[3,224,224]` untuk setiap mata. Pada protokol utama terbaru, bentuk satu data adalah citra kiri `[3,512,512]`, citra kanan `[3,512,512]`, dan target `[8]`. Dengan batch size 16, bentuknya menjadi citra kiri `[16,3,512,512]`, citra kanan `[16,3,512,512]`, dan target `[16,8]`.

Pembagian data harus dilakukan berdasarkan `patient_id`. Kedua citra milik pasien yang sama harus selalu berada pada subset yang sama. Aturan ini mencegah model melihat satu mata saat training lalu diuji menggunakan mata lain dari pasien yang sama.

## Tahap pertama

Jalankan `scripts/build_patient_manifest.py` untuk membentuk satu baris data
per pasien. Manifest akan memasangkan citra mata kiri dan kanan, menyimpan
delapan label, serta memeriksa keberadaan semua citra.

Contoh penggunaan lokal:

```powershell
python scripts/build_patient_manifest.py \
  --excel "../03_Data_ODIR5K/ODIR_5K/ODIR-5K/ODIR-5K/data.xlsx" \
  --images-dir "../03_Data_ODIR5K/ODIR_5K/ODIR-5K/ODIR-5K/Training Images" \
  --output-dir artifacts
```

Output yang diharapkan:

- `artifacts/patient_manifest.csv`: satu baris per pasien untuk pipeline model.
- `artifacts/manifest_report.json`: ringkasan pemeriksaan data dan distribusi label.

Data test hanya digunakan pada evaluasi akhir. Parameter model dan threshold
tidak boleh ditentukan menggunakan data test.

## Tahap kedua

Setelah manifest valid, buat patient-level split 70/15/15 dengan skrip make_patient_splits.py. Masukan: artifacts/patient_manifest.csv. Keluaran: artifacts/splits. Gunakan seed 42.

Skrip menggunakan iterative multi-label stratification, yaitu pembagian yang berupaya menjaga proporsi delapan label di train, validation, dan test. Skrip juga menghentikan proses apabila satu pasien muncul pada lebih dari satu subset.
