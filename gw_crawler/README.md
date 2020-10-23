# GW Crawler

## Scraper Sites 

**VirusShare**: https://virusshare.com/
  - Requires login (free)
  - ZIP password is “infected"

**The Zoo**: https://github.com/ytisf/theZoo

  - Look in malwares/Binaries subdirectory
  - ZIP password is “infected"

**Malshare**: https://malshare.com

  - Immediate access - register to get an API key allowing download of 1000 samples/day

**Das Malwerk**: http://dasmalwerk.eu/

  - Immediate access
  - ZIP password is “infected”
  
**Tek Defence** : http://www.tekdefense.com/downloads/malware-samples/
  - Immediate access

## Usage  

    Create virusshare api key from https://virusshare.com/apiv2_reference , 
    
    Create malshare api key from https://malshare.com/doc.php,
    
    Update .env (see .env_sample)
    
## Build

```
    docker build -t glasswallcrawler:1.0 .
     
```
## To push

    `docker push <username>/glasswallcrawler:1.0`











