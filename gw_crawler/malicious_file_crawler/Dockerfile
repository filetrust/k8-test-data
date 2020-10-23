FROM python:3.6
SHELL [ "/bin/bash", "-c" ]

RUN mkdir /malicious_file_crawler
WORKDIR /malicious_file_crawler
EXPOSE 6800

RUN pip install python-dotenv==0.13.0
RUN pip install scrapy-dotpersistence==0.3.0
RUN pip install scrapyd
RUN pip install git+https://github.com/scrapy/scrapyd-client
RUN pip install python-scrapyd-api

COPY . .

CMD set -m; scrapyd & cd . && scrapyd-deploy  && fg scrapyd








