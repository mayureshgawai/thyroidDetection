import logging
import sys
import os
from exception import AppException
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

class ModelFinder:
    logging.basicConfig(filename="logs/training/model_finder/modelFinder_logs",
                        filemode='a',
                        level=logging.INFO,
                        format='%(asctime)s: %(levelname)s:: %(message)s)')


    def getBestModel(self, X_train, X_test, y_train, y_test):
        """
            To find the best model for out training dataset
            :param X_train:
            :param X_test:
            :return:
        """
        params_dt = {
                'criterion': ['gini', 'entropy'],
                'splitter': ['best', 'random'],
                'max_depth': range(2, 40, 1),
                'min_samples_split': range(2, 10, 1),
                'min_samples_leaf': range(1, 10, 1)
            }

        params_svc = {
                'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
                'C': [.1, .4, .6, 1, 2, 3, 100, 200, 500],
                'gamma': [.001, .1, .4, .004, .003]
            }


        logging.info("Finding the bset model")
        try:
            # Decision Tree
            decisionTreeParam = self.getBestParams(X_train, y_train, params_dt, DecisionTreeClassifier())
            criterion = decisionTreeParam.best_params_['criterion']
            splitter = decisionTreeParam.best_params_['splitter']
            max_depth = decisionTreeParam.best_params_['max_depth']
            min_samples_split = decisionTreeParam.best_params_['min_samples_split']
            min_samples_leaf = decisionTreeParam.best_params_['min_samples_leaf']

            model_dt = DecisionTreeClassifier(criterion=criterion, splitter=splitter, max_depth=max_depth,
                                              min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf)


            # SVC
            svcParams = self.getBestParams(X_train, y_train, params_svc, SVC())
            kernel = svcParams.best_params_['kernel']
            C = svcParams.best_params_['C']
            gamma = svcParams.best_params_['gamma']

            model_svc = SVC(kernel=kernel, C=C, gamma=gamma)

            # getting Adj. R2 model
            adjDtScore = 1 - ((1 - model_dt.score(X_test, y_test)) * (len(y_test)-1)/(len(y_test) - X_test.shape[1] - 1))
            adjSvcScore = 1 - ((1 - model_svc.score(X_test, y_test)) * (len(y_test) - 1) / (len(y_test) - X_test.shape[1] - 1))
            logging.info("Adjusted R2 score for Decision tree: "+str(adjDtScore))
            logging.info("Adjusted R2 score for SVC: " + str(adjSvcScore))


            if(adjDtScore > adjSvcScore):
                return



        except Exception as e:
            raise AppException(e, sys)


    def getBestParams(self, X_train, y_train, paramGrid, model):

        grid = GridSearchCV(model, paramGrid, cv=5)
        grid.fit(X_train, y_train)

        return grid.best_params_

        # criterion = grid.best_params_['criterion']
        # splitter = grid.best_params_['splitter']
        # max_depth = grid.best_params_['max_depth']
        # min_samples_split = grid.best_params_['min_samples_split']
        # min_samples_leaf = grid.best_params_['min_samples_leaf']
