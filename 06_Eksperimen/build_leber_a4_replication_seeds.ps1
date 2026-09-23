$ErrorActionPreference = "Stop"

$experimentRoot = Join-Path $PSScriptRoot "Baseline Bilateral ResNet50 512"
$a4Root = Join-Path $experimentRoot "05_LEBER_Ablation\A4_LabelWise_Router"
$readyDir = Join-Path $a4Root "Notebooks\Ready"
$sourcePath = Join-Path $readyDir "leber_a4_labelwise_router_resnet50_bce_seed42_ready.ipynb"

if (-not (Test-Path $sourcePath)) {
    throw "Notebook sumber tidak ditemukan di: $sourcePath"
}

$seeds = @(52, 62)

foreach ($seed in $seeds) {
    $notebook = Get-Content -Raw -LiteralPath $sourcePath | ConvertFrom-Json
    
    foreach ($cell in $notebook.cells) {
        $source = $cell.source -join ""
        $source = $source.Replace("Seed 42", "Seed $seed")
        $source = $source.Replace("SEED = 42", "SEED = $seed")
        $source = $source.Replace('"seed": 42', "`"seed`": $seed")
        $source = $source.Replace("seed42", "seed$seed")
        $cell.source = @($source)

        if ($cell.cell_type -eq "code") {
            $cell.outputs = @()
            $cell.execution_count = $null
            if ($cell.PSObject.Properties.Name -contains "metadata") {
                $cell.metadata = [pscustomobject]@{}
            }
        }
    }

    $outputPath = Join-Path $readyDir "leber_a4_labelwise_router_resnet50_bce_seed$($seed)_ready.ipynb"
    $jsonContent = $notebook | ConvertTo-Json -Depth 100
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText($outputPath, $jsonContent, $utf8NoBom)
    Write-Output "Berhasil membuat notebook replikasi: $outputPath"
}

Write-Output "Seluruh notebook replikasi LEBER A4 (Seed 52 dan Seed 62) berhasil dibangun!"
