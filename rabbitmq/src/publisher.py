import logging
import time
from queue import Queue

from src.utils.rabbit_client import RabbitClient

logger = logging.getLogger('GW: RabbitMQ Publisher')


class Publisher:

    @staticmethod
    def publish_job(bucket_name, file_name):
        q = Queue()
        logger.info(f'publish_jobs : File_Name {file_name}')
        payload = {"type": "process_zip", "file": file_name, "bucket": bucket_name}
        try:
            q.put(payload)
        except Exception as err:
            logger.error(err)

        RabbitClient(q)

    @staticmethod
    def run(bucket, file):
        try:
            Publisher.publish_job(bucket, file)
            time.sleep(1)
            # schedule.every(1).minutes.do(Publisher.publish_job(bucket_name=bucket_name,file_name=file_name))
            # while True:
            #     schedule.run_pending()
            #     time.sleep(1)
        except Exception as err:
            logger.error(str(err))
