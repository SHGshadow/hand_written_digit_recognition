from tensorflow.keras.datasets import mnist


def load_dataset():
    """
    Load the MNIST handwritten digit dataset.
    Returns:
        x_train, y_train, x_test, y_test
    """

    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    return x_train, y_train, x_test, y_test


if __name__ == "__main__":

    x_train, y_train, x_test, y_test = load_dataset()

    print("Training Images :", x_train.shape)
    print("Training Labels :", y_train.shape)

    print("Testing Images :", x_test.shape)
    print("Testing Labels :", y_test.shape)