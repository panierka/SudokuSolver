import pickle
import os
from PIL import Image
import numpy as np
import pandas as pd

def preprocess_testing_data(img):
    image = img.resize((28, 28))
    image_array = np.array(image).reshape(1, 784).reshape(-1)
    normalized_array = image_array / 255.0
    binary_array = (normalized_array > 0.5).astype(int)
    return pd.DataFrame(binary_array, columns=[f"pixel{i}" for i in range(1, 785)])

def main(img):
    with open('knn_model.pkl', 'rb') as file:
        model = pickle.load(file)
    X_test = preprocess_testing_data(img)
    prediction = model.predict(X_test)
    print(prediction)

if __name__ == '__main__':
    main(img)