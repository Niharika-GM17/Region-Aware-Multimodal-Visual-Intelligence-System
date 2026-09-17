import os

_reader = None

def _get_reader():
    global _reader

    if _reader is None:
        import easyocr
        use_gpu = os.getenv("EASYOCR_GPU", "false").lower() == "true"
        _reader = easyocr.Reader(["en"], gpu=use_gpu)

    return _reader

def extract_text(image):
    try:
        import numpy as np

        reader = _get_reader()
        results = reader.readtext(np.array(image))

        return [
            {
                "text": text,
                "confidence": round(float(confidence), 3)
            }
            for _, text, confidence in results
        ]

    except Exception as exc:
        return [{
            "text": "OCR unavailable",
            "confidence": 0,
            "error": str(exc)
        }]
