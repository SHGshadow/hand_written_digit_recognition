from pathlib import Path
import pickle

import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay,
)

from tensorflow.keras.models import load_model

from dataset import load_dataset
from preprocess import preprocess_data


# ----------------------------------------------------
# Project Paths
# ----------------------------------------------------
project_root = Path(__file__).resolve().parent.parent

history_path = project_root / "models" / "training_history.pkl"
model_path = project_root / "models" / "digit_model.keras"
experiment_path = project_root / "experiments"

experiment_path.mkdir(exist_ok=True)

# ----------------------------------------------------
# Load History
# ----------------------------------------------------
with open(history_path, "rb") as f:
    history = pickle.load(f)

# ----------------------------------------------------
# Accuracy Graph
# ----------------------------------------------------
plt.figure(figsize=(8,5))

plt.plot(history["accuracy"], label="Training Accuracy")
plt.plot(history["val_accuracy"], label="Validation Accuracy")

plt.title("Training Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)

plt.savefig(experiment_path / "accuracy.png")
plt.close()

# ----------------------------------------------------
# Loss Graph
# ----------------------------------------------------
plt.figure(figsize=(8,5))

plt.plot(history["loss"], label="Training Loss")
plt.plot(history["val_loss"], label="Validation Loss")

plt.title("Training Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.grid(True)

plt.savefig(experiment_path / "loss.png")
plt.close()

# ----------------------------------------------------
# Load Dataset
# ----------------------------------------------------
x_train, y_train, x_test, y_test = load_dataset()

x_train, y_train, x_test, y_test = preprocess_data(
    x_train,
    y_train,
    x_test,
    y_test,
)

# ----------------------------------------------------
# Load Model
# ----------------------------------------------------
model = load_model(model_path)

# ----------------------------------------------------
# Predictions
# ----------------------------------------------------
predictions = model.predict(x_test)

predicted_labels = np.argmax(predictions, axis=1)

# ----------------------------------------------------
# Confusion Matrix
# ----------------------------------------------------
cm = confusion_matrix(y_test, predicted_labels)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=np.arange(10),
)

fig, ax = plt.subplots(figsize=(8,8))

disp.plot(ax=ax)

plt.savefig(experiment_path / "confusion_matrix.png")

plt.close()

# ----------------------------------------------------
# Classification Report
# ----------------------------------------------------
report = classification_report(
    y_test,
    predicted_labels
)

with open(experiment_path / "classification_report.txt", "w") as f:
    f.write(report)

print(report)

# ----------------------------------------------------
# Sample Predictions
# ----------------------------------------------------
plt.figure(figsize=(10,10))

for i in range(25):

    plt.subplot(5,5,i+1)

    plt.imshow(
        x_test[i].reshape(28,28),
        cmap="gray"
    )

    plt.title(
        f"Pred: {predicted_labels[i]}"
    )

    plt.axis("off")

plt.tight_layout()

plt.savefig(
    experiment_path /
    "sample_predictions.png"
)

plt.close()

print("\nEvaluation completed successfully!")