from pathlib import Path

import numpy as np

from tensorflow.keras.models import load_model


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "digit_model.keras"

model = load_model(MODEL_PATH)


def preprocess_image(image_array):
    """
    Convert image into CNN input format.
    """

    image = image_array.astype("float32") / 255.0

    image = image.reshape(1, 28, 28, 1)

    return image