#!/bin/sh

DOCKER_REGISTRY=karthyuom
DOCKER_VERSION=1.0.22

docker build -t $DOCKER_REGISTRY/k8-file-processor:$DOCKER_VERSION -f ../../Dockerfile ../../

docker push $DOCKER_REGISTRY/k8-file-processor:$DOCKER_VERSION
