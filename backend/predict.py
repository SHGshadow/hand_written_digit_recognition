import numpy as np

from backend.model_utils import model, preprocess_image


def predict_digit(image_file):

    image = preprocess_image(image_file)

    prediction = model.predict(image, verbose=0)

    digit = int(np.argmax(prediction))

    confidence = float(np.max(prediction))

    return digit, confidence