#!/bin/sh

#export KUBECONFIG=/etc/kubernetes/admin.conf
kubectl create -f ../k8s/k8s_s3_sync_deploy_def.yml
kubectl create -f ../k8s/k8s_s3_sync_ingress_def.yml
