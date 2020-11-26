# GOV UK k8-test-data

#To run GOV_UK FILES please refer gov_uk_file_migration/readme.md

    # Gov-UK files migrator and processor

##Pre-requisites

###EC2
    Instance type - m5.xlarge
    Volume size - 48 gb
    custom security group
        minio - 9001
        postgres- 5432
        
        
## Usage

    * Set .env variables from .env.sample


## Build

     cd gov_uk_file_migration/

    `docker build -t gov-uk-migration .`
    
    `docker build -t storage:1.0 ../storage`
    
    `docker build -t k8-file-processor:1.0 ../file_processor`
    
    `docker build -t glasswall-rebuild:1.0 ../glasswall_rebuild`
    
    `docker build -t k8-s3-sync ../s3_sync`
   
## To run

    `docker-compose up -d postgres`
    
    `docker-compose up -d minio`
    
    `docker-compose up -d storage-adapter`
    
    `docker-compose up`
    
#Postgress
    
    Currently we are using Postgres in docker container

    You can setup external postgres by changin SQLALCHEMY_DATABASE_URI endpoint in file_processor/.env
    
    Download postgress browser client
    https://www.postgresql.org/download/
    
    Setup your db 
    Name : Anythin you want
    host: <EC2 IP>
    port:5432
    username : postgres
    password : toor
    
    table name: file_metadata
    
    Using simple sql queries, one can easily get desired information in CSV export
    
#Minio

    Minio will be having unprocessed files which are failed in file processor
    
    minio browser url : http://<EC2 IP>:9001/
    username : minio1
    password: minio1@123
    
##Possible Errors

    * Storage error in ec2
    
        Need to delete all data once it is processed.  
        If there is error for particular file format or type,it wont be deleted and it might stay in container leading to storage error(you will find it in minio)
        
   
    * icap Rebuild license error
    
        take latest icap libglasswall.classic.so and update in k8-test-data/glasswall_rebuild/Library/libglasswall.classic.so

        
    


