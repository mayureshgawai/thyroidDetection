import logging
import datetime
from exception import AppException
import sys
from app_util.util import readYamlFile
import os
from constants import constants
from RawDataValidation import DataValidation
from data_from_database import MySqlDBConnect

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
            if(data == None):
                # raise AppException("Failed to create dataframe", sys)
                raise Exception("Failed to create database")

            logging.info("Successfully retrieved data from database and created dataframe")

            logging.info("Moving to the data cleaning")
            # replacing all "?" and or improper string with None with dataset
            data = self.validation.replaceWithNone(data)

            # "sex" is object column with string data in it, so we cannot convert its datatype directly
            # we have to encode it first. We cannot directly encode it with None values in it. So we can use "apply()"
            data = self.validation.handleObjectColumns(data)

            # Removing outliers from "age column"
            # Age should be between 10 and 90 only.
            data = data[(data['age'] < 90) & (data['age'] > 10)]

            # Encoding of the data
            data  = self.validation.encodeColumns(data)

            # handling missing values
            nullPresent = self.validation.checkForNanInDataset(data)
            if(nullPresent):
                # Applyig imputer
                X_imputed, y = self.validation.impute(data)

            y = y.reset_index()







        except Exception as e:
            raise AppException(e, sys)
