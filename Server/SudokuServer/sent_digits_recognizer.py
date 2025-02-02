import pickle
import os
from PIL import Image
import numpy as np
import pandas as pd
import cv2
from tensorflow import keras


with open('knn_mnist_model.pkl', 'rb') as file:
    model_mnist = pickle.load(file)



def preprocess_testing_data(img):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    n = 8
    img = img[n:50 - n, n:50 - n]
    img = cv2.resize(img, (32, 32))
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    #cv2.imwrite('std.jpg', img)
    #image_array = np.array(img).reshape(1, 784).reshape(-1)
    normalized_array = np.array(img) / 255.0
    binary_array = (normalized_array > 0.5).astype(int)
    #cv2.imwrite('std.jpg', binary_array)
    return binary_array


def main(img):
    X_test = preprocess_testing_data(img)
    model = keras.models.load_model("lenet5_mnist.h5")
    single_image_batch = np.expand_dims(X_test, axis=0)
    predictions = model.predict(single_image_batch)
    print(predictions)
    predicted_label = np.argmax(predictions)
    print(predicted_label)
    #prediction = model.predict(X_test.reshape(1, -1).unsqueeze(0).to(device))
    #print(model_mnist.predict_proba(X_test.reshape(1, -1)))
    return predicted_label
