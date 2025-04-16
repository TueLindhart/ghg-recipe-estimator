# Food CO2 Estimator

This repository contains code for estimating CO2 emissions from the ingredient lists of recipes using Large Language Models (LLMs). The project leverages various tools and libraries to fetch, parse, and analyze recipe data to provide CO2 emission estimates.

## Table of Contents

- [Food CO2 Estimator](#food-co2-estimator)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Running the Flask App](#running-the-flask-app)
  - [Heroku](#heroku)
  - [Using the CO2 Estimator](#using-the-co2-estimator)
  - [Environment Variables](#environment-variables)
- [Docker](#docker)
  - [Build backend](#build-backend)
  - [Build frontend](#build-frontend)
  

## Installation

To install the necessary packages, use the following command:

```bash
poetry install
```

This will install all the dependencies listed in the `pyproject.toml` file.

## Running the Flask App

To run the Flask app, follow these steps:

1. Ensure you have all dependencies installed using `poetry install`.
2. Run the Flask app using the following command:

```bash
poetry run flask run
```

The app will be available at `http://127.0.0.1:8000`.

## Heroku
The app is automatically deployed in heroku every time code is merged into main. To make sure the deployment does not fail, the pyproject.toml and poetry.lock file must be updated with all required packages.

## Using the CO2 Estimator

The CO2 estimator can be used to calculate the CO2 emissions of recipes. Here's how you can use it:

1. **Calculate CO2 Emission**:
   - Navigate to the home page of the Flask app.
   - Enter the recipe URL or the ingredients manually in the provided textarea.
   - Click on the "Calculate CO2e Emission" button.
   - The result will be displayed after processing.

2. **Monitor App Output**:
   - You can monitor the app output using Heroku logs (if deployed on Heroku):

```bash
heroku logs --source app
```


## Environment Variables
Set the following environment variables according to template.env file:

# Docker

## Build backend

1. Build image locally
```bash
docker build -t foodprint-backend:latest  .
```

2. Test image locally
```bash
docker run \
  --env-file .env \
  -p 8080:8080 \
  -v "$(pwd)/.credentials:/var/secrets/credentials:ro" \
  -e GOOGLE_APPLICATION_CREDENTIALS=/var/secrets/credentials/$GOOGLE_APPLICATION_CREDENTIALS_FILENAME \
  -it foodprint-backend:latest
```

3. Build image in cloud and deploy
```bash
gcloud builds submit --region=europe-west1 --config cloudbuild.yaml 
```

## Build frontend

1. Build image locally
```bash
cd foodprint
docker build -t foodprint-frontend:latest  .
```

2. Test image locally
```bash
docker run \
  --env API_BASE="http://host.docker.internal:8000"  \
  --env FOODPRINT_API_KEY=$FOODPRINT_API_KEY \
  -p 3000:3000 \
  -it foodprint-frontend:latest
```

Note, that http://host.docker.internal:8000 requires backend code is running locally 

1. Build image in cloud and deploy
```bash
cd foodprint
gcloud builds submit --region=europe-west1 --config cloudbuild.yaml 
```




