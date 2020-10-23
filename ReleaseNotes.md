#k8-test-data

# Release 0.3
## Date : 14/10/2020 [github commit link](https://github.com/k8-proxy/k8-test-data/commit/1f4ec83730357d62e80d494eb12b54a52c1f1c44)
           

* Integration of Distribution Api , GW_crawler , Storage , Rabbit mq , glass_rebuild , file processor and s3 sync modules

* File processing bug fixes, suppport for icap_rebuild file and xml report, fixed processing of zip files

* Exception handling in all places

* Sy sync and creating folder in s3 and storing files under extension name as folder name

* The integration is tested and imporved efficiency

* Deployment of codebase in ec2 instance

* Bundle zip will contain metadata.json, rebuild_xml , rebuild file , virustotal report, original file inside zip file 

* Gloabl hashing is done and the files in bundle zip are stored with hash name

* Collection of 10000 files in glasswall s3 under bucket k8-test-data ( in progress )

* Refactoring of api calls configartable from .env files

### ToDo Tasks

* Configaration ELK for logging

* Batch processing of crawler

* Reaching 4million target

* Testing the code for large data

* Completing pending SOW tickets

* Data persistance

* Multilevel compressed test file with malicious content.

* Test files with different type of supported compression Zip, 7z, gz, tar, rar.


# Release 0.2
## Date : 6/10/2020


[github commit link](https://github.com/k8-proxy/k8-test-data/commit/048699117da4f57b1283765033ba1a4c1097252f)
            
            
**All entities will be running in different pod and are independent of each other and communicate through endpoints.**

        The entities are listed below

        Gw Crawler , 
        
        Storage adapter ,
        
        File processing , 
        
        Rabbit MQ reciver ,

        Rabbit MQ publisher,
        
        Dsitrubution api,
        
        s3 sync
             
**Web scraping for below sites has been completed**

        VirusShare: https://virusshare.com/
        
        The Zoo: https://github.com/ytisf/theZoo/
        
        Malshare: https://malshare.com/
        
        Das Malwerk: http://dasmalwerk.eu/
        
        Tek Defecnce: http://www.tekdefense.com/
        
**Minio Storage**

        GW_Crawler communicate with Storage adapter using api endpoint to call minio adapter.
        
        Stores malware files directly to minio.
        
        Files will be stored in minio bucket where bucket name will be extension of files.
        
        The files will be renamed with global sha1 hashing before storing it to minio. ( Filename = hash + extension )


**Rabbit MQ reciver**,
        Rabbit mq reciver uses rabbit mq queueing.

        Reciver recives minio files from the queue and send it to File processing module

**Rabbit MQ publisher**
        Rabbit MQ publisher runs asynchronous process where it will get all the files from minio endpoint.

        Send it to rabbit mq queue for reciver.

**File processing**

        The files stored in minio will be downloaed in this pod.
        
        If it is zip file, it will be unzipped first and sent to next step of file processing.
        
        Metadata like name, extension , size and hash will be extracted and saved in a json file
        
        The file is sent to virus total scan and report is fetched and saved in a file
        
        The file is sent to GW icap rebuild and clean file will be downloaded
        
        Finally metadata json file, virus total report, GW icap cleaned file along with original malware is bungle zipped with hash of file as zipname.
        
        The bundle zip is stored in the minio pod with "processed" as bucket name
        
        Once bundle minio upload is done s3 sych will be triggered and queued through rabbitmq by  passing consumer minio and reciver s3 endpoints.
        
**s3 sync**

        s3 synch will accept minio endpoint as consumer, s3 endpoint as target endpoint
        
        It downloads from minio and sync it to s3 storage.
    
**File Distribution API**

        This api is responsible for dsitribution of the the above bundle zip on demand.

## Tasks pending for next release
        Batch processing in gw_crawler

        Collecting atleast 10000 malware files and do file processing for the same and store in s3

        Configaration of ELK for logs and cache

        selectConnection instead of BlockingConnection in rabbit mq.

        Exception code for GW rebuild API failure, should be there in Ashish code.

        Testing for large amount of data and handling edge condition


# Release 0.1 
## Date : 18/09/2020

        Goal : Goal is to fetch malware files from various sites, store it in cloud and distribution of the same using api

        The code does web crawling of Das malverk site https://das-malwerk.herokuapp.com/ and fetches malicious zip 

        The app is fetching all malicious zip links from https://das-malwerk.herokuapp.com
        
        We are downloading only .zip files .
        
        The web scraper , minio and distribution api will be running in differnet pods and independent of each other
        
## Pedning tasks

        Fetching XML report from virustotal is not implemented since once we send file to virustotal,it will go to queue and report will be generated after some minites. 
        
        Storing zip according to file type is yet to be done.
        
        Persisting transaction in mysql is yet to be completed.
        
