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
        
        python -m src.glasswall_crawler_runner DASMAL

        Note:You can run single cralwer or  multiple site crawler.See config.ini
    
```
##update storage/src/config/config.ini

        [MINIO]
        ENDPOINT='http://play.min.io:80'
        HOSTNAME=play.min.io:80
        FILES_STORE=s3://mybucket/bucket3/
        AWS_ACCESS_KEY_ID=Q3AM3UQ867SPQQA43P2F
        AWS_SECRET_ACCESS_KEY=zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG
        
        [S3]
        ENDPOINT=http://172.18.0.9:9000
        HOSTNAME=127.0.0.1:9001
        AWS_ACCESS_KEY_ID=minio1
        AWS_SECRET_ACCESS_KEY=minio1@123
        SECURE=False

##update malicious_file_crawler/src/config config.ini

        [DASMAL]
        name = das_malwerk_scraper
        url = https://das-malwerk.herokuapp.com/
        
        [TEKDEF]
        name = tek_defence_spider
        login_url = http://www.tekdefense.com/downloads/malware-samples/
        file_page_url = http://www.tekdefense.com/downloads/malware-samples/

### Run scrapper in kubernetes
```
    docker build -t glasswallcrawler:1.0 .
    
    kubectl apply -f minio-service.yaml
    
    kubectl apply -f deployment.yaml
   
    docker run --env-file .env glasswallcrawler:1.0

```










