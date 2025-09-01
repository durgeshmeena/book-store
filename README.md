# 📚 Book Store 

This project demonstrates modern DevOps and Cloud-Native practices by building, containerizing, and deploying a Flask-based Book Store application with full automation, Infrastructure as Code (IaC), and observability.

# 🚀 Features
## 🔹 Application & Containerization

- Flask Book Store Application – containerized Python microservice.

- Multi-stage Docker builds – lean and secure runtime images.

- Gunicorn server – production-ready WSGI with multiple workers.

- Distroless, non-root container – reduced attack surface for security.

- Multi-arch builds – compatible with both amd64 and arm64.

## 🔹 Infrastructure as Code (IaC)

- Terraform-based provisioning – declarative, repeatable environments on Azure Cloud.

- Modular structure – separate Terraform modules/projects:

  - Networking – VNet, Subnet, NSG with required ingress rules (SSH, HTTP, HTTPS, Kubernetes API).

  - VM Provisioning – Azure Linux VM (with Public IP + NIC) bootstrapped via Terraform provisioners.

  - Cluster Setup – KIND (Kubernetes-in-Docker) installed on VM, with kubeconfig dynamically retrieved.

  - Application Deployment – Book Store + observability stack deployed on the cluster.

- On-demand lifecycle – VM and cluster can be destroyed/re-created anytime to save cloud costs.

- Terraform remote state – securely stored in Azure Blob Storage for collaboration.

## 🔹 CI/CD with GitHub Actions

- End-to-end pipeline automating:

  - Infrastructure provisioning (Terraform).

  - Application build + Docker image push.

  - KIND cluster setup.

  - Deployment of workloads (Book Store, Prometheus, Grafana).

- Manual workflow dispatch – choose specific actions:

  - Create Storage

  - Provision VM

  - Create Cluster

  - Deploy Application

  - Destroy Infrastructure


- Secure credential management – handled with GitHub Secrets.

- Efficient builds – Docker layer caching

## 🔹 Observability & Monitoring

- Zero-code auto-instrumentation – Book Store Flask app uses OpenTelemetry without changing source code.

- Prometheus metrics export – HTTP request metrics (rate, errors, latency) exposed for scraping.

- Multi-process metrics support – handles Gunicorn workers correctly using OpenTelemetry multi-proc mode.

- Pre-configured Grafana dashboard – deployed as code, based on the RED Method (Rate, Errors, Duration):

  - Request Rate (RPS) & Error Rate (%)

  - Latency (p99, p95, p50)

  - Active Requests & Status Code distribution

  - Python process health: CPU, memory, garbage collection
  

## ⚙️ Setup Instructions

- 1️⃣ Create Free Tier account on Azure

- 2️⃣ Provision Infrastructure
    - Create azure storage for storing terraform backend
    - create vm & network resource
    - create kind cluster

- 3️⃣ Build & Deploy
    - Build Docker Image (required to setup dockerhub account)
    - Deploy Application
    - Deploy Observability
    - Deploy Nginx Ingress Controller (expose application and obserbavility using ingress)

- 4️⃣ Access Application

  - **App URL**: https://book-store.centralindia.cloudapp.azure.com/

  - **Prometheus**: https://monitoring-book-store.centralindia.cloudapp.azure.com/prometheus

  - **Grafana**: https://monitoring-book-store.centralindia.cloudapp.azure.com/grafana

## 💰 Cost Optimization

VM and resources can be destroyed with:

`terraform destroy`


Persistent data (Docker volumes, disks) remain intact across stop/start cycles.

Default setup is free-tier friendly – small VM sizes used.

## 🛠️ Tools & Technologies

- Flask, Gunicorn, Docker – Application & containerization

- Terraform, Azure, KIND – Infrastructure & cluster setup

- GitHub Actions – CI/CD pipeline

- OpenTelemetry, Prometheus, Grafana – Observability stack

## 📊 Dashboard Preview

The Grafana dashboard provides insights into:

-  Request Rate, Error Rate, Latency (RED Method)

-  CPU & Memory usage

-  Active Requests & Status breakdown

-  Python runtime metrics (GC, workers, etc.)

# Screenshots

