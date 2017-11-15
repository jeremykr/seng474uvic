import numpy as np
from utils import Utils
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error
from sklearn import svm
from sklearn import preprocessing
from sklearn.linear_model import BayesianRidge, LogisticRegression, SGDRegressor, Perceptron, PassiveAggressiveRegressor, RANSACRegressor, TheilSenRegressor

# Train and test using the given classifier with k-fold cross-validation
def classify(X, y, k, clf):
    # Split data into folds
    kf = KFold(n_splits=k, shuffle=True)
    splits = kf.split(X)

    err = 0
    for train_index, test_index in splits:
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        err += mean_absolute_error(y_test, y_pred)
    print(err/k)

def main():
    houses = Utils.get_house_data('../RemaxScrape/remaxDataset2.json')
    print("Total listings: " + str(len(houses)))
    X, y = Utils.create_matrices(houses, 8)

    # Scale feature data a bit (doesn't seem to help much)
    X = preprocessing.scale(X) 

    n_splits = 5
    
    print("Support Vector Regression with " + str(n_splits) + "-fold cross-validation")
    print("==========mean absolute error==========")
    classify(X, y, 5, svm.SVR())
    print()  

    print("Bayesian Ridge Regression with " + str(n_splits) + "-fold cross-validation")
    print("==========mean absolute error==========")
    classify(X, y, 5, BayesianRidge())
    print()

    print("Logistic Regression with " + str(n_splits) + "-fold cross-validation, liblinear solver")
    print("==========mean absolute error==========")
    classify(X, y, 5, LogisticRegression(solver="liblinear"))
    print()

    print("Logistic Regression with " + str(n_splits) + "-fold cross-validation, newton-cg solver")
    print("==========mean absolute error==========")
    classify(X, y, 5, LogisticRegression(solver="newton-cg"))
    print()

    print("Logistic Regression with " + str(n_splits) + "-fold cross-validation, lbfgs solver")
    print("==========mean absolute error==========")
    classify(X, y, 5, LogisticRegression(solver="lbfgs"))
    print()

    print("Stochastic Gradient Descent Regressor with " + str(n_splits) + "-fold cross-validation, squared loss")
    print("==========mean absolute error==========")
    classify(X, y, 5, SGDRegressor(loss="squared_loss"))
    print()

    print("Stochastic Gradient Descent Regressor with " + str(n_splits) + "-fold cross-validation, huber loss")
    print("==========mean absolute error==========")
    classify(X, y, 5, SGDRegressor(loss="huber"))
    print()
    
    print("Stochastic Gradient Descent Regressor with " + str(n_splits) + "-fold cross-validation, epsilon insensitive loss")
    print("==========mean absolute error==========")
    classify(X, y, 5, SGDRegressor(loss="epsilon_insensitive"))
    print()

    print("Stochastic Gradient Descent Regressor with " + str(n_splits) + "-fold cross-validation, squared epsilon insensitive loss")
    print("==========mean absolute error==========")
    classify(X, y, 5, SGDRegressor(loss="squared_epsilon_insensitive"))
    print()
    
    print("Perceptron with " + str(n_splits) + "-fold cross-validation")
    print("==========mean absolute error==========")
    classify(X, y, 5, Perceptron())
    print()
    
    print("Passive-Aggressive Regressor with " + str(n_splits) + "-fold cross-validation")
    print("==========mean absolute error==========")
    classify(X, y, 5, PassiveAggressiveRegressor())
    print()
    
    print("RANSAC Regressor with " + str(n_splits) + "-fold cross-validation")
    print("==========mean absolute error==========")
    classify(X, y, 5, RANSACRegressor())
    print()
    
    print("Theil-Sen Regressor with " + str(n_splits) + "-fold cross-validation")
    print("==========mean absolute error==========")
    classify(X, y, 5, TheilSenRegressor())
    print()

if __name__ == "__main__":
    main()
