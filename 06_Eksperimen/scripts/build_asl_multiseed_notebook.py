import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ASL ResNet50" / "asl-resnet50.ipynb"
OUTPUT = ROOT / "ASL ResNet50" / "asl-resnet50-multiseed-52-62.ipynb"


def code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.strip().splitlines()],
    }


def markdown_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.strip().splitlines()],
    }


cells = [
    markdown_cell(
        """
# ASL ResNet50 Multi-Seed (52 dan 62)

Notebook ini melanjutkan eksperimen Asymmetric Loss seed 42. Arsitektur, data split, augmentasi, optimizer, scheduler, dan parameter loss dipertahankan. Setiap seed membuat model, optimizer, scheduler, checkpoint, threshold, dan hasil test yang terpisah.
"""
    ),
    code_cell(
        r'''
from pathlib import Path
import gc
import json
import random
import shutil

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.models import ResNet50_Weights, resnet50

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    hamming_loss,
    multilabel_confusion_matrix,
    precision_recall_fscore_support,
    roc_auc_score,
)

SEEDS = [52, 62]
BATCH_SIZE = 16
NUM_WORKERS = 2
IMAGE_SIZE = 224
LEARNING_RATE = 1e-4
WEIGHT_DECAY = 1e-4
MAX_EPOCHS = 30
EARLY_STOPPING_PATIENCE = 7
DROPOUT = 0.30

ASL_GAMMA_NEG = 4.0
ASL_GAMMA_POS = 1.0
ASL_CLIP = 0.05

LABELS = ["N", "D", "G", "C", "A", "H", "M", "O"]
DISEASE_LABELS = ["D", "G", "C", "A", "H", "M"]
DISEASE_INDICES = [LABELS.index(label) for label in DISEASE_LABELS]

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

DATASET_DIR = Path(
    "/kaggle/input/datasets/kevinardhana/"
    "odir-5k-patient-level-multi-label-fundus-dataset"
)
IMAGE_DIR = DATASET_DIR / "Training Images" / "Training Images"
TRAIN_CSV = DATASET_DIR / "train.csv"
VALID_CSV = DATASET_DIR / "validation.csv"
TEST_CSV = DATASET_DIR / "test.csv"

OUTPUT_DIR = Path("/kaggle/working/asl_resnet50_multiseed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def seed_worker(worker_id):
    worker_seed = torch.initial_seed() % (2**32)
    random.seed(worker_seed)
    np.random.seed(worker_seed)


train_df = pd.read_csv(TRAIN_CSV)
valid_df = pd.read_csv(VALID_CSV)
test_df = pd.read_csv(TEST_CSV)

assert len(train_df) == 2450
assert len(valid_df) == 525
assert len(test_df) == 525
assert set(train_df["patient_id"]).isdisjoint(valid_df["patient_id"])
assert set(train_df["patient_id"]).isdisjoint(test_df["patient_id"])
assert set(valid_df["patient_id"]).isdisjoint(test_df["patient_id"])

positive_counts = train_df[LABELS].sum()
negative_counts = len(train_df) - positive_counts
class_distribution_table = pd.DataFrame(
    {
        "label": LABELS,
        "positif_train": positive_counts.values.astype(int),
        "negatif_train": negative_counts.values.astype(int),
    }
)

train_transform = transforms.Compose(
    [
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(15),
        transforms.ColorJitter(
            brightness=0.1,
            contrast=0.1,
            saturation=0.1,
            hue=0.02,
        ),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ]
)

eval_transform = transforms.Compose(
    [
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ]
)


class FundusPairDataset(Dataset):
    def __init__(self, dataframe, image_dir, transform):
        self.dataframe = dataframe.reset_index(drop=True)
        self.image_dir = Path(image_dir)
        self.transform = transform

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, index):
        row = self.dataframe.iloc[index]
        left_image = Image.open(self.image_dir / row["left_image"]).convert("RGB")
        right_image = Image.open(self.image_dir / row["right_image"]).convert("RGB")

        return {
            "left_image": self.transform(left_image),
            "right_image": self.transform(right_image),
            "labels": torch.tensor(
                row[LABELS].values.astype(np.float32),
                dtype=torch.float32,
            ),
            "patient_id": int(row["patient_id"]),
        }


class SharedResNet50(nn.Module):
    def __init__(self, num_labels=8, dropout=0.30):
        super().__init__()
        self.backbone = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
        feature_dim = self.backbone.fc.in_features
        self.backbone.fc = nn.Identity()
        self.classifier = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(feature_dim * 2, num_labels),
        )

    def forward(self, left_image, right_image):
        left_features = self.backbone(left_image)
        right_features = self.backbone(right_image)
        combined_features = torch.cat([left_features, right_features], dim=1)
        return self.classifier(combined_features)


class AsymmetricLoss(nn.Module):
    def __init__(self, gamma_neg=4.0, gamma_pos=1.0, clip=0.05, eps=1e-8):
        super().__init__()
        if gamma_neg < 0.0 or gamma_pos < 0.0:
            raise ValueError("gamma tidak boleh negatif")
        if clip < 0.0:
            raise ValueError("clip tidak boleh negatif")
        self.gamma_neg = gamma_neg
        self.gamma_pos = gamma_pos
        self.clip = clip
        self.eps = eps

    def forward(self, logits, targets):
        positive_probabilities = torch.sigmoid(logits)
        negative_probabilities = 1.0 - positive_probabilities

        if self.clip > 0.0:
            negative_probabilities = (negative_probabilities + self.clip).clamp(max=1.0)

        positive_loss = targets * torch.log(
            positive_probabilities.clamp(min=self.eps)
        )
        negative_loss = (1.0 - targets) * torch.log(
            negative_probabilities.clamp(min=self.eps)
        )
        loss = positive_loss + negative_loss

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

        return -(asymmetric_weight * loss).mean()


train_dataset = FundusPairDataset(train_df, IMAGE_DIR, train_transform)
valid_dataset = FundusPairDataset(valid_df, IMAGE_DIR, eval_transform)
test_dataset = FundusPairDataset(test_df, IMAGE_DIR, eval_transform)

valid_loader = DataLoader(
    valid_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=NUM_WORKERS,
    pin_memory=DEVICE.type == "cuda",
)
test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=NUM_WORKERS,
    pin_memory=DEVICE.type == "cuda",
)


def build_train_loader(seed):
    generator = torch.Generator()
    generator.manual_seed(seed)
    return DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=DEVICE.type == "cuda",
        worker_init_fn=seed_worker,
        generator=generator,
    )


def build_model():
    return SharedResNet50(num_labels=len(LABELS), dropout=DROPOUT).to(DEVICE)


def build_criterion():
    return AsymmetricLoss(
        gamma_neg=ASL_GAMMA_NEG,
        gamma_pos=ASL_GAMMA_POS,
        clip=ASL_CLIP,
    )


def train_one_epoch(model, loader, criterion, optimizer):
    model.train()
    total_loss = 0.0
    total_samples = 0

    for batch in loader:
        left_images = batch["left_image"].to(DEVICE, non_blocking=True)
        right_images = batch["right_image"].to(DEVICE, non_blocking=True)
        labels = batch["labels"].to(DEVICE, non_blocking=True)

        optimizer.zero_grad(set_to_none=True)
        logits = model(left_images, right_images)
        loss = criterion(logits, labels)
        loss.backward()
        optimizer.step()

        batch_size = labels.size(0)
        total_loss += loss.item() * batch_size
        total_samples += batch_size

    return total_loss / total_samples


@torch.no_grad()
def evaluate_at_threshold(model, loader, criterion, threshold=0.5):
    model.eval()
    total_loss = 0.0
    total_samples = 0
    all_labels = []
    all_probabilities = []

    for batch in loader:
        left_images = batch["left_image"].to(DEVICE, non_blocking=True)
        right_images = batch["right_image"].to(DEVICE, non_blocking=True)
        labels = batch["labels"].to(DEVICE, non_blocking=True)

        logits = model(left_images, right_images)
        loss = criterion(logits, labels)
        probabilities = torch.sigmoid(logits)

        batch_size = labels.size(0)
        total_loss += loss.item() * batch_size
        total_samples += batch_size
        all_labels.append(labels.cpu().numpy())
        all_probabilities.append(probabilities.cpu().numpy())

    true_labels = np.concatenate(all_labels, axis=0)
    probabilities = np.concatenate(all_probabilities, axis=0)
    predictions = (probabilities >= threshold).astype(np.int32)

    return {
        "loss": total_loss / total_samples,
        "macro_f1": float(
            f1_score(true_labels, predictions, average="macro", zero_division=0)
        ),
        "micro_f1": float(
            f1_score(true_labels, predictions, average="micro", zero_division=0)
        ),
    }


@torch.no_grad()
def collect_predictions(model, loader):
    model.eval()
    patient_ids = []
    all_labels = []
    all_probabilities = []

    for batch in loader:
        left_images = batch["left_image"].to(DEVICE, non_blocking=True)
        right_images = batch["right_image"].to(DEVICE, non_blocking=True)
        probabilities = torch.sigmoid(model(left_images, right_images))

        patient_ids.extend(batch["patient_id"].cpu().numpy().tolist())
        all_labels.append(batch["labels"].cpu().numpy())
        all_probabilities.append(probabilities.cpu().numpy())

    return (
        np.asarray(patient_ids),
        np.concatenate(all_labels, axis=0),
        np.concatenate(all_probabilities, axis=0),
    )


print("Device:", DEVICE)
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
print("Seed yang akan dijalankan:", SEEDS)
print("Train / validation / test:", len(train_df), len(valid_df), len(test_df))
print("ASL gamma_neg / gamma_pos / clip:", ASL_GAMMA_NEG, ASL_GAMMA_POS, ASL_CLIP)
display(class_distribution_table)
'''
    ),
    code_cell(
        r'''
training_runs = {}

for seed in SEEDS:
    print(f"\nMemulai training seed {seed}")
    set_seed(seed)

    seed_dir = OUTPUT_DIR / f"seed_{seed}"
    seed_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = seed_dir / "best_asl_resnet50.pt"
    history_path = seed_dir / "training_history.json"

    train_loader = build_train_loader(seed)
    model = build_model()
    criterion = build_criterion()
    optimizer = AdamW(
        model.parameters(),
        lr=LEARNING_RATE,
        weight_decay=WEIGHT_DECAY,
    )
    scheduler = ReduceLROnPlateau(
        optimizer,
        mode="max",
        factor=0.5,
        patience=2,
    )

    history = []
    best_macro_f1 = -1.0
    best_epoch = 0
    patience_counter = 0

    for epoch in range(1, MAX_EPOCHS + 1):
        train_loss = train_one_epoch(model, train_loader, criterion, optimizer)
        validation_result = evaluate_at_threshold(
            model,
            valid_loader,
            criterion,
            threshold=0.5,
        )

        scheduler.step(validation_result["macro_f1"])
        current_lr = optimizer.param_groups[0]["lr"]
        epoch_result = {
            "epoch": epoch,
            "train_loss": float(train_loss),
            "validation_loss": float(validation_result["loss"]),
            "validation_macro_f1": float(validation_result["macro_f1"]),
            "validation_micro_f1": float(validation_result["micro_f1"]),
            "learning_rate": float(current_lr),
        }
        history.append(epoch_result)

        print(
            f"Seed {seed} | Epoch {epoch:02d}/{MAX_EPOCHS} | "
            f"train loss: {train_loss:.4f} | "
            f"val loss: {validation_result['loss']:.4f} | "
            f"val Macro-F1: {validation_result['macro_f1']:.4f} | "
            f"val Micro-F1: {validation_result['micro_f1']:.4f} | "
            f"lr: {current_lr:.6f}"
        )

        if validation_result["macro_f1"] > best_macro_f1:
            best_macro_f1 = validation_result["macro_f1"]
            best_epoch = epoch
            patience_counter = 0
            torch.save(
                {
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "best_macro_f1": float(best_macro_f1),
                    "labels": LABELS,
                    "asl_gamma_neg": ASL_GAMMA_NEG,
                    "asl_gamma_pos": ASL_GAMMA_POS,
                    "asl_clip": ASL_CLIP,
                    "image_size": IMAGE_SIZE,
                    "dropout": DROPOUT,
                    "learning_rate": LEARNING_RATE,
                    "weight_decay": WEIGHT_DECAY,
                    "seed": seed,
                },
                checkpoint_path,
            )
            print("Checkpoint terbaik disimpan.")
        else:
            patience_counter += 1

        with open(history_path, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=2)

        if patience_counter >= EARLY_STOPPING_PATIENCE:
            print(
                f"Early stopping pada epoch {epoch}. "
                f"Checkpoint terbaik: epoch {best_epoch}."
            )
            break

    training_runs[seed] = {
        "seed_dir": seed_dir,
        "checkpoint_path": checkpoint_path,
        "history": history,
        "best_epoch": best_epoch,
        "best_macro_f1_at_050": float(best_macro_f1),
    }

    del model, optimizer, scheduler, train_loader
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

print("\nSeluruh training ASL multi-seed selesai.")
'''
    ),
    code_cell(
        r'''
evaluation_runs = {}
threshold_candidates = np.arange(0.05, 0.96, 0.01)

for seed in SEEDS:
    print(f"\nEvaluasi validation dan test seed {seed}")
    run = training_runs[seed]
    checkpoint = torch.load(
        run["checkpoint_path"],
        map_location=DEVICE,
        weights_only=False,
    )
    model = build_model()
    model.load_state_dict(checkpoint["model_state_dict"])

    (
        validation_patient_ids,
        validation_labels,
        validation_probabilities,
    ) = collect_predictions(model, valid_loader)

    best_thresholds = []
    best_validation_f1 = []

    for label_index in range(len(LABELS)):
        label_scores = []
        for threshold in threshold_candidates:
            label_predictions = (
                validation_probabilities[:, label_index] >= threshold
            ).astype(np.int32)
            label_scores.append(
                f1_score(
                    validation_labels[:, label_index],
                    label_predictions,
                    zero_division=0,
                )
            )

        best_index = int(np.argmax(label_scores))
        best_thresholds.append(float(threshold_candidates[best_index]))
        best_validation_f1.append(float(label_scores[best_index]))

    best_thresholds = np.asarray(best_thresholds, dtype=np.float32)
    default_validation_predictions = (
        validation_probabilities >= 0.5
    ).astype(np.int32)
    tuned_validation_predictions = (
        validation_probabilities >= best_thresholds
    ).astype(np.int32)

    default_validation_macro_f1 = f1_score(
        validation_labels,
        default_validation_predictions,
        average="macro",
        zero_division=0,
    )
    tuned_validation_macro_f1 = f1_score(
        validation_labels,
        tuned_validation_predictions,
        average="macro",
        zero_division=0,
    )

    threshold_table = pd.DataFrame(
        {
            "label": LABELS,
            "threshold_terbaik": best_thresholds,
            "f1_validation": best_validation_f1,
            "jumlah_positif_validation": validation_labels.sum(axis=0).astype(int),
        }
    )
    threshold_path = run["seed_dir"] / "best_thresholds.json"
    with open(threshold_path, "w", encoding="utf-8") as file:
        json.dump(
            {
                "seed": seed,
                "checkpoint_epoch": int(checkpoint["epoch"]),
                "default_validation_macro_f1": float(default_validation_macro_f1),
                "tuned_validation_macro_f1": float(tuned_validation_macro_f1),
                "thresholds": {
                    label: float(threshold)
                    for label, threshold in zip(LABELS, best_thresholds)
                },
                "validation_f1_per_label": {
                    label: float(score)
                    for label, score in zip(LABELS, best_validation_f1)
                },
            },
            file,
            indent=2,
        )

    test_patient_ids, test_labels, test_probabilities = collect_predictions(
        model,
        test_loader,
    )
    test_predictions = (test_probabilities >= best_thresholds).astype(np.int32)

    test_macro_f1 = f1_score(
        test_labels,
        test_predictions,
        average="macro",
        zero_division=0,
    )
    test_micro_f1 = f1_score(
        test_labels,
        test_predictions,
        average="micro",
        zero_division=0,
    )
    disease_macro_f1 = f1_score(
        test_labels[:, DISEASE_INDICES],
        test_predictions[:, DISEASE_INDICES],
        average="macro",
        zero_division=0,
    )
    test_macro_auroc = roc_auc_score(
        test_labels,
        test_probabilities,
        average="macro",
    )
    test_hamming_loss = hamming_loss(test_labels, test_predictions)
    test_subset_accuracy = accuracy_score(test_labels, test_predictions)

    precision, recall, label_f1, support = precision_recall_fscore_support(
        test_labels,
        test_predictions,
        average=None,
        zero_division=0,
    )
    label_auroc = [
        roc_auc_score(test_labels[:, index], test_probabilities[:, index])
        for index in range(len(LABELS))
    ]
    confusion_matrices = multilabel_confusion_matrix(test_labels, test_predictions)

    per_label_results = []
    for index, label_name in enumerate(LABELS):
        tn, fp, fn, tp = confusion_matrices[index].ravel()
        per_label_results.append(
            {
                "label": label_name,
                "precision": float(precision[index]),
                "recall": float(recall[index]),
                "f1_score": float(label_f1[index]),
                "auroc": float(label_auroc[index]),
                "support": int(support[index]),
                "threshold": float(best_thresholds[index]),
                "TN": int(tn),
                "FP": int(fp),
                "FN": int(fn),
                "TP": int(tp),
            }
        )

    per_label_table = pd.DataFrame(per_label_results)
    test_summary = {
        "loss_function": "Asymmetric Loss",
        "backbone": "ResNet50",
        "seed": seed,
        "asl_gamma_neg": ASL_GAMMA_NEG,
        "asl_gamma_pos": ASL_GAMMA_POS,
        "asl_clip": ASL_CLIP,
        "checkpoint_epoch": int(checkpoint["epoch"]),
        "validation_macro_f1": float(tuned_validation_macro_f1),
        "test_macro_f1": float(test_macro_f1),
        "test_micro_f1": float(test_micro_f1),
        "test_six_disease_macro_f1": float(disease_macro_f1),
        "test_macro_auroc": float(test_macro_auroc),
        "test_hamming_loss": float(test_hamming_loss),
        "test_subset_accuracy": float(test_subset_accuracy),
    }

    with open(run["seed_dir"] / "test_summary.json", "w", encoding="utf-8") as file:
        json.dump(test_summary, file, indent=2)
    per_label_table.to_csv(
        run["seed_dir"] / "test_metrics_per_label.csv",
        index=False,
    )
    class_distribution_table.to_csv(
        run["seed_dir"] / "class_distribution.csv",
        index=False,
    )

    prediction_data = {"patient_id": test_patient_ids}
    for index, label_name in enumerate(LABELS):
        prediction_data[f"true_{label_name}"] = test_labels[:, index].astype(int)
        prediction_data[f"prob_{label_name}"] = test_probabilities[:, index]
        prediction_data[f"pred_{label_name}"] = test_predictions[:, index].astype(int)
    pd.DataFrame(prediction_data).to_csv(
        run["seed_dir"] / "test_predictions.csv",
        index=False,
    )

    evaluation_runs[seed] = {
        "summary": test_summary,
        "per_label_table": per_label_table,
        "threshold_table": threshold_table,
    }

    print("Checkpoint epoch:", checkpoint["epoch"])
    print("Validation Macro-F1 tuned:", f"{tuned_validation_macro_f1:.4f}")
    print("Test Macro-F1 8 label:", f"{test_macro_f1:.4f}")
    print("Test Macro-F1 6 penyakit:", f"{disease_macro_f1:.4f}")
    print("Test Micro-F1:", f"{test_micro_f1:.4f}")
    print("Test Macro-AUROC:", f"{test_macro_auroc:.4f}")
    display(threshold_table)
    display(per_label_table)

    del model, checkpoint
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
'''
    ),
    code_cell(
        r'''
summary_table = pd.DataFrame(
    [evaluation_runs[seed]["summary"] for seed in SEEDS]
).sort_values("seed")

metric_columns = [
    "validation_macro_f1",
    "test_macro_f1",
    "test_micro_f1",
    "test_six_disease_macro_f1",
    "test_macro_auroc",
    "test_hamming_loss",
    "test_subset_accuracy",
]

aggregate_rows = []
for metric in metric_columns:
    values = summary_table[metric].astype(float)
    aggregate_rows.append(
        {
            "metric": metric,
            "mean_seed_52_62": float(values.mean()),
            "std_seed_52_62": float(values.std(ddof=1)),
            "minimum": float(values.min()),
            "maximum": float(values.max()),
        }
    )

aggregate_table = pd.DataFrame(aggregate_rows)
summary_table.to_csv(OUTPUT_DIR / "multiseed_test_summary.csv", index=False)
aggregate_table.to_csv(OUTPUT_DIR / "multiseed_aggregate_52_62.csv", index=False)

for seed in SEEDS:
    history_table = pd.DataFrame(training_runs[seed]["history"])
    best_epoch = training_runs[seed]["best_epoch"]
    figure, axes = plt.subplots(1, 2, figsize=(13, 5))

    axes[0].plot(history_table["epoch"], history_table["train_loss"], label="Training loss")
    axes[0].plot(history_table["epoch"], history_table["validation_loss"], label="Validation loss")
    axes[0].set_title(f"Asymmetric Loss, seed {seed}")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    axes[1].plot(
        history_table["epoch"],
        history_table["validation_macro_f1"],
        label="Validation Macro-F1",
    )
    axes[1].plot(
        history_table["epoch"],
        history_table["validation_micro_f1"],
        label="Validation Micro-F1",
    )
    axes[1].axvline(
        best_epoch,
        color="red",
        linestyle="--",
        label="Checkpoint terbaik",
    )
    axes[1].set_title(f"Performa validation, seed {seed}")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("F1-score")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(
        training_runs[seed]["seed_dir"] / "training_curves.png",
        dpi=200,
        bbox_inches="tight",
    )
    plt.show()

archive_path = shutil.make_archive(
    "/kaggle/working/asl_resnet50_multiseed_52_62",
    "zip",
    root_dir=OUTPUT_DIR,
)

print("Ringkasan setiap seed:")
display(summary_table)
print("Ringkasan seed 52 dan 62:")
display(aggregate_table)
print("Arsip unduhan:", archive_path)

for path in sorted(OUTPUT_DIR.rglob("*")):
    if path.is_file():
        print(f"- {path.relative_to(OUTPUT_DIR)}: {path.stat().st_size / 1024:.2f} KB")
'''
    ),
]


with SOURCE.open("r", encoding="utf-8") as file:
    source_notebook = json.load(file)

notebook = {
    "cells": cells,
    "metadata": source_notebook.get("metadata", {}),
    "nbformat": 4,
    "nbformat_minor": source_notebook.get("nbformat_minor", 5),
}

with OUTPUT.open("w", encoding="utf-8") as file:
    json.dump(notebook, file, ensure_ascii=False, indent=1)

print(OUTPUT)
