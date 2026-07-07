import pickle
from pathlib import Path

import matplotlib.pyplot as plt


project_root = Path(__file__).resolve().parent.parent

history_file = project_root / "models" / "training_history.pkl"

with open(history_file, "rb") as f:
    history = pickle.load(f)


# Accuracy Graph
plt.figure(figsize=(8,5))
plt.plot(history["accuracy"], label="Training Accuracy")
plt.plot(history["val_accuracy"], label="Validation Accuracy")
plt.title("Model Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)

plt.savefig(project_root / "experiments" / "accuracy.png")

plt.close()


# Loss Graph
plt.figure(figsize=(8,5))
plt.plot(history["loss"], label="Training Loss")
plt.plot(history["val_loss"], label="Validation Loss")
plt.title("Model Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.grid(True)

plt.savefig(project_root / "experiments" / "loss.png")

plt.close()

print("Graphs generated successfully!")