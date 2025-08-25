#!/bin/bash

# install kind
function install_kind {
  curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.29.0/kind-linux-amd64
  sudo install -o root -g root -m 0755 kind /usr/local/bin/
  kind version
  if [ $? -ne 0 ]; then
    echo "Failed to install kind"
    exit 1
  fi
}

# setup kind cluster
function setup_cluster {
  local public_ip=$1

  local host_ip=$(hostname -I | awk '{print $1}')

  echo "Creating kind cluster with API server address: $host_ip"

  # if previous kubeconfig exists, remove it
  sudo rm -rf ~/.kube/*

cat <<EOF | sudo kind create cluster --config -
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  apiServerAddress: "$host_ip"
  apiServerPort: 6443
nodes:
  - role: control-plane
    extraPortMappings:
      - containerPort: 32080
        hostPort: 80
        protocol: TCP
        listenAddress: "$host_ip"
      - containerPort: 32443
        hostPort: 443
        protocol: TCP
        listenAddress: "$host_ip"
kubeadmConfigPatches:
  - |
    kind: ClusterConfiguration
    apiServer:
      certSANs:
      - "localhost"
      - "127.0.0.1"
      - "$host_ip"
      - "$public_ip"
      - "*.centralindia.cloudapp.azure.com"
      extraArgs:
        runtime-config: ""
EOF
  if [[ $? -ne 0 ]]; then
    echo "Failed to create kind cluster"
    # it might have failed due to cni issue(https://bugs.launchpad.net/ubuntu/+source/libpod/+bug/2024394)
    if [[ -f /etc/cni/net.d/kind.conflist ]]; then
      echo "CNI configuration file found, attempting to fix..."
      # replace "cniVersion": "1.0.0", with 0.4.0
      # if the file contains "cniVersion": "1.0.0"
      if grep -q '"cniVersion": "1.0.0"' /etc/cni/net.d/kind.conflist; then
        sudo sed -i 's/"cniVersion": "1.0.0"/"cniVersion": "0.4.0"/' /etc/cni/net.d/kind.conflist
        setup_cluster "$public_ip"
      fi

    fi
  fi

  echo "Kind cluster created successfully"
}

# main
main() {

  local public_ip=$1

  # check kind
  if ! command -v kind &> /dev/null; then
    echo "kind not found, installing..."
    install_kind
  else
    echo "kind is already installed"
  fi

  # check kind cluster
  if sudo kind get clusters | grep -q kind &> /dev/null; then
    echo "kind cluster is already created"
    if sudo podman ps -a --format '{{.Names}}' | grep -q "^kind-control-plane$"; then
      if sudo podman ps --format '{{.Names}}' | grep -q "^kind-control-plane$"; then
        echo "kind-control-plane is running"
      else
        echo "kind-control-plane is not running"
        echo "trying to start kind-control-plane"
        sudo podman start kind-control-plane
        if [[ $? -ne 0 ]]; then
          echo "Failed to start kind-control-plane"
          exit 1
        fi
      fi
    else
      echo "kind-control-plane container does not exist"
      echo "trying to re-create cluster"
      kind delete cluster
      setup_cluster "$public_ip"
    fi
  else
    echo "kind cluster not found, creating..."
    setup_cluster "$public_ip"
  fi

  echo ""
  echo "Creating public kubeconfig"
  sudo cp /root/.kube/config ~/.kube/azure-public-kubeconfig
  # get the host IP again for replacement
  local host_ip=$(hostname -I | awk '{print $1}')
  # replace private ip with public ip
  sudo sed -i "s/$host_ip/$public_ip/g" ~/.kube/azure-public-kubeconfig
  sudo chown $(id -u):$(id -g) ~/.kube/azure-public-kubeconfig


}

main "$@"