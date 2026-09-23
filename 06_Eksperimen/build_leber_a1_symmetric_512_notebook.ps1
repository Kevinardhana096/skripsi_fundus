$ErrorActionPreference = "Stop"

$experimentRoot = Join-Path $PSScriptRoot "Baseline Bilateral ResNet50 512"
$sourcePath = Join-Path $experimentRoot "01_BCE\Notebooks\Executed\bce_seed42_executed.ipynb"
$a1Root = Join-Path $experimentRoot "05_LEBER_Ablation\A1_Symmetric"
$readyDir = Join-Path $a1Root "Notebooks\Ready"
$executedDir = Join-Path $a1Root "Notebooks\Executed"
$resultsDir = Join-Path $a1Root "Results"
$outputPath = Join-Path $readyDir "leber_a1_symmetric_resnet50_bce_seed42_ready.ipynb"

foreach ($directory in @($readyDir, $executedDir, $resultsDir)) {
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
}

$notebook = Get-Content -Raw -LiteralPath $sourcePath | ConvertFrom-Json

foreach ($cell in $notebook.cells) {
    $source = $cell.source -join ""
    $source = $source.Replace(
        "Baseline Bilateral ResNet50 512 x 512 - BCE - Seed 42",
        "LEBER A1 - Symmetric Bilateral Features - ResNet50 - BCE - Seed 42"
    )
    $source = $source.Replace(
        "Pilot resolusi 512 dengan shared backbone, batch fisik 16, mixed precision, dan split pasien yang telah dikunci.",
        "A1 menguji fitur bilateral simetris berupa jumlah, selisih absolut, dan perkalian fitur kedua mata. Backbone, loss, split, dan konfigurasi training sama dengan A0."
    )
    $source = $source.Replace(
        "best_bilateral_bce_resnet50_512_seed42.pt",
        "best_leber_a1_symmetric_resnet50_bce_512_seed42.pt"
    )
    $source = $source.Replace(
        "bilateral_bce_512_seed42",
        "leber_a1_symmetric_bce_512_seed42"
    )
    $source = $source.Replace('"backbone": "shared_resnet50"', '"backbone": "shared_resnet50_symmetric_features"')
    $source = $source.Replace("Hasil final test set, BCE baseline", "Validation diagnostics, LEBER A1 symmetric features")
    $cell.source = @($source)

    if ($cell.cell_type -eq "code") {
        $cell.outputs = @()
        $cell.execution_count = $null
        if ($cell.PSObject.Properties.Name -contains "metadata") {
            $cell.metadata = [pscustomobject]@{}
        }
    }
}

# A1 dipilih hanya menggunakan train dan validation. Test set belum dibaca.
$dataSource = $notebook.cells[1].source -join ""
$dataSource = $dataSource.Replace('TEST_CSV = DATASET_DIR / "test.csv"' + "`n", "")
$dataSource = $dataSource.Replace('test_df = pd.read_csv(TEST_CSV)' + "`n", "")
$dataSource = $dataSource.Replace('print("Test       :", test_df.shape)' + "`n", "")
$dataSource = $dataSource.Replace('assert len(test_df) == 525' + "`n", "")
$notebook.cells[1].source = @($dataSource)

$loaderSource = $notebook.cells[3].source -join ""
$loaderSource = $loaderSource.Replace(
    'test_dataset = FundusPairDataset(test_df, IMAGE_DIR, eval_transform)' + "`n",
    ""
)
$testLoaderBlock = @'
test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=NUM_WORKERS,
    pin_memory=True,
)

'@
$loaderSource = $loaderSource.Replace($testLoaderBlock, "")
$notebook.cells[3].source = @($loaderSource)

$notebook.cells[4].source = @(@'
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Device:", DEVICE)
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))


class SymmetricBilateralResNet50(nn.Module):
    def __init__(self, num_labels=8, dropout=0.30, pretrained=True):
        super().__init__()

        weights = (
            ResNet50_Weights.IMAGENET1K_V2
            if pretrained else None
        )
        self.backbone = resnet50(weights=weights)

        feature_dim = self.backbone.fc.in_features
        self.backbone.fc = nn.Identity()

        self.classifier = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(feature_dim * 3, num_labels)
        )

    @staticmethod
    def symmetric_features(left_features, right_features):
        sum_features = left_features + right_features
        difference_features = torch.abs(left_features - right_features)
        product_features = left_features * right_features
        return torch.cat(
            [sum_features, difference_features, product_features],
            dim=1
        )

    def forward(self, left_image, right_image):
        left_features = self.backbone(left_image)
        right_features = self.backbone(right_image)
        bilateral_features = self.symmetric_features(
            left_features,
            right_features
        )
        return self.classifier(bilateral_features)


model = SymmetricBilateralResNet50(
    num_labels=len(LABELS)
).to(DEVICE)

left_batch = batch["left_image"].to(DEVICE)
right_batch = batch["right_image"].to(DEVICE)

model.eval()
with torch.no_grad():
    logits = model(left_batch, right_batch)
    swapped_logits = model(right_batch, left_batch)
    probabilities = torch.sigmoid(logits)

swap_error = torch.max(
    torch.abs(logits - swapped_logits)
).item()

assert logits.shape == (BATCH_SIZE, len(LABELS))
assert swap_error < 1e-6, (
    f"Fitur A1 tidak invariant terhadap swap: {swap_error}"
)

