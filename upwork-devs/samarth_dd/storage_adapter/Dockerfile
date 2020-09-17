FROM python:3-alpine


RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN apk add --no-cache libressl-dev musl-dev libffi-dev


RUN mkdir /storage

COPY storage /storage

WORKDIR /storage

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8001
CMD ["cd", "/storage"]
CMD [ "python", "-m", "src.adapter_object_creator.py"]
