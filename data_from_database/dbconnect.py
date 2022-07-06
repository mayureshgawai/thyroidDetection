import mysql.connector as connect
from mysql.connector.connection import MySQLConnection
import logging
import datetime
import pandas as pd
from app_util import readYamlFile
from constants import constants
from exception import AppException
import sys

class MySqlDBConnect:

    def __init__(self):

        self.appConfig = readYamlFile(constants.CONFIG_FILE_PATH)
        logging.basicConfig(filename=r"logs\training\db_Connection\db_Connection_" + str(datetime.datetime.date()),
                            filemode='a',
                            level=logging.INFO,
                            format='%(asctime)s: %(levelname)s:: %(message)s)')


    def getConenction(self) -> MySQLConnection:

        """
        Fetch the data from 'clever cloud' MySql instance
        Configs mentioned in config.yaml
        :return:
        """

        try:
            databaseConfig = self.appConfig['databaseConfig']
            host = databaseConfig['host']
            database = databaseConfig['database']
            user = databaseConfig['user']
            password = databaseConfig['password']

            mydb = connect.connect(host=host, user=user,
                                   passwd=password, database=database)

            return mydb

        except Exception as e:
            raise AppException(e, sys)

