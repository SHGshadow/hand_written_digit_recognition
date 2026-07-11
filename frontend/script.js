console.log("Page loaded at:", new Date().toLocaleTimeString());
// ===============================
// Get Canvas
// ===============================

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

// ===============================
// Canvas Style
// ===============================

ctx.fillStyle = "black";
ctx.fillRect(0, 0, canvas.width, canvas.height);

ctx.strokeStyle = "white";
ctx.lineWidth = 18;
ctx.lineCap = "round";
ctx.lineJoin = "round";

// ===============================
// Drawing Variables
// ===============================

let drawing = false;

// ===============================
// Start Drawing
// ===============================

canvas.addEventListener("mousedown", startDrawing);

function startDrawing(event) {

    drawing = true;

    const rect = canvas.getBoundingClientRect();

    ctx.beginPath();

    ctx.moveTo(
        event.clientX - rect.left,
        event.clientY - rect.top
    );

}

// ===============================
// Draw
// ===============================

canvas.addEventListener("mousemove", draw);

function draw(event) {

    if (!drawing) return;

    const rect = canvas.getBoundingClientRect();

    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    ctx.lineTo(x, y);
    ctx.stroke();

}

// ===============================
// Stop Drawing
// ===============================

canvas.addEventListener("mouseup", stopDrawing);
canvas.addEventListener("mouseleave", stopDrawing);

function stopDrawing() {

    drawing = false;

    ctx.beginPath();

}

// ===============================
// Clear Canvas
// ===============================

document
    .getElementById("clearBtn")
    .addEventListener("click", clearCanvas);

function clearCanvas() {

    ctx.fillStyle = "black";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    ctx.beginPath();

    document.getElementById("prediction").textContent = "-";
    document.getElementById("confidence").textContent = "-";

}

// ===============================
// Check if Canvas is Empty
// ===============================

function isCanvasBlank() {

    const pixels = ctx.getImageData(
        0,
        0,
        canvas.width,
        canvas.height
    ).data;

    for (let i = 0; i < pixels.length; i += 4) {

        if (
            pixels[i] !== 0 ||
            pixels[i + 1] !== 0 ||
            pixels[i + 2] !== 0
        ) {
            return false;
        }

    }

    return true;

}

// ===============================
// Predict Button
// ===============================

document
    .getElementById("predictBtn")
    .addEventListener("click", predictDigit);

async function predictDigit() {
    alert("Predict function started");

    if (isCanvasBlank()) {

        alert("Please draw a digit first.");

        return;

    }

    document.getElementById("prediction").textContent = "...";
    document.getElementById("confidence").textContent = "Predicting...";

    canvas.toBlob(async (blob) => {

        const formData = new FormData();

        formData.append(
            "file",
            blob,
            "digit.png"
        );

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/predict",
                {
                    method: "POST",
                    body: formData
                }
            );

            if (!response.ok) {

                throw new Error(
                    `Server Error: ${response.status}`
                );

            }

            const text = await response.text();

            console.log("Raw response:", text);

            const result = JSON.parse(text);

            document.getElementById("prediction").textContent =
                result.digit;

            document.getElementById("confidence").textContent =
                (result.confidence * 100).toFixed(2) + "%";

        }
        catch (error) {

            console.error(error);

            document.getElementById("prediction").textContent = "Error";
            document.getElementById("confidence").textContent = "-";

            alert("Unable to connect to the backend.");

        }

    }, "image/png");

}