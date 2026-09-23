$ErrorActionPreference = "Stop"

$scriptRoot = $PSScriptRoot
$projectRoot = Split-Path $scriptRoot -Parent
$generatorScript = Join-Path $projectRoot "tmp\generate_test_eval_notebook.py"

if (-not (Test-Path $generatorScript)) {
    throw "Skrip generator tidak ditemukan di: $generatorScript"
}

Write-Output "Menjalankan skrip generator notebook evaluasi final..."
python $generatorScript

$outputPath = Join-Path $scriptRoot "Baseline Bilateral ResNet50 512\05_LEBER_Ablation\A4_LabelWise_Router\Notebooks\Ready\leber_a4_final_test_evaluation_ready.ipynb"

if (-not (Test-Path $outputPath)) {
    throw "Gagal menemukan notebook keluaran di: $outputPath"
}

# Verifikasi sintaks dan integritas JSON
try {
    $content = Get-Content -Raw -LiteralPath $outputPath
    $jsonObj = $content | ConvertFrom-Json
    $cellCount = $jsonObj.cells.Count
    Write-Output "Verifikasi Berhasil: Notebook adalah JSON valid dengan $cellCount cells."
}
catch {
    throw "Gagal memverifikasi integritas JSON notebook: $_"
}

Write-Output "Notebook Evaluasi Akhir Test Set LEBER A4 (525 Pasien) siap digunakan!"
Write-Output "Lokasi: $outputPath"
