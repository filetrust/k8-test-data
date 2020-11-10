import logging as logger
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.config import Config as AppConfig
import azure
from azure.storage.blob import BlockBlobService, PublicAccess

logger.basicConfig(level=logger.INFO)


class AzureClient:
    def __init__(self, azure_account_name, azure_account_key):
        self.block_blob_service = BlockBlobService(account_name=azure_account_name,
                                      account_key=azure_account_key)

    def list_azure_containers(self):
        logger.info(f"Azure list containers ")
        containers = self.block_blob_service.list_containers()
        return containers

    def list_azure_files(self, container_name):
        logger.info(f"Azure list files ")
        my_files = self.block_blob_service.list_blobs(container_name)

        return my_files

    def download_single_azure_blob(self,container_name,blob_name):
        try:
            logger.info(f"Azure download_single_azure_blob")
            if not os.path.exists(AppConfig.s3_download_path):
                os.makedirs(AppConfig.s3_download_path)
            download_path = os.path.join(AppConfig.s3_download_path, blob_name)
            self.block_blob_service.get_blob_to_path(container_name, blob_name, download_path)
            logger.info(f"Downloaded file")

        except Exception as e:
            logger.error(e)
            raise e

        return 1


