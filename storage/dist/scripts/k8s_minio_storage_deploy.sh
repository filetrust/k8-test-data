#!/bin/sh

#export KUBECONFIG=/etc/kubernetes/admin.conf
kubectl create -f ../k8s/k8s_minio_storage_deploy_def.yml
kubectl create -f ../k8s/k8s_minio_storage_ingress_def.yml
