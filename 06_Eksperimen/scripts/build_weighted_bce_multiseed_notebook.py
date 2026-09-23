import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "BCE ResNet50" / "bce-resnet50-multiseed-52-62.ipynb"
WEIGHTED_SOURCE = (
    ROOT
    / "Weighted BCE ResNet50"
    / "weighted-bce-resnet50-untuk-klasifikasi-multi-labe.ipynb"
)
OUTPUT = (
    ROOT
    / "Weighted BCE ResNet50"
    / "weighted-bce-resnet50-multiseed-52-62.ipynb"
)


with SOURCE.open("r", encoding="utf-8") as file:
    notebook = json.load(file)

with WEIGHTED_SOURCE.open("r", encoding="utf-8") as file:
    weighted_source_notebook = json.load(file)

notebook["metadata"] = weighted_source_notebook.get("metadata", {})

weight_setup = '''positive_counts = train_df[LABELS].sum()
negative_counts = len(train_df) - positive_counts
pos_weight = torch.tensor(
    (negative_counts / positive_counts).values,
    dtype=torch.float32,
    device=DEVICE,
)

assert torch.isfinite(pos_weight).all()
assert (pos_weight > 0).all()

class_distribution_table = pd.DataFrame(
    {
        "label": LABELS,
        "positif_train": positive_counts.values.astype(int),
        "negatif_train": negative_counts.values.astype(int),
    }
)
weight_table = class_distribution_table.copy()
weight_table["pos_weight"] = pos_weight.detach().cpu().numpy()'''

standard_weight_setup = '''positive_counts = train_df[LABELS].sum()
negative_counts = len(train_df) - positive_counts
class_distribution_table = pd.DataFrame(
    {
        "label": LABELS,
        "positif_train": positive_counts.values.astype(int),
        "negatif_train": negative_counts.values.astype(int),
    }
)'''

for cell in notebook["cells"]:
    source = "".join(cell.get("source", []))

    source = source.replace(
        "# BCE ResNet50 Multi-Seed (52 dan 62)",
        "# Weighted BCE ResNet50 Multi-Seed (52 dan 62)",
    )
    source = source.replace(
        "Notebook ini melanjutkan eksperimen BCE standar seed 42.",
        "Notebook ini melanjutkan eksperimen Weighted BCE seed 42.",
    )
    source = source.replace(standard_weight_setup, weight_setup)
    source = source.replace(
        'OUTPUT_DIR = Path("/kaggle/working/bce_resnet50_multiseed")',
        'OUTPUT_DIR = Path("/kaggle/working/weighted_bce_resnet50_multiseed")',
    )
    source = source.replace(
        "def build_criterion():\n    return nn.BCEWithLogitsLoss()",
        "def build_criterion():\n    return nn.BCEWithLogitsLoss(pos_weight=pos_weight)",
    )
    source = source.replace(
        'print("Loss: BCEWithLogitsLoss tanpa pos_weight")\n'
        "display(class_distribution_table)",
        'print("Loss: BCEWithLogitsLoss dengan pos_weight dari data train")\n'
        "display(weight_table)",
    )
    source = source.replace(
        'checkpoint_path = seed_dir / "best_bce_resnet50.pt"',
        'checkpoint_path = seed_dir / "best_weighted_bce_resnet50.pt"',
    )
    source = source.replace(
        '"loss_function": "BCEWithLogitsLoss",\n'
        '                    "bce_pos_weight": None,',
        '"loss_function": "Weighted BCE",\n'
        '                    "pos_weight": pos_weight.detach().cpu().tolist(),',
    )
    source = source.replace(
        '"loss_function": "BCEWithLogitsLoss",\n'
        '        "bce_pos_weight": None,',
        '"loss_function": "Weighted BCE",\n'
        '        "pos_weight": pos_weight.detach().cpu().tolist(),',
    )
    source = source.replace(
        'print("\\nSeluruh training BCE multi-seed selesai.")',
        'print("\\nSeluruh training Weighted BCE multi-seed selesai.")',
    )
    source = source.replace(
        'class_distribution_table.to_csv(\n'
        '        run["seed_dir"] / "class_distribution.csv",\n'
        "        index=False,\n"
        "    )",
        'weight_table.to_csv(\n'
        '        run["seed_dir"] / "pos_weight.csv",\n'
        "        index=False,\n"
        "    )",
    )
    source = source.replace(
        'axes[0].set_title(f"BCE, seed {seed}")',
        'axes[0].set_title(f"Weighted BCE, seed {seed}")',
    )
    source = source.replace(
        '"/kaggle/working/bce_resnet50_multiseed_52_62",',
        '"/kaggle/working/weighted_bce_resnet50_multiseed_52_62",',
    )

    source = source.replace(
        '"loss_function": "BCEWithLogitsLoss"',
        '"loss_function": "Weighted BCE"',
    )
    source = source.replace(
        '"bce_pos_weight": None',
        '"pos_weight": pos_weight.detach().cpu().tolist()',
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
    "positive_counts = train_df[LABELS].sum()",
    "negative_counts = len(train_df) - positive_counts",
    "(negative_counts / positive_counts).values",
    "return nn.BCEWithLogitsLoss(pos_weight=pos_weight)",
    '"pos_weight": pos_weight.detach().cpu().tolist()',
    'seed_dir = OUTPUT_DIR / f"seed_{seed}"',
    "tuned_validation_macro_f1",
    "test_six_disease_macro_f1",
    "weighted_bce_resnet50_multiseed_52_62",
]

for fragment in required:
    assert fragment in all_code, f"Bagian wajib tidak ditemukan: {fragment}"

for forbidden in [
    "SEED = 42",
    "return nn.BCEWithLogitsLoss()",
    '"bce_pos_weight": None',
    "SigmoidFocalLoss",
    "AsymmetricLoss",
]:
    assert forbidden not in all_code, f"Konfigurasi yang tidak sesuai ditemukan: {forbidden}"

print(f"Notebook valid: {OUTPUT}")
print(f"Jumlah sel: {len(validated['cells'])}")
