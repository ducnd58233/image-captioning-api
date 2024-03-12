# Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installing](#installing)
- [Running the App](#running-the-app)
  - [Local](#local)

# Getting Started

- This project is about generating text from image. To get started, follow the instructions below.
- This is the project structure:

```txt
|-jenkins                      - Directory for Jenkins configuration files
|-k8s                          - Directory for Helm chart to deploy the application
|-models                       - Directory for Deep Learning models
|--vocabs.json                 - File for vocabulary NLP model
|-notebooks                    - Directory for crawling and training data
|--data                        - Directory for data (crawling)
|--data_crawler.ipynb
|--requirements.txt            - File contains packages for training and crawling
|--training.ipynb
|-src                          - Directory for main application
|-Dockerfile                   - File to create and deploy main application
|-Makefile                     - File contains some commands (make + <cmd>)
|-requirements.txt             - File contains packages for main application
```

# Prerequisites

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Anaconda (optional)](https://www.anaconda.com/download)
- [Python: **_3.9_**](https://www.python.org/downloads/)
- [Kubernates](https://kubernetes.io/releases/download/)
- [Minikube (for weak machine) - using this in this project](https://minikube.sigs.k8s.io/docs/start/) or [Minikf](https://v0-6.kubeflow.org/docs/other-guides/virtual-dev/getting-started-minikf/)
- [Docker](https://docs.docker.com/desktop/)
- Makefile (optional)

# Installing

Using anaconda:

```bash
conda create -n <env_name> python=3.9
conda activate <env_name>
pip install -r requirements.txt
```

# Running the App

## Local

### Running in Local

```bash
uvicorn src.main:app --reload
```

Or

```bash
make start-app-dev
```

## Running in Docker

```bash
docker build --tag "jigglediggle1/image-captioning" .
docker run -d --name="image-captioning" -p 30000:30000 "jigglediggle1/image-captioning"
```

Or

```bash
make start-app-dev
```

## Running with K8S

### Start the Docker (Engine or Desktop)

Notes: The docker's memory default only has `3GB` memory, may not enough for this project, should increase it (in Desktop) to at least `6G`

### Start the Minikube

Notes: The minikube's memory default only has `2GB` memory, may not enough for this project, should increase it by the following command in MB (**and it should be lower than Docker's memory**)

```bash
minikube config set memory 4000
```

And delete the `minikube` (if you already initialized one before).\
<span style="color:yellow">WARNING:</span> This will <span style="color:red">delete all</span> of your pods

```bash
minikube delete
```

Then start the minikube

```bash
minikube start
```

Minikube has dashboard to monitor the pods and more. To open it, run:

```bash
minikube dashboard
```

### Run the K8S Helm Chart

```
helm upgrade --install nginx-ingress ./k8s/nginx-ingress/. --namespace=image-captioning
helm upgrade --install ic-app ./k8s/ic-app/. --namespace=image-captioning
```

Then, we will need to run [minikube tunnel](https://minikube.sigs.k8s.io/docs/commands/tunnel/)

```bash
minikube tunnel
```

And finally, open new terminal, run port-forward to use the application

```bash
kubectl --namespace image-captioning port-forward svc/ic-app 5000:30000
```

Or

```bash
export NODE_PORT=$(kubectl get --namespace {{ .Release.Namespace }} -o jsonpath="{.spec.ports[0].nodePort}" services {{ include "ic-app.fullname" . }})
kubectl --namespace {{ .Release.Namespace }} port-forward $POD_NAME 5000:30000
```
And open this url to visit the application: [localhost:5000/docs](localhost:5000/docs)
