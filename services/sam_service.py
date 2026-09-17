import os

_model = None

def _get_model():
    global _model

    if _model is None:
        from ultralytics import SAM
        model_name = os.getenv("SAM_MODEL", "sam2.1_b.pt")
        _model = SAM(model_name)

    return _model

def segment_selected_region(image, box):
    if not box or os.getenv("ENABLE_SAM", "true").lower() != "true":
        return {
            "available": False,
            "reason": "SAM disabled or no YOLO box was available."
        }

    try:
        model = _get_model()

        results = model.predict(
            source=image,
            bboxes=[box],
            verbose=False
        )

        if not results or results[0].masks is None:
            return {
                "available": False,
                "reason": "SAM did not return a mask."
            }

        mask = results[0].masks.data[0].cpu().numpy()

        return {
            "available": True,
            "width": int(mask.shape[1]),
            "height": int(mask.shape[0]),
            "foreground_pixels": int(mask.sum())
        }

    except Exception as exc:
        return {
            "available": False,
            "error": str(exc)
        }
