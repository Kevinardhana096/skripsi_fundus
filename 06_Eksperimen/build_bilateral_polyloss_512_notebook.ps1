$ErrorActionPreference = "Stop"

$sourcePath = Join-Path $PSScriptRoot "Baseline Bilateral ResNet50 512\01_BCE\Notebooks\Executed\bce_seed42_executed.ipynb"
$outputDir = Join-Path $PSScriptRoot "Baseline Bilateral ResNet50 512\03_PolyLoss\Notebooks\Ready"
$outputPath = Join-Path $outputDir "polyloss_seed42_ready.ipynb"

$notebook = Get-Content -Raw -LiteralPath $sourcePath | ConvertFrom-Json

foreach ($cell in $notebook.cells) {
    $source = $cell.source -join ""
    $source = $source.Replace("Baseline Bilateral ResNet50 512 x 512 - BCE - Seed 42", "Baseline Bilateral ResNet50 512 x 512 - Poly-1 Loss - Seed 42")
    $source = $source.Replace("Pilot resolusi 512 dengan shared backbone, batch fisik 16, mixed precision, dan split pasien yang telah dikunci.", "Eksperimen Poly-1 Loss resolusi 512 dengan shared backbone, batch fisik 16, mixed precision, dan split pasien yang telah dikunci.")
    $source = $source.Replace("/kaggle/working/bilateral_bce_512_seed42", "/kaggle/working/bilateral_polyloss_512_seed42")
    $source = $source.Replace("best_bilateral_bce_resnet50_512_seed42.pt", "best_bilateral_polyloss_resnet50_512_seed42.pt")
    $source = $source.Replace("validation_thresholds_bilateral_bce_512_seed42", "validation_thresholds_bilateral_polyloss_512_seed42")
    $source = $source.Replace("test_per_class_metrics_bilateral_bce_512_seed42", "test_per_class_metrics_bilateral_polyloss_512_seed42")
    $source = $source.Replace("test_confusion_matrix_bilateral_bce_512_seed42", "test_confusion_matrix_bilateral_polyloss_512_seed42")
    $source = $source.Replace("test_predictions_bilateral_bce_512_seed42", "test_predictions_bilateral_polyloss_512_seed42")
    $source = $source.Replace("test_metrics_bilateral_bce_512_seed42", "test_metrics_bilateral_polyloss_512_seed42")
    $source = $source.Replace('"loss_function": "BCEWithLogitsLoss"', '"loss_function": "Poly1Loss",' + "`n" + '                "poly_epsilon": 1.0')
    $source = $source.Replace("Hasil final test set, BCE baseline", "Hasil final test set, Poly-1 Loss")
    $source = $source.Replace("# Memuat checkpoint terbaik dan menentukan threshold BCE", "# Memuat checkpoint terbaik dan menentukan threshold Poly-1 Loss")
    $cell.source = @($source)
    if ($cell.cell_type -eq "code") {
        $cell.outputs = @()
        $cell.execution_count = $null
    }
}

$trainingCellIndex = 5
$trainingSource = $notebook.cells[$trainingCellIndex].source -join ""
$polyDefinition = @'

POLY_EPSILON = 1.0


class Poly1Loss(nn.Module):
    def __init__(self, epsilon=1.0):
        super().__init__()
        self.epsilon = epsilon

    def forward(self, logits, targets):
        bce_loss = torch.nn.functional.binary_cross_entropy_with_logits(
            logits,
            targets,
            reduction="none"
        )
        probabilities = torch.sigmoid(logits)
        p_t = (
            probabilities * targets
            + (1.0 - probabilities) * (1.0 - targets)
        )
        poly_term = self.epsilon * (1.0 - p_t)
        return (bce_loss + poly_term).mean()


'@
$criterionCode = @'
criterion = Poly1Loss(epsilon=POLY_EPSILON)
'@
$trainingSource = $trainingSource.Replace("criterion = nn.BCEWithLogitsLoss()`n", $polyDefinition + $criterionCode + "`n")
$trainingSource = $trainingSource.Replace("BCE, AdamW, scheduler, dan fungsi training siap.", "Poly-1 Loss, AdamW, scheduler, dan fungsi training siap.")
$notebook.cells[$trainingCellIndex].source = @($trainingSource)

$json = $notebook | ConvertTo-Json -Depth 100
Set-Content -LiteralPath $outputPath -Value $json -Encoding utf8
Write-Output $outputPath
