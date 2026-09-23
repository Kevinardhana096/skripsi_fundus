$ErrorActionPreference = "Stop"

$sourcePath = Join-Path $PSScriptRoot "BCE ResNet50\bce-baseline-resnet50-untuk-klasifikasi-multi-la (1).ipynb"
$outputDir = Join-Path $PSScriptRoot "Baseline Bilateral ResNet50 512\01_BCE\Notebooks\Ready"
$outputPath = Join-Path $outputDir "bce_seed42_ready.ipynb"

New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
$notebook = Get-Content -Raw -LiteralPath $sourcePath | ConvertFrom-Json

foreach ($cell in $notebook.cells) {
    $source = $cell.source -join ""
    $source = $source.Replace("(224, 224)", "(512, 512)")
    $source = $source.Replace("(224,224)", "(512,512)")
    $source = $source.Replace("/kaggle/working/bce_baseline", "/kaggle/working/bilateral_bce_512_seed42")
    $source = $source.Replace("best_bce_resnet50.pt", "best_bilateral_bce_resnet50_512_seed42.pt")
    $source = $source.Replace("validation_thresholds_bce", "validation_thresholds_bilateral_bce_512_seed42")
    $source = $source.Replace("test_per_class_metrics_bce", "test_per_class_metrics_bilateral_bce_512_seed42")
    $source = $source.Replace("test_confusion_matrix_bce", "test_confusion_matrix_bilateral_bce_512_seed42")
    $source = $source.Replace("test_predictions_bce", "test_predictions_bilateral_bce_512_seed42")
    $source = $source.Replace("test_metrics_bce", "test_metrics_bilateral_bce_512_seed42")
    $checkpointMetadata = '"backbone": "shared_resnet50",' + "`n" +
        '                "input_size": 512,' + "`n" +
        '                "batch_size": 16,' + "`n" +
        '                "seed": 42,'
    $source = $source.Replace('"backbone": "ResNet50",', $checkpointMetadata)
    $cell.source = @($source)
    $cell.outputs = @()
    $cell.execution_count = $null
}

# Hilangkan augmentasi geometris independen yang dapat merusak hubungan kiri-kanan.
$cell2 = $notebook.cells[2].source -join ""
$cell2 = $cell2.Replace("    transforms.RandomHorizontalFlip(p=0.5),`n", "")
$cell2 = $cell2.Replace("    transforms.RandomRotation(degrees=15),`n", "")
$cell2 = $cell2.Replace("torch.backends.cudnn.deterministic = True", "torch.backends.cudnn.deterministic = True`ntorch.backends.cudnn.benchmark = False")
$notebook.cells[2].source = @($cell2)

# Aktifkan automatic mixed precision pada training dan validation.
$cell4 = $notebook.cells[4].source -join ""
$cell4 = $cell4.Replace("criterion = nn.BCEWithLogitsLoss()", "criterion = nn.BCEWithLogitsLoss()`nscaler = torch.amp.GradScaler('cuda', enabled=DEVICE.type == 'cuda')")
$cell4 = $cell4.Replace("def train_one_epoch(model, loader, criterion, optimizer, device):", "def train_one_epoch(model, loader, criterion, optimizer, scaler, device):")
$oldTrain = @'
        optimizer.zero_grad()

        logits = model(left_images, right_images)
        loss = criterion(logits, labels)

        loss.backward()
        optimizer.step()
'@
$newTrain = @'
        optimizer.zero_grad(set_to_none=True)

        with torch.autocast(
            device_type="cuda",
            dtype=torch.float16,
            enabled=device.type == "cuda"
        ):
            logits = model(left_images, right_images)
            loss = criterion(logits, labels)

        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
'@
$cell4 = $cell4.Replace($oldTrain, $newTrain)
$oldEval = @'
        logits = model(left_images, right_images)
        loss = criterion(logits, labels)
        probabilities = torch.sigmoid(logits)
'@
$newEval = @'
        with torch.autocast(
            device_type="cuda",
            dtype=torch.float16,
            enabled=device.type == "cuda"
        ):
            logits = model(left_images, right_images)
            loss = criterion(logits, labels)
        probabilities = torch.sigmoid(logits.float())
'@
$cell4 = $cell4.Replace($oldEval, $newEval)
$notebook.cells[4].source = @($cell4)

$cell5 = $notebook.cells[5].source -join ""
$cell5 = $cell5.Replace("        optimizer=optimizer,`n        device=DEVICE", "        optimizer=optimizer,`n        scaler=scaler,`n        device=DEVICE")
$notebook.cells[5].source = @($cell5)

# Tambahkan pengenal eksperimen pada awal notebook.
$header = [PSCustomObject]@{
    cell_type = "markdown"
    metadata = [PSCustomObject]@{}
    source = @("# Baseline Bilateral ResNet50 512 x 512 - BCE - Seed 42`n", "`n", "Pilot resolusi 512 dengan shared backbone, batch fisik 16, mixed precision, dan split pasien yang telah dikunci.")
}
$notebook.cells = @($header) + @($notebook.cells)

$notebook.metadata.kernelspec = [PSCustomObject]@{
    display_name = "Python 3"
    language = "python"
    name = "python3"
}

$json = $notebook | ConvertTo-Json -Depth 100
Set-Content -LiteralPath $outputPath -Value $json -Encoding utf8
Write-Output $outputPath
