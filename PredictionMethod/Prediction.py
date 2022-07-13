import logging
import os
from app_util import readYamlFile
from constants import constants
from exception import AppException
import sys
import pickle

class Prediction:
    def __init__(self):

        self.appConfig = readYamlFile(constants.CONFIG_FILE_PATH)
        logging.basicConfig(filename="logs/prediction/prediction_pipeline/predictionMethod_logs",
                            filemode='a',
                            level=logging.INFO,
                            format='%(asctime)s: %(levelname)s:: %(message)s)')

    def prediction(self, data, cluster):

        try:

            modelDirectory = self.appConfig['path']['models']
            files = [f for f in os.listdir("./"+modelDirectory)]

            for file in files:
                if(file.find(str(cluster)) != -1):
                    with open(modelDirectory + "/" + file + "/" + file + ".sav", "rb") as file:
                        model = pickle.load(file)
                    break

            y_pred = model.predict(data)
            return y_pred

        except Exception as e:
            raise AppException(e, sys)