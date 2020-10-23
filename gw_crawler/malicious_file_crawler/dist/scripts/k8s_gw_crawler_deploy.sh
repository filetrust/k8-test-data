#!/bin/sh

#export KUBECONFIG=/etc/kubernetes/admin.conf
kubectl create -f ../k8s/k8s_scrapyd_deploy_def.yml
kubectl create -f ../k8s/k8s_gw_crawler_job_def.yml
