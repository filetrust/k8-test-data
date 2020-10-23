# Storage Adapter Service
    
## Usage

    * Set .env variables from .env_sample

## Build

    To build the Docker image and name it `storage` run:

    docker build storage:1.0 .
    
## To push

`docker push <username>/storage:1.0`

## Endpoints 

| Endpoint | Description             | Payload     | Params | Data |
| -------- | ------------------------| ----------- |------| -----|
| `/ping` | Test connection   | `{"file_name": "<File_name>","bucket_name": "<bucket_name>"}` |	
| `/upload_stream` | upload byte data directly to minio   | - |	 bucket_name : <minio_bucket_name>, name : <object_name> , length : <length of bytedata>, metadata : <json_metadata> | Data : ByteData
