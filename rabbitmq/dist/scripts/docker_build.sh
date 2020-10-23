#!/bin/sh

DOCKER_REGISTRY=karthyuom
DOCKER_VERSION=1.5

docker build -t $DOCKER_REGISTRY/rabbit-mq:$DOCKER_VERSION -f ../../Dockerfile ../../

docker push $DOCKER_REGISTRY/rabbit-mq:$DOCKER_VERSION
