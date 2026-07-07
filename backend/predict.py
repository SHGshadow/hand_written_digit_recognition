import numpy as np

from model_utils import model
from model_utils import preprocess_image


def predict_digit(image):

    image = preprocess_image(image)

    prediction = model.predict(image, verbose=0)

    digit = int(np.argmax(prediction))

    confidence = float(np.max(prediction))

    return digit, confidence