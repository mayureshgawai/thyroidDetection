import logging
import datetime
from exception import AppException
import sys
from app_util import readYamlFile
import os
from constants import constants
from RawDataValidation import DataValidation

class TrainValidation:
    def __init__(self, path):

        self.appConfig = readYamlFile(constants.CONFIG_FILE_PATH)
        self.validation = DataValidation(path)

        logging.basicConfig(filename=r"logs\train_validation_insertion\train_"+str(datetime.datetime.date()),
                            filemode='a',
                            level=logging.INFO,
                            format='%(asctime)s: %(levelname)s:: %(message)s)')

    def trainValidationAndInsertion(self):

        try:


            pass



        except Exception as e:
            raise AppException(e, sys)
