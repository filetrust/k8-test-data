#!/bin/sh

DOCKER_REGISTRY=karthyuom
DOCKER_VERSION=1.0

docker build -t $DOCKER_REGISTRY/glasswall-rebuild -f ../../Dockerfile ../../

docker push $DOCKER_REGISTRY/glasswall-rebuild
