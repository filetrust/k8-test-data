import os

from azure.storage.fileshare import ShareServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions,ShareDirectoryClient,ShareFileClient,ShareClient
from datetime import datetime, timedelta
from src.config import Config as AppConfig
import logging as logger

logger.basicConfig(level=logger.INFO)

class AzureFileShareClient:

    def __init__(self):

        self.conn_str = AppConfig.conn_str
        self.share_name = AppConfig.share_name
        self.parent_dir_name = AppConfig.parent_dir_name


    def get_share_directory_client(self,directory_path):
        logger.info("AzureFileShareClient: get_share_directory_client")
        dir=ShareDirectoryClient.from_connection_string(conn_str=self.conn_str, share_name=self.share_name,
                                                    directory_path=directory_path)
        return dir

    def list_files(self):
        logger.info("AzureFileShareClient: list_files")

        try:
            file_list=[]
            parent_dir = self.get_share_directory_client(directory_path=self.parent_dir_name)
            dir1_list = list(parent_dir.list_directories_and_files())

            for i in dir1_list:
                if (i["is_directory"] == True):
                    sub_dir_name = str(i["name"])
                    dir_path = self.parent_dir_name + "/" + sub_dir_name
                    sub_dir = self.get_share_directory_client(directory_path=dir_path)


                    dir2_list=list(sub_dir.list_directories_and_files())

                    for j in dir2_list:
                        if (j["is_directory"] == True):
                            sub_dir_path=dir_path+"/"+str(j["name"])

                            sub_sub_dir =  self.get_share_directory_client(directory_path=sub_dir_path)

                            dir3_list=list(sub_sub_dir.list_directories_and_files())

                            for k in dir3_list:
                                if (k["is_directory"] == True):
                                    sub_sub_dir_path = sub_dir_path + "/" + str(k["name"])

                                    sub_sub_sub_dir = self.get_share_directory_client(directory_path=sub_sub_dir_path)
                                    dir4_list = list(sub_sub_sub_dir.list_directories_and_files())

                                    for l in dir4_list:
                                        file_path=sub_sub_dir_path+"/"+str(l["name"])
                                        if(l["is_directory"] == False):
                                            file_list.append(file_path)
            return file_list
        except Exception as e:
            logger.error(f"AzureFileShareClient: list_files: {e}")
            raise e
            pass

    def download_file(self,file_path):
        file_client = ShareFileClient.from_connection_string(conn_str=self.conn_str, share_name=self.share_name,
                                                             file_path=file_path)
        if not os.path.exists(AppConfig.s3_download_path):
            os.makedirs(AppConfig.s3_download_path)
        download_path=os.path.join(AppConfig.s3_download_path, file_path.split("/")[-1])
        with open(download_path, "wb") as file_handle:
            data = file_client.download_file()
            data.readinto(file_handle)



