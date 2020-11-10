#CSV Crawler for gov uk excel
    Crawls CSV,
    Check status,if not 200 then proceed,
    Replace proxy url with original url,
    Download file with modified url to expected path.
    
##Usage
    Add csv file under csv_cralwer
    Change the self.csv_file  in giv_uk_csv_crawler.csv to uploaded csv file name 

##Run
    pip install -r requirements.txt 
    
    python gov_uk_csv_crawler.py
