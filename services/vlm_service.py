import os
import io
from PIL import Image

def answer_with_vlm(image, question, intent, context):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "answer": fallback_answer(question, intent, context),
            "source": "local_cv_pipeline",
            "warning": "GEMINI_API_KEY is missing. Add it to .env for open-ended multimodal reasoning."
        }

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        prompt = f"""
You are the multimodal reasoning engine of VisionCircle.

The user selected ONLY the supplied image region.

User question:
{question}

Detected intent:
{intent}

YOLO detections:
{context["detections"]}

OCR results:
{context["ocr"]}

Tasks:
1. Understand the selected visual region.
2. Identify the relevant object, scene, text, food, plant, animal,
   product, landmark, diagram, or other content.
3. Answer the user's exact question.
4. Use YOLO and OCR only as supporting evidence; visually verify them.
5. If the selected region contains several things, explain which one
   is most relevant.
6. Never invent an exact identity, model, location, price, species,
   or other fact when the image is insufficient.
7. For location questions, clearly distinguish visual inference
   from confirmed location.
8. For products, do not claim an exact model unless the visual evidence
   supports it.
9. Give a useful, structured answer without unnecessary technical jargon.

Return only the final answer for the user.
"""

        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
            contents=[prompt, image]
        )

        return {
            "answer": response.text,
            "source": "Gemini multimodal AI",
            "warning": None
        }

    except Exception as exc:
        return {
            "answer": fallback_answer(question, intent, context),
            "source": "local_cv_pipeline",
            "warning": f"VLM failed: {exc}"
        }

def fallback_answer(question, intent, context):
    labels = [
        item["label"]
        for item in context["detections"]
        if item.get("confidence", 0) > 0
    ]

    texts = [
        item["text"]
        for item in context["ocr"]
        if item.get("confidence", 0) > 0
    ]

    answer = [
        f"Analysis type: {intent}."
    ]

    if labels:
        answer.append(
            "YOLO detected: " + ", ".join(labels[:8]) + "."
        )

    if texts:
        answer.append(
            "OCR detected text: " + " | ".join(texts[:8]) + "."
        )

    answer.append(
        "Configure GEMINI_API_KEY to enable open-ended multimodal "
        "visual reasoning for arbitrary selected content."
    )

    return " ".join(answer)
