import numpy as np
from utils import Utils
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn import svm
from sklearn import preprocessing
from sklearn.linear_model import BayesianRidge, LogisticRegression, SGDRegressor, Perceptron, PassiveAggressiveRegressor, RANSACRegressor, TheilSenRegressor

# Train and test using the given classifier with k-fold cross-validation
def classify(X, y, k, clf):
	# Split data into folds
	kf = KFold(n_splits=k, shuffle=True)
	splits = kf.split(X)
	
	abs_err = 0
	per_err = 0
	count = 0
	r2_scores = 0

	for train_index, test_index in splits:
		X_train, X_test = X[train_index], X[test_index]
		y_train, y_test = y[train_index], y[test_index]
		clf.fit(X_train, y_train)
		y_pred = clf.predict(X_test)

		abs_err += mean_absolute_error(y_test, y_pred)
		per_err += np.mean(np.abs((y_test - y_pred) / y_test) * 100)
		r2_scores += r2_score(y_test, y_pred)

	#Some statistics
	for i in range(len(y_pred)):
		if np.mean(np.abs((y_test[i]-y_pred[i]))/y_test[i])*100 >= 20:
			'''print("True price: " + str(round(y_test[i], 2)) + 
					 "\nEst. price: " + str(round(y_pred[i], 2)) +
					 "\nAbsolute error: " + str(round(np.abs(y_test[i]-y_pred[i]), 2)) +
					 "\nPercentage error: " + str(round(np.mean(np.abs((y_test[i]-y_pred[i]))/y_test[i])*100, 2)) +
					 "\nBuilding type: " + str(round(X_test[i][6], 2)) + "\n")
			'''
			count += 1

	print("===========================================================")
	print("Number of  properties with >= 20% error: " + str(count))
	print("Mean absolute percentage error: " + str(round(per_err/k, 2)))
	print("Mean absolute error: " + str(round(abs_err/k, 2)))
	print("Mean R2 scores: " + str(round(r2_scores/k, 2)))
	print("")

def main():
	#houses = Utils.get_house_data('../RemaxScrape/remaxDataset2.json', region="Victoria")
	houses = Utils.get_house_data("../RemaxScrape/remaxVanDataset.json", region="Vancouver")
	print("Total listings: " + str(len(houses)) + "\n")
	X, y = Utils.create_matrices(houses, 10)

	# Scale feature data a bit (doesn't seem to help much)
	X = preprocessing.scale(X) 

	n_splits = 5
	
	print("Support Vector Regression with " + str(n_splits) + "-fold cross-validation")
	classify(X, y, n_splits, svm.SVR())  

	print("Bayesian Ridge Regression with " + str(n_splits) + "-fold cross-validation")
	classify(X, y, n_splits, BayesianRidge())

	print("Logistic Regression with " + str(n_splits) + "-fold cross-validation, liblinear solver")
	classify(X, y, n_splits, LogisticRegression(solver="liblinear"))
	'''
	print("Logistic Regression with " + str(n_splits) + "-fold cross-validation, newton-cg solver")
	classify(X, y, n_splits, LogisticRegression(solver="newton-cg"))
	
	print("Logistic Regression with " + str(n_splits) + "-fold cross-validation, lbfgs solver")
	classify(X, y, n_splits, LogisticRegression(solver="lbfgs"))
	'''
	print("Stochastic Gradient Descent Regressor with " + str(n_splits) + "-fold cross-validation, squared loss")
	classify(X, y, n_splits, SGDRegressor(loss="squared_loss"))

	print("Stochastic Gradient Descent Regressor with " + str(n_splits) + "-fold cross-validation, huber loss")
	classify(X, y, n_splits, SGDRegressor(loss="huber"))
	
	print("Stochastic Gradient Descent Regressor with " + str(n_splits) + "-fold cross-validation, epsilon insensitive loss")
	classify(X, y, n_splits, SGDRegressor(loss="epsilon_insensitive"))

	print("Stochastic Gradient Descent Regressor with " + str(n_splits) + "-fold cross-validation, squared epsilon insensitive loss")
	classify(X, y, n_splits, SGDRegressor(loss="squared_epsilon_insensitive"))
	
	print("Perceptron with " + str(n_splits) + "-fold cross-validation")
	classify(X, y, n_splits, Perceptron())
	
	print("Passive-Aggressive Regressor with " + str(n_splits) + "-fold cross-validation")
	classify(X, y, n_splits, PassiveAggressiveRegressor())
	
	print("RANSAC Regressor with " + str(n_splits) + "-fold cross-validation")
	classify(X, y, n_splits, RANSACRegressor())
	
	print("Theil-Sen Regressor with " + str(n_splits) + "-fold cross-validation")
	classify(X, y, n_splits, TheilSenRegressor())
	
if __name__ == "__main__":
	main()
