#!/bin/sh

#export KUBECONFIG=/etc/kubernetes/admin.conf
kubectl create -f ../k8s/k8s_test_data_namespace_def.yml
kubectl create -f ../k8s/k8s_file_processor_deploy_def.yml
kubectl create -f ../k8s/k8s_file_processor_ingress_def.yml
