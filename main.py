from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
import os
from wsgiref import simple_server
import logging
import datetime

# from flask_monitoringdashboard.main import app

logging.basicConfig(filename=f'logs\main\main_{datetime.datetime.date()}',
                    filemode='a', level=logging.INFO,
                    format='%(asctime)s: %(levelname)s:: %(message)s')

app =Flask(__name__)

@app.route('/train', methods=['GET', 'POST'])
def trainRoute():
    try:
        path = request.json['folderPath']
        trainobj = ""

    except Exception as e:
        return Response("Error Occcured! %s", e)





if __name__=='__main__':
    # app.run()
    host = '127.0.0.1'
    httpd = simple_server.make_server(host, 5000, app)
    httpd.serve_forever()