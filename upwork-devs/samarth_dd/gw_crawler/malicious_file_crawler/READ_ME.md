## Run scraper in local machine

###Create virtual env 

```
        virtualenv venv
    
```

### Install requirements
```
        cd malicious_file_crawler/
        pip install -r requirements.txt
```

### Run scrapper

```
        configure .env (Regfere .env sample)
        create a bucket named mybucket in minio
 
        python -m src.glasswall_crawler_runner DASMAL,TEKDEF

        Note:You can run single cralwer or  multiple site crawler.See config.ini
    
```

### Run scrapper in kubernetes(Work in progress)
```
    docker build -t glasswallcrawler:1.0 .
    
    kubectl apply -f minio-service.yaml
    
    kubectl apply -f deployment.yaml
    
    docker-compose up -d
    
    docker run --env-file .env glasswallcrawler:1.0

```










