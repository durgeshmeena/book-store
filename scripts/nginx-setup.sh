#!/bin/bash

helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace

# create ingress resource for application
kubectl apply -f ./deployment/ingress.yaml -n book-store