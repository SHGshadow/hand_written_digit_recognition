from tensorflow.keras.utils import to_categorical
import pickle
from pathlib import Path

from dataset import load_dataset
from preprocess import preprocess_data
from model import build_model


# Load dataset
x_train, y_train, x_test, y_test = load_dataset()

# Preprocess data
x_train, y_train, x_test, y_test = preprocess_data(
    x_train,
    y_train,
    x_test,
    y_test
)

# Convert labels to one-hot encoding
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# Build model
model = build_model()

# Compile model
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# Train model
history = model.fit(
    x_train,
    y_train,
    validation_data=(x_test, y_test),
    epochs=10,
    batch_size=64
)

# Save model
model.save("models/digit_model.keras")

print("\nModel saved successfully!")

#Training history

project_root = Path(__file__).resolve().parent.parent

history_path = project_root / "models" / "training_history.pkl"

with open(history_path, "wb") as f:
    pickle.dump(history.history, f)

print("Training history saved successfully!")