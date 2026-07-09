from pathlib import Path

import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist

(_, _), (x_test, y_test) = mnist.load_data()

project_root = Path(__file__).resolve().parent.parent
output_dir = project_root / "test_images"
output_dir.mkdir(exist_ok=True)

index = 0  # Change this to save a different digit

plt.imsave(
    output_dir / f"digit_{y_test[index]}.png",
    x_test[index],
    cmap="gray"
)

print(f"Saved: test_images/digit_{y_test[index]}.png")