## Aplication
### Home Page
  <img width="1460" height="781" alt="Application-1-Home" src="https://github.com/user-attachments/assets/2a6e879e-28ea-4083-bdd0-299f00d108c1" />

### Books Page
  <img width="1409" height="697" alt="Application-1-Books" src="https://github.com/user-attachments/assets/956a06ad-9976-4fe9-9e19-77202bd8bde7" />

### Import Books
  <img width="1171" height="560" alt="Application-1-Import-Books" src="https://github.com/user-attachments/assets/0fc325bd-391b-4672-9519-48e4398adf49" />


### Members
  <img width="1232" height="641" alt="Application-1-Members" src="https://github.com/user-attachments/assets/c82e5001-e6c1-4dfe-8fc9-d845ec66b6a9" />


### Menber profile
  <img width="1436" height="609" alt="Application-1-Member-Profile" src="https://github.com/user-attachments/assets/7e9559de-d3a9-44f0-8f1a-8a5bd8b84a25" />


### Transactions
  <img width="1037" height="475" alt="Application-1-Transactions" src="https://github.com/user-attachments/assets/adcafa61-cd59-4c86-885d-18a67ccc47aa" />


## Azure Infra Resources
<img width="1461" height="666" alt="Azure-Dashboard" src="https://github.com/user-attachments/assets/671ad694-f950-4da5-8a89-5b18c4d287a3" />

## CI/CD with IaC
### Docker Image Build
  ![github-workflow-CI-image-build](https://github.com/user-attachments/assets/9c4c7121-1cb2-4e8f-9262-d5b745ffc466)

### Azure Storage Provisioning
  ![github-workflow-infra-setup-storage-provision](https://github.com/user-attachments/assets/363a3648-b2f4-43ba-ae4b-72c8c90a9251)
  
### Cluster Setup
  ![github-workflow-infra-setup-cluster-setup](https://github.com/user-attachments/assets/66631acf-e627-4c20-aa16-a7f904f78c73)
  
### Deployments
  ![github-workflow-CD-deployment](https://github.com/user-attachments/assets/768d46d1-3e3f-4583-aa61-46dce10cdda3)


## Grafana Dashboards
<img width="1469" height="706" alt="Grafana-Dashboard-home" src="https://github.com/user-attachments/assets/ffabdef4-fc98-451a-86a3-c42bdb45d49c" />

### Kubernetes Pod Health
  <img width="1470" height="675" alt="grafana-k8s-pod-dashboard-full" src="https://github.com/user-attachments/assets/f3c8afef-cb64-4e86-919b-d5d42c4cd30c" />
  <img width="1469" height="515" alt="grafana-k8s-pod-dashboard-1" src="https://github.com/user-attachments/assets/e3fe9cd9-6ce6-4e89-8ea1-5e7cb4aff2ac" />
  <img width="1462" height="639" alt="grafana-k8s-pod-dashboard-2" src="https://github.com/user-attachments/assets/40df02f5-21d4-45c7-9edb-2c6a1b984ff7" />
  <img width="1470" height="534" alt="grafana-k8s-pod-dashboard-3" src="https://github.com/user-attachments/assets/3f6ee2a1-6187-410f-8c80-fe06d1a64937" />

### Application Health Overview
  <img width="1469" height="798" alt="grafana-otel-metrics-dashboard-full" src="https://github.com/user-attachments/assets/067555ae-2e5c-4b24-8ff7-bea4ba56cfc8" />
  <img width="1469" height="568" alt="grafana-otel-metrics-dashboard-1" src="https://github.com/user-attachments/assets/08a08f97-5e6d-42dc-b4ab-42eb0bc57a2b" />
  <img width="1461" height="376" alt="grafana-otel-metrics-dashboard-2" src="https://github.com/user-attachments/assets/a0e4aa78-90d8-4b7c-b722-6c5e474519ba" />
  <img width="1465" height="345" alt="grafana-otel-metrics-dashboard-3" src="https://github.com/user-attachments/assets/7fecc8eb-96f2-4830-9e69-708c4a48d5aa" />
  <img width="1465" height="391" alt="grafana-otel-metrics-dashboard-4" src="https://github.com/user-attachments/assets/d95c70d0-b0a0-49f1-8acc-1a704cca95b1" />








  


  



