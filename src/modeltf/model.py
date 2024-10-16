import tensorflow as tf
import pandas as pd
import numpy as np

from tensorflow.keras.optimizers import Adam

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# Paths
base_path = Path(__file__).parent
modelsave_path = Path(__file__).parent.parent.parent

def load_data():
    csv_file = base_path / "sample_data" / "melb_data.csv"

    base_frame = pd.read_csv(csv_file)

    df = base_frame[['Rooms', 'Bathroom', 'Landsize', 'Lattitude', 'Longtitude', 'Price']].copy()
    df = df.dropna()

    return df


def split_data(data):
    x = data[['Rooms', 'Bathroom', 'Landsize', 'Lattitude', 'Longtitude']].copy()
    y = data['Price'].copy()

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    return x_train, x_test, y_train, y_test


def create_model(normalizer, adam_optimizer):
    model = tf.keras.Sequential([
        normalizer,
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    model.compile(loss='mean_squared_error', optimizer=adam_optimizer, metrics=['r2_score'])

    return model


def reset_weights(model):
    for layer in model.layers:
        if hasattr(layer, 'kernel_initializer') and hasattr(layer, 'bias_initializer'):
            # Reinitialize weights and biases
            layer.kernel.assign(layer.kernel_initializer(tf.shape(layer.kernel)))
            layer.bias.assign(layer.bias_initializer(tf.shape(layer.bias)))


def main():
    # Load the data from csv
    data = load_data()

    # Split the Data into Training and Testing
    x_train, x_test, y_train, y_test = split_data(data)

    # Normalize the Data and Create Optimizer
    normalizer = tf.keras.layers.Normalization(axis=-1)
    normalizer.adapt(tf.convert_to_tensor(x_train))

    optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)

    # Create the Model
    model = create_model(normalizer, optimizer)

    # Fit the Model
    model.fit(x_train, y_train, epochs=20)

    # Predict Model and Evaluate Results
    y_pred = model.predict(x_test)
    print(r2_score(y_test, y_pred))

    # Save the Model
    modelsave = modelsave_path /  "saved_model.keras"
    model.save(modelsave)

    # Reset the weights of the model
    # reset_weights(model)


if __name__ == "__main__":
    main()