#!/bin/sh

DOCKER_REGISTRY=karthyuom
DOCKER_VERSION=1.5

docker build -t $DOCKER_REGISTRY/k8-s3-sync:$DOCKER_VERSION -f ../../Dockerfile ../../

docker push $DOCKER_REGISTRY/k8-s3-sync:$DOCKER_VERSION
