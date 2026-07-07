from pydantic import BaseModel


class PredictionResponse(BaseModel):

    digit: int

    confidence: float