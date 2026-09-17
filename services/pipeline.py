from services.yolo_service import detect_objects
from services.ocr_service import extract_text
from services.sam_service import segment_selected_region
from services.specialist_service import detect_intent, build_context
from services.vlm_service import answer_with_vlm

def analyze_region(image, question, mode):
    detections = detect_objects(image)
    ocr = extract_text(image)
    intent = detect_intent(question, detections, ocr, mode)

    segmentation = segment_selected_region(
        image,
        detections[0]["box"] if detections else None
    )

    context = build_context(intent, detections, ocr)

    vlm = answer_with_vlm(
        image=image,
        question=question,
        intent=intent,
        context=context
    )

    return {
        "success": True,
        "intent": intent,
        "detections": detections,
        "ocr": ocr,
        "segmentation": segmentation,
        "answer": vlm["answer"],
        "source": vlm["source"],
        "warning": vlm.get("warning")
    }
