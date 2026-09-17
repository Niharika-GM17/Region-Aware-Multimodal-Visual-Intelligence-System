import os

_model = None

def _get_model():
    global _model

    if _model is None:
        from ultralytics import YOLO
        model_name = os.getenv("YOLO_MODEL", "yolo26n.pt")
        _model = YOLO(model_name)

    return _model

def detect_objects(image):
    try:
        model = _get_model()
        confidence = float(os.getenv("YOLO_CONF", "0.20"))

        results = model.predict(
            source=image,
            conf=confidence,
            verbose=False
        )

        detections = []

        for result in results:
            if result.boxes is None:
                continue

            names = result.names

            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence_value = float(box.conf[0])
                x1, y1, x2, y2 = [
                    round(value, 2)
                    for value in box.xyxy[0].tolist()
                ]

                detections.append({
                    "label": names[class_id],
                    "confidence": round(confidence_value, 3),
                    "box": [x1, y1, x2, y2]
                })

        detections.sort(
            key=lambda item: item["confidence"],
            reverse=True
        )

        return detections[:20]

    except Exception as exc:
        return [{
            "label": "YOLO unavailable",
            "confidence": 0,
            "box": [],
            "error": str(exc)
        }]
