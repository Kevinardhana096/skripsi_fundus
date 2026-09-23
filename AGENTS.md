# Antigravity UI Compatibility Rules

## 1. Matematika & Formula (Anti-LaTeX)
DILARANG menggunakan sintaks LaTeX berat seperti `$...$`, `$$...$$`, `\frac{}{}`, `\sqrt{}`, atau `\sum`. Karena UI chat Antigravity tidak merender KaTeX/LaTeX, gunakan format Unicode atau notasi teks standar yang mudah dibaca:
- Gunakan simbol Unicode untuk operator: × (perkalian), ÷ (pembagian), ±, ≠, ≤, ≥, √x.
- Gunakan superscript/subscript Unicode jika memungkinkan: x², y³, H₂O, aₙ.
- Untuk rumus kompleks atau pecahan, gunakan notasi inline bergaya pemrograman atau teks biasa yang jelas.
  * *Contoh Buruk:* \(\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}\)
  * *Contoh Bagus:* x = (-b ± √(b² - 4ac)) / (2a)

## 2. Diagram & Arsitektur (Anti-Mermaid/PlantUML)
DILARANG membuat diagram menggunakan blok kode `mermaid` atau `plantuml` karena akan terhenti di teks mentah. Sebagai gantinya:
- Gunakan **ASCII Art / Box-drawing characters** (─, │, ┌, ┐, └, ┘, ├, ┤, ┬, ┴, ┼, ▲, ▼, ►, ◄) untuk alur sederhana.
- Gunakan **Indented Bullet Lists** (daftar berpoin berundak) untuk menggambarkan hierarki atau pohon keputusan yang kompleks agar tetap rapi secara visual.

## 3. Struktur Output Umum
- Maksimalkan penggunaan tabel Markdown standar (`| kolom |`) karena tabel dasar biasanya masih didukung dengan baik oleh parser Markdown Antigravity.
- Gunakan format cetak tebal (**bold**) sebagai penanda visual penting untuk memecah teks yang panjang.

## 4. Ilustrasi & Gambar Visual (Jika Diminta)
Jika pengguna meminta gambar ilustrasi, diagram visual, bagan alur grafis, atau infografis:
- **Generate Gambar Secara Nyata**: Jangan hanya memberikan deskripsi teks atau ASCII art jika pengguna secara eksplisit meminta gambar/ilustrasi.
- **Metode Pembuatan**:
  * Untuk **diagram teknis, alur proses (flowchart), arsitektur model, atau visualisasi data**: Buat skrip (misalnya Python menggunakan `matplotlib` / `seaborn` / `PIL`) dengan rendering berkualitas tinggi (DPI 300), tipografi rapi, dan estetika visual modern.
  * Untuk **ilustrasi konseptual atau aset grafis**: Gunakan tool `generate_image` yang tersedia.
- **Penyimpanan & Tautan**: Simpan gambar ke direktori aset (misalnya `05_Aset/` atau folder terkait proyek), lalu berikan tautan / sematkan gambar di respon agar pengguna dapat melihat dan menggunakannya langsung dalam dokumen atau naskah skripsi.
