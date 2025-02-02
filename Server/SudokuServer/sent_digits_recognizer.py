import pickle
import os
from PIL import Image
import numpy as np
import pandas as pd
import cv2


with open('knn_mnist_model.pkl', 'rb') as file:
    model_mnist = pickle.load(file)


def preprocess_testing_data(img):
    img = cv2.resize(img, (28, 28))
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    #cv2.imwrite('std.jpg', img)
    image_array = np.array(img).reshape(1, 784).reshape(-1)
    normalized_array = image_array / 255.0
    binary_array = (normalized_array > 0.5).astype(int)
    #cv2.imwrite('std.jpg', binary_array)
    return binary_array


def main(img):
    X_test = preprocess_testing_data(img)
    prediction = model_mnist.predict(X_test.reshape(1, -1))

    return prediction[0]
