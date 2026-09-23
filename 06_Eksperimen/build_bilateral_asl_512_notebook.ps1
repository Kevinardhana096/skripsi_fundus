$ErrorActionPreference = "Stop"

$sourcePath = Join-Path $PSScriptRoot "Baseline Bilateral ResNet50 512\01_BCE\Notebooks\Executed\bce_seed42_executed.ipynb"
$outputDir = Join-Path $PSScriptRoot "Baseline Bilateral ResNet50 512\02_ASL\Notebooks\Ready"
$outputPath = Join-Path $outputDir "asl_seed42_ready.ipynb"

$notebook = Get-Content -Raw -LiteralPath $sourcePath | ConvertFrom-Json

foreach ($cell in $notebook.cells) {
    $source = $cell.source -join ""
    $source = $source.Replace("Baseline Bilateral ResNet50 512 x 512 - BCE - Seed 42", "Baseline Bilateral ResNet50 512 x 512 - ASL - Seed 42")
    $source = $source.Replace("Pilot resolusi 512 dengan shared backbone, batch fisik 16, mixed precision, dan split pasien yang telah dikunci.", "Eksperimen ASL resolusi 512 dengan shared backbone, batch fisik 16, mixed precision, dan split pasien yang telah dikunci.")
    $source = $source.Replace("/kaggle/working/bilateral_bce_512_seed42", "/kaggle/working/bilateral_asl_512_seed42")
    $source = $source.Replace("best_bilateral_bce_resnet50_512_seed42.pt", "best_bilateral_asl_resnet50_512_seed42.pt")
    $source = $source.Replace("validation_thresholds_bilateral_bce_512_seed42", "validation_thresholds_bilateral_asl_512_seed42")
    $source = $source.Replace("test_per_class_metrics_bilateral_bce_512_seed42", "test_per_class_metrics_bilateral_asl_512_seed42")
    $source = $source.Replace("test_confusion_matrix_bilateral_bce_512_seed42", "test_confusion_matrix_bilateral_asl_512_seed42")
    $source = $source.Replace("test_predictions_bilateral_bce_512_seed42", "test_predictions_bilateral_asl_512_seed42")
    $source = $source.Replace("test_metrics_bilateral_bce_512_seed42", "test_metrics_bilateral_asl_512_seed42")
    $source = $source.Replace('"loss_function": "BCEWithLogitsLoss"', '"loss_function": "AsymmetricLoss",' + "`n" + '                "asl_gamma_neg": 4.0,' + "`n" + '                "asl_gamma_pos": 1.0,' + "`n" + '                "asl_clip": 0.05')
    $source = $source.Replace("Hasil final test set, BCE baseline", "Hasil final test set, ASL baseline")
    $source = $source.Replace("# Memuat checkpoint terbaik dan menentukan threshold BCE", "# Memuat checkpoint terbaik dan menentukan threshold ASL")
    $cell.source = @($source)
    if ($cell.cell_type -eq "code") {
        $cell.outputs = @()
        $cell.execution_count = $null
    }
}

$trainingCellIndex = 5
$trainingSource = $notebook.cells[$trainingCellIndex].source -join ""
$aslDefinition = @'

ASL_GAMMA_NEG = 4.0
ASL_GAMMA_POS = 1.0
ASL_CLIP = 0.05


class AsymmetricLoss(nn.Module):
    def __init__(self, gamma_neg=4.0, gamma_pos=1.0, clip=0.05, eps=1e-8):
        super().__init__()
        self.gamma_neg = gamma_neg
        self.gamma_pos = gamma_pos
        self.clip = clip
        self.eps = eps

    def forward(self, logits, targets):
        positive_probabilities = torch.sigmoid(logits)
        negative_probabilities = 1.0 - positive_probabilities

        if self.clip > 0.0:
            negative_probabilities = (
                negative_probabilities + self.clip
            ).clamp(max=1.0)

        positive_loss = targets * torch.log(
            positive_probabilities.clamp(min=self.eps)
        )
        negative_loss = (1.0 - targets) * torch.log(
            negative_probabilities.clamp(min=self.eps)
        )
        base_loss = positive_loss + negative_loss

        with torch.no_grad():
            positive_focus = 1.0 - positive_probabilities
            negative_focus = 1.0 - negative_probabilities
            asymmetric_focus = (
                positive_focus * targets
                + negative_focus * (1.0 - targets)
            )
            asymmetric_gamma = (
                self.gamma_pos * targets
                + self.gamma_neg * (1.0 - targets)
            )
            asymmetric_weight = asymmetric_focus.pow(asymmetric_gamma)

        return -(asymmetric_weight * base_loss).mean()


'@
$criterionCode = @'
criterion = AsymmetricLoss(
    gamma_neg=ASL_GAMMA_NEG,
    gamma_pos=ASL_GAMMA_POS,
    clip=ASL_CLIP
)
'@
$trainingSource = $trainingSource.Replace("criterion = nn.BCEWithLogitsLoss()`n", $aslDefinition + $criterionCode + "`n")
$trainingSource = $trainingSource.Replace("BCE, AdamW, scheduler, dan fungsi training siap.", "ASL, AdamW, scheduler, dan fungsi training siap.")
$notebook.cells[$trainingCellIndex].source = @($trainingSource)

$json = $notebook | ConvertTo-Json -Depth 100
Set-Content -LiteralPath $outputPath -Value $json -Encoding utf8
Write-Output $outputPath
