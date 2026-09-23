$ErrorActionPreference = "Stop"

$experimentDir = Join-Path $PSScriptRoot "Baseline Bilateral ResNet50 512"
$experiments = @(
    @{
        Name = "bce"
        Source = "01_BCE\Notebooks\Executed\bce_seed42_executed.ipynb"
        OutputDir = "01_BCE\Notebooks\Ready"
        OutputPrefix = "bce"
        RequiredLoss = "nn.BCEWithLogitsLoss()"
        ForbiddenLoss = "AsymmetricLoss"
    },
    @{
        Name = "asl"
        Source = "02_ASL\Notebooks\Executed\asl_seed42_executed.ipynb"
        OutputDir = "02_ASL\Notebooks\Ready"
        OutputPrefix = "asl"
        RequiredLoss = "AsymmetricLoss"
        ForbiddenLoss = "Poly1Loss"
    }
)

foreach ($experiment in $experiments) {
    $sourcePath = Join-Path $experimentDir $experiment.Source
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

        $allCode = (
            $notebook.cells |
            Where-Object cell_type -eq "code" |
            ForEach-Object { $_.source -join "" }
        ) -join "`n"

        if (-not $allCode.Contains($experiment.RequiredLoss)) {
            throw "Loss wajib tidak ditemukan untuk $($experiment.Name) seed $seed"
        }

        if ($allCode.Contains($experiment.ForbiddenLoss)) {
            throw "Loss yang tidak sesuai ditemukan untuk $($experiment.Name) seed $seed"
        }

        $destinationDir = Join-Path $experimentDir $experiment.OutputDir
        $outputPath = Join-Path $destinationDir "$($experiment.OutputPrefix)_seed$($seed)_ready.ipynb"
        $notebook | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath $outputPath -Encoding utf8
        Write-Output $outputPath
    }
}
