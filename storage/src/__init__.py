import ast
import json
import logging
import os
import socket
import zipfile
from io import BytesIO
from os.path import basename

import requests
from flask import Flask, request, Response, jsonify, send_from_directory

from .config import Config
from .minio_service import MinioService
from .s3_client import S3Client

logger = logging.getLogger('GW:Storage')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    client = MinioService(endpoint=os.environ['MINIO_HOSTNAME'], access_key=os.environ['MINIO_ACCESS_KEY_ID'],
                          secret_key=os.environ['MINIO_SECRET_ACCESS_KEY'], secure=False)

    s3_client = S3Client(Config.S3_URL,
                         Config.S3_ACCESS_KEY,
                         Config.S3_SECRET_KEY)

    def server_info():
        return {"hostname": socket.gethostname()}

    @app.route("/ping", methods=["GET"])
    def ping():
        data = server_info()
        try:
            data['error']: None
            data["action"] = "pong"
        except Exception as error:
            data['error']: error
            data["action"] = "error"
            raise error
        return Response(json.dumps(data), mimetype='application/json')

    @app.route("/upload", methods=['GET', 'POST'])
    def upload_file():
        try:

            content = request.json
            client.upload_file(bucket_name=content['bucket_name'], file_name=content['minio_path'],
                               file_path=content['file'])
            ret = {"err": "none", 'details': content}
        except Exception as error:
            ret = {"err": "none", "details": error}
            raise error

        return Response(json.dumps(ret), mimetype='application/json')

    @app.route("/upload_stream", methods=['GET', 'POST'])
    def upload_stream():
        try:
            logger.info(f'file name : {request.args.get("name")}')

            bucket = request.args.get('bucket_name')
            name = request.args.get('name')
            length = request.args.get('length')
            metadata = request.args.get('metadata')
            meta = ast.literal_eval(metadata)
            data = BytesIO(request.data)

            client.upload_data_stream(bucket_name=bucket, file_name=name, data_stream=data,
                                      length=data.getbuffer().nbytes, metadata=meta)

            try:
                rabbit_mq_api = os.environ.get('rabbit_mq_api', None)
                logger.info(f"calling rabbit_mq_api {rabbit_mq_api}")

                payload = {'file_name': name, 'bucket_name': bucket}
                payload = json.dumps(payload)
                payload = json.loads(payload)

                logger.info(type(payload))
                logger.info(f"calling payload {payload}")
                response = requests.post(rabbit_mq_api, json=payload)
                logger.info(f"calling response {response}")
                ret = {"err": "none"}
            except Exception as err:
                ret = {"err": err}
                logger.error(err)
                raise err

        except Exception as error:
            logger.error(f'create_app : upload_stream : {error}')
            ret = {"err": error }
            raise error

        return Response(json.dumps(ret), mimetype='application/json')

    @app.route("/list_bucket_files", methods=['GET'])
    def list_bucket_files():

        """ returns all list files from the bucket and subdirectory(if present) """
        content = request.args
        bucket_name = content["bucket_name"]
        sub_dir = content["sub_dir"]

        file_list = s3_client.list_s3_bucket_files(bucket_name, sub_dir)

        response = {
            "file_list": file_list,
            "bucket_name": bucket_name,
            "sub_dir": sub_dir
        }

        return jsonify(json.dumps(response))

    @app.route("/s3_file_download", methods=['GET'])
    def s3_download_file():
        """ download single file from s3 given the key. """
        content = request.args
        bucket_name = content["bucket_name"]
        file_key = content["file_key"]
        file_name = content["file_name"]

        # download file to local container
        s3_client.download_single_s3_file(bucket_name, file_key, file_name)

        # send the file back as bytes
        dir = os.path.join(app.root_path, "download")
        return send_from_directory(directory=dir,
                                   filename=file_name,
                                   as_attachment=True)

    @app.route("/s3_upload", methods=['GET', 'POST'])
    def upload_file_to_s3():
        try:
            content = request.json
            file = request.files.get("file")
            if not file:
                return jsonify({"message": "please supply a file"})
            s3_client.upload_file(file=file,file_name=content['file_name'],bucket=content['bucket_name'])
            ret = {"err": "none", 'details': content}
        except Exception as error:
            ret = {"err": "none", "details": error}
            raise error

        return Response(json.dumps(ret), mimetype='application/json')

    @app.route("/s3_download/<path:path>", methods=['GET', 'POST'])
    def download_files_from_s3(path):
        try:
            content = request.json
            s3_client.download_files(bucket_name=content['bucket_name'],num_files=content['num_files'],file_path=Config.s3_download_path)

            with zipfile.ZipFile(Config.s3_download_path +"/files.zip", "w", zipfile.ZIP_DEFLATED) as zipObj:
                for folderName, subfolders, filenames in os.walk(Config.s3_download_path):
                    for filename in filenames:
                        filePath = os.path.join(folderName, filename)
                        zipObj.write(filePath, basename(filePath))
            return send_from_directory(Config.s3_download_path , path, as_attachment=True)

        except Exception as error:
            logger.error(f'create_app : download_files_from_s3 : {error}')
            return None




    @app.route("/s3_download_dir/<path:path>", methods=['GET', 'POST'])
    def download_dir_file_from_s3(path):
        try:
            content = request.json
            s3_client.download_subdirectory_files(bucket_name=content['bucket_name'],num_files=content['num_files'],file_download_path=Config.s3_download_path)

            with zipfile.ZipFile(Config.s3_download_path + "/files.zip", "w", zipfile.ZIP_DEFLATED) as zipObj:
                for folderName, subfolders, filenames in os.walk(Config.s3_download_path):
                    for filename in filenames:
                        filePath = os.path.join(folderName, filename)
                        zipObj.write(filePath, basename(filePath))

            return send_from_directory(Config.s3_download_path, path, as_attachment=True)

        except Exception as error:
            logger.error(f'create_app : download_dir_file_from_s3 : {error}')
            return None



    return app