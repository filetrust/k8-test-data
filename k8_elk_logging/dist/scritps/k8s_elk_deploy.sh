#!/bin/sh

#export KUBECONFIG=/etc/kubernetes/admin.conf
kubectl create -f ../k8s/k8s_common_namespace_def.yml
kubectl create -f ../k8s/k8s_elasticsearch_deploy_def.yml
kubectl create -f ../k8s/k8s_elasticsearch_ingress_def.yml
kubectl create -f ../k8s/k8s_kibana_deploy_def.yml
kubectl create -f ../k8s/k8s_kibana_ingress_def.yml
kubectl create -f ../k8s/k8s-filebeat-deploy.yml
