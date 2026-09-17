def detect_intent(question, detections, ocr, mode="auto"):
    if mode and mode != "auto":
        return mode

    q = question.lower()

    if any(word in q for word in [
        "read", "text", "translate", "written",
        "summarize", "meaning", "document"
    ]):
        return "text"

    if any(word in q for word in [
        "where", "location", "landmark",
        "place", "city", "country"
    ]):
        return "location"

    if any(word in q for word in [
        "product", "brand", "model",
        "price", "buy", "specification"
    ]):
        return "product"

    if any(word in q for word in [
        "food", "dish", "ingredient",
        "calorie", "nutrition", "recipe"
    ]):
        return "food"

    if any(word in q for word in [
        "plant", "flower", "tree",
        "leaf", "care", "water"
    ]):
        return "plant"

    if any(word in q for word in [
        "animal", "breed", "species",
        "habitat"
    ]):
        return "animal"

    if any(word in q for word in [
        "diagram", "chart", "graph",
        "equation", "architecture"
    ]):
        return "diagram"

    return "general_visual"

def build_context(intent, detections, ocr):
    return {
        "intent": intent,
        "detections": detections[:10],
        "ocr": ocr[:10]
    }
