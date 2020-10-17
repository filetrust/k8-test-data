import os
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

