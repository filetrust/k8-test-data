#!/bin/sh

DOCKER_REGISTRY=karthyuom
DOCKER_VERSION=1.1

docker build -t $DOCKER_REGISTRY/k8-file-distribution:$DOCKER_VERSION -f ../../Dockerfile ../../

docker push $DOCKER_REGISTRY/k8-file-distribution:$DOCKER_VERSION
