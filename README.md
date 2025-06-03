# Food CO2 Estimator

Estimate CO2 emissions from recipe ingredient lists using Large Language Models (LLMs). This project fetches, parses, and analyzes recipe data to provide CO2 emission estimates.

## Table of Contents

- [Food CO2 Estimator](#food-co2-estimator)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Backend](#backend)
    - [Running Locally](#running-locally)
    - [Docker (Backend)](#docker-backend)
    - [Cloud Deployment (Backend)](#cloud-deployment-backend)
  - [Frontend](#frontend)
    - [Docker (Frontend)](#docker-frontend)
    - [Cloud Deployment (Frontend)](#cloud-deployment-frontend)

---

## Features

- Estimate CO2 emissions for recipes via web interface or API
- Dockerized backend and frontend for easy deployment

---

## Installation

Install Python dependencies:

```bash
poetry install
```

---

## Environment Variables

Copy `template.env` to `.env` and fill in the required values. These variables are used for both local and Docker deployments.

---

## Backend

### Running Locally

1. Install dependencies:
    ```bash
    poetry install
    ```
2. Start the Flask app:
    ```bash
    poetry run flask run
    ```
   The app will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Docker (Backend)

1. Build the backend image:
    ```bash
    docker build -t foodprint-backend:latest .
    ```
2. Run the backend container:
    ```bash
    docker run \
      --env-file .env \
      -p 8080:8080 \
      -v "$(pwd)/.credentials:/var/secrets/credentials:ro" \
      -e GOOGLE_APPLICATION_CREDENTIALS=/var/secrets/credentials/$GOOGLE_APPLICATION_CREDENTIALS_FILENAME \
      -e ENV=prod \
      -it foodprint-backend:latest
    ```

### Cloud Deployment (Backend)

Build and deploy using Google Cloud Build:
```bash
gcloud builds submit --region=europe-west1 --config cloudbuild.yaml 
```

---

## Frontend

### Docker (Frontend)

1. Build the frontend image:
    ```bash
    cd foodprint
    docker build -t foodprint-frontend:latest .
    ```
2. Run the frontend container:
    ```bash
    docker run \
      --env API_BASE="http://host.docker.internal:8000" \
      --env FOODPRINT_API_KEY=$FOODPRINT_API_KEY \
      -p 3000:3000 \
      -it foodprint-frontend:latest
    ```
   > Note: `http://host.docker.internal:8000` requires the backend to be running locally.

### Cloud Deployment (Frontend)

Build and deploy using Google Cloud Build:
```bash
cd foodprint
gcloud builds submit --region=europe-west1 --config cloudbuild.yaml 
```

---