print("Logits shape       :", logits.shape)
print("Probabilities shape:", probabilities.shape)
print("Maksimum selisih logit setelah swap:", swap_error)
print(
    "Parameter trainable:",
    sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)
)
'@)

$oldEvaluationArchitecture = @'
# Arsitektur harus sama dengan model saat training
class SharedResNet50(nn.Module):
    def __init__(
        self,
        num_labels=8,
        dropout=0.30
    ):
        super().__init__()

        # Tidak mengunduh bobot ImageNet karena bobot model
        # akan dimuat dari checkpoint hasil training.
        self.backbone = resnet50(
            weights=None
        )

        feature_dim = (
            self.backbone.fc.in_features
        )

        self.backbone.fc = nn.Identity()

        self.classifier = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(
                feature_dim * 2,
                num_labels
            )
        )

    def forward(
        self,
        left_image,
        right_image
    ):
        left_features = self.backbone(
            left_image
        )

        right_features = self.backbone(
            right_image
        )

        combined_features = torch.cat(
            [
                left_features,
                right_features
            ],
            dim=1
        )

        return self.classifier(
            combined_features
        )


'@

$newEvaluationArchitecture = @'
# Arsitektur harus sama dengan model saat training
class SymmetricBilateralResNet50(nn.Module):
    def __init__(self, num_labels=8, dropout=0.30):
        super().__init__()
        self.backbone = resnet50(weights=None)
        feature_dim = self.backbone.fc.in_features
        self.backbone.fc = nn.Identity()
        self.classifier = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(feature_dim * 3, num_labels)
        )

    @staticmethod
    def symmetric_features(left_features, right_features):
        return torch.cat(
            [
                left_features + right_features,
                torch.abs(left_features - right_features),
                left_features * right_features
            ],
            dim=1
        )

    def forward(self, left_image, right_image):
        left_features = self.backbone(left_image)
        right_features = self.backbone(right_image)
        bilateral_features = self.symmetric_features(
            left_features,
            right_features
        )
        return self.classifier(bilateral_features)


'@

$evaluationSource = $notebook.cells[8].source -join ""
$evaluationSource = $evaluationSource.Replace(
    $oldEvaluationArchitecture,
    $newEvaluationArchitecture
)
$evaluationSource = $evaluationSource.Replace(
    "model = SharedResNet50(",
    "model = SymmetricBilateralResNet50("
)

if ($evaluationSource.Contains("class SharedResNet50")) {
    throw "Arsitektur evaluasi A0 masih tertinggal pada cell threshold."
}
$notebook.cells[8].source = @($evaluationSource)

$notebook.cells[9].source = @(@'
# Audit konsistensi pertukaran mata pada validation set

@torch.no_grad()
def collect_original_and_swapped_probabilities(model, loader, device):
    model.eval()
    all_targets = []
    original_probabilities = []
    swapped_probabilities = []

    for batch in loader:
        left_images = batch["left_image"].to(device)
        right_images = batch["right_image"].to(device)
        labels = batch["labels"].cpu().numpy()

        original_logits = model(left_images, right_images)
        swapped_logits = model(right_images, left_images)

        all_targets.append(labels)
        original_probabilities.append(
            torch.sigmoid(original_logits).cpu().numpy()
        )
        swapped_probabilities.append(
            torch.sigmoid(swapped_logits).cpu().numpy()
        )

    return (
        np.concatenate(all_targets),
        np.concatenate(original_probabilities),
        np.concatenate(swapped_probabilities)
    )


y_swap, probabilities_original, probabilities_swapped = (
    collect_original_and_swapped_probabilities(
        model=model,
        loader=valid_loader,
        device=DEVICE
    )
)

absolute_probability_difference = np.abs(
    probabilities_original - probabilities_swapped
)

predictions_original = (
    probabilities_original >= best_thresholds
).astype(np.int32)

predictions_swapped = (
    probabilities_swapped >= best_thresholds
).astype(np.int32)

swap_metrics = {
    "split": "validation",
    "mean_absolute_probability_difference": float(
        absolute_probability_difference.mean()
    ),
    "maximum_absolute_probability_difference": float(
        absolute_probability_difference.max()
    ),
    "label_decision_disagreement_rate": float(
        np.not_equal(
            predictions_original,
            predictions_swapped
        ).mean()
    ),
    "patient_exact_agreement_rate": float(
        np.all(
            predictions_original == predictions_swapped,
            axis=1
        ).mean()
    )
}

assert swap_metrics["mean_absolute_probability_difference"] < 1e-6
assert swap_metrics["label_decision_disagreement_rate"] == 0.0

swap_metrics_path = (
    OUTPUT_DIR
    / "validation_swap_metrics_leber_a1_symmetric_bce_512_seed42.json"
)

with open(swap_metrics_path, "w") as file:
    json.dump(swap_metrics, file, indent=2)

print("Audit swap validation A1:")
for key, value in swap_metrics.items():
    print(f"{key}: {value}")

print("\nArtefak disimpan di:", OUTPUT_DIR)
print("Test set belum digunakan pada tahap pemilihan arsitektur A1.")
'@)

$json = $notebook | ConvertTo-Json -Depth 100
Set-Content -LiteralPath $outputPath -Value $json -Encoding utf8
Write-Output $outputPath
