"""Create reproducible 70/15/15 patient-level multi-label splits.

The splitter is a deterministic greedy iterative stratification implementation.
It assigns rare remaining labels first while preserving each split capacity.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

LABELS = ["N", "D", "G", "C", "A", "H", "M", "O"]
SPLIT_NAMES = ("train", "validation", "test")
SPLIT_FRACTIONS = np.array([0.70, 0.15, 0.15], dtype=float)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def split_capacities(n_samples: int) -> np.ndarray:
    capacities = np.floor(n_samples * SPLIT_FRACTIONS).astype(int)
    capacities[-1] = n_samples - capacities[:-1].sum()
    return capacities


def iterative_multilabel_split(labels: np.ndarray, seed: int) -> np.ndarray:
    """Assign every patient to train, validation, or test without overlap."""
    n_samples, n_labels = labels.shape
    rng = np.random.default_rng(seed)
    capacities = split_capacities(n_samples)
    desired_label_counts = labels.sum(axis=0, keepdims=True) * SPLIT_FRACTIONS[:, None]
    assigned_label_counts = np.zeros((len(SPLIT_NAMES), n_labels), dtype=float)
    assignment = np.full(n_samples, -1, dtype=int)
    unassigned = np.ones(n_samples, dtype=bool)

    while unassigned.any():
        remaining_label_counts = labels[unassigned].sum(axis=0)
        positive_labels = np.flatnonzero(remaining_label_counts > 0)
        if len(positive_labels) == 0:
            candidates = np.flatnonzero(unassigned)
        else:
            rarest_label = positive_labels[
                np.argmin(remaining_label_counts[positive_labels])
            ]
            candidates = np.flatnonzero(unassigned & (labels[:, rarest_label] == 1))

        rng.shuffle(candidates)
        for patient_index in candidates:
            if not unassigned[patient_index]:
                continue
            patient_labels = labels[patient_index]
            unmet = (desired_label_counts[:, rarest_label] - assigned_label_counts[:, rarest_label])
            eligible = np.flatnonzero(capacities > 0)
            if len(eligible) == 0:
                raise RuntimeError("Kapasitas split habis sebelum semua pasien ditetapkan.")
            best_unmet = unmet[eligible].max()
            best = eligible[np.isclose(unmet[eligible], best_unmet)]
            if len(best) > 1:
                max_capacity = capacities[best].max()
                best = best[capacities[best] == max_capacity]
            chosen_split = int(rng.choice(best))
            assignment[patient_index] = chosen_split
            capacities[chosen_split] -= 1
            assigned_label_counts[chosen_split] += patient_labels
            unassigned[patient_index] = False

    if capacities.any():
        raise RuntimeError("Kapasitas split tidak terpenuhi.")
    return assignment


def summary(frame: pd.DataFrame) -> dict[str, object]:
    return {
        "patient_count": int(len(frame)),
        "label_counts": {label: int(frame[label].sum()) for label in LABELS},
        "label_prevalence": {
            label: round(float(frame[label].mean()), 6) for label in LABELS
        },
    }


def main() -> None:
    args = parse_args()
    manifest = pd.read_csv(args.manifest)
    missing = {"patient_id", *LABELS}.difference(manifest.columns)
    if missing:
        raise ValueError(f"Kolom manifest tidak lengkap: {sorted(missing)}")
    if manifest["patient_id"].duplicated().any():
        raise ValueError("Manifest harus memiliki satu baris untuk setiap pasien.")

    labels = manifest[LABELS].to_numpy(dtype=int)
    if not np.isin(labels, [0, 1]).all():
        raise ValueError("Label manifest harus bernilai 0 atau 1.")
    assignment = iterative_multilabel_split(labels, args.seed)

    outputs = {
        split_name: manifest.loc[assignment == split_index].copy()
        for split_index, split_name in enumerate(SPLIT_NAMES)
    }
    patient_sets = {
        split_name: set(frame["patient_id"]) for split_name, frame in outputs.items()
    }
    if any((
        patient_sets["train"] & patient_sets["validation"],
        patient_sets["train"] & patient_sets["test"],
        patient_sets["validation"] & patient_sets["test"],
    )):
        raise RuntimeError("Patient leakage terdeteksi.")
    if sum(len(values) for values in patient_sets.values()) != len(manifest):
        raise RuntimeError("Tidak semua pasien masuk tepat satu subset.")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for split_name, frame in outputs.items():
        frame.assign(split=split_name).to_csv(
            args.output_dir / f"{split_name}.csv", index=False
        )
    patient_split = pd.concat(
        [frame.assign(split=name) for name, frame in outputs.items()],
        ignore_index=True,
    )
    patient_split.to_csv(args.output_dir / "patient_split.csv", index=False)

    report = {name: summary(frame) for name, frame in outputs.items()}
    report["seed"] = args.seed
    report["split_method"] = "greedy_iterative_multilabel_stratification"
    with (args.output_dir / "split_report.json").open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
