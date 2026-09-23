import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Focal Loss ResNet50" / "focal-loss-resnet50-multiseed-52-62.ipynb"
POLY_SOURCE = ROOT / "PolyLoss ResNet50" / "polyloss-resnet50.ipynb"
OUTPUT = ROOT / "PolyLoss ResNet50" / "polyloss-resnet50-multiseed-52-62.ipynb"


with SOURCE.open("r", encoding="utf-8") as file:
    notebook = json.load(file)

with POLY_SOURCE.open("r", encoding="utf-8") as file:
    poly_source_notebook = json.load(file)

notebook["metadata"] = poly_source_notebook.get("metadata", {})

for cell in notebook["cells"]:
    source = "".join(cell.get("source", []))

    source = source.replace(
        "# Focal Loss ResNet50 Multi-Seed (52 dan 62)",
        "# Poly-1 Loss ResNet50 Multi-Seed (52 dan 62)",
    )
    source = source.replace(
        "Notebook ini melanjutkan eksperimen Focal Loss seed 42.",
        "Notebook ini melanjutkan eksperimen Poly-1 Loss seed 42.",
    )
    source = source.replace(
        "FOCAL_ALPHA = 0.25\nFOCAL_GAMMA = 2.0",
        "POLY_EPSILON = 1.0",
    )
    source = source.replace(
        'OUTPUT_DIR = Path("/kaggle/working/focal_loss_resnet50_multiseed")',
        'OUTPUT_DIR = Path("/kaggle/working/polyloss_resnet50_multiseed")',
    )
    source = source.replace(
        'checkpoint_path = seed_dir / "best_focal_loss_resnet50.pt"',
        'checkpoint_path = seed_dir / "best_polyloss_resnet50.pt"',
    )
    source = source.replace(
        '"loss_function": "Focal Loss",',
        '"loss_function": "Poly-1 Loss",',
    )
    source = source.replace(
        '"focal_alpha": FOCAL_ALPHA,\n'
        '        "focal_gamma": FOCAL_GAMMA,',
        '"poly_epsilon": POLY_EPSILON,',
    )
    source = source.replace(
        '"focal_alpha": FOCAL_ALPHA,\n'
        '                    "focal_gamma": FOCAL_GAMMA,',
        '"poly_epsilon": POLY_EPSILON,',
    )
    source = source.replace(
        'print("Focal alpha / gamma:", FOCAL_ALPHA, FOCAL_GAMMA)',
        'print("Poly-1 epsilon:", POLY_EPSILON)',
    )
    source = source.replace(
        'print("\\nSeluruh training Focal Loss multi-seed selesai.")',
        'print("\\nSeluruh training Poly-1 Loss multi-seed selesai.")',
    )
    source = source.replace(
        'axes[0].set_title(f"Focal Loss, seed {seed}")',
        'axes[0].set_title(f"Poly-1 Loss, seed {seed}")',
    )
    source = source.replace(
        '"/kaggle/working/focal_loss_resnet50_multiseed_52_62",',
        '"/kaggle/working/polyloss_resnet50_multiseed_52_62",',
    )

    class_pattern = re.compile(
        r"class SigmoidFocalLoss\(nn\.Module\):.*?\n\n\ntrain_dataset =",
        flags=re.DOTALL,
    )
    poly_class = '''class Poly1Loss(nn.Module):
    def __init__(self, epsilon=1.0):
        super().__init__()
        self.epsilon = epsilon

    def forward(self, logits, targets):
        bce_loss = F.binary_cross_entropy_with_logits(
            logits,
            targets,
            reduction="none",
        )
        probabilities = torch.sigmoid(logits)
        p_t = (
            probabilities * targets
            + (1.0 - probabilities) * (1.0 - targets)
        )
        poly_term = self.epsilon * (1.0 - p_t)
        return (bce_loss + poly_term).mean()


train_dataset ='''
    source = class_pattern.sub(poly_class, source)

    criterion_pattern = re.compile(
        r"def build_criterion\(\):\n"
        r"    return SigmoidFocalLoss\(.*?\n    \)\n",
        flags=re.DOTALL,
    )
    poly_criterion = '''def build_criterion():
    return Poly1Loss(epsilon=POLY_EPSILON)
'''
    source = criterion_pattern.sub(poly_criterion, source)

    cell["source"] = [line + "\n" for line in source.rstrip().splitlines()]
    if cell["cell_type"] == "code":
        cell["execution_count"] = None
        cell["outputs"] = []

with OUTPUT.open("w", encoding="utf-8") as file:
    json.dump(notebook, file, ensure_ascii=False, indent=1)

with OUTPUT.open("r", encoding="utf-8") as file:
    validated = json.load(file)

all_code = "\n".join(
    "".join(cell["source"])
    for cell in validated["cells"]
    if cell["cell_type"] == "code"
)

for index, cell in enumerate(validated["cells"]):
    if cell["cell_type"] == "code":
        compile("".join(cell["source"]), f"cell_{index}", "exec")

required = [
    "SEEDS = [52, 62]",
    "POLY_EPSILON = 1.0",
    "class Poly1Loss",
    'reduction="none"',
    "poly_term = self.epsilon * (1.0 - p_t)",
    "return (bce_loss + poly_term).mean()",
    "return Poly1Loss(epsilon=POLY_EPSILON)",
    'seed_dir = OUTPUT_DIR / f"seed_{seed}"',
    "tuned_validation_macro_f1",
    "test_six_disease_macro_f1",
    "polyloss_resnet50_multiseed_52_62",
]

for fragment in required:
    assert fragment in all_code, f"Bagian wajib tidak ditemukan: {fragment}"

for forbidden in [
    "SEED = 42",
    "SigmoidFocalLoss",
    "FOCAL_ALPHA",
    "FOCAL_GAMMA",
    "AsymmetricLoss",
    "pos_weight=",
]:
    assert forbidden not in all_code, f"Konfigurasi yang tidak sesuai ditemukan: {forbidden}"

print(f"Notebook valid: {OUTPUT}")
print(f"Jumlah sel: {len(validated['cells'])}")
