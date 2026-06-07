# SecureShare — Secure File Sharing Platform

A secure file-sharing web application built with Flask that allows users to upload, manage, and securely share files through private access links.

This project also demonstrates modern DevOps practices, including containerization, automated code quality checks, static code analysis, security scanning, CI/CD automation, Docker image publishing, and Kubernetes deployment.

---

## Overview

SecureShare enables authenticated users to:

* Create an account and securely log in
* Upload and manage files
* Generate secure sharing links
* Revoke file access at any time
* Download shared files through unique access tokens
* Manage personal profile information

The project was designed as both a full-stack web application and a practical DevOps learning project.

---

## Features

### User Authentication

* User registration
* Secure login and logout
* Session management using Flask-Login
* Profile management

### File Management

* Upload files
* Download files
* Delete files
* Personal file ownership

### Secure File Sharing

* Generate unique sharing links
* Token-based access control
* Public download links without authentication
* Share link revocation

### Responsive Interface

* Dashboard overview
* File management page
* Profile page
* Mobile-friendly design

---

## Tech Stack

### Backend

* Python 3.11
* Flask
* Flask-Login
* Flask-SQLAlchemy

### Database

* PostgreSQL

### Frontend

* HTML5
* CSS3
* JavaScript

### DevOps & Quality

* Docker
* Docker Compose
* Kubernetes (Minikube)
* GitHub Actions
* Flake8
* SonarCloud
* Trivy
* Docker Hub

---

## Project Structure

```text
secure-file-sharing-platform/
├── .github/
│   └── workflows/
│       └── ci.yml
├── k8s/
│   ├── namespace.yaml
│   ├── secret.yaml
│   ├── configmap.yaml
│   ├── postgres-volume.yaml
│   ├── postgres.yaml
│   ├── flask.yaml
│   └── ingress.yaml
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── sonar-project.properties
├── .gitignore
├── README.md
├── models/
│   ├── __init__.py
│   └── models.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── files.html
│   ├── profile.html
│   └── error.html
└── uploads/
```

---

## One-Command Setup

This project is fully containerized using Docker and Docker Compose.

No manual installation of Python, PostgreSQL, or dependencies is required.

### Requirements

- Docker
- Docker Compose

### Run the project

```bash
git clone https://github.com/amenkhelil/secure-file-sharing-platform.git
cd secure-file-sharing-platform
docker compose up --build
```

The application will be available at:

```
http://localhost:5000
```

---

## Docker Commands

### Start Services

```bash
docker compose up -d
```

### Stop Services

```bash
docker compose down
```

### View Logs

```bash
docker compose logs -f
```

### Rebuild Containers

```bash
docker compose up --build
```

---

## Kubernetes Deployment

The project includes a complete Kubernetes setup for local deployment using Minikube.

### Requirements

- Docker
- Minikube
- kubectl

### Start the cluster

```bash
minikube start --driver=docker
minikube addons enable ingress
```

### Deploy

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/
```

### Check status

```bash
kubectl get pods -n secure-share
```

### Access the application

```bash
minikube service flask-service -n secure-share
```

### Stop

```bash
kubectl delete -f k8s/
minikube stop
```

---

## Kubernetes Resources

| File | Resource |
|---|---|
| `namespace.yaml` | Isolated environment for all resources |
| `secret.yaml` | Database credentials and Flask secret key |
| `configmap.yaml` | Database connection URL |
| `postgres-volume.yaml` | Persistent storage for PostgreSQL data |
| `postgres.yaml` | PostgreSQL Deployment and Service |
| `flask.yaml` | Flask Deployment and Service |
| `ingress.yaml` | External HTTP routing |

---

## Application Pages

| Route | Description |
|---|---|
| `/` | Home page |
| `/login` | User login |
| `/register` | User registration |
| `/dashboard` | User dashboard |
| `/files` | Upload and manage files |
| `/profile` | Profile management |
| `/share/<token>` | Public file download |

---

## DevOps Implementation

This project includes a complete DevOps workflow.

### Containerization

* Dockerized Flask application using `python:3.11-slim`
* Dockerized PostgreSQL database
* Docker Compose orchestration
* Portable and reproducible development environment

### Continuous Integration

Implemented with GitHub Actions:

* Repository checkout
* Project structure validation
* Flake8 linting
* Kubernetes YAML syntax validation
* SonarCloud analysis
* Docker image build and publish
* Trivy security scan

### Code Quality

Automated quality checks include:

* PEP8 compliance verification with Flake8
* Static code analysis with SonarCloud
* Code smell detection
* Security hotspot detection
* Maintainability analysis

### Continuous Delivery

Docker images are automatically published to Docker Hub using:

```
latest
sha-<commit-id>
```

This enables:

* Version tracking
* Reproducible deployments
* Reliable rollbacks

---

## CI/CD Pipeline

The GitHub Actions workflow is composed of four stages:

### 1. Lint and Validate

* Project structure check
* Python syntax and code style with Flake8
* Kubernetes YAML syntax validation
* Confirms `.env` is not committed

### 2. SonarCloud Analysis

* Static code analysis
* Bug and security hotspot detection
* Code quality evaluation

### 3. Docker Build and Publish

* Docker image build using `python:3.11-slim`
* Tagging with `:latest` and `:sha-<commit>`
* Publication to Docker Hub

### 4. Trivy Security Scan

* Scans the published Docker image for vulnerabilities
* Reports CRITICAL, HIGH, and MEDIUM severity issues
* Reduced from 822 vulnerabilities (`python:3.11`) to 38 (`python:3.11-slim`)

---

## Data Persistence

### Docker Compose

PostgreSQL data is stored in a Docker-managed volume and survives container restarts.

### Kubernetes

PostgreSQL data is stored in a PersistentVolumeClaim (PVC) mounted at `/var/lib/postgresql/data`. Uploaded files are also persisted within the cluster.

---

## Architecture

### Docker Compose

```
┌──────────────────────┐
│      Flask App       │
│      Container       │
└──────────┬───────────┘
           │ SQLAlchemy
┌──────────▼───────────┐
│      PostgreSQL      │
│      Container       │
└──────────────────────┘
```

### Kubernetes

```
Browser
   │
   ▼
Ingress (nginx)
   │
   ▼
flask-service (ClusterIP)
   │
   ▼
Flask Pod
   │
   ▼
postgres-service (ClusterIP)
   │
   ▼
PostgreSQL Pod
   │
   ▼
PersistentVolumeClaim
```

---

## SonarCloud Integration

The project is connected to SonarCloud for continuous inspection of:

* Reliability
* Security
* Maintainability
* Code duplication
* Technical debt

Each push triggers a new analysis through GitHub Actions.

---

## Security Considerations

For production deployments:

* Use HTTPS
* Secure PostgreSQL credentials
* Store secrets in environment variables
* Configure regular backups
* Restrict upload types and sizes
* Use a production-grade reverse proxy

---

## Future Improvements

* Terraform infrastructure provisioning
* Monitoring with Prometheus and Grafana

---

## Author

Amenallah Khelil

Telecommunications Engineering Student @ ENET'Com

Interested in DevOps, Cloud Computing, Cybersecurity, and MLOps.

- GitHub: https://github.com/amenkhelil
- LinkedIn: https://www.linkedin.com/in/amenallah-khelil