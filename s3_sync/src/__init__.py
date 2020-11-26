import os
import shutil

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from src.config import Config
from src.utils.minio_client import MinioClient
from src.utils.s3_client import S3Client
import logging as logger

logger.basicConfig(level=logger.INFO)


def validation_error(msg):
    logger.error(f'create_app : validation_error {msg}')
    return jsonify({"message": msg}), 400 


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(1000), index=True, unique=True)
    path = db.Column(db.String(1000))
    def __repr__(self):
        return '<File %r>' % (self.filename)

db.create_all()
db.session.commit()

def add_to_db(filename, path):
    f = File(filename = filename, path = path)
    try:
        db.session.add(f)
        db.session.commit()
    except Exception as ex:
        logger.error(str(ex))


@app.route("/tos3", methods=["POST"])
def sync_to_s3():
    if not os.path.exists(Config.download_path):
        os.makedirs(Config.download_path)

    file_to_fetch = request.json
    
    if not "s3_bucket" in file_to_fetch:
        return validation_error("s3_bucket parameter is missing!")

    if not "minio_bucket" in file_to_fetch:
        return validation_error("minio_bucket parameter is missing!")
    
    if not "file" in file_to_fetch:
        return validation_error("file parameter is missing!")
        
    minio_client = MinioClient(Config.MINIO_URL, Config.MINIO_ACCESS_KEY, Config.MINIO_SECRET_KEY)
    try:
        file_from_minio = minio_client.download_files(bucket_name=file_to_fetch['minio_bucket'], file_name=file_to_fetch['file'], download_path=Config.download_path)
    except Exception as err:
        logger.error(f'create_app: file_from_minio {err}')
        return validation_error(str(err))

    s3_client = S3Client(Config.S3_URL, Config.S3_ACCESS_KEY, Config.S3_SECRET_KEY)
    try:
        # bucket_name=file_to_fetch['s3_bucket'], # use later
        s3_client.upload_file(file_path=file_from_minio, file_name=file_to_fetch['file'], bucket=file_to_fetch['s3_bucket'])
        add_to_db(filename=file_to_fetch['file'], path=file_to_fetch['s3_bucket'])
        logger.info(f"deleting object {file_to_fetch['minio_bucket']} /{file_to_fetch['file']}")
        minio_client.delete_file(bucket_name=file_to_fetch['minio_bucket'], object_name=file_to_fetch['file'])
        logger.info(f"Deleted {file_to_fetch['file']}")
        original_name = file_to_fetch['original_file']
        logger.info(f"deleting object {file_to_fetch['s3_bucket']} /{file_to_fetch['original_file']}")
        minio_client.delete_file(bucket_name=file_to_fetch['s3_bucket'], object_name=file_to_fetch['original_file'])
        logger.info(f"Deleted {file_to_fetch['file']}")
    except Exception as err:
        logger.error(f'create_app: s3_client {err}')
        return validation_error(str(err))

    return jsonify({"message": ""})


@app.route("/folder_tos3", methods=["POST"])
def sync_folder_to_s3():
    if not os.path.exists(Config.download_path):
        os.makedirs(Config.download_path)

    file_to_fetch = request.json

    if not "s3_bucket" in file_to_fetch:
        return validation_error("s3_bucket parameter is missing!")

    if not "minio_bucket" in file_to_fetch:
        return validation_error("minio_bucket parameter is missing!")

    if not "file" in file_to_fetch:
        return validation_error("file parameter is missing!")

    minio_client = MinioClient(Config.MINIO_URL, Config.MINIO_ACCESS_KEY, Config.MINIO_SECRET_KEY)
    s3_client = S3Client(Config.S3_URL, Config.S3_ACCESS_KEY, Config.S3_SECRET_KEY)
    try:

        folder_name=file_to_fetch['folder']
        file_name=file_to_fetch['file']
        metadata_name=file_to_fetch['metadata_name']
        rebuild_xml=file_to_fetch['rebuild_xml']
        rebuild_file=file_to_fetch['rebuild_file']

        files=[]
        files.extend([file_name,metadata_name,rebuild_xml,rebuild_file,])
        try:
            for f in files:
                if f:
                    logger.info(f"file {f} to be uploaded to s3 in folder {folder_name}")
                    folder_path=Config.download_path+"/"+folder_name.split("/")[0]
                    if not os.path.exists(folder_path):
                        os.makedirs(Config.download_path+"/"+folder_name.split("/")[0])
                    file_from_minio = minio_client.download_files(bucket_name=file_to_fetch['minio_bucket'],
                                                              file_name=folder_name+f,
                                                              download_path=Config.download_path)
                    logger.info(f'file_from_minio : {file_from_minio}')
                    s3_client.upload_file(file_path=file_from_minio, file_name=folder_name+f,
                                          bucket=file_to_fetch['s3_bucket'])
                    logger.info(f's3 path : {folder_name}{f}')
                    logger.info(f"deleting object {file_to_fetch['minio_bucket']}/{folder_name+f}")
                    minio_client.delete_file(bucket_name=file_to_fetch['minio_bucket'],object_name=folder_name+f)
                    logger.info(f"Deleted object {folder_name}/{f}")

                    try:
                        shutil.rmtree(folder_path)
                    except Exception as err:
                        logger.error((f'Error while deleted download upload path'))
                        raise err
        except Exception as err:
            logger.error((f'Error while deleting'))
        try:
            file = file_name
            logger.info(f"Deleting object {file}")
            minio_client.delete_file(bucket_name=file_to_fetch['s3_bucket'], object_name=file)
            logger.info(f"Deleted object {file}")
        except Exception as err:
            logger.error("error while deleting original file")
            raise err

        try:
            logger.info(f"Deleting object {file}")
            minio_client.delete_file(bucket_name=file_to_fetch['minio_bucket'], object_name=folder_name)
            logger.info(f"Deleted folder {folder_name}")
        except Exception as err:
            logger.error("error while deleting original folder")
            raise err

    except Exception as err:
        logger.error(f'create_app: file_from_minio {err}')
        return validation_error(str(err))

    try:
        # bucket_name=file_to_fetch['s3_bucket'], # use later
        add_to_db(filename=file_to_fetch['folder'], path=file_to_fetch['s3_bucket'])
    except Exception as err:
        logger.error(f'create_app: s3_client {err}')
        return validation_error(str(err))

    return jsonify({"message": ""})

@app.route("/files", methods=["GET"])
def get_files():
    output = []
    files = File.query
    file_type = request.args.get('file_type', None)
    if file_type:
        files = files.filter(File.path==file_type)
    files = files.all()

    for f in files:
        output.append({
                'filename': f.filename,
                'path': f.path + '/' + f.filename,
                'file_type': f.path
            })
    return jsonify({"files": output})


@app.route("/sync_from_s3", methods=["GET"])
def sync_from_s3():
    s3_client = S3Client(Config.S3_URL, Config.S3_ACCESS_KEY, Config.S3_SECRET_KEY)
    file_type = request.args.get("file_type", None)
    if not file_type:
        return jsonify({"message":"invalid file_type"})

    files = s3_client.get_files(file_type)
    if files:
        files = files.get('Contents', [])
        for file in files:
            filename = file['Key'].split("/")[-1]
            add_to_db(filename=filename, path=file_type)

    return jsonify({})




