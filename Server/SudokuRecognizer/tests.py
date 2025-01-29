from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd

#file with performing test on various parameters and models
def main():
    X_train, X_test, y_train, y_test = pd.read_csv("data/x_training_data.csv").drop(columns = ['Unnamed: 0']), pd.read_csv("data/x_testing_data.csv").drop(columns = ['Unnamed: 0']), pd.read_csv("data/y_training_data.csv").drop(columns = ['Unnamed: 0']), pd.read_csv("data/y_testing_data.csv").drop(columns = ['Unnamed: 0'])
    for i in range(1,10):
        model = KNeighborsClassifier(i)
        model.fit(X_train, y_train)
        print("Score: ", model.score(X_test, y_test))
        preds = model.predict(X_test)
        print(confusion_matrix(y_test, preds, labels=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'puste']))

if __name__ == '__main__':
    main()