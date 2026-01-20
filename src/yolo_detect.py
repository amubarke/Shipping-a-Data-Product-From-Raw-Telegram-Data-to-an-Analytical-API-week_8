# src/yolo_detect.py

import os
import csv
from ultralytics import YOLO

# -----------------------------
# 1. Configuration
# -----------------------------

IMAGE_ROOT_DIR = r"E:\Shipping-a-Data-Product-From-Raw-Telegram-Data-to-an-Analytical-API-week_8\data\raw\images"
OUTPUT_CSV = "data/processed/yolo_detections.csv"

MODEL_NAME = "yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.5

PRODUCT_OBJECTS = {"bottle", "box", "container", "package", "tube", "jar", "pill"}

# -----------------------------
# 2. Load YOLO model
# -----------------------------

model = YOLO(MODEL_NAME)

# -----------------------------
# 3. Helper functions
# -----------------------------

def extract_message_id(filename):
    """
    Extract message_id from image filename like 180746.jpg
    """
    return int(os.path.splitext(filename)[0])


def classify_image(detected_objects):
    has_person = "person" in detected_objects
    has_product = any(obj in PRODUCT_OBJECTS for obj in detected_objects)

    if has_person and has_product:
        return "promotional"
    elif has_product and not has_person:
        return "product_display"
    elif has_person and not has_product:
        return "lifestyle"
    else:
        return "other"

# -----------------------------
# 4. Run detection
# -----------------------------

results_rows = []

for channel_folder in os.listdir(IMAGE_ROOT_DIR):
    channel_path = os.path.join(IMAGE_ROOT_DIR, channel_folder)

    if not os.path.isdir(channel_path):
        continue

    for file_name in os.listdir(channel_path):
        if not file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        image_path = os.path.join(channel_path, file_name)
        message_id = extract_message_id(file_name)

        detections = model(image_path)[0]

        detected_objects = []
        confidence_scores = []

        for box in detections.boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = model.names[cls_id]

            if confidence >= CONFIDENCE_THRESHOLD:
                detected_objects.append(class_name)
                confidence_scores.append(confidence)

                results_rows.append({
                    "message_id": message_id,
                    "image_name": file_name,
                    "detected_class": class_name,
                    "confidence_score": round(confidence, 3)
                })

        if not detected_objects:
            results_rows.append({
                "message_id": message_id,
                "image_name": file_name,
                "detected_class": "none",
                "confidence_score": 0.0
            })
            image_category = "other"
        else:
            image_category = classify_image(detected_objects)

        for row in results_rows:
            if row["image_name"] == file_name and row["message_id"] == message_id:
                row["image_category"] = image_category

# -----------------------------
# 5. Save results
# -----------------------------

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "message_id",
            "image_name",
            "detected_class",
            "confidence_score",
            "image_category"
        ]
    )
    writer.writeheader()
    writer.writerows(results_rows)

print("YOLO detection completed successfully.")
