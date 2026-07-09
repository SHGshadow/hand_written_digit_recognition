from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "digit_model.keras"

EXPERIMENT_PATH = PROJECT_ROOT / "experiments"
EXPERIMENT_PATH.mkdir(exist_ok=True)

# --------------------------------------------------
# Load Model
# --------------------------------------------------

model = load_model(MODEL_PATH)


def preprocess_image(image_file):
    """
    Preprocess an uploaded image to match the MNIST format.
    Saves intermediate preprocessing images for debugging.
    """

    # --------------------------------------------------
    # 1. Read image
    # --------------------------------------------------

    image = Image.open(image_file).convert("L")

    image = np.array(image)

    cv2.imwrite(
        str(EXPERIMENT_PATH / "1_original.png"),
        image
    )

    # --------------------------------------------------
    # 2. Invert colors
    # --------------------------------------------------

    image = 255 - image

    cv2.imwrite(
        str(EXPERIMENT_PATH / "2_inverted.png"),
        image
    )

    # --------------------------------------------------
    # 3. Threshold
    # --------------------------------------------------

    _, image = cv2.threshold(
        image,
        30,
        255,
        cv2.THRESH_BINARY
    )

    cv2.imwrite(
        str(EXPERIMENT_PATH / "3_threshold.png"),
        image
    )

    # --------------------------------------------------
    # 4. Find Bounding Box
    # --------------------------------------------------

    points = cv2.findNonZero(image)

    if points is None:
        raise ValueError("No digit detected.")

    x, y, w, h = cv2.boundingRect(points)

    digit = image[y:y + h, x:x + w]

    cv2.imwrite(
        str(EXPERIMENT_PATH / "4_cropped.png"),
        digit
    )

    # --------------------------------------------------
    # 5. Resize while preserving aspect ratio
    # --------------------------------------------------

    SIZE = 20

    height, width = digit.shape

    if height > width:

        new_height = SIZE
        new_width = max(1, int(width * SIZE / height))

    else:

        new_width = SIZE
        new_height = max(1, int(height * SIZE / width))

    digit = cv2.resize(
        digit,
        (new_width, new_height),
        interpolation=cv2.INTER_AREA
    )

    cv2.imwrite(
        str(EXPERIMENT_PATH / "5_resized.png"),
        digit
    )

    # --------------------------------------------------
    # 6. Put digit in center of 28x28 image
    # --------------------------------------------------

    canvas = np.zeros((28, 28), dtype=np.uint8)

    x_offset = (28 - new_width) // 2
    y_offset = (28 - new_height) // 2

    canvas[
        y_offset:y_offset + new_height,
        x_offset:x_offset + new_width
    ] = digit

    cv2.imwrite(
        str(EXPERIMENT_PATH / "6_final_28x28.png"),
        canvas
    )

    # --------------------------------------------------
    # 7. Normalize
    # --------------------------------------------------

    canvas = canvas.astype("float32") / 255.0

    canvas = canvas.reshape(1, 28, 28, 1)

    return canvas