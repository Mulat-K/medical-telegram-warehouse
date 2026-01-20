import csv
from pathlib import Path
from ultralytics import YOLO

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
IMAGE_DIR = BASE_DIR / "data" / "raw" / "images"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_CSV = OUTPUT_DIR / "image_detections.csv"

# --------------------------------------------------
# Load Model
# --------------------------------------------------
model = YOLO("yolov8n.pt")

# --------------------------------------------------
# Classification Logic
# --------------------------------------------------
def classify_image(objects):
    has_person = "person" in objects
    has_product = any(o in objects for o in ["bottle", "cup", "container"])

    if has_person and has_product:
        return "promotional"
    elif has_product and not has_person:
        return "product_display"
    elif has_person and not has_product:
        return "lifestyle"
    else:
        return "other"

# --------------------------------------------------
# Detection Loop
# --------------------------------------------------
rows = []

for channel_dir in IMAGE_DIR.iterdir():
    if not channel_dir.is_dir():
        continue

    channel_name = channel_dir.name

    for image_path in channel_dir.glob("*.jpg"):
        message_id = image_path.stem

        results = model(image_path, verbose=False)
        detected_objects = []
        confidences = []

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]
                conf = float(box.conf[0])

                detected_objects.append(label)
                confidences.append(conf)

        image_category = classify_image(detected_objects)
        avg_conf = round(sum(confidences) / len(confidences), 3) if confidences else None

        rows.append({
            "message_id": message_id,
            "channel_name": channel_name,
            "detected_objects": ",".join(set(detected_objects)),
            "confidence_score": avg_conf,
            "image_category": image_category
        })

# --------------------------------------------------
# Write CSV
# --------------------------------------------------
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["message_id", "channel_name", "detected_objects", "confidence_score", "image_category"]
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"Detection completed. Output saved to {OUTPUT_CSV}")
