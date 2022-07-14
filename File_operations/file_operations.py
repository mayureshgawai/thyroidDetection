import shutil
import pickle
import logging
import os
from exception import AppException
import sys

class FileOperations:
    def __init__(self):
        self.modelDirectory = "./models"
        logging.basicConfig(filename="logs/training/file_handle/file_logs.txt",
                            filemode='a',
                            level=logging.INFO,
                            format='%(asctime)s: %(levelname)s:: %(message)s)')


    def saveModel(self, modelName, model):

        """
        Saving the standard Machine Learning model using this method .
        :param modelName:
        :param model:
        :return:
        """

        logging.info("Saving model is in progress")
        try:
            path = os.path.join(self.modelDirectory, modelName)
            if (os.path.isdir(path)):
                shutil.rmtree(path)
                os.makedirs(path)
            else:
                os.makedirs(path)

            with open(path+"/"+modelName+".sav", "wb") as f:
                pickle.dump(model, f)
            logging.info("Model saved successfully")


        except Exception as e:
            raise AppException(e, sys)



