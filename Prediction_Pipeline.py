import logging
import datetime
from exception import AppException
import sys
from app_util.util import readYamlFile
import os
from constants import constants
from RawDataValidation import DataValidation
from data_from_database import MySqlDBConnect
import pandas as pd
from sklearn.model_selection import train_test_split
from Data_Clustering import Clustering
from model_selection import ModelFinder
from File_operations import FileOperations
from PredictionMethod import Predictions
from RawDataValidation import DataValidation

class Prediction:

    def __init__(self):
        self.appConfig = readYamlFile(constants.CONFIG_FILE_PATH)
        self.dbConenct = MySqlDBConnect()
        self.cluster = Clustering()
        self.fileOperations = FileOperations()
        self.prediction = Predictions()
        self.validation = DataValidation()
        logging.basicConfig(filename="logs/prediction/prediction_pipeline/prediction_logs.txt",
                            filemode='a',
                            level=logging.INFO,
                            format='%(asctime)s: %(levelname)s:: %(message)s)')


    def predict(self):
        try:
            logging.info("Prediction Pipeline Started")

            # create database connection (MySql instance created on "clever cloud")
            conncetion = self.dbConenct.getConenction()
            # fetching all data from database
            data = self.dbConenct.getPredictData(conncetion)

            logging.info("Successfully retrieved data from database and created dataframe")

            logging.info("Performing some data cleaning before moving to the prediction")
            # replacing all "?" and or improper string with None with dataset
            data = self.validation.replaceWithNone(data)

            # "sex" is object column with string data in it, so we cannot convert its datatype directly
            # we have to encode it first. We cannot directly encode it with None values in it. So we can use "apply()"
            # Replacing Female:0 and Male:1
            data = self.validation.handleObjectColumns(data)

            # Removing outliers from "age column"
            # Age should be between 10 and 90 only.
            # data['age'] = pd.to_numeric(data['age'])
            # data = data[(data['age'] < 90) & (data['age'] > 10)]

            # Removing columns with no unique values or None values
            # Encoding of the data
            data = self.validation.encodeColumns(data)

            # Checking for unqiue values in columns
            columnsToBeDeleted = self.validation.checkForUniqueForPred(data)

            nullPresent = self.validation.checkForNanInDataset(data)
            if (nullPresent):
                # Applying imputer
                X_imputed = self.validation.predImpute(data)

            logging.info("Data Cleaning Done!!")

            logging.info("Data clustering")
            data = self.cluster.cluster_prediction(X_imputed, columnsToBeDeleted)

            listOfNums = data['cluster'].unique()

            for cluster in listOfNums:
                dataSeperation = data[data['cluster'] == int(cluster)]
                features = data.drop(['cluster'], axis=1)

                predicted_data = self.prediction.prediction(features, cluster, columnsToBeDeleted)
                # loading predicted classes into main datatset, because we are not showing the main cleaned dataset
                data['Class'] = predicted_data

                self.dbConenct.loadToStructure(data, conncetion)

            logging.info("Prediction Pipeline End")
        except Exception as e:
            raise AppException(e, sys)