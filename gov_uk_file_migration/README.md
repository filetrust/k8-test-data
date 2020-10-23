# Gov-UK files migrator and processor

## Usage
* Set .env variables from .env.sample

## Build

    `To build the Docker image and name it `gov-uk-migration` 

    `docker build -t gov-uk-migration .`
    
    `docker build -t storage:1.0 ../storage`
    
    `docker build -t k8-file-processor:1.0 ../file_processor`
    
    `docker build -t glasswall-rebuild:1.0 ../glasswall_rebuild`
    
    `docker build -t k8-s3-sync ../s3_sync`
    
    
## To run

    `docker-compose up -d postgres`
    
    `docker-compose up`
    
