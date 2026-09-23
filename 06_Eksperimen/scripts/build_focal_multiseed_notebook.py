import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ASL ResNet50" / "asl-resnet50-multiseed-52-62.ipynb"
FOCAL_SOURCE = ROOT / "Focal Loss ResNet50" / "focal-loss-resnet50.ipynb"
OUTPUT = ROOT / "Focal Loss ResNet50" / "focal-loss-resnet50-multiseed-52-62.ipynb"


with SOURCE.open("r", encoding="utf-8") as file:
    notebook = json.load(file)

with FOCAL_SOURCE.open("r", encoding="utf-8") as file:
    focal_source_notebook = json.load(file)

notebook["metadata"] = focal_source_notebook.get("metadata", {})

for cell in notebook["cells"]:
    source = "".join(cell.get("source", []))

    source = source.replace(
        "# ASL ResNet50 Multi-Seed (52 dan 62)",
        "# Focal Loss ResNet50 Multi-Seed (52 dan 62)",
    )
    source = source.replace(
        "Notebook ini melanjutkan eksperimen Asymmetric Loss seed 42.",
        "Notebook ini melanjutkan eksperimen Focal Loss seed 42.",
    )
    source = source.replace(
        "import torch.nn as nn\n",
        "import torch.nn as nn\nimport torch.nn.functional as F\n",
    )
    source = source.replace(
        "ASL_GAMMA_NEG = 4.0\nASL_GAMMA_POS = 1.0\nASL_CLIP = 0.05",
        "FOCAL_ALPHA = 0.25\nFOCAL_GAMMA = 2.0",
    )
    source = source.replace(
        'OUTPUT_DIR = Path("/kaggle/working/asl_resnet50_multiseed")',
        'OUTPUT_DIR = Path("/kaggle/working/focal_loss_resnet50_multiseed")',
    )
    source = source.replace(
        'checkpoint_path = seed_dir / "best_asl_resnet50.pt"',
        'checkpoint_path = seed_dir / "best_focal_loss_resnet50.pt"',
    )
    source = source.replace(
        '"loss_function": "Asymmetric Loss",',
        '"loss_function": "Focal Loss",',
    )
    source = source.replace(
        '"asl_gamma_neg": ASL_GAMMA_NEG,\n'
        '        "asl_gamma_pos": ASL_GAMMA_POS,\n'
        '        "asl_clip": ASL_CLIP,',
        '"focal_alpha": FOCAL_ALPHA,\n'
        '        "focal_gamma": FOCAL_GAMMA,',
    )
    source = source.replace(
        '"asl_gamma_neg": ASL_GAMMA_NEG,\n'
        '                    "asl_gamma_pos": ASL_GAMMA_POS,\n'
        '                    "asl_clip": ASL_CLIP,',
        '"focal_alpha": FOCAL_ALPHA,\n'
        '                    "focal_gamma": FOCAL_GAMMA,',
    )
    source = source.replace(
        'print("ASL gamma_neg / gamma_pos / clip:", ASL_GAMMA_NEG, ASL_GAMMA_POS, ASL_CLIP)',
        'print("Focal alpha / gamma:", FOCAL_ALPHA, FOCAL_GAMMA)',
    )
    source = source.replace(
        'print("\\nSeluruh training ASL multi-seed selesai.")',
        'print("\\nSeluruh training Focal Loss multi-seed selesai.")',
    )
    source = source.replace(
        'axes[0].set_title(f"Asymmetric Loss, seed {seed}")',
        'axes[0].set_title(f"Focal Loss, seed {seed}")',
    )
    source = source.replace(
        '"/kaggle/working/asl_resnet50_multiseed_52_62",',
        '"/kaggle/working/focal_loss_resnet50_multiseed_52_62",',
    )

    class_pattern = re.compile(
        r"class AsymmetricLoss\(nn\.Module\):.*?\n\n\ntrain_dataset =",
        flags=re.DOTALL,
    )
    focal_class = '''class SigmoidFocalLoss(nn.Module):
    def __init__(self, alpha=0.25, gamma=2.0):
        super().__init__()
        if not 0.0 <= alpha <= 1.0:
            raise ValueError("alpha harus berada pada rentang 0 sampai 1")
        if gamma < 0.0:
            raise ValueError("gamma tidak boleh negatif")
        self.alpha = alpha
        self.gamma = gamma

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
        alpha_t = (
            self.alpha * targets
            + (1.0 - self.alpha) * (1.0 - targets)
        )
        focal_factor = (1.0 - p_t).pow(self.gamma)
        return (alpha_t * focal_factor * bce_loss).mean()


train_dataset ='''
    source = class_pattern.sub(focal_class, source)

    criterion_pattern = re.compile(
        r"def build_criterion\(\):\n"
        r"    return AsymmetricLoss\(.*?\n    \)\n",
        flags=re.DOTALL,
    )
    focal_criterion = '''def build_criterion():
    return SigmoidFocalLoss(
        alpha=FOCAL_ALPHA,
        gamma=FOCAL_GAMMA,
    )
'''
    source = criterion_pattern.sub(focal_criterion, source)

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
    "FOCAL_ALPHA = 0.25",
    "FOCAL_GAMMA = 2.0",
    "class SigmoidFocalLoss",
    "model = build_model()",
    "tuned_validation_macro_f1",
    "test_six_disease_macro_f1",
    "focal_loss_resnet50_multiseed_52_62",
]

for fragment in required:
    assert fragment in all_code, f"Bagian wajib tidak ditemukan: {fragment}"

for forbidden in ["SEED = 42", "AsymmetricLoss", "ASL_GAMMA", "ASL_CLIP"]:
    assert forbidden not in all_code, f"Sisa konfigurasi ASL ditemukan: {forbidden}"

print(f"Notebook valid: {OUTPUT}")
print(f"Jumlah sel: {len(validated['cells'])}")
