import logging as logger
import os

import requests

logger.basicConfig(level=logger.INFO)
import pandas
class Crawler:

    def __init__(self):
        self.csv_file = "./ProxyResult.csv"
        self.download_folder="download"

    def read_csv(self):
        try:
            # reading the CSV file
            #getting only responseCode and URL
            col_list = ["responseCode", "URL"]
            df = pandas.read_csv(self.csv_file,usecols=col_list)
            return df
        except Exception as e:
            logger.error(f"Error in reading csv { self.csv_file} : {e}")
            raise e

    def process_and_download(self,df):
        #extra proxy url ,
        #check status
        #replace to proxy url with original
        #Download file to expected path under download folder
        try:
            for row in df.itertuples():
                logger.info(f"Status code :{row.responseCode}")
                if not row.responseCode == "200":
                    proxy_url = row.URL
                    logger.info(f"Proxy_url :{proxy_url}")
                    url=proxy_url.replace(".glasswall-icap.com","")
                    logger.info(f"Modified_url :{url}")
                    list=proxy_url.split("/")[3:10]
                    file_name = proxy_url.split("/")[-1]

                    delimiter = "/"
                    target_folder = delimiter.join(list)

                    response=requests.get(url)
                    if response.status_code==200:
                        download_folder=os.path.join(self.download_folder, target_folder)
                        logger.info(f"Download folder :{download_folder}")

                        if not os.path.exists(download_folder):
                            os.makedirs(download_folder)
                        file_path=download_folder + "/" + file_name

                        logger.info(f"File path :{file_path}")

                        with open(file_path, "wb") as fp:
                            fp.write(response.content)
                    else:
                        logger.info(f"Failed to download file {url}")

        except Exception as e:
            logger.error(f"Error in processing file {e}")
            raise e


if __name__ == "__main__":
    crawler=Crawler()

    df=crawler.read_csv()
    df = pandas.DataFrame(df)

    crawler.process_and_download(df)

