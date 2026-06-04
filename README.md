# SecureShare — Secure File Sharing Platform

A secure file-sharing web application built with Flask that allows users to upload, manage, and securely share files through private access links.

This project also demonstrates modern DevOps practices, including containerization, automated code quality checks, static code analysis, CI/CD automation, and Docker image publishing.

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

* Python 3
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
* GitHub Actions
* Flake8
* SonarCloud
* Docker Hub

---

## Project Structure

```text
secure-file-sharing-platform/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
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

```text
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

## Application Pages

| Route            | Description             |
| ---------------- | ----------------------- |
| `/`              | Home page               |
| `/login`         | User login              |
| `/register`      | User registration       |
| `/dashboard`     | User dashboard          |
| `/files`         | Upload and manage files |
| `/profile`       | Profile management      |
| `/share/<token>` | Public file download    |

---

## DevOps Implementation

This project includes a complete DevOps workflow.

### Containerization

* Dockerized Flask application
* Dockerized PostgreSQL database
* Docker Compose orchestration
* Portable and reproducible development environment

### Continuous Integration

Implemented with GitHub Actions:

* Repository checkout
* Dependency installation
* Project validation
* Flake8 linting
* SonarCloud analysis
* Docker image build

### Code Quality

Automated quality checks include:

* PEP8 compliance verification with Flake8
* Static code analysis with SonarCloud
* Code smell detection
* Security hotspot detection
* Maintainability analysis

### Continuous Delivery

Docker images are automatically published to Docker Hub using:

```text
latest
sha-<commit-id>
```

This enables:

* Version tracking
* Reproducible deployments
* Reliable rollbacks

---

## Data Persistence

The application uses Docker volumes to persist database data.

### PostgreSQL Volume

- PostgreSQL data is stored in a Docker-managed volume
- This ensures data is not lost when containers are restarted or rebuilt

---

## CI/CD Pipeline

The GitHub Actions workflow is composed of three stages:

### 1. Lint & Validation

Checks:

* Project structure
* Required files
* Python code quality

Tools:

* Flake8

### 2. SonarCloud Analysis

Performs:

* Static code analysis
* Bug detection
* Security checks
* Code quality evaluation

Tools:

* SonarCloud

### 3. Docker Build & Publish

Performs:

* Docker image build
* Image tagging
* Docker Hub publication

Tools:

* Docker Buildx
* Docker Hub

---

## Architecture

```text
┌──────────────────────┐
│      Flask App       │
│      Container       │
└──────────┬───────────┘
           │
           │ SQLAlchemy
           │
┌──────────▼───────────┐
│      PostgreSQL      │
│      Container       │
└──────────────────────┘
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

## Future Improvements

Potential future enhancements:

* Virus scanning
* Kubernetes deployment
* Terraform infrastructure provisioning
* Monitoring with Prometheus and Grafana

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

## Author

Amenallah Khelil

Telecommunications Engineering Student

Interested in:

* DevOps
* Cloud Computing
* Cybersecurity
* MLOps
* Software Engineering

GitHub: https://github.com/amenkhelil
Linkedin: https://www.linkedin.com/in/amenallah-khelil
