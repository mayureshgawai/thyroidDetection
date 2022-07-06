import logging
import datetime
from constants import constants
from app_util import readYamlFile
from constants import constants

class DataValidation:
    def __init__(self):

        self.appconfig = readYamlFile(constants.CONFIG_FILE_PATH)
        logging.basicConfig(filename=r"logs\data_validation\data_validation_"+str(datetime.datetime.date()),
                            filemode='a',
                            level=logging.INFO,
                            format='%(asctime)s: %(levelname)s:: %(message)s)')


