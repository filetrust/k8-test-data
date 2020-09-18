import os
import logging
import sys




sys.path.append(sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

logger = logging.getLogger("GW:minio")

class MinioClient:

    def __init__(self):

        self.storage_url = os.environ['storage_url']


    def get_exist(self):
        pass


        # client=MinioService.get_storage_adapter()
        # found=client.bucket_exists('mybucket')
        # print(found)
        # return found




