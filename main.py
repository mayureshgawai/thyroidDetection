from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
import os
from wsgiref import simple_server
import logging
import datetime
from Training_Validation_and_Insertion import TrainValidation

# from flask_monitoringdashboard.main import app

logging.basicConfig(filename='logs/main/main_logs',
                    filemode='a', level=logging.INFO,
                    format='%(asctime)s: %(levelname)s:: %(message)s')

app =Flask(__name__)

@app.route('/train', methods=['GET', 'POST'])
def trainRoute():
    try:
        logging.info("Training started")
        # path = request.json['folderPath']
        trainobj = TrainValidation()
        trainobj.trainValidationAndInsertion()


        logging.info("Training ends")

    except Exception as e:
        logging.error("Error occured while training", e)
        # return Response("Error Occcured! %s", e)





if __name__=='__main__':
    # app.run()
    host = '127.0.0.1'
    httpd = simple_server.make_server(host, 5000, app)
    httpd.serve_forever()