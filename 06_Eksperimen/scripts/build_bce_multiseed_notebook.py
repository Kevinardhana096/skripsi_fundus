import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Focal Loss ResNet50" / "focal-loss-resnet50-multiseed-52-62.ipynb"
BCE_SOURCE = ROOT / "BCE ResNet50" / "bce-baseline-resnet50-untuk-klasifikasi-multi-la (1).ipynb"
OUTPUT = ROOT / "BCE ResNet50" / "bce-resnet50-multiseed-52-62.ipynb"


with SOURCE.open("r", encoding="utf-8") as file:
    notebook = json.load(file)

with BCE_SOURCE.open("r", encoding="utf-8") as file:
    bce_source_notebook = json.load(file)

notebook["metadata"] = bce_source_notebook.get("metadata", {})

for cell in notebook["cells"]:
    source = "".join(cell.get("source", []))

    source = source.replace(
        "# Focal Loss ResNet50 Multi-Seed (52 dan 62)",
        "# BCE ResNet50 Multi-Seed (52 dan 62)",
    )
    source = source.replace(
        "Notebook ini melanjutkan eksperimen Focal Loss seed 42.",
        "Notebook ini melanjutkan eksperimen BCE standar seed 42.",
    )
    source = source.replace("import torch.nn.functional as F\n", "")
    source = source.replace(
        "FOCAL_ALPHA = 0.25\nFOCAL_GAMMA = 2.0\n",
        "",
    )
    source = source.replace(
        'OUTPUT_DIR = Path("/kaggle/working/focal_loss_resnet50_multiseed")',
        'OUTPUT_DIR = Path("/kaggle/working/bce_resnet50_multiseed")',
    )
    source = source.replace(
        'checkpoint_path = seed_dir / "best_focal_loss_resnet50.pt"',
        'checkpoint_path = seed_dir / "best_bce_resnet50.pt"',
    )
    source = source.replace(
        '"loss_function": "Focal Loss",',
        '"loss_function": "BCEWithLogitsLoss",',
    )
    source = source.replace(
        '"focal_alpha": FOCAL_ALPHA,\n'
        '        "focal_gamma": FOCAL_GAMMA,',
        '"bce_pos_weight": None,',
    )
    source = source.replace(
        '"focal_alpha": FOCAL_ALPHA,\n'
        '                    "focal_gamma": FOCAL_GAMMA,',
        '"loss_function": "BCEWithLogitsLoss",\n'
        '                    "bce_pos_weight": None,',
    )
    source = source.replace(
        'print("Focal alpha / gamma:", FOCAL_ALPHA, FOCAL_GAMMA)',
        'print("Loss: BCEWithLogitsLoss tanpa pos_weight")',
    )
    source = source.replace(
        'print("\\nSeluruh training Focal Loss multi-seed selesai.")',
        'print("\\nSeluruh training BCE multi-seed selesai.")',
    )
    source = source.replace(
        'axes[0].set_title(f"Focal Loss, seed {seed}")',
        'axes[0].set_title(f"BCE, seed {seed}")',
    )
    source = source.replace(
        '"/kaggle/working/focal_loss_resnet50_multiseed_52_62",',
        '"/kaggle/working/bce_resnet50_multiseed_52_62",',
    )

    class_pattern = re.compile(
        r"class SigmoidFocalLoss\(nn\.Module\):.*?\n\n\ntrain_dataset =",
        flags=re.DOTALL,
    )
    source = class_pattern.sub("train_dataset =", source)

    criterion_pattern = re.compile(
        r"def build_criterion\(\):\n"
        r"    return SigmoidFocalLoss\(.*?\n    \)\n",
        flags=re.DOTALL,
    )
    source = criterion_pattern.sub(
        "def build_criterion():\n    return nn.BCEWithLogitsLoss()\n",
        source,
    )

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
    "return nn.BCEWithLogitsLoss()",
    '"bce_pos_weight": None',
    "model = build_model()",
    'seed_dir = OUTPUT_DIR / f"seed_{seed}"',
    "tuned_validation_macro_f1",
    "test_six_disease_macro_f1",
    "bce_resnet50_multiseed_52_62",
]

for fragment in required:
    assert fragment in all_code, f"Bagian wajib tidak ditemukan: {fragment}"

for forbidden in [
    "SEED = 42",
    "SigmoidFocalLoss",
    "FOCAL_ALPHA",
    "FOCAL_GAMMA",
    "pos_weight=",
]:
    assert forbidden not in all_code, f"Konfigurasi yang tidak sesuai ditemukan: {forbidden}"

print(f"Notebook valid: {OUTPUT}")
print(f"Jumlah sel: {len(validated['cells'])}")
