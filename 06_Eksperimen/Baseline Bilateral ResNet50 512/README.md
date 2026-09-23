# Baseline Bilateral ResNet50 512

Folder ini menyimpan eksperimen klasifikasi multi-label tingkat pasien dengan pasangan citra fundus kiri-kanan, shared ResNet50, dan resolusi 512 x 512.

## Struktur

- `01_BCE/`
  - `Notebooks/Executed/`: notebook BCE yang telah selesai dijalankan.
  - `Notebooks/Ready/`: notebook BCE yang siap diimpor ke Kaggle.
  - `Results/`: checkpoint dan metrik BCE untuk setiap seed.
- `02_ASL/`
  - `Notebooks/Executed/`: notebook ASL yang telah selesai dijalankan.
  - `Notebooks/Ready/`: notebook ASL yang siap diimpor ke Kaggle.
  - `Results/`: checkpoint dan metrik ASL untuk setiap seed.
- `03_PolyLoss/`
  - `Notebooks/Executed/`: notebook PolyLoss yang telah selesai dijalankan.
  - `Notebooks/Ready/`: notebook PolyLoss yang belum dijalankan, jika ada.
  - `Results/`: checkpoint dan metrik PolyLoss untuk setiap seed.
- `04_Backbone_Control_EfficientNetB2/`
  - `Notebooks/Ready/`: notebook pilot EfficientNet-B2 bilateral dengan BCE.
  - `Notebooks/Executed/`: notebook pilot yang telah selesai dijalankan.
  - `Results/`: artefak hasil kontrol backbone EfficientNet-B2.
- `05_LEBER_Ablation/`
  - `A1_Symmetric/Notebooks/Ready/`: notebook A1 dengan fitur bilateral simetris.
  - `A1_Symmetric/Results/`: checkpoint, metrik validation, threshold, dan audit swap A1.

## Status eksperimen

| Fungsi loss | Seed 42 | Seed 52 | Seed 62 |
|---|---|---|---|
| BCE | Selesai | Selesai | Selesai |
| ASL | Selesai | Selesai | Selesai |
| PolyLoss | Selesai | Selesai; rerun 1 terverifikasi identik | Selesai; rerun 1 terverifikasi identik |

## Kontrol backbone

| Backbone | Loss | Seed | Status |
|---|---|---:|---|
| ResNet50 | BCE | 42 | Selesai |
| EfficientNet-B2 | BCE | 42 | Selesai; hasil campuran, perlu seed 52/62 untuk keputusan final |

## Ablation LEBER

| ID | Konfigurasi | Status |
|---|---|---|
| A0 | Shared ResNet50, concatenation, BCE | Selesai, tiga seed |
| A1 | Shared ResNet50, fitur simetris, BCE | Selesai, seed 42; validation Macro-F1 optimal 0,6596; swap invariant sempurna |
| A2-A6 | Expert, router, supervisi, dan exchange equivariance | Belum dijalankan |

## Aturan penyimpanan

- Notebook hasil unduhan Kaggle masuk ke `Notebooks/Executed/`.
- Notebook yang belum dijalankan masuk ke `Notebooks/Ready/`.
- Seluruh folder output Kaggle masuk ke `Results/` tanpa mengubah isi artefaknya.
- Jangan memilih loss hanya dari satu seed; gunakan rata-rata dan standar deviasi tiga seed.
