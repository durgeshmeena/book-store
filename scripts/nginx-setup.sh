#!/bin/bash

# install ingress-nginx controller
# use fixed nodePort (80:32080, 443:32443)
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace \
  --set controller.service.type=NodePort \
  --set controller.service.nodePorts.http=32080 \
  --set controller.service.nodePorts.https=32443

# exit if the release is not successful
if [ $? -ne 0 ]; then
  echo "Failed to install ingress-nginx"
  exit 1
fi

# wait for all pods to be up
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s


# create ingress resource for application
kubectl apply -f ./deployment/ingress.yaml -n book-store