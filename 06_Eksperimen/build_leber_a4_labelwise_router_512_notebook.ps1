$ErrorActionPreference = "Stop"

$experimentRoot = Join-Path $PSScriptRoot "Baseline Bilateral ResNet50 512"
$sourcePath = Join-Path $experimentRoot "01_BCE\Notebooks\Executed\bce_seed42_executed.ipynb"
$a4Root = Join-Path $experimentRoot "05_LEBER_Ablation\A4_LabelWise_Router"
$readyDir = Join-Path $a4Root "Notebooks\Ready"
$executedDir = Join-Path $a4Root "Notebooks\Executed"
$resultsDir = Join-Path $a4Root "Results"
$outputPath = Join-Path $readyDir "leber_a4_labelwise_router_resnet50_bce_seed42_ready.ipynb"

foreach ($directory in @($readyDir, $executedDir, $resultsDir)) {
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
}

$notebook = Get-Content -Raw -LiteralPath $sourcePath | ConvertFrom-Json

foreach ($cell in $notebook.cells) {
    $source = $cell.source -join ""
    $source = $source.Replace(
        "Baseline Bilateral ResNet50 512 x 512 - BCE - Seed 42",
        "LEBER A4 - Label-Wise Dynamic Router - ResNet50 - BCE - Seed 42"
    )
    $source = $source.Replace(
        "Pilot resolusi 512 dengan shared backbone, batch fisik 16, mixed precision, dan split pasien yang telah dikunci.",
        "A4 menguji inovasi inti LEBER: modul router dinamis adaptif independen untuk setiap label (w_L,c, w_R,c, w_B,c). Memungkinkan alokasi porsi berbeda untuk penyakit lokal (katarak) dan penyakit sistemik (diabetes/hipertensi) dengan penjaminan sifat exchange-equivariant. Backbone, loss, split, dan konfigurasi training identik dengan A0 s.d. A3."
    )
    $source = $source.Replace(
        "best_bilateral_bce_resnet50_512_seed42.pt",
        "best_leber_a4_labelwise_router_resnet50_bce_512_seed42.pt"
    )
    $source = $source.Replace(
        "bilateral_bce_512_seed42",
        "leber_a4_labelwise_router_bce_512_seed42"
    )
    $source = $source.Replace('"backbone": "shared_resnet50"', '"backbone": "shared_resnet50_labelwise_router"')
    $source = $source.Replace("Hasil final test set, BCE baseline", "Validation diagnostics, LEBER A4 label-wise dynamic router")
    $cell.source = @($source)

    if ($cell.cell_type -eq "code") {
        $cell.outputs = @()
        $cell.execution_count = $null
        if ($cell.PSObject.Properties.Name -contains "metadata") {
            $cell.metadata = [pscustomobject]@{}
        }
    }
}

# A4 diproteksi: hanya menggunakan train dan validation. Test set tetap terkunci bebas kebocoran.
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

# Cell 4: Arsitektur Model A4 dengan Router Dinamis Per-Label (Label-Wise) dan Sanity Check
$notebook.cells[4].source = @(@'
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Device:", DEVICE)
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))


