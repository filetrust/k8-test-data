import os
import json
import logging as logger
import shutil

import requests
from minio import Minio
from src.config import Config

logger.basicConfig(level=logger.INFO)


class GovUKFileMigration:
    """ Class to migrate gov_uk files from s3 through the standard k8-test-data file processing
        and upload back the bundled zip with the rebuild data, file meta data, virus-total report
        along with the zipped original file to respective s3 buckets."""

    def __init__(self):
        logger.info("GovUKFileMigration::__init__ Starting file migration process.")
        self.download_dir = Config.LOCAL_REPO_PATH
        self.n_files_to_fetch = float('inf')

    def get_file_list_from_s3(self):

        try:
            file_list=[]
            # file_list = {}
            if(Config.S3_SUB_FOLDER_PREFIX):
                s3_bucket_list_obj = requests.get(Config.S3_LIST_BUCKET_FILES_URL,
                                                  params={
                                                      "bucket_name": Config.S3_BUCKET,
                                                      "sub_dir": Config.S3_SUB_FOLDER_PREFIX
                                                  })
            else:
                s3_bucket_list_obj = requests.get(Config.S3_LIST_BUCKET_FILES_URL,
                                                  params={
                                                      "bucket_name": Config.S3_BUCKET,
                                                      "sub_dir": ""
                                                  })

            logger.info(s3_bucket_list_obj)
            if s3_bucket_list_obj.status_code==200:
                logger.info(s3_bucket_list_obj)
                result = s3_bucket_list_obj.json()
                file_list = json.loads(result)["file_list"]

        except Exception as e:
            logger.error("get_file_list_from_s3 Got error while calling storage s3 client service, %s" % e)
            raise e

        return file_list

    def download_file(self, file_name, file_key):

        try:
            # download files from s3 bucket using s3client generator method
            s3_file_download_obj = requests.get(Config.S3_FILE_DOWNLOAD_URL,
                                                params={
                                                    "bucket_name": Config.S3_BUCKET,
                                                    "file_name": file_name,
                                                    "file_key": file_key,
                                                })

            byte_content = s3_file_download_obj.content

            # recreate original file from received byte content
            recreated_file_path = self.recreate_file(byte_content, file_name)

            logger.info("GovUKFileMigration::get_file "
                        "Downloaded file header from s3.".format(s3_file_download_obj.headers))

        except Exception as e:
            logger.info("GovUKFileMigration::get_file Got error {} "
                        "while downloading files from {}.".format(e, Config.S3_BUCKET))
            raise e

        return recreated_file_path

    def recreate_file(self, byte_content, file_name):

        # store pdf bytes to txt
        byte_file_name = file_name.split('.')[0] + '.txt'
        downloaded_file_path = os.path.join(Config.LOCAL_REPO_PATH, file_name)
        try:
            file = open(byte_file_name, 'wb')
            file.write(byte_content)
            file.close()
        except Exception as e:
            logger.error("GovUKFileMigration::recreate_file Error: %s" % e)
            raise e

        # recreate pdf from bytes
        try:
            file = open(downloaded_file_path, 'wb')
            for line in open(byte_file_name, 'rb').readlines():
                file.write(line)
            file.close()
        except Exception as e:
            logger.error("GovUKFileMigration::recreate_file Error: %s" % e)
            raise e

        # remove the created byte text file
        if os.path.exists(byte_file_name):
            os.remove(byte_file_name)

        return downloaded_file_path

    @staticmethod
    def get_bucket_name(path):

        # extract file stats and return bucket name
        extension = path.split("/")[-1].split('.')[-1]
        logger.info(f"Extension of file {extension}")
        if extension:
            bucket_name = extension.lower()
            if len(bucket_name) > 62 or len(bucket_name) < 3:
                bucket_name = 'miscellaneous'
        else:
            bucket_name = 'miscellaneous'
        logger.info(f"Bucket_name for minio upload  {bucket_name}")
        return bucket_name

    def preprocess_files(self, file):
        try:

            # 1. extract meta data of the file
            bucket_name = GovUKFileMigration.get_bucket_name(file)
            file_name = file.split('/')[-1]

            logger.info("GovUKFileMigration::preprocess_files Iterating file: %s |"
                        " Bucket Name: %s | Filename: %s" % (file, bucket_name, file_name))

            try:
                # 2. upload the file to minio before passing it to processor.
                metadata = {"malicious": False}
                GovUKFileMigration.upload_to_minio(bucket_name=bucket_name, file_path=file, file_name=file_name,
                                                   metadata=metadata)
            except Exception as e:
                logger.info("GovUKFileMigration::preprocess_files Got error {} "
                            "while uploading to minio.".format(e))
                raise e

            # 3. pass received file to file processor
            processor_response = GovUKFileMigration.process_file(file=file, bucket_name=bucket_name)
            logger.info("GovUKFileMigration::preprocess_files File processor response: %s for "
                        "file %s and bucket name %s" % (processor_response, file, bucket_name))
            try:
                logger.info(f"deleting  file after preprocess: {download_path}")
                os.remove(download_path)
            except Exception as err:
                logger.error((f'Error while deleted download upload path'))
                pass
        except Exception as err:
            logger.error(f"preprocess_files {err}")

    @staticmethod
    def upload_to_minio(bucket_name, file_name, file_path, metadata):

        logger.info("GovUKFileMigration::upload_to_minio Uploading %s present at %s "
                    "to minio bucket %s" % (file_name, file_path, bucket_name))
        _client = Minio(endpoint=Config.MINIO_ENDPOINT,
                        access_key=Config.MINIO_ACCESS_KEY,
                        secret_key=Config.MINIO_SECRET_KEY,
                        secure=False)

        if not _client.bucket_exists(bucket_name):
            _client.make_bucket(bucket_name=bucket_name)
            logger.info("GovUKFileMigration::upload_to_minio created bucket %s with "
                        "client object %s" % (bucket_name, _client))
        try:
            _client.fput_object(bucket_name=bucket_name,
                                object_name=file_name,
                                file_path=file_path, metadata=metadata)
            logger.info(f"GovUKFileMigration::upload_to_minio Uploaded file {file_name}")
        except Exception as e:
            logger.error("GovUKFileMigration::upload_to_minio Got error while uploaing to minio %s" % e)
            raise Exception(e)

    @staticmethod
    def process_file(file, bucket_name):

        payload = {
            "file": file.split('/')[-1],
            "bucket": bucket_name
        }
        try:
            file_processor_api = os.environ.get('file_processor_api', None)
            fp_response = requests.post(file_processor_api, json=payload)
            logger.info("GovUKFileMigration::process_file Got response %s while processing file"
                        "with payload %s" % (fp_response, payload))

        except Exception as e:
            logger.error("GovUKFileMigration::process_file Got error %s while processing file"
                         "with payload %s" % (payload, e))
            raise e

        return fp_response.status_code

    def download_file_from_azure(self,container_name,blob_name):
        try:
            # download files from azure bucket using s3client generator method
            azure_file_download_obj = requests.get(Config.AZURE_FILE_DOWNLOAD_URL,
                                                params={
                                                    "container_name": container_name,
                                                    "blob_name": blob_name,
                                                })

            byte_content = azure_file_download_obj.content

            # recreate original file from received byte content
            recreated_file_path = self.recreate_file(byte_content, blob_name)

            logger.info("GovUKFileMigration::get_file "
                        "Downloaded file header from azure.".format(azure_file_download_obj.headers))

        except Exception as e:
            logger.info("GovUKFileMigration::get_file Got error {} "
                        "while downloading files from azure container {}.".format(e, container_name))
            raise e

        return recreated_file_path



    def get_azure_list_blob(self,azure_container_name):
        try:
            file_list = []
            azure_list_obj = requests.get(Config.AZURE_LIST_FILES_URL,
                                          params={
                                              "container_name": azure_container_name,
                                          })
            if azure_list_obj.status_code == 200:
                logger.info(f"Azure blob list : {azure_list_obj}")
                result = azure_list_obj
                file_list = result
            return file_list
        except Exception as error:
            logger.info(f"Azure get_azure_list_blobs : Error: {error}")
            return None

    def get_azure_containers(self):
        try:
            container_list = requests.get(Config.AZURE_LIST_CONTAINER_URL)
            if container_list.status_code == 200:
                logger.info(f"Azure container list : {container_list}")
            return container_list
        except Exception as error:
            logger.info(f"Azure get_azure_list_blobs : Error: {error}")
            return None






if __name__ == '__main__':
    # create compression obj
    migration_obj = GovUKFileMigration()

    # get all files already downloaded
    try:
        s3_bucket_target_list_obj = requests.get(Config.S3_LIST_BUCKET_FILES_URL,
                                                 params={
                                                     "bucket_name": os.environ["S3_TARGET_BUCKET"],
                                                     "sub_dir": "",
                                                     "receiver": True
                                                 })

        # downloaded_files = s3_bucket_target_list_obj.content
        result = s3_bucket_target_list_obj.json()
        download_file_list = json.loads(result)["file_list"]
        logger.info("Downloaded file list from icap bucket: %s" % download_file_list)
    except Exception as e:
        logger.error(e)
        download_file_list = []

    if Config.type_of_source.lower()=="s3":
        logger.info("Dowbnloading files from AWS S3")
        # get file list from S3 sub directory
        file_list = migration_obj.get_file_list_from_s3()
        logger.info("GovUKFileMigration::__main__ Number of files from gov-uk bucket: {}".format(len(file_list)))

        # iterate over each file and download
        for file_idx in range(1, len(file_list)):

            try:
                if any(file_list[file_idx].split('/')[-1] in dwld_file for dwld_file in download_file_list):
                    logger.info("Already downloaded: %s" % file_list[file_idx])
                    continue
            except Exception as e:
                logger.error(e)

            logger.info("This will be downloaded: %s" % file_list[file_idx])

            # download file which is not in icap bucket list
            download_path = migration_obj.download_file(file_list[file_idx].split('/')[-1], file_list[file_idx])
            logger.info(f"download_path of preprocess_files : {download_path}")

            # pass the file to file processor as it downloads
            migration_obj.preprocess_files(download_path)
    else:

        # iterate over each file and download
        logger.info("Dowbnloading files from AZURE")
        container_list=migration_obj.get_azure_containers()
        for c in container_list:
            container_name =c.name

            file_list=migration_obj.get_azure_list_blob(azure_container_name=container_name)
            for file_idx in range(1, len(file_list)):
                try:
                    if any(file_list[file_idx].name in dwld_file for dwld_file in download_file_list):
                        logger.info("Already downloaded: %s" % file_list[file_idx])
                        continue
                except Exception as e:
                    logger.error(e)

                blob_name=file_list[file_idx].name
                download_path=migration_obj.download_file_from_azure(container_name=container_name,blob_name=blob_name)
                logger.info(f"download_path of preprocess_files : {download_path}")

                # pass the file to file processor as it downloads
                migration_obj.preprocess_files(download_path)







