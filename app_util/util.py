import logging
import yaml
from exception import AppException
import sys
import datetime

logging.basicConfig(filename="logs/load_yaml/yamlCode_logs",
                            filemode='a',
                            level=logging.INFO,
                            format='%(asctime)s: %(levelname)s:: %(message)s)'
                            )

def readYamlFile(filePath: str) -> dict:
    try:
        with open(filePath, 'rb') as yamlFile:
            logging.info("yaml file loaded")
            return yaml.safe_load(yamlFile)
    except Exception as e:
        logging.info("Exception occured while loading yaml %s", e)
        raise AppException(e, sys)