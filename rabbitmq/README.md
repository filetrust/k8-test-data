# Rabbit Mq Api

## Usage

* Set .env variables from .env_sample

## Build

To build the Docker image and name it `rabbit-mq:1.0` run:

`docker build -t rabbit-mq:1.0 .`

## To push
`docker push <username>/rabbit-mq:1.0`

## Endpoints 

| Endpoint | Description             | Payload     |
| -------- | ------------------------| ----------- |
| `/publish` | Publisher add file to queue and Consumer fetches the file from the queue and calls file processing   | `{"file_name": "<File_name>","bucket_name": "<bucket_name>"}` |	

