#!/bin/sh

export PYTHONUNBUFFERED=1
export MINIO_ENDPOINT=192.168.99.1:9001
export MINIO_ACCESS_KEY_ID="minio1"
export MINIO_SECRET_ACCESS_KEY="minio1@123"
export MINIO_SECURE=False
export MINIO_BUCKET="zip"
export MQ_USERNAME="guest"
export MQ_PASSWORD="guest"
export MQ_HOST="192.168.99.1"
export MQ_PORT="5672"
export MQ_EXCHANGE=
export MQ_EXCHANGE_TYPE=
export MQ_QUEUE="queue01"
export MQ_ROUTING_KEY="queue01"

CURRENT_DIR=`pwd`
cd ../../
python main.py

cd $CURRENT_DIR
