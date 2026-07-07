from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D,
    MaxPooling2D,
    Flatten,
    Dense,
    Dropout
)


def build_model():
    """
    Builds and returns the CNN model.
    """

    model = Sequential()

    # First Convolution Layer
    model.add(
        Conv2D(
            filters=32,
            kernel_size=(3, 3),
            activation="relu",
            input_shape=(28, 28, 1)
        )
    )

    # First Pooling Layer
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # Second Convolution Layer
    model.add(
        Conv2D(
            filters=64,
            kernel_size=(3, 3),
            activation="relu"
        )
    )

    # Second Pooling Layer
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # Convert feature maps into a vector
    model.add(Flatten())

    # Fully Connected Layer
    model.add(Dense(128, activation="relu"))

    # Reduce overfitting
    model.add(Dropout(0.5))

    # Output Layer
    model.add(Dense(10, activation="softmax"))

    return model


if __name__ == "__main__":
    model = build_model()
    model.summary()