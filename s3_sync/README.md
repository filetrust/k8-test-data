# S3 Sync Api

## Usage

* Set .env variables from .env_sample

## Build

To build the Docker image and name it `k8-s3-sync` run:

`docker build -t k8-s3-sync .`

## To push
`docker push <username>/rabbit-mq:1.0`

## Endpoints 

| Endpoint | Description             | Payload     |
| -------- | ------------------------| ----------- |
| `/tos3` |  Fetches file from minio and store it in S3   | `{"s3_bucket": "<s3_bucket_name>","minio_bucket": "<minio_bucket_namw>","file":"<file_name"}` |	

        