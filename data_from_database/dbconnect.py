import mysql.connector as connect
from mysql.connector.connection import MySQLConnection
import logging
import datetime
import pandas as pd
from app_util.util import readYamlFile
from constants import constants
from exception import AppException
import sys

class MySqlDBConnect:

    def __init__(self):

        self.appConfig = readYamlFile(constants.CONFIG_FILE_PATH)
        logging.basicConfig(filename=r"logs/training/db_Connection/db_Connection_logs",
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
            logging.info("Creating Database connection")
            databaseConfig = self.appConfig['databaseConfig']
            host = databaseConfig['host']
            database = databaseConfig['database']
            user = databaseConfig['user']
            password = databaseConfig['password']

            mydb = connect.connect(host=host, user=user,
                                   passwd=password, database=database)
            logging.info("Created Database connection")
            return mydb

        except Exception as e:
            raise AppException(e, sys)

    def getRawData(self, connection):
        """
        Fetches all data from the raw_data table
        :return:
        """
        try:
            cursor = connection.cursor()
            query = "select * from raw_data_train"

            cursor.execute(query)
            table_rows = cursor.fetchall()
            # df = pd.DataFrame(table_rows)

            df = pd.read_sql("select * from raw_data_train", con=connection)
            return df
        except Exception as e:
            raise AppException(e, sys)


    def getPredictData(self, connection):
        """
                Fetches all data from the prediction_data table
                :return:
                """
        try:
            cursor = connection.cursor()
            query = "select * from prediction_data"

            cursor.execute(query)
            table_rows = cursor.fetchall()
            # df = pd.DataFrame(table_rows)

            df = pd.read_sql("select * from prediction_data", con=connection)
            return df
        except Exception as e:
            raise AppException(e, sys)