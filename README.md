# Skripsi Fundus: Klasifikasi Penyakit Mata Multi-Label (ODIR-5K)

Repository ini berisi dokumen skripsi, catatan penelitian, skrip eksperimen, notebook, dan artefak evaluasi untuk penelitian klasifikasi penyakit mata multi-label pada citra fundus bilateral berbasis dataset ODIR-5K.

## Ringkasan Proyek

- **Objek Penelitian**: Klasifikasi multi-label penyakit mata berbasis citra fundus bilateral (kedua mata: kiri & kanan).
- **Dataset**: ODIR-5K (Ocular Disease Intelligent Recognition 5000).
- **Metode**: 
  - Studi pendahuluan fungsi loss (BCE, Weighted BCE, Focal Loss, Asymmetric Loss / ASL, PolyLoss).
  - Eksperimen baseline bilateral resolusi 512.
  - Pengembangan dan ablasi arsitektur **LEBER** (*Label-wise Expert Bilateral Examination and Reasoning*).

## Struktur Repositori

| Direktori / Berkas | Deskripsi |
|---|---|
| `01_Dokumen_Aktif/` | Naskah aktif skripsi (Bab 1 s.d. Bab 5) dan draf terkait |
| `02_Arsip_Revisi/` | Arsip revisi dan draf naskah sebelumnya |
| `04_Referensi/` | Dokumen rujukan, literatur paper, dan kajian pustaka |
| `05_Aset/` | Visualisasi arsitektur, diagram alur, dan heatmap LayerCAM |
| `06_Eksperimen/` | Pipeline kode, skrip otomatisasi (`.ps1`), notebook Colab/Jupyter (`.ipynb`), dan ringkasan metrik |
| `Catatan Hasil Eksperimen.md` | Catatan komparasi performa metrik antar model dan loss |
| `AGENTS.md` | Panduan formatting dan aturan instruksi agen |

> **Catatan**: Berkas dataset mentah (`03_Data_ODIR5K/`) dan berkas bobot model berukuran besar (`*.pt`, `*.pth`, `*.zip`) dikecualikan dari pelacakan git via `.gitignore` karena batasan ukuran berkas.
