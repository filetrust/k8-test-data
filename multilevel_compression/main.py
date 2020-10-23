import os
import boto3
import logging
from zipfile import ZipFile
from .src.config import Config
from .src.utils.s3_client import S3Client

logger = logging.getLogger("GW:s3")


class CreateMultilevelCompression:
    """ Class to create multilevel compression file by fetching n files from s3 bucket
        based on the level provided (level=5, requires 10 files) and
        storing the resulting file back to target s3 bucket. """

    def __init__(self):
        self.s3 = S3Client(Config.S3_URL, Config.S3_ACCESS_KEY, Config.S3_SECRET_KEY)
        logger.info("CreateMultilevelCompression::__init__ Creating s3 client object: %s" % self.s3)
        self.level = Config.COMPRESSION_LEVEL
        self.download_dir = Config.LOCAL_REPO_PATH

    def get_files(self):

        # number of files to download
        n_files_to_fetch = self.level * 2
        # download files from s3 bucket using s3client
        try:
            list_files = self.s3.download_files(Config.S3_BUCKET, n_files_to_fetch, file_download_path=self.download_dir)
            logger.info("CreateMultilevelCompression::get_files "
                        "Downloaded {} files from s3: {}".format(n_files_to_fetch,
                                                                                                        list_files))
        except Exception as e:
            logger.info("CreateMultilevelCompression::get_files Got error {} "
                        "while downloading files from {}.".format(e, Config.S3_BUCKET))
            return -1

        return list_files

    def gen_multilevel_compression_file(self, files):

        # set previous zipped file name
        last_compressed_file = None
        files = sorted(files)

        # Get file in tuples
        for i in range(0, len(files), 2):
            nzip_filename = os.path.join(self.download_dir, 'file_%s.zip' % i)

            try:
                zip_obj = ZipFile(nzip_filename, 'w')
            except Exception as e:
                logger.info("CreateMultilevelCompression::gen_multilevel_compression_file "
                            "Got error {} while creating ZipFile object for {}".format(e, nzip_filename))
                return -1

            logger.info("CreateMultilevelCompression::get_files File tuples: {}.".format(files[i:i+2]))
            file_1, file_2 = files[i:i+2]

            try:
                if last_compressed_file:
                    zip_obj.write(last_compressed_file)
                zip_obj.write(file_1)
                zip_obj.write(file_2)
            except Exception as e:
                logger.info("CreateMultilevelCompression::gen_multilevel_compression_file"
                            "Got error {} while writing to the ZipFile '{}'".format(e, nzip_filename))
            finally:
                zip_obj.close()

            last_compressed_file = nzip_filename

            logger.info("CreateMultilevelCompression::gen_multilevel_compression_file"
                        "Final compressed file: %s" % last_compressed_file)

        return last_compressed_file

    def upload_to_target_s3(self, final_compressed_file):

        file_path = os.path.join(self.download_dir, final_compressed_file)
        bucket = Config.S3_FOLDER_NAME

        logger.info("CreateMultilevelCompression::upload_to_target_s3 File path to final compressed file: {}, "
                    "sub-directory to create in S3 Bucket: {}.".format(file_path, bucket))
        try:
            self.s3.upload_file(file_path=file_path,
                                file_name=final_compressed_file,
                                bucket=bucket)

        except Exception as e:
            logger.info("CreateMultilevelCompression::upload_to_target_s3 "
                        "An Exception encountered while uploading file to s3: {} for "
                        "sub-directory {} and file path{}.".format(e, bucket, file_path))

            return


if __name__ == '__main__':

    # create compression obj
    ml_compression_obj = CreateMultilevelCompression()

    # fetch files
    s3_files = ml_compression_obj.get_files()

    # generate multilevel compression file
    ml_compressed_file = ml_compression_obj.gen_multilevel_compression_file(s3_files)

    # save file to target s3 bucket
    ml_compression_obj.upload_to_target_s3(ml_compressed_file)






