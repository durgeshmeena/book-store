#!/bin/bash

# check env variables required for creating k8s secret
if [[ -z "$SECRET_KEY" || -z "$MONGO_URI" ]]; then
  echo "SECRET_KEY and MONGO_URI environment variables must be set"
  exit 1
fi

namespace="book-store"

# create the namespace if it doesn't exist
kubectl create namespace $namespace --dry-run=client -o yaml | kubectl apply -f -

# create secret if it doesn't exist
kubectl create secret generic book-store \
    --from-literal=SECRET_KEY="$SECRET_KEY" \
    --from-literal=MONGO_URI="$MONGO_URI" \
    -n $namespace --dry-run=client -o yaml | kubectl apply -f -

# apply k8s manifests, stored in deployment of project
kubectl apply -f ./deployment/k8s-resources.yaml -n $namespace
