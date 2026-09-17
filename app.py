from flask import Flask, render_template, request, jsonify
from PIL import Image
import io, base64
from services.pipeline import analyze_region

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/analyze")
def analyze():
    data = request.get_json(silent=True) or {}
    image_data = data.get("image")
    question = (data.get("question") or "What is this?").strip()
    mode = data.get("mode", "auto")

    if not image_data:
        return jsonify({"error": "No selected image region was received."}), 400

    try:
        image = decode_data_url(image_data)
        result = analyze_region(image, question, mode)
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

def decode_data_url(data_url):
    if "," not in data_url:
        raise ValueError("Invalid image data.")
    _, encoded = data_url.split(",", 1)
    return Image.open(io.BytesIO(base64.b64decode(encoded))).convert("RGB")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
