from fastapi import FastAPI, UploadFile, File

from backend.predict import predict_digit
from backend.schemas import PredictionResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Handwritten Digit Recognition API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Handwritten Digit Recognition API is running!"
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):

    digit, confidence = predict_digit(file.file)

    return PredictionResponse(
        digit=digit,
        confidence=confidence
    )