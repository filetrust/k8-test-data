# File Processor Service

## Usage
* Create virustotal_key from https://www.virustotal.com/
* Set .env variables from .env.sample

## Build

To build the Docker image and name it `k8-file-processor` run:

`docker build -t k8-file-processor .`

##To push
`docker push <username>/k8-file-processor`

## Endpoints 

| Endpoint | Description             | Payload     |
| -------- | ------------------------| ----------- |
| `/process` | Various file operations and bundle ziping and s3 synch   | `{"file": "<File_name>","bucket": "<bucket_name>"}` |	




