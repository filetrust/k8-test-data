#!/bin/sh

#export KUBECONFIG=/etc/kubernetes/admin.conf
kubectl create -f ../k8s/k8s_rabbitmq_process_deploy_def.yml
kubectl create -f ../k8s/k8s_rabbitmq_process_ingress_def.yml
