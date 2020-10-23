# Compressed File Generator

    Downloads file from minio and compresss to 7z,rar,zip,tar,gz and upload to s3 bucket 
    
## Usage
* Set .env variables from .env.sample


## Build

    `To build the Docker image and name it `compressed-file-generator` 

    `docker build -t compressed-file-generator .`


##To run

     cd k8-test-data/
     
         docker-compose up -d minio
         docker-compose up -d storage_service
         
     cd compressed-file-generator/
     
        `docker run --env-file .env compressed-file-generator`

