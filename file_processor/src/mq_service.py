import json
import logging as logger
import os

import requests

logger.basicConfig(level=logger.INFO)
class MQService:

    @staticmethod
    def send(payload):
        s3_sync_api=os.environ.get('s3_sync_api')
        logger.info(f's3_sync_api : {s3_sync_api}')

        payload=json.dumps(payload)
        payload=json.loads(payload)

        logger.info(f'MQService: send : payload : {payload}')

        response = requests.post(s3_sync_api, json=payload)