class LabelWiseRouterBilateralResNet50(nn.Module):
    """
    Ablasi A4: Tiga Expert (Kiri, Kanan, Bilateral) + Router Dinamis Per-Label (Label-Wise Routing).
    
    Menghasilkan bobot adaptif independen untuk setiap penyakit:
      w_{L, c} + w_{R, c} + w_{B, c} = 1.0, untuk c in {N, D, G, C, A, H, M, O}.
    
    Menjamin sifat matematis:
      - Exchange-Equivariant pada router: saat citra kiri dan kanan ditukar,
        bobot w_L dan w_R saling bertukar posisi untuk setiap label.
      - Exchange-Invariant pada prediksi: logit dan probabilitas pasien bernilai identik (Delta p = 0.0000).
    """
    def __init__(self, num_labels=8, dropout=0.30, pretrained=True):
        super().__init__()
        self.num_labels = num_labels

        weights = (
            ResNet50_Weights.IMAGENET1K_V2
            if pretrained else None
        )
        self.backbone = resnet50(weights=weights)

        feature_dim = self.backbone.fc.in_features  # 2048
        self.backbone.fc = nn.Identity()

        # Shared Monocular Expert: Linear(2048 -> 8) [equivariant monocular branch]
        self.expert_mono = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(feature_dim, num_labels)
        )

        # Bilateral Expert: Linear(6144 -> 8)
        self.expert_bilateral = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(feature_dim * 3, num_labels)
        )

        # Equivariant Label-Wise Router
        # Menghasilkan skor routing berdimensi [B, num_labels] untuk masing-masing cabang
        self.router_mono = nn.Sequential(
            nn.Linear(feature_dim, 64),
            nn.ReLU(),
            nn.Linear(64, num_labels)
        )
        self.router_bilateral = nn.Sequential(
            nn.Linear(feature_dim * 3, 64),
            nn.ReLU(),
            nn.Linear(64, num_labels)
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

    def forward(self, left_image, right_image, return_weights=False):
        left_features = self.backbone(left_image)
        right_features = self.backbone(right_image)

        # Pendapat awal masing-masing expert: [B, num_labels]
        z_left = self.expert_mono(left_features)
        z_right = self.expert_mono(right_features)

        bilateral_features = self.symmetric_features(
            left_features,
            right_features
        )
        z_bilateral = self.expert_bilateral(bilateral_features)

        # Scoring router per-label: masing-masing berukuran [B, num_labels]
        s_left = self.router_mono(left_features)
        s_right = self.router_mono(right_features)
        s_bilateral = self.router_bilateral(bilateral_features)

        # Stack sepanjang dimensi cabang (dim=1) -> [B, 3, num_labels]
        scores = torch.stack([s_left, s_right, s_bilateral], dim=1)

        # Softmax sepanjang dimensi cabang (dim=1) secara independen untuk tiap label
        weights = torch.softmax(scores, dim=1)  # [B, 3, num_labels]

        w_left = weights[:, 0, :]       # [B, num_labels]
        w_right = weights[:, 1, :]      # [B, num_labels]
        w_bilateral = weights[:, 2, :]  # [B, num_labels]

        # Fusi bukti tertimbang per-label: [B, num_labels]
        # (w_left * z_left + w_right * z_right) bersifat komutatif terhadap pertukaran kiri-kanan
        fused_logits = (w_left * z_left + w_right * z_right) + (w_bilateral * z_bilateral)

        if return_weights:
            return fused_logits, weights
        return fused_logits


model = LabelWiseRouterBilateralResNet50(
    num_labels=len(LABELS)
).to(DEVICE)

left_batch = batch["left_image"].to(DEVICE)
right_batch = batch["right_image"].to(DEVICE)

model.eval()
with torch.no_grad():
    logits, weights_orig = model(left_batch, right_batch, return_weights=True)
    swapped_logits, weights_swap = model(right_batch, left_batch, return_weights=True)
    probabilities = torch.sigmoid(logits)

swap_error_p = torch.max(
    torch.abs(logits - swapped_logits)
).item()

# Cek equivariance per label: w_left <-> w_right, w_bilat invariant
swap_error_w_mono = torch.max(
    torch.abs(weights_orig[:, 0, :] - weights_swap[:, 1, :])
).item()

swap_error_w_bilat = torch.max(
    torch.abs(weights_orig[:, 2, :] - weights_swap[:, 2, :])
).item()

assert logits.shape == (BATCH_SIZE, len(LABELS))
assert weights_orig.shape == (BATCH_SIZE, 3, len(LABELS))
assert swap_error_p < 1e-6, f"Prediksi A4 tidak invariant terhadap swap: {swap_error_p}"
assert swap_error_w_mono < 1e-6, f"Bobot monocular A4 tidak equivariant: {swap_error_w_mono}"
assert swap_error_w_bilat < 1e-6, f"Bobot bilateral A4 tidak invariant: {swap_error_w_bilat}"

print("Logits shape       :", logits.shape)
print("Weights shape      :", weights_orig.shape)
print("Maksimum selisih swap logit (Delta p):", swap_error_p)
print("Maksimum selisih swap bobot (Delta w):", max(swap_error_w_mono, swap_error_w_bilat))
print(
    "Parameter trainable total:",
    sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)
)
print(
    "Parameter classifier 3 Expert:",
    sum(p.numel() for p in model.expert_mono.parameters() if p.requires_grad) +
    sum(p.numel() for p in model.expert_bilateral.parameters() if p.requires_grad)
)
print(
    "Parameter Label-Wise Router MLP:",
    sum(p.numel() for p in model.router_mono.parameters() if p.requires_grad) +
    sum(p.numel() for p in model.router_bilateral.parameters() if p.requires_grad)
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
class LabelWiseRouterBilateralResNet50(nn.Module):
    def __init__(self, num_labels=8, dropout=0.30):
        super().__init__()
        self.num_labels = num_labels
        self.backbone = resnet50(weights=None)
        feature_dim = self.backbone.fc.in_features
        self.backbone.fc = nn.Identity()

        self.expert_mono = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(feature_dim, num_labels)
        )
        self.expert_bilateral = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(feature_dim * 3, num_labels)
        )

        self.router_mono = nn.Sequential(
            nn.Linear(feature_dim, 64),
            nn.ReLU(),
            nn.Linear(64, num_labels)
        )
        self.router_bilateral = nn.Sequential(
            nn.Linear(feature_dim * 3, 64),
            nn.ReLU(),
            nn.Linear(64, num_labels)
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

    def forward(self, left_image, right_image, return_weights=False):
        left_features = self.backbone(left_image)
        right_features = self.backbone(right_image)

        z_left = self.expert_mono(left_features)
        z_right = self.expert_mono(right_features)

        bilateral_features = self.symmetric_features(
            left_features,
            right_features
        )
        z_bilateral = self.expert_bilateral(bilateral_features)

        s_left = self.router_mono(left_features)
        s_right = self.router_mono(right_features)
        s_bilateral = self.router_bilateral(bilateral_features)

        scores = torch.stack([s_left, s_right, s_bilateral], dim=1)
        weights = torch.softmax(scores, dim=1)  # [B, 3, 8]

        w_left = weights[:, 0, :]
        w_right = weights[:, 1, :]
        w_bilateral = weights[:, 2, :]

        fused_logits = (w_left * z_left + w_right * z_right) + (w_bilateral * z_bilateral)
        if return_weights:
            return fused_logits, weights
        return fused_logits


'@

$evaluationSource = $notebook.cells[8].source -join ""
$evaluationSource = $evaluationSource.Replace(
    $oldEvaluationArchitecture,
    $newEvaluationArchitecture
)
$evaluationSource = $evaluationSource.Replace(
    "model = SharedResNet50(",
    "model = LabelWiseRouterBilateralResNet50("
)
$evaluationSource = $evaluationSource.Replace(
    "validation_thresholds_bilateral_bce_512_seed42",
    "validation_thresholds_leber_a4_labelwise_router_bce_512_seed42"
)

if ($evaluationSource.Contains("class SharedResNet50")) {
    throw "Arsitektur evaluasi A0 masih tertinggal pada cell threshold."
}
$notebook.cells[8].source = @($evaluationSource)

# Cell 9: Audit Konsistensi Prediksi (Delta p), Bobot Router (Delta w), dan Ringkasan Bobot Per-Label
$notebook.cells[9].source = @(@'
# Audit konsistensi pertukaran mata pada validation set (LEBER A4)
# Mengukur Delta p (probabilitas), Delta w (bobot router), dan analisis distribusi bobot per label

@torch.no_grad()
def collect_original_and_swapped_outputs(model, loader, device):
    model.eval()
    all_targets = []
    original_probabilities = []
    swapped_probabilities = []
    original_weights_list = []
    swapped_weights_list = []

    for batch in loader:
        left_images = batch["left_image"].to(device)
        right_images = batch["right_image"].to(device)
        labels = batch["labels"].cpu().numpy()

        orig_logits, orig_w = model(left_images, right_images, return_weights=True)
        swap_logits, swap_w = model(right_images, left_images, return_weights=True)

        all_targets.append(labels)
        original_probabilities.append(
            torch.sigmoid(orig_logits).cpu().numpy()
        )
        swapped_probabilities.append(
            torch.sigmoid(swap_logits).cpu().numpy()
        )
        original_weights_list.append(orig_w.cpu().numpy())
        swapped_weights_list.append(swap_w.cpu().numpy())

    return (
        np.concatenate(all_targets),
        np.concatenate(original_probabilities),
        np.concatenate(swapped_probabilities),
        np.concatenate(original_weights_list),
        np.concatenate(swapped_weights_list)
    )


y_val, prob_original, prob_swapped, weights_original, weights_swapped = (
    collect_original_and_swapped_outputs(
        model=model,
        loader=valid_loader,
        device=DEVICE
    )
)

absolute_probability_diff = np.abs(prob_original - prob_swapped)

# Evaluasi bobot router per-label:
# weights_original: [N, 3, 8], weights_swapped: [N, 3, 8]
# branch 0 (kiri) orig harus sama dengan branch 1 (kanan) swap
# branch 1 (kanan) orig harus sama dengan branch 0 (kiri) swap
# branch 2 (bilat) orig harus sama dengan branch 2 (bilat) swap
delta_w_left = np.abs(weights_original[:, 0, :] - weights_swapped[:, 1, :])
delta_w_right = np.abs(weights_original[:, 1, :] - weights_swapped[:, 0, :])
delta_w_bilat = np.abs(weights_original[:, 2, :] - weights_swapped[:, 2, :])
max_delta_w = float(max(delta_w_left.max(), delta_w_right.max(), delta_w_bilat.max()))

predictions_orig = (prob_original >= best_thresholds).astype(np.int32)
predictions_swap = (prob_swapped >= best_thresholds).astype(np.int32)

swap_metrics = {
    "split": "validation",
    "mean_absolute_probability_difference": float(absolute_probability_diff.mean()),
    "maximum_absolute_probability_difference": float(absolute_probability_diff.max()),
    "maximum_router_weight_difference": max_delta_w,
    "label_decision_disagreement_rate": float(
        np.not_equal(predictions_orig, predictions_swap).mean()
    ),
    "patient_exact_agreement_rate": float(
        np.all(predictions_orig == predictions_swap, axis=1).mean()
    )
}

assert swap_metrics["mean_absolute_probability_difference"] < 1e-6
assert swap_metrics["maximum_router_weight_difference"] < 1e-6
assert swap_metrics["label_decision_disagreement_rate"] == 0.0

swap_metrics_path = (
    OUTPUT_DIR
    / "validation_swap_metrics_leber_a4_labelwise_router_bce_512_seed42.json"
)

with open(swap_metrics_path, "w") as file:
    json.dump(swap_metrics, file, indent=2)

print("Audit swap validation LEBER A4:")
for key, value in swap_metrics.items():
    print(f"{key}: {value}")

# Analisis Distribusi Bobot Router per Label Penyakit
# Rata-rata bobot w_L, w_R, w_B untuk setiap dari 8 label
LABEL_NAMES = {
    "N": "Normal",
    "D": "Diabetes",
    "G": "Glaucoma",
    "C": "Cataract",
    "A": "AMD",
    "H": "Hypertension",
    "M": "Myopia",
    "O": "Others"
}

labelwise_weights_rows = []
print("\nDistribusi Rata-Rata Bobot Router per Label:")
print(f"{'Label':<6} {'Nama Penyakit':<20} {'w_Left':<12} {'w_Right':<12} {'w_Bilateral':<12}")
print("-" * 65)

for idx, label in enumerate(LABELS):
    mean_w_l = float(weights_original[:, 0, idx].mean())
    mean_w_r = float(weights_original[:, 1, idx].mean())
    mean_w_b = float(weights_original[:, 2, idx].mean())
    
    labelwise_weights_rows.append({
        "label": label,
        "mean_weight_left": mean_w_l,
        "mean_weight_right": mean_w_r,
        "mean_weight_bilateral": mean_w_b
    })
    print(f"{label:<6} {LABEL_NAMES[label]:<20} {mean_w_l:<12.4f} {mean_w_r:<12.4f} {mean_w_b:<12.4f}")

weights_summary_df = pd.DataFrame(labelwise_weights_rows)
weights_summary_path = (
    OUTPUT_DIR
    / "validation_labelwise_weights_summary_leber_a4_bce_512_seed42.csv"
)
weights_summary_df.to_csv(weights_summary_path, index=False)
print(f"\nRingkasan bobot per-label disimpan di: {weights_summary_path}")

print("\nArtefak disimpan di:", OUTPUT_DIR)
print("Test set tetap terjaga bebas dari kebocoran data untuk evaluasi final.")
'@)

$json = $notebook | ConvertTo-Json -Depth 100
[System.IO.File]::WriteAllText($outputPath, $json, (New-Object System.Text.UTF8Encoding($false)))
Write-Output "Notebook A4 berhasil dibuat di: $outputPath"
