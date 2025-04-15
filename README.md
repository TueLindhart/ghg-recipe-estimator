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

1. Build image
```bash
docker build -t foodprint-backend:latest --platform linux/amd64 -f Dockerfile.backend  .
```

2. Test locally
```bash
docker run \
  --env-file .env \
  -p 8080:8080 \
  -v "$(pwd)/.credentials:/var/secrets/credentials:ro" \
  -e GOOGLE_APPLICATION_CREDENTIALS=/var/secrets/credentials/$GOOGLE_APPLICATION_CREDENTIALS_FILENAME \
  -it foodprint-backend:latest
```

3. Push to google artifact registry

```bash
docker tag foodprint-backend:latest $LOCATION-docker.pkg.dev/$PROJECT_ID/foodprint/foodprint-backend:latest
docker push $LOCATION-docker.pkg.dev/$PROJECT_ID/foodprint/foodprint-backend:latest
```

4. Deploy app to cloud run

```bash
gcloud run deploy foodprint \
  --image $LOCATION-docker.pkg.dev/$PROJECT_ID/foodprint/foodprint-backend:latest \
  --platform managed \
  --region $LOCATION \
  --port 8080 \
  --env-vars-file .env-files.yaml \
  --allow-unauthenticated
```

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:748386344174-compute@developer.gserviceaccount.com" \
  --role="roles/run.admin"
