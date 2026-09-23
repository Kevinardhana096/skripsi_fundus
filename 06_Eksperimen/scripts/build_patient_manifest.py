"""Build and validate a patient-level manifest from the labelled ODIR-5K data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


LABELS = ["N", "D", "G", "C", "A", "H", "M", "O"]
REQUIRED_COLUMNS = ["ID", "Left-Fundus", "Right-Fundus", *LABELS]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--excel", type=Path, required=True, help="Path to data.xlsx")
    parser.add_argument(
        "--images-dir", type=Path, required=True, help="Path to Training Images"
    )
    parser.add_argument(
        "--output-dir", type=Path, required=True, help="Directory for manifest outputs"
    )
    return parser.parse_args()


def validate_columns(frame: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Kolom wajib tidak ditemukan: {missing}")


def main() -> None:
    args = parse_args()
    if not args.excel.is_file():
        raise FileNotFoundError(f"File label tidak ditemukan: {args.excel}")
    if not args.images_dir.is_dir():
        raise NotADirectoryError(f"Folder citra tidak ditemukan: {args.images_dir}")

    frame = pd.read_excel(args.excel)
    validate_columns(frame)

    if frame["ID"].duplicated().any():
        duplicates = frame.loc[frame["ID"].duplicated(), "ID"].tolist()
        raise ValueError(f"patient_id duplikat ditemukan: {duplicates[:10]}")

    labels = frame[LABELS].apply(pd.to_numeric, errors="raise").astype(int)
    invalid = ~labels.isin([0, 1]).all(axis=1)
    if invalid.any():
        raise ValueError("Label harus bernilai 0 atau 1.")

    manifest = pd.DataFrame(
        {
            "patient_id": frame["ID"].astype(int),
            "left_image": frame["Left-Fundus"].astype(str),
            "right_image": frame["Right-Fundus"].astype(str),
        }
    )
    manifest = pd.concat([manifest, labels], axis=1)
    manifest["label_count"] = labels.sum(axis=1)
    manifest["is_multilabel"] = (manifest["label_count"] > 1).astype(int)

    manifest["left_exists"] = manifest["left_image"].map(
        lambda name: (args.images_dir / name).is_file()
    )
    manifest["right_exists"] = manifest["right_image"].map(
        lambda name: (args.images_dir / name).is_file()
    )
    missing_images = manifest.loc[
        ~manifest["left_exists"] | ~manifest["right_exists"],
        ["patient_id", "left_image", "right_image", "left_exists", "right_exists"],
    ]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = args.output_dir / "patient_manifest.csv"
    report_path = args.output_dir / "manifest_report.json"
    missing_path = args.output_dir / "missing_images.csv"

    report = {
        "patient_count": int(len(manifest)),
        "expected_image_count": int(len(manifest) * 2),
        "missing_image_count": int((~manifest["left_exists"]).sum() + (~manifest["right_exists"]).sum()),
        "multilabel_patient_count": int(manifest["is_multilabel"].sum()),
        "label_counts": {label: int(manifest[label].sum()) for label in LABELS},
    }

    manifest.to_csv(manifest_path, index=False)
    with report_path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
    missing_images.to_csv(missing_path, index=False)

    print(json.dumps(report, indent=2))
    print(f"Manifest tersimpan: {manifest_path}")
    print(f"Laporan tersimpan: {report_path}")
    if not missing_images.empty:
        raise RuntimeError(f"Ada citra yang tidak ditemukan. Lihat: {missing_path}")


if __name__ == "__main__":
    main()
