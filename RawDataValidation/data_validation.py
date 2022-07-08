import logging
import datetime
from constants import constants
from app_util.util import readYamlFile
from constants import constants
from data_from_database import MySqlDBConnect

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

        checkNull = data.isnull().sum()
        isNullPresent = False

        for nullCount in checkNull:
            return True if(nullCount>0) else False


    def replaceWithNone(self, data):

        """
        Replacing all inappropriate data in dataset with some meaningful data to make decisions easier.
        :param data:
        :return:Dataframe
        """

        data2 = data.copy()
        for col in range(0, len(data2.columns)):
            data2[data.columns[col]] = data[data.columns[col]].apply(lambda x: None if ((x == '?') or (x == "Nan")) else x)

        return data2



