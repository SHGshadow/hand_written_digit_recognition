from fastapi import FastAPI

app = FastAPI(
    title="Handwritten Digit Recognition API",
    version="1.0.0"
)


@app.get("/")
def home():

    return {
        "message": "Handwritten Digit Recognition API is running!"
    }