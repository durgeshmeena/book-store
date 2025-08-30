#!/bin/bash

# check if grafana admin password is set
if [[ -z "$GRAFANA_ADMIN_PASSWORD" ]]; then
  echo "GRAFANA_ADMIN_PASSWORD environment variable must be set"
  exit 1
fi

# add prometheus-community helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# update helm repos
helm repo update

# install monitoring stack(prometheus,grafana,kube-state-metrics) prometheus and create Service Monitor and Pod Monitor for book-store
helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
    --namespace monitoring --create-namespace \
    --debug \
    -f ./deployment/monitoring/kube-prometheus-stack-helm-values.yaml \
    -f ./deployment/monitoring/book-store-monitoring-helm-values.yaml

if [ $? -ne 0 ]; then
  echo "Failed to install kube-prometheus-stack"
  exit 1
fi    

# create configMap containgin grafana dashboard for book-store
kubectl apply -f ./deployment/monitoring/book-store-grafana-dashboard-config.yaml
kubectl apply -f ./deployment/monitoring/flask-app-internal-metrics-grafana-dashboard-config.yaml