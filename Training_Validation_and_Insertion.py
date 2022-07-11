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

class TrainValidation:
    def __init__(self):

        self.appConfig = readYamlFile(constants.CONFIG_FILE_PATH)
        self.validation = DataValidation()
        self.dbConenct = MySqlDBConnect()
        self.cluster = Clustering()
        self.fileOperations = FileOperations()
        logging.basicConfig(filename="logs/training/train_validation_insertion/train_logs",
                            filemode='a',
                            level=logging.INFO,
                            format='%(asctime)s: %(levelname)s:: %(message)s)')


    def trainValidationAndInsertion(self):

        try:
            """
                This method is responsible for taking data from database, validating it according to requirement
                and cleaning the data. Then apply clustering and training models.
            """
            logging.info("Getting data from database")
            # create database connection (MySql instance created on "clever cloud")
            conncetion = self.dbConenct.getConenction()
            # fetching all data from database
            data = self.dbConenct.getRawData(conncetion)
            # to check if database returned some data
            logging.info("Successfully retrieved data from database and created dataframe")

            logging.info("Moving to the data cleaning")
            # replacing all "?" and or improper string with None with dataset
            data = self.validation.replaceWithNone(data)

            # "sex" is object column with string data in it, so we cannot convert its datatype directly
            # we have to encode it first. We cannot directly encode it with None values in it. So we can use "apply()"
            # Replacing Female:0 and Male:1
            data = self.validation.handleObjectColumns(data)

            # Removing outliers from "age column"
            # Age should be between 10 and 90 only.
            data['age'] = pd.to_numeric(data['age'])
            data = data[(data['age'] < 90) & (data['age'] > 10)]

            # Removing columns with no unique values or None values


            # Encoding of the data
            data  = self.validation.encodeColumns(data)

            # Checking for unqiue values in columns
            data = self.validation.checkForUnique(data)

            # handling missing values
            nullPresent = self.validation.checkForNanInDataset(data)
            if(nullPresent):
                # Applying imputer
                X_imputed, y = self.validation.impute(data)

            y = y.reset_index()
            if('index' in y.columns):
                y.drop(['index'], axis=1, inplace=True)

            logging.info("Data Cleaning Done!!")

            logging.info("Data clustering")
            y_kmeans = self.cluster.createClusters(X_imputed)
            X_imputed['cluster'] = y_kmeans

            listOfCluster = X_imputed['cluster'].unique()
            logging.info("Data Clustered in: "+ str(listOfCluster))

            df = X_imputed.copy()
            df["Class"] = y

            # df.to_csv("df.csv")
            for num in listOfCluster:
                dataSeperation = df[df['cluster'] == int(num)]
                features = dataSeperation.drop(['cluster', 'Class'], axis=1)
                y = dataSeperation['Class']
                s = features.shape

                X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.2, random_state=30)
                modelFinder = ModelFinder()
                modelName, model = modelFinder.getBestModel(X_train, X_test, y_train, y_test)
                modelName = modelName + str(num)
                self.fileOperations.saveModel(modelName, model)


        except Exception as e:
            raise AppException(e, sys)
