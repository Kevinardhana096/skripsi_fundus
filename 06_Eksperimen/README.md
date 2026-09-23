# Eksperimen ODIR-5K

Folder ini menyimpan pipeline, artefak, notebook, dan hasil eksperimen klasifikasi multi-label ODIR-5K dengan ResNet50. Perbandingan fungsi loss menjadi studi pendahuluan untuk memilih konfigurasi loss pada pengembangan metode bilateral LEBER.

## Dokumentasi

1. [Dataset dan pembagian data](dokumentasi/01_dataset_dan_split.md) menjelaskan delapan label, unit pasien, bentuk data, manifest, dan patient-level split.
2. [Pipeline model dan fungsi loss](dokumentasi/02_pipeline_model_dan_fungsi_loss.md) menjelaskan alur shared ResNet50, flowchart, logits, sigmoid, serta cara kerja BCE, Weighted BCE, Focal Loss, ASL, dan PolyLoss.
3. [Hasil BCE dan Weighted BCE](dokumentasi/03_hasil_bce_dan_weighted_bce.md) memuat konfigurasi, metrik test, hasil per label, dan interpretasi dua baseline.
4. [Hasil Focal Loss, ASL, dan PolyLoss](dokumentasi/04_hasil_focal_asl_dan_polyloss.md) memuat konfigurasi dan hasil tiga fungsi loss lanjutan.
5. [Perbandingan dan kesimpulan eksperimen](dokumentasi/05_perbandingan_dan_kesimpulan.md) memuat perbandingan lima loss, analisis enam penyakit spesifik, hasil setiap label, dan kesimpulan studi pendahuluan.
6. [Rencana eksperimen LEBER](dokumentasi/06_rencana_eksperimen_leber.md) memuat arsitektur, ablation study, pengujian pertukaran input, metrik, dan kriteria keberhasilan metode utama.

## Folder utama

| Folder atau file | Isi |
|---|---|
| `artifacts/` | Manifest pasien, laporan pemeriksaan, dan pembagian train, validation, serta test |
| `scripts/` | Skrip penyusunan manifest dan split |
| `BCE ResNet50/` | Notebook, checkpoint, dan hasil BCE |
| `Weighted BCE ResNet50/` | Notebook, checkpoint, dan hasil Weighted BCE |
| `Focal Loss ResNet50/` | Notebook, checkpoint, dan hasil Focal Loss |
| `ASL ResNet50/` | Notebook, checkpoint, dan hasil ASL |
| `PolyLoss ResNet50/` | Notebook, checkpoint, dan hasil PolyLoss |
| `Baseline Bilateral ResNet50 512/` | Notebook dan artefak konfirmasi BCE, ASL, dan PolyLoss pada resolusi 512 |
| `requirements_manifest.txt` | Dependensi untuk pipeline manifest |

## Status

Kelima fungsi loss pada resolusi 224 telah menjalani training, validation, dan testing menggunakan pembagian pasien yang sama pada seed 42, 52, dan 62. Totalnya 15 run dan menjadi studi pendahuluan. Tahap aktif adalah konfirmasi BCE, ASL, dan PolyLoss pada baseline bilateral 512. BCE 512 seed 42 telah selesai dengan Test Macro-F1 0,6122; ASL 512 seed 42 sedang berjalan; PolyLoss 512 belum dijalankan. Setelah loss dikunci berdasarkan validation dan kestabilan seed, eksperimen dilanjutkan ke LEBER A0-A6.
