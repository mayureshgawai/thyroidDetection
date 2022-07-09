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

class TrainValidation:
    def __init__(self):

        self.appConfig = readYamlFile(constants.CONFIG_FILE_PATH)
        self.validation = DataValidation()
        self.dbConenct = MySqlDBConnect()

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
                # Applyig imputer
                X_imputed, y = self.validation.impute(data)

            y = y.reset_index()




        except Exception as e:
            raise AppException(e, sys)
