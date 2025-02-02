import os
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pickle
import pandas as pd
import numpy as np
from PIL import Image
import cv2
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow_datasets import load
import scipy.io

def get_data():
    df_train = scipy.io.loadmat('data/train_32x32.mat')
    df_test = scipy.io.loadmat('data/test_32x32.mat')
    # Extract images and labels
    X_train = np.array(df_train['X'])  # Shape: (32, 32, 3, num_samples)
    y_train = np.array(df_train['y'])  # Shape: (num_samples, 1)
    X_test = np.array(df_test['X'])
    y_test = np.array(df_test['y'])
    # Convert images from (H, W, C, N) to (N, H, W, C) for TensorFlow compatibility
    X_train = np.transpose(X_train, (3, 0, 1, 2))
    X_test = np.transpose(X_test, (3, 0, 1, 2))
    # Convert labels to integers (MATLAB often uses 1-based indexing, change to 0-based)
    y_train = y_train.flatten()
    y_test = y_test.flatten()
    y_train[y_train == 10] = 0  # Example: Convert '10' (used for digit '0') to 0
    y_test[y_test == 10] = 0

    # Convert NumPy arrays to TensorFlow Dataset
    train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
    test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test))

    # Preprocessing function (normalize images)
    def preprocess(image, label):
        image = tf.image.rgb_to_grayscale(image)
        image = tf.cast(image, tf.float32) / 255.0  # Normalize to [0, 1]
        return image, label

    # Apply preprocessing, shuffle, batch, and prefetch
    train_dataset = train_dataset.map(preprocess).shuffle(10000).batch(64).prefetch(tf.data.AUTOTUNE)
    test_dataset = test_dataset.map(preprocess).shuffle(10000).batch(64).prefetch(tf.data.AUTOTUNE)
    # Print final dataset structure

    return train_dataset, test_dataset



def preproces(image, label):
    image = tf.cast(image, tf.float32)
    image /= 255.0
    return image, label

def get_and_transform_augmented_data(dir):
    to_df = []
    for path in [file for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file))]:
        image = cv2.imread(dir + "/" + path)
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(image, (21, 21), 0)
        image = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        #cv2.imwrite(dir + "/tests/" + path, image)
        image_array = np.array(image).reshape(1,784).reshape(-1)
        normalized_array = image_array / 255.0
        binary_array = (normalized_array > 0.5).astype(int)
        to_df.append(binary_array)
    return pd.DataFrame(to_df, columns = [f"pixel{i}" for i in range(1, 785)]), pd.Series(np.full((len(to_df), 1), 'puste').reshape(-1))

def get_data_from_board(dir):
    to_df = []
    labels = pd.read_csv('data/train_data_labels.csv', sep = ";", header = 0)['label'].reset_index(drop = True).values
    for path in os.listdir(dir):
        image = cv2.imread(dir + "/" + path)
        image = cv2.resize(image, (28, 28))
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(image, (15, 15), 0)
        image = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        cv2.imwrite("data/tests/" + path, image)
        image_array = np.array(image).reshape(1, 784).reshape(-1)
        normalized_array = image_array / 255.0
        binary_array = (normalized_array > 0.5).astype(int)
        to_df.append(binary_array)
    return pd.DataFrame(to_df, columns=[f"pixel{i}" for i in range(1, 785)]), labels

def concatenate_training_data(X_train, X_train_aug, y_train, y_train_aug):
    return pd.concat([X_train, X_train_aug], axis = 0), pd.concat([y_train, y_train_aug], axis = 0)

def save_files(X_train, y_train, X_test, y_test):
    X_train.to_csv("data/x_training_data.csv")
    y_train.to_csv("data/y_training_data.csv")
    X_test.to_csv("data/x_testing_data.csv")
    y_test.to_csv("data/y_testing_data.csv")

def knn_model(n):
    model = KNeighborsClassifier(n_neighbors=n)
    return model

def build_lenet5():
    model = keras.Sequential([
        layers.Conv2D(6, kernel_size=5, padding='same', activation='relu', input_shape=(32, 32, 1)),
        layers.AveragePooling2D(pool_size=2, strides=2),
        layers.Conv2D(16, kernel_size=5, activation='relu'),
        layers.AveragePooling2D(pool_size=2, strides=2),
        layers.Flatten(),
        layers.Dense(120, activation='relu'),
        layers.Dense(84, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    return model
'''
    # Evaluate the model
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in testloader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()


    print(f"Accuracy: {100 * correct / total:.2f}%")
'''
def train_model(model, X_train, y_train):
    model.fit(X_train, y_train)
    return model

def save_model(model, path):
    with open(path, 'wb') as file:
        pickle.dump(model, file)

def main():
    #X_train_bin, y_train_bin = get_data_from_board('data/training_data_cells')
    #model_bin = knn_model(3)
    #model_bin = train_model(model_bin, X_train_bin, y_train_bin)
    #save_model(model_bin, 'knn_binary_model.pkl')
    train_df, test_df = get_data()
    #x_train = np.expand_dims(X_train, axis=-1)  # Add channel dimension
    #x_test = np.expand_dims(X_test, axis=-1)
    model = build_lenet5()
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(train_df, epochs=20, validation_data=test_df)
    # Save the model
    model.save("lenet5_mnist.h5")
    #model_mnist = knn_model(3)
    #model_mnist = train_model(model_mnist, X_train, y_train)


    #save_model(model_mnist, 'knn_mnist_model.pkl')
    '''
    X_train_aug, y_train_aug = get_data_from_board('data/train_data')
    X_test_aug, y_test_aug = get_and_transform_augmented_data('data/augmented_test_data')
    X_train, y_train = concatenate_training_data(X_train, X_train_aug, y_train, y_train_aug)
    X_test, y_test = concatenate_training_data(X_test, X_test_aug, y_test, y_test_aug)
    save_files(X_train, y_train, X_test, y_test)'''

if __name__ == '__main__':
    main()