import os
import uuid
import zipfile


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

download_path=file_path=BASE_DIR+"/static/unzip/"

class FileService:



    @staticmethod
    def unzip_files(file, key=None):
        """
        Unzip :file to local path
        """
        with zipfile.ZipFile(file, "r") as zp:
            path = download_path
            if key:
                path = download_path + "/" + key
            zp.extractall(path, pwd=bytes(os.environ["vs_zip_pwd"], "utf-8"))

    @staticmethod
    def zip_files(files, key=None):
        """
        Compress :files to zip
        """
        path = download_path
        if key:
            path = path + "/" + key
        fname = download_path + "/" + str(uuid.uuid4()) + ".zip"
        zipObj = zipfile.ZipFile(fname, "w")
        for file in files:
            arcname = file.rsplit("/", 1)[-1]
            zipObj.write(file, arcname=arcname)
        zipObj.close()
        return fname


    @staticmethod
    def get_file_meta(file_path):
        meta = {}
        try:
            meta["name"] = file_path.split("/")[-1]
            meta["extension"] = file_path.split(".")[-1]
        except Exception:
            return None
        else:
            return meta