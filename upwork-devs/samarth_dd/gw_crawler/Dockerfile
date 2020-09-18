FROM python:3-alpine
RUN mkdir /malicious_file_crawler

RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN apk add --no-cache libressl-dev musl-dev libffi-dev

COPY malicious_file_crawler /malicious_file_crawler

WORKDIR /malicious_file_crawler

RUN pip install --no-cache-dir -r requirements.txt

CMD ["cd", "/malicious_file_crawler"]

CMD [ "python", "-m", "src.glasswall_crawler_runner","DASMAL" ]
