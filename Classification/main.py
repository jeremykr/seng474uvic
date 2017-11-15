import numpy as np
from utils import Utils
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error
from sklearn import svm
from sklearn import preprocessing

def main():
    houses = Utils.get_house_data('../RemaxScrape/remaxDataset2.json')
    X, y = Utils.create_matrices(houses, 9)

    # Scale feature data a bit (doesn't seem to help much)
    X = preprocessing.scale(X) 

    # Split data into folds
    n_splits = 3
    kf = KFold(n_splits=n_splits, shuffle=True)
    split = kf.split(X)

    # Support Vector Regression
    clf = svm.SVR()
    print("Support Vector Regression with " + str(n_splits) + "-fold cross-validation")
    print("==========mean absolute error==========")
    err = 0
    for train_index, test_index in split:
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        err += mean_absolute_error(y_test, y_pred)
    print(err/n_splits)
    
if __name__ == "__main__":
    main()
