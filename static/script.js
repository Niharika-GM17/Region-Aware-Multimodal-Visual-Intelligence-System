const fileInput = document.getElementById("fileInput");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const analyzeBtn = document.getElementById("analyzeBtn");
const clearBtn = document.getElementById("clearBtn");

const question = document.getElementById("question");
const mode = document.getElementById("mode");

const answer = document.getElementById("answer");
const status = document.getElementById("status");
const emptyState = document.getElementById("emptyState");

let image = new Image();

let drawing = false;
let selected = false;

let startX = 0;
let startY = 0;
let endX = 0;
let endY = 0;

fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];

    if (!file) return;

    const reader = new FileReader();

    reader.onload = (event) => {
        image.onload = () => {

            const maxWidth = 1000;
            const scale = Math.min(
                1,
                maxWidth / image.width
            );

            canvas.width = Math.round(image.width * scale);
            canvas.height = Math.round(image.height * scale);

            emptyState.style.display = "none";

            redraw();

            selected = false;
            analyzeBtn.disabled = true;

            answer.textContent =
                "Draw a circle around anything you want to analyze.";
        };

        image.src = event.target.result;
    };

    reader.readAsDataURL(file);
});

function getMousePosition(event) {
    const rect = canvas.getBoundingClientRect();

    return {
        x: (event.clientX - rect.left) *
           (canvas.width / rect.width),

        y: (event.clientY - rect.top) *
           (canvas.height / rect.height)
    };
}

canvas.addEventListener("mousedown", (event) => {

    const point = getMousePosition(event);

    startX = point.x;
    startY = point.y;

    endX = startX;
    endY = startY;

    drawing = true;
    selected = false;

    analyzeBtn.disabled = true;
});

canvas.addEventListener("mousemove", (event) => {

    if (!drawing) return;

    const point = getMousePosition(event);

    endX = point.x;
    endY = point.y;

    redraw();
    drawSelection();
});

canvas.addEventListener("mouseup", () => {

    drawing = false;

    if (
        Math.abs(endX - startX) > 10 &&
        Math.abs(endY - startY) > 10
    ) {
        selected = true;
        analyzeBtn.disabled = false;
    }
});

function redraw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    if (image.src) {
        ctx.drawImage(
            image,
            0,
            0,
            canvas.width,
            canvas.height
        );
    }
}

function drawSelection() {

    const centerX = (startX + endX) / 2;
    const centerY = (startY + endY) / 2;

    const radiusX = Math.abs(endX - startX) / 2;
    const radiusY = Math.abs(endY - startY) / 2;

    ctx.beginPath();

    ctx.ellipse(
        centerX,
        centerY,
        radiusX,
        radiusY,
        0,
        0,
        Math.PI * 2
    );

    ctx.strokeStyle = "#ff0000";
    ctx.lineWidth = 5;

    ctx.stroke();
}

function createSelectedImage() {

    const x = Math.min(startX, endX);
    const y = Math.min(startY, endY);

    const width = Math.abs(endX - startX);
    const height = Math.abs(endY - startY);

    const selectedCanvas =
        document.createElement("canvas");

    selectedCanvas.width = Math.max(
        1,
        Math.round(width)
    );

    selectedCanvas.height = Math.max(
        1,
        Math.round(height)
    );

    const selectedContext =
        selectedCanvas.getContext("2d");

    selectedContext.drawImage(
        canvas,
        x,
        y,
        width,
        height,
        0,
        0,
        width,
        height
    );

    return selectedCanvas.toDataURL(
        "image/jpeg",
        0.92
    );
}

function addBadge(container, text) {

    const element =
        document.createElement("span");

    element.className = "badge";
    element.textContent = text;

    container.appendChild(element);
}

clearBtn.addEventListener("click", () => {

    if (image.src) {
        redraw();
    }

    selected = false;
    analyzeBtn.disabled = true;

    answer.textContent =
        "Draw a circle around anything you want to analyze.";

    document.getElementById("detections").textContent =
        "No analysis yet.";

    document.getElementById("ocr").textContent =
        "No analysis yet.";

    document.getElementById("segmentation").textContent =
        "No analysis yet.";

    document.getElementById("intent").textContent =
        "Auto";

    status.textContent = "";
});

analyzeBtn.addEventListener("click", async () => {

    if (!selected) return;

    analyzeBtn.disabled = true;

    status.textContent =
        "Running YOLO + OCR + SAM + multimodal AI...";

    try {

        const response = await fetch(
            "/api/analyze",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    image: createSelectedImage(),
                    question: question.value,
                    mode: mode.value
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Analysis failed."
            );
        }

        answer.textContent = data.answer;

        document.getElementById("intent")
            .textContent = data.intent;

        const detections =
            document.getElementById("detections");

        detections.innerHTML = "";

        if (
            data.detections &&
            data.detections.length
        ) {

            data.detections.forEach((item) => {

                if (item.confidence > 0) {

                    addBadge(
                        detections,
                        `${item.label} — ` +
                        `${(item.confidence * 100).toFixed(1)}%`
                    );
                }
            });

        } else {

            detections.textContent =
                "No objects detected.";
        }

        const ocr =
            document.getElementById("ocr");

        ocr.innerHTML = "";

        if (data.ocr && data.ocr.length) {

            data.ocr.forEach((item) => {

                if (item.confidence > 0) {

                    addBadge(
                        ocr,
                        `${item.text} — ` +
                        `${(item.confidence * 100).toFixed(1)}%`
                    );
                }
            });

        } else {

            ocr.textContent =
                "No readable text detected.";
        }

        const segmentation =
            document.getElementById("segmentation");

        if (
            data.segmentation &&
            data.segmentation.available
        ) {

            segmentation.textContent =
                `Mask generated: ` +
                `${data.segmentation.foreground_pixels} ` +
                `foreground pixels.`;

        } else {

            segmentation.textContent =
                data.segmentation?.reason ||
                data.segmentation?.error ||
                "Segmentation unavailable.";
        }

        status.textContent =
            data.warning || "Analysis complete.";

    } catch (error) {

        status.textContent = "Error";

        answer.textContent =
            error.message;

    } finally {

        analyzeBtn.disabled = false;
    }
});
