const canvas = document.getElementById("canvas");

const ctx = canvas.getContext("2d");

ctx.fillStyle = "black";
ctx.fillRect(0,0,canvas.width,canvas.height);

ctx.strokeStyle = "white";
ctx.lineWidth = 18;
ctx.lineCap = "round";

let drawing = false;

canvas.addEventListener("mousedown", (event) => {

    drawing = true;

    const rect = canvas.getBoundingClientRect();

    ctx.beginPath();

    ctx.moveTo(
        event.clientX - rect.left,
        event.clientY - rect.top
    );

});

canvas.addEventListener("mouseup",()=>{

    drawing = false;

    ctx.beginPath();

});

canvas.addEventListener("mousemove",(event)=>{

    if(!drawing) return;

    const rect = canvas.getBoundingClientRect();

    const x = event.clientX - rect.left;

    const y = event.clientY - rect.top;

    ctx.lineTo(x,y);

    ctx.stroke();

    ctx.beginPath();

    ctx.moveTo(x,y);

});

document.getElementById("clearBtn").addEventListener("click", () => {

    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Reset drawing path
    ctx.beginPath();

    // Clear previous prediction
    document.getElementById("prediction").textContent = "-";
    document.getElementById("confidence").textContent = "-";

});

function isCanvasBlank(canvas) {

    const context = canvas.getContext("2d");

    const pixels = context.getImageData(
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

const predictBtn = document.getElementById("predictBtn");

predictBtn.addEventListener("click", async () => {

    if (isCanvasBlank(canvas)) {

        alert("Please draw a digit first.");

        return;

    }

    // Convert canvas to Blob
    canvas.toBlob(async (blob) => {

        const formData = new FormData();

        formData.append("file", blob, "digit.png");

        try {
            document.getElementById("prediction").textContent = "...";
            document.getElementById("confidence").textContent = "Predicting...";

            const response = await fetch(
                "http://127.0.0.1:8000/predict",
                {
                    method: "POST",
                    body: formData
                }
            );

            if (!response.ok) {

                throw new Error(`HTTP Error ${response.status}`);

            }

            const result = await response.json();

            document.getElementById("prediction").textContent =
                result.digit;

            document.getElementById("confidence").textContent =
                (result.confidence * 100).toFixed(2) + "%";

        }
        catch (error) {

            alert("Unable to connect to the server.");

            console.error(error);

        }

    }, "image/png");

});