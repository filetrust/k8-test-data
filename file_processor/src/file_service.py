import logging
import os
import pathlib
from os.path import basename
import zipfile
from src.services import MinioService
import datetime

class FileService:
    @staticmethod
    def unzip(file_path, extract_path, password=None):
        with zipfile.ZipFile(file_path, "r") as zp:
            params = {
                "path": extract_path,
            }
            params["pwd"] = bytes(os.environ["vs_zip_pwd"], "utf-8")
            zp.extractall(**params)

    @staticmethod
    def prepare_zip(zip_filename, folder_path, zip_path):

        zip_filename = f"{zip_path}/{zip_filename}.zip"
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipObj:
            for folderName, subfolders, filenames in os.walk(folder_path):
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    zipObj.write(filePath, basename(filePath))
        return zip_filename

    @staticmethod
    def get_file_meta(file_path):
        """
            get_file_meta :extract file name and file type
            size, extension, name , hash
        """
        # initializing empty meta dict
        meta = {}

        try:
            file_stat = os.stat(file_path)
            size = file_stat.st_size
            suffix = pathlib.Path(file_path).suffix
            extension = suffix.split(".")[-1]

            meta['size']= str(file_stat.st_size) +  " bytes"
            meta["name"] = file_path.split("/")[-1]
            meta['hash']=file_path.split("/")[-1].split('.')[0]
            meta['creation_date'] = datetime.datetime.now()
            meta['expiry_date'] = None
            if not extension:
                meta["extension"] = 'txt'
            else:
                meta["extension"] = extension
        except Exception as error:
            raise error
        else:
            return meta