$ErrorActionPreference = "Stop"

$experimentRoot = Join-Path $PSScriptRoot "Baseline Bilateral ResNet50 512"
$sourcePath = Join-Path $experimentRoot "01_BCE\Notebooks\Executed\bce_seed42_executed.ipynb"
$pilotRoot = Join-Path $experimentRoot "04_Backbone_Control_EfficientNetB2"
$readyDir = Join-Path $pilotRoot "Notebooks\Ready"
$executedDir = Join-Path $pilotRoot "Notebooks\Executed"
$resultsDir = Join-Path $pilotRoot "Results"
$outputPath = Join-Path $readyDir "efficientnetb2_bce_seed42_pilot_ready.ipynb"

foreach ($directory in @($readyDir, $executedDir, $resultsDir)) {
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
}

$notebook = Get-Content -Raw -LiteralPath $sourcePath | ConvertFrom-Json

foreach ($cell in $notebook.cells) {
    $source = $cell.source -join ""

    $source = $source.Replace(
        "Baseline Bilateral ResNet50 512 x 512 - BCE - Seed 42",
        "Backbone Control EfficientNet-B2 Bilateral 512 x 512 - BCE - Seed 42"
    )
    $source = $source.Replace(
        "Pilot resolusi 512 dengan shared backbone, batch fisik 16, mixed precision, dan split pasien yang telah dikunci.",
        "Kontrol backbone EfficientNet-B2 dengan fusi concatenation, BCE, resolusi 512, batch fisik 16, mixed precision, dan split pasien yang sama."
    )
    $source = $source.Replace(
        "best_bilateral_bce_resnet50_512_seed42.pt",
        "best_bilateral_efficientnetb2_bce_512_seed42.pt"
    )
    $source = $source.Replace(
        "bilateral_bce_512_seed42",
        "bilateral_efficientnetb2_bce_512_seed42"
    )
    $source = $source.Replace(
        "from torchvision.models import resnet50, ResNet50_Weights",
        "from torchvision.models import efficientnet_b2, EfficientNet_B2_Weights"
    )
    $source = $source.Replace(
        "from torchvision.models import resnet50",
        "from torchvision.models import efficientnet_b2"
    )
    $source = $source.Replace("SharedResNet50", "SharedEfficientNetB2")
    $source = $source.Replace("ResNet50_Weights.IMAGENET1K_V2", "EfficientNet_B2_Weights.IMAGENET1K_V1")
    $source = $source.Replace("resnet50(weights=weights)", "efficientnet_b2(weights=weights)")
    $source = $source.Replace("resnet50(`n            weights=None`n        )", "efficientnet_b2(`n            weights=None`n        )")
    $source = $source.Replace("resnet50(weights=None)", "efficientnet_b2(weights=None)")
    $source = $source.Replace("self.backbone.fc.in_features", "self.backbone.classifier[1].in_features")
    $source = $source.Replace("self.backbone.fc = nn.Identity()", "self.backbone.classifier = nn.Identity()")
    $source = $source.Replace('"backbone": "shared_resnet50"', '"backbone": "shared_efficientnet_b2"')
    $source = $source.Replace("Hasil final test set, BCE baseline", "Hasil final test set, EfficientNet-B2 BCE backbone control")

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
