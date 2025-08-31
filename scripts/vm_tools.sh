#!/bin/bash

sudo apt-get update -y

# install required tools
sudo apt-get install -y git curl podman

# ensure /usr/local/bin/
sudo mkdir -p /usr/local/bin/

# install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/
kubectl version --client

# setup helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version