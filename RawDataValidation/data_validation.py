import logging
import datetime

import pandas as pd

from constants import constants
from app_util.util import readYamlFile
from constants import constants
from exception import AppException
import sys
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.impute import KNNImputer

class DataValidation:
    def __init__(self):

        self.appconfig = readYamlFile(constants.CONFIG_FILE_PATH)
        logging.basicConfig(filename=r"logs\training\data_validation\data_validation_logs",
                            filemode='a',
                            level=logging.INFO,
                            format='%(asctime)s: %(levelname)s:: %(message)s)')


    def checkForNanInDataset(self, data):

        """
        Considering the summation of None values from all over the dataset. If found more than 0, return True
        :param data:
        :return: boolean
        """
        try:
            checkNull = data.isnull().sum()

            for nullCount in checkNull:
                # return True if(nullCount>0) else False
                if(nullCount>0):
                    return True
            return False
        except Exception as e:
            raise AppException(e, sys)


    def replaceWithNone(self, data):

        """
        Replacing all inappropriate data in dataset with some meaningful data to make decisions easier.
        :param data:
        :return:Dataframe
        """
        try:
            data2 = data.copy()
            for col in range(0, len(data2.columns)):
                data2[data.columns[col]] = data[data.columns[col]].apply(lambda x: None if ((x == '?') or (x == "Nan")) else x)

            return data2
        except Exception as e:
            raise AppException(e, sys)

    def encode_sex_col(self, num):
        if num == 'F':
            return int(0)
        elif num == 'M':
            return int(1)
        else:
            return num

    def handleObjectColumns(self, data):

        data['sex'] = data['sex'].apply(self.encode_sex_col)
        return data

    def encodeColumns(self, data):

        """
        Encoding all column values into numeric
        :param data:
        :return:
        """

        encode = LabelEncoder()
        for col in range(0, int(data.shape[1])):
            if(data[data.columns[col]].dtype == "object"):
                data[data.columns[col]] = encode.fit_transform(data[data.columns[col]])

        return data

    def impute(self, data):

        """
        This method is responible for imputing all None values in dataset and for binary columns checking if all imputed
        values are perfectly imputed or not.
        :param data:
        :return:Dataframe
        """

        X = data.drop(['Class'], axis=1)
        y = data['Class']

        imputer = KNNImputer(n_neighbors=5, weights='uniform', missing_values=np.nan)
        X_imputed = imputer.fit_transform(X)
        X_imputed = pd.DataFrame(X_imputed)
        X_imputed.columns = constants.COLUMN_NAMES


        # Converting wrongly converted values for binary columns
        NonBinaryColumns = constants.NON_BINARY_COLUMNS
        for col in X_imputed.columns:
            if(col in NonBinaryColumns):
                continue

            if(len(X_imputed[col].unique()) > 2):
                # X_imputed[(X_imputed[col] < 1) & (X_imputed[col] > 0)]
                X_imputed1 = X_imputed[col].apply(lambda x: 1 if (x >= 0.6) else 0)
                X_imputed[col] = X_imputed1

        return [X_imputed,y]



    def checkForUnique(self, data):

        columns = data.columns
        for col in columns:
            if(len(data[col].unique()) <= 1):
                data.drop([col], axis=1, inplace=True)

        return data



