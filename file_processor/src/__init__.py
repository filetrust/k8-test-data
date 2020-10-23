import hashlib
import logging as logger
import os
import time
from pathlib import Path
from ast import literal_eval
import pyminizip
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from src.config import Config
from src.services import (
    MinioService,
    FileService,
    VirusTotalService,
    GlasswallService,
    MQService,
)

logger.basicConfig(level=logger.INFO)


class Processor:
    def __init__(self):
        self.filename = None
        self.bucket_name = None
        self.hash = None
        self.ext = None
        self.directory = None
        self.path = None
        self.infected_path = None
        self.infected_file = None
        self.virus_total_status = False
        self.gw_rebuild_file_status = False
        self.gw_rebuild_xml_status = False
        self.minio = MinioService(
            Config.MINIO_URL, Config.MINIO_ACCESS_KEY, Config.MINIO_SECRET_KEY
        )
        self.vt = VirusTotalService(Config.virustotal_key)
        self.input_file = None
        self.isMalicious = None
        self.metadata = {}
        self.rebuild_hash = None
        self.minio_meta = None

    def get_files(self, filename):
        files = []
        self.filename = filename
        name, ext = self.filename.split(".")
        self.bucket_name = ext
        logger.info(f"downloading file {filename} from minio")
        self.directory = Config.download_path + "/" + name
        self.minio.download_files(
            bucket_name=ext, file_name=filename, download_path=Config.download_path
        )
        self.minio_meta = self.minio.get_stat(bucket_name=self.bucket_name, file_name=filename)

        if ext == "zip":
            FileService.unzip(Config.download_path + "/" + filename, self.directory)
            _files = os.listdir(self.directory)
            if not _files:
                logger.error("no file inside zip")
            else:
                for f in _files:
                    files.append(self.directory + "/" + f)
        else:
            files.append(Config.download_path + "/" + filename)

        return files

    def set_current_file(self, file_path):
        logger.info(f"setting current file {file_path}")
        _dir, filename = file_path.rsplit("/", 1)

        try:
            self.filename, self.ext = filename.split(".")

        except Exception:
            self.filename = filename
            self.ext = None

        # convert file to hash
        with open(file_path, mode='rb') as file:  # b is important -> binary
            fileContent = file.read()

        original_hash = hashlib.sha1(fileContent).hexdigest()
        self.hash = original_hash
        logger.info(f"Original_hash : {original_hash}")
        # self.hash = hashlib.sha1(str(self.filename).encode()).hexdigest()

        # Create directory for this file
        self.directory = _dir + "/" + self.hash
        Path(self.directory).mkdir(parents=True, exist_ok=True)

        # Move current file to it's own directory
        if self.ext:
            self.file_path = self.directory + "/" + self.hash + "." + self.ext
        else:
            self.file_path = self.directory + "/" + self.hash

        logger.info(f'renaming of file {file_path} to {self.file_path} after sha1 hashing')
        os.rename(file_path, self.file_path)

    def check_virustotal(self):
        try:
            if 'x-amz-meta-malicious' in self.minio_meta.metadata:
                self.isMalicious = literal_eval(self.minio_meta.metadata['x-amz-meta-malicious'])
                logger.info(f"isMalicious : {self.isMalicious}")
            if not self.isMalicious == False:
                logger.info("checking malicious with VirusTotal")
                time.sleep(30)
                resp = self.vt.file_scan(self.file_path)
                time.sleep(30)
                report = self.vt.file_report([resp['json_resp']['resource']])
                if report["status_code"] == 204:
                    count = 0
                    while report["status_code"] == 204:
                        if count == 3:
                            count = 0
                            break
                        count = count + 1
                        time.sleep(60)
                        report = self.vt.file_report([resp['json_resp']['resource']])
                        logger.info(f"VIRUSTOTAL REPORT after retrying {self.file_path} {report}")

                elif report["status_code"] == 200:
                    logger.info(f'check_virustotal : response_code : {report["json_resp"]["response_code"]}')
                    if report["json_resp"]["response_code"] == 1:
                        logger.info(f"VIRUSTOTAL REPORT response code retrying {report['json_resp']['response_code']}")

                        self.virus_total_status = True
                        vt_file_name = self.directory + "/virustotal_" + self.hash + ".json"
                        with open(vt_file_name, "w") as fp:
                            fp.write(str(report))

                        if 'positives' in report["json_resp"]:
                            if int(report["json_resp"]["positives"] == 0):
                                self.isMalicious = False
                            else:
                                self.isMalicious = True

                logger.info(f"isMalicious : {self.isMalicious}")
                logger.info(
                    f"Processor : check_virustotal report status: {report['status_code']}"
                )
        except Exception as e:
            logger.error(f"Processor : check_virustotal error: {e}")
            raise e

    def get_metadata(self):
        logger.info("getting metadata of the file")
        try:
            self.metadata = FileService.get_file_meta(self.file_path)
            meta = self.metadata
            meta['url'] = None
            if meta:

                logger.info(f'get_metadata : bucket_name {self.bucket_name}')
                minio_meta = self.minio_meta
                logger.info(f'minio_meta {minio_meta}')
                if minio_meta:
                    if 'x-amz-meta-url' in minio_meta.metadata:
                        meta['url'] = minio_meta.metadata['x-amz-meta-url']
                ext = self.ext if self.ext is not None else ""
                real_name = self.filename + "." + ext
                meta["file_name"] = real_name
                meta['virus_total_status'] = self.virus_total_status
                meta['gw_rebuild_xml_status'] = self.gw_rebuild_xml_status
                meta['gw_rebuild_file_status'] = self.gw_rebuild_file_status
                meta['rebuild_hash'] = self.rebuild_hash
                meta['isMalicious'] = self.isMalicious

            meta_file_name = self.directory + "/metadata_" + self.hash + ".json"
            self.metadata = meta

            with open(meta_file_name, "w") as fp:
                fp.write(str(meta))

        except Exception as e:
            logger.error(f"Processor : get_metadata error: {e}")
            raise e

    def rebuild_glasswall(self):
        logger.info("rebuilding with GW engine")
        try:
            rebuild_file_name = self.hash + '.' + self.ext if self.ext is not None else self.hash
            response = GlasswallService.rebuild(
                rebuild_file_name, self.directory, Config.GW_REBUILD_MODE["file"]
            )
            logger.info(f"rebuild file response : {response} ")
            if response:
                file = response.content
                status = response.status_code
                self.rebuild_hash = hashlib.sha1(file).hexdigest()
                logger.info(f"status of rebuild file {response.status_code}")
                if status == 200:
                    self.gw_rebuild_file_status = True
                    with open(self.directory + f"/rebuild_{rebuild_file_name}", "wb") as fp:
                        fp.write(file)
            # Get xml report
            response = GlasswallService.rebuild(
                rebuild_file_name, self.directory, Config.GW_REBUILD_MODE["xml_report"]
            )
            logger.info(f"rebuild xml_file response : {response} ")
            if response:
                xml_file = response.content
                status = response.status_code
                logger.info(f"status of rebuild {response.status_code}")
                if status == 200:
                    self.gw_rebuild_xml_status = True
                    with open(
                            self.directory + f"/rebuild_report_" + self.hash + ".xml", "wb"
                    ) as fp:
                        fp.write(xml_file)

            logger.info(f"Rebuild_hash : {self.rebuild_hash}")

        except Exception as error:
            logger.error(f"Processor : rebuild_glasswall: {error}")
            raise error

    def prepare_result(self):
        try:
            logger.info(
                "combining all reports, original file and malicious file to a zip"
            )

            malware_zip_name = self.directory + "/" + self.hash + ".zip"
            ext = self.ext if self.ext is not None else ""
            real_name = self.filename + "." + ext
            original_file = self.directory + "/" + real_name
            os.rename(self.file_path, original_file)
            # zipfile.ZipFile(malware_zip_name, mode="w").write(
            #     original_file, basename(original_file)
            # )
            pyminizip.compress(original_file, None, malware_zip_name, 'infected', 5)
            try:
                os.remove(original_file)
            except Exception:
                logger.error(f"Unable to remove input file {original_file}")

            FileService.prepare_zip(
                zip_filename=self.directory.split("/")[-1],
                folder_path=self.directory,
                zip_path=Config.download_path,
            )

        except Exception as error:
            logger.error(f"Processor : prepare_result: {error}")
            raise error

    def upload(self):
        try:
            logger.info("uploading to minio")
            name = self.directory.split("/")[-1]
            self.minio.upload(
                file_path=Config.download_path + "/" + name + ".zip",
                bucket_name="processed",
                file_name=self.hash + ".zip",
            )
        except Exception as error:
            logger.error(f"Processor : upload error: {error}")
            raise error

    def send_mq(self):
        try:
            logger.info("sending file to rabbitmq for s3 sync, %s" % self.directory)
            name = self.directory.split("/")[-1]
            payload = {
                "s3_bucket": self.ext,
                "minio_bucket": "processed",
                "file": name + ".zip",
            }
            response = MQService.send(payload)

            meta = self.metadata
            meta['path'] = None
            logger.info(f's3 sync status : {response.status_code}')
            if response.status_code == 200:
                meta['path'] = self.ext + "/" + name + ".zip"
                logger.info(f"s3 upload_path : {meta['path']}")
                self.metadata = meta
            try:
                logger.info("Posting file information to DB")
                self.add_metadata_to_db(metadata=self.metadata)
            except Exception as err:
                logger.error(f"Error while posting data to DB {err}")
                raise err

        except Exception as error:
            logger.error(f"Processor : send_mq: {error}")
            raise error

    def upload_original_file_to_s3(self):
        logger.info("sending original file to s3 through storage micro service")
        malware_zip_name = self.directory + "/" + self.hash + ".zip"
        try:
            self.storage_base_url = os.environ.get("storage_base_url", None)
            bucket_name = os.environ.get("TESTING_S3_BUCKET")
            file_name = self.hash + ".zip"
            file = malware_zip_name
            payload = {'bucket_name': bucket_name, 'folder_name': None}
            files = {"file": (file_name, open(file, "rb")), }
            re = requests.post(self.storage_base_url + "upload_to_s3", files=files, params=payload)
            logger.info(f'Processor : upload_original_file_to_s3 : status : {re.status_code}')
        except Exception as error:
            logger.error(f"Process : upload_original_file_to_s3 : {error}")
            raise error

    def process(self, input_file):
        logger.info(f"processing Main file : {input_file}")
        self.input_file = input_file

        default_exceptions = Exception
        processes = [
            (self.check_virustotal, default_exceptions),
            (self.rebuild_glasswall, default_exceptions),
            (self.get_metadata, default_exceptions),
            (self.prepare_result, default_exceptions),
            (self.upload, default_exceptions),
            (self.send_mq, default_exceptions),
            (self.upload_original_file_to_s3, default_exceptions),
        ]

        files = self.get_files(input_file)
        logger.info("total files : {}".format(len(files)))
        logger.info(files)
        for f in files:
            logger.info(f"processing {f}")
            self.set_current_file(f)
            for proc, exceptions in processes:
                try:
                    proc()
                except exceptions as e:
                    logger.error(f"Error processing file {f} : " + str(e))
                    break

    def add_metadata_to_db(self, metadata):
        f = FileInfo(filename=metadata['file_name'], path=metadata['path'], size=metadata['size'],
                     type=metadata['extension'], isMalicious=metadata['isMalicious'],
                     original_hash=metadata['original_hash'], rebuild_hash=metadata['rebuild_hash'],
                     date_created=metadata['date_created'],
                     virus_total_status=metadata['virus_total_status'],
                     gw_rebuild_xml_status=metadata['gw_rebuild_xml_status'],
                     gw_rebuild_file_status=metadata['gw_rebuild_file_status'])
        try:
            logger.info("Posting metadat to DB")
            logger.info(f'File Name {f}')
            db.session.add(f)
            db.session.commit()
        except Exception as ex:
            logger.error(f'Error while posting to DB{ex}')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route("/process", methods=["POST"])
    def get_files():
        data = request.json
        """
        To do process file 
        """
        file = data.get("file", None)
        # bucket_name = data.get("bucket", None)
        if not file:
            return jsonify({"message": "No file"})

        Processor().process(file)
        return jsonify({})

    return app


app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
session_options = {'autocommit': False, 'autoflush': False}

db = SQLAlchemy(app)


class FileInfo(db.Model):
    __tablename__ = 'file_metadata'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(1000), index=True)
    path = db.Column(db.String(1000), nullable=True)
    size = db.Column(db.String(1000))
    type = db.Column(db.String(1000), index=True)
    isMalicious = db.Column(db.Boolean, default=False, nullable=False)
    original_hash = db.Column(db.String(1000), index=True)
    rebuild_hash = db.Column(db.String(1000), index=True)
    date_created = db.Column(db.DateTime, nullable=False)
    virus_total_status = db.Column(db.Boolean, default=False, nullable=False)
    gw_rebuild_xml_status = db.Column(db.Boolean, default=False, nullable=False)
    gw_rebuild_file_status = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return '<File %r>' % (self.filename)


db.create_all()
db.session.commit()
