import gzip
import os
import shutil
import tarfile
import zipfile
from os.path import basename

import py7zr


class Compress:
    @staticmethod
    def zip_compresstion(zip_path, zip_filename, file_path):
        zip_name = f'{zip_filename}.zip'
        filename = f"{zip_path}{zip_name}"
        with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(file_path, basename(file_path))
        return zip_name

    @staticmethod
    def seven_z_compresstion(zip_path, zip_filename, file_path):
        zip_name = f'{zip_filename}.7z'
        filename = f"{zip_path}{zip_name}"

        with py7zr.SevenZipFile(filename, 'w') as z:
            z.writeall(file_path, basename(file_path))
        return zip_name

    @staticmethod
    def tar_compresstion(zip_path, zip_filename, file_path):
        zip_name = f"{zip_filename}.tar"
        filename = f"{zip_path}{zip_name}"
        with tarfile.open(filename, "w:gz") as tar_handle:
            tar_handle.add(file_path, arcname=os.path.basename(file_path))
        tar_handle.close()
        return zip_name

    @staticmethod
    def gz_compresstion(zip_path, zip_filename, file_path):
        try:
            name, ext = file_path.split("/")[-1].split(".")
        except:
            ext = 'txt'
        zip_name = f"{zip_filename}.{ext}.gz"
        gz_filename = f"{zip_path}{zip_name}"

        with gzip.open(gz_filename, 'wb') as f_out:
            with open(file_path, 'rb') as f_in:
                shutil.copyfileobj(f_in, f_out)
        return zip_name

    @staticmethod
    def rar_compresstion(zip_path, zip_filename, file_path):
        zip_name = f"{zip_filename}.rar"
        filename = f"{zip_path}{zip_name}"
        with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(file_path, basename(file_path))
        return zip_name
