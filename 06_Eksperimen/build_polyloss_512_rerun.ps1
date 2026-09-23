$ErrorActionPreference = "Stop"

$root = Join-Path $PSScriptRoot "Baseline Bilateral ResNet50 512\03_PolyLoss"
$executedDir = Join-Path $root "Notebooks\Executed"
$readyDir = Join-Path $root "Notebooks\Ready"

New-Item -ItemType Directory -Path $readyDir -Force | Out-Null

foreach ($seed in @(52, 62)) {
    $sourcePath = Join-Path $executedDir "polyloss_seed$($seed)_executed.ipynb"
    $outputPath = Join-Path $readyDir "polyloss_seed$($seed)_rerun1_ready.ipynb"

    if (-not (Test-Path -LiteralPath $sourcePath)) {
        throw "Notebook sumber tidak ditemukan: $sourcePath"
    }

    $notebook = Get-Content -Raw -LiteralPath $sourcePath | ConvertFrom-Json

    foreach ($cell in $notebook.cells) {
        $source = $cell.source -join ""
        $source = $source.Replace("seed$seed", "seed$($seed)_rerun1")
        $source = $source.Replace("Seed $seed", "Seed $seed - Rerun 1")
        $cell.source = @($source)

        if ($cell.cell_type -eq "code") {
            $cell.outputs = @()
            $cell.execution_count = $null

            if ($cell.PSObject.Properties.Name -contains "metadata") {
                $cell.metadata = [pscustomobject]@{}
            }
        }
    }

    $notebook | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath $outputPath -Encoding utf8
    Write-Output $outputPath
}
