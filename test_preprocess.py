from src.dataset import load_dataset
from src.preprocess import preprocess_data

x_train, y_train, x_test, y_test = load_dataset()

x_train, y_train, x_test, y_test = preprocess_data(
    x_train,
    y_train,
    x_test,
    y_test
)

print("Training Shape :", x_train.shape)
print("Testing Shape :", x_test.shape)
print("Data Type :", x_train.dtype)
print("Pixel Range :", x_train.min(), "-", x_train.max())