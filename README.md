# Region-Aware Multimodal Visual Intelligence System

## VisionCircle

VisionCircle is an interactive multimodal computer-vision application.

A user uploads an image, draws a circle around any region, and asks a question about that selected region.

## 🧠 System Architecture
               IMAGE
               ↓
       User draws a circle
               ↓
       Selected Region
               ↓
      ┌────────────────┐
      │ Vision Pipeline │
      └───────┬────────┘
              ↓
      What is selected?
              ↓
   ┌──────────┼───────────┐
   ↓          ↓           ↓
 Object      Text       Scene/Place
   ↓          ↓           ↓
Analysis     OCR       Geo/Context
   └──────────┼───────────┘
              ↓
       Multimodal AI
              ↓
       Relevant Answer
       ---
## Why multiple models?

YOLO is useful for fast predefined object detection.

OCR handles text.

SAM 2 provides promptable segmentation.

The Vision-Language Model provides open-ended visual understanding and visual question answering.

Together they allow the application to handle content that is not limited to one fixed object-detection label set.

## Setup — Windows

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Open `.env` and add your Gemini API key:

```text
GEMINI_API_KEY=your_key_here
```

Run:

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## First run

YOLO and SAM model weights may be downloaded automatically by Ultralytics.

EasyOCR may also download its language model on its first run.

SAM 2 is significantly heavier than YOLO. CPU-only systems may take a while.

## Example questions

After circling a region:

```text
What is this?
Where is this?
Explain this.
What is this product?
What are the ingredients?
What plant is this?
What animal is this?
Read the text.
What does this diagram mean?
```

## Important limitation

The system should not claim that an uncertain visual inference is a confirmed fact.

For example, visual geolocation is inherently uncertain unless the image contains decisive evidence.

## Project modules

- `app.py` — Flask API and web server
- `services/pipeline.py` — orchestration
- `services/yolo_service.py` — YOLO
- `services/ocr_service.py` — OCR
- `services/sam_service.py` — SAM 2
- `services/specialist_service.py` — intent routing
- `services/vlm_service.py` — Gemini multimodal reasoning
- `templates/index.html` — interface
- `static/script.js` — image selection and API calls
- `static/style.css` — UI

## Future upgrades

- Real web search for current product/location information
- Visual similarity search using CLIP
- Dedicated geolocation model
- Multiple region selection
- User accounts
- Analysis history
- PostgreSQL/MongoDB
- Docker deployment
- Authentication and rate limiting
