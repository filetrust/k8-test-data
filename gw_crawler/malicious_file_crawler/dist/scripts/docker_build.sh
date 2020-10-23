#!/bin/sh

DOCKER_REGISTRY=karthyuom
DOCKER_VERSION=1.0

docker build -t $DOCKER_REGISTRY/scrapyd:$DOCKER_VERSION -f ../../Dockerfile ../../

docker push $DOCKER_REGISTRY/scrapyd:$DOCKER_VERSION

docker build -t $DOCKER_REGISTRY/glasswallcrawler:$DOCKER_VERSION -f ../../../Dockerfile ../../../

docker push $DOCKER_REGISTRY/glasswallcrawler:$DOCKER_VERSION
