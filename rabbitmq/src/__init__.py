import json
import logging
import time

from .config import Config
from .publisher import Publisher
from .consumer import Consumer
from multiprocessing import Process
from flask import Flask, request, jsonify
from flask import Flask, request, Response
logger = logging.getLogger('GW: RabbitMQ app')
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route("/publish", methods=['POST'])
    def mq_service():
        try:
            logger.info("Inside publish function")
            data = request.json
            """
            To publish file in rabbit mq and call receiver 
            """
            file_name = data.get("file_name", None)
            bucket_name = data.get("bucket_name", None)
            logger.info(f"file_name : {file_name}")
            logger.info(f"bucket_name : {bucket_name}")

            publisher = Process(target=Publisher.run,args=(bucket_name,file_name))
            publisher.start()

            consumer = Process(target=Consumer.run)
            consumer.start()

            ret = {"err": "none"}
        except Exception as error:
            ret = {"err": error}
            logger.error(f'main: error {error}')
        else:
            return Response(json.dumps(ret), mimetype='application/json')


    return app