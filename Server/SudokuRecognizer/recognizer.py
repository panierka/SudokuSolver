import os
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pickle
import pandas as pd
import numpy as np
from PIL import Image
import cv2

def get_data():
    mnist = fetch_openml('mnist_784', version=1)
    X, y = mnist['data'], mnist['target'].astype(int)
    #mask = y != 0
    #X = X[mask]
    #y = y[mask]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

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
    X_train, X_test, y_train, y_test = get_data()
    model_mnist = knn_model(3)
    model_mnist = train_model(model_mnist, X_train, y_train)
    #save_model(model_mnist, 'knn_mnist_model.pkl')
    '''
    X_train_aug, y_train_aug = get_data_from_board('data/train_data')
    X_test_aug, y_test_aug = get_and_transform_augmented_data('data/augmented_test_data')
    X_train, y_train = concatenate_training_data(X_train, X_train_aug, y_train, y_train_aug)
    X_test, y_test = concatenate_training_data(X_test, X_test_aug, y_test, y_test_aug)
    save_files(X_train, y_train, X_test, y_test)'''

if __name__ == '__main__':
    main()