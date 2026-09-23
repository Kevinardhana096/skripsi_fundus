$ErrorActionPreference = "Stop"

$sourcePath = Join-Path $PSScriptRoot "Baseline Bilateral ResNet50 512\03_PolyLoss\Notebooks\Executed\polyloss_seed42_executed.ipynb"
$outputDir = Join-Path $PSScriptRoot "Baseline Bilateral ResNet50 512\03_PolyLoss\Notebooks\Ready"
$sourceNotebook = Get-Content -Raw -LiteralPath $sourcePath | ConvertFrom-Json

foreach ($seed in @(52, 62)) {
    $notebook = $sourceNotebook | ConvertTo-Json -Depth 100 | ConvertFrom-Json

    foreach ($cell in $notebook.cells) {
        $source = $cell.source -join ""
        $source = $source.Replace("Seed 42", "Seed $seed")
        $source = $source.Replace("SEED = 42", "SEED = $seed")
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

    $outputPath = Join-Path $outputDir "polyloss_seed$($seed)_ready.ipynb"
    $notebook | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath $outputPath -Encoding utf8
    Write-Output $outputPath
}
