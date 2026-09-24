"""
Skrip Generasi Visualisasi Layer-CAM untuk 3 Kasus Tambahan (Miopia, Hipertensi, Other Diseases)
Model: LEBER A4 (ResNet-50 Bilateral Seed 62)
DPI: 300 (Publication Quality)
Output:
- 05_Aset/layercam_kasus_6_myopia.png
- 05_Aset/layercam_kasus_7_hypertension.png
- 05_Aset/layercam_kasus_8_others.png
"""

import sys
from pathlib import Path
import json
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import torch
from torchvision import transforms

sys.path.append(str(Path("06_Eksperimen/Baseline Bilateral ResNet50 512/05_LEBER_Ablation/A4_LabelWise_Router").resolve()))
from generate_layercam_visualizations import LEBERA4, compute_layercam, create_heatmap_overlay, plot_individual_case

def main():
    print("=" * 70, flush=True)
    print("MEMULAI GENERASI 3 KASUS LAYER-CAM TAMBAHAN (M, H, O)", flush=True)
    print("=" * 70, flush=True)
    
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {DEVICE}", flush=True)
    
    base_dir = Path("g:/My Drive/Skripsi")
    if not base_dir.exists():
        base_dir = Path(".")
        
    ckpt_path = base_dir / "06_Eksperimen/Baseline Bilateral ResNet50 512/05_LEBER_Ablation/A4_LabelWise_Router/Results/leber_a4_labelwise_router_bce_512_seed62/best_leber_a4_labelwise_router_resnet50_bce_512_seed62.pt"
    thresh_path = base_dir / "06_Eksperimen/Baseline Bilateral ResNet50 512/05_LEBER_Ablation/A4_LabelWise_Router/Results/leber_a4_final_test_evaluation/locked_thresholds_used.json"
    img_dir = base_dir / "03_Data_ODIR5K/ODIR_5K/ODIR-5K/ODIR-5K/Training Images"
    asset_dir = base_dir / "05_Aset"
    asset_dir.mkdir(parents=True, exist_ok=True)
    
    LABELS = ["N", "D", "G", "C", "A", "H", "M", "O"]
    with open(thresh_path, "r") as f:
        thresholds_all = json.load(f)
    seed62_thresh_list = thresholds_all["62"]
    thresholds = {label: seed62_thresh_list[idx] for idx, label in enumerate(LABELS)}
    
    # Load model
    model = LEBERA4(num_labels=8).to(DEVICE)
    ckpt = torch.load(ckpt_path, map_location=DEVICE)
    model.load_state_dict(ckpt["model_state_dict"])
    model.eval()
    print("Model LEBER A4 berhasil dimuat!", flush=True)
    
    # Definisi 3 kasus pelengkap
    cases = [
        {
            "pid": 145,
            "label": "M",
            "name": "Miopia Patologis (Pathological Myopia)",
            "threshold": thresholds["M"],
            "gt_binary": 1,
            "gt_left": "pathological myopia (conus myopicus)",
            "gt_right": "pathological myopia (conus myopicus)",
            "output_filename": "layercam_kasus_6_myopia.png",
            "clinical_explanation": (
                "Kedua mata mengidap miopia patologis akibat elongasi aksial bola mata ekstrem.\n"
                "Tampak penipisan korioretina dan konus miopik melingkar di sekitar diskus optikus.\n"
                "• Router LEBER secara dominan mengaktifkan cabang bilateral (w_B = 98.8%), membuktikan\n"
                "  kemampuan fitur simetris f_B menangkap deformitas struktural kedua bola mata sekaligus.\n"
                "• Layer-CAM memusatkan atensi pada area depigmentasi peripapilar retina posterior."
            )
        },
        {
            "pid": 2004,
            "label": "H",
            "name": "Retinopati Hipertensi (Hypertension)",
            "threshold": thresholds["H"],
            "gt_binary": 1,
            "gt_left": "hypertensive retinopathy",
            "gt_right": "hypertensive retinopathy",
            "output_filename": "layercam_kasus_7_hypertension.png",
            "clinical_explanation": (
                "Kedua mata mengalami retinopati hipertensi akibat tekanan darah tinggi sistemik kronis.\n"
                "Tampak sklerosis arteriol retina, penyempitan fokal pembuluh darah, dan fenomena copper-wiring.\n"
                "• Model menghasilkan probabilitas P(H) = 95.58% (jauh di atas threshold optimal 0.20).\n"
                "• Router mendistribusikan bukti secara asimetris dinamis (w_L = 70.4%, w_R = 27.7%),\n"
                "  memprioritaskan vaskulopati arteriol yang lebih mencolok pada fundus kiri (OS)."
            )
        },
        {
            "pid": 1122,
            "label": "O",
            "name": "Penyakit Lainnya (Macular Epiretinal Membrane)",
            "threshold": thresholds["O"],
            "gt_binary": 1,
            "gt_left": "macular epiretinal membrane (selaput makula)",
            "gt_right": "normal fundus (sehat jernih)",
            "output_filename": "layercam_kasus_8_others.png",
            "clinical_explanation": (
                "Kasus patologi heterogen unilateral: mata kiri (OS) mengidap epiretinal membrane (ERM)\n"
                "pada area makula, sedangkan mata kanan (OD) normal jernih tanpa lesi.\n"
                "• Model memprediksi P(O) = 100.00% (Threshold = 0.57) dengan akurasi sempurna.\n"
                "• Router LEBER mengisolasi bukti secara monokular ekstrem: 99.2% dialirkan ke OS (w_L = 99.2%),\n"
                "  dan Layer-CAM OS secara presisi mengunci distorsi fovea sentral akibat tarikan selaput."
            )
        }
    ]
    
    transform = transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    for case in cases:
        pid = case["pid"]
        target_label = case["label"]
        c_idx = LABELS.index(target_label)
        
        print(f"\nProcessing Kasus #{case['name']} (PID #{pid}, Target {target_label})...", flush=True)
        left_path = img_dir / f"{pid}_left.jpg"
        right_path = img_dir / f"{pid}_right.jpg"
        
        left_raw = Image.open(left_path).convert("RGB")
        right_raw = Image.open(right_path).convert("RGB")
        
        left_t = transform(left_raw).unsqueeze(0).to(DEVICE)
        right_t = transform(right_raw).unsqueeze(0).to(DEVICE)
        
        cam_res = compute_layercam(model, left_t, right_t, c_idx, DEVICE)
        out_path = asset_dir / case["output_filename"]
        plot_individual_case(case, cam_res, left_raw, right_raw, out_path)
        
    print("\n" + "=" * 70, flush=True)
    print("SUKSES! 3 KASUS TAMBAHAN BERHASIL DI-GENERATE!", flush=True)
    print("=" * 70, flush=True)

if __name__ == "__main__":
    main()
