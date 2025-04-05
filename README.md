# Food CO2 Estimator

This repository contains code for estimating CO2 emissions from the ingredient lists of recipes using Large Language Models (LLMs). The project leverages various tools and libraries to fetch, parse, and analyze recipe data to provide CO2 emission estimates.

## Table of Contents

- [Food CO2 Estimator](#food-co2-estimator)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Running the Flask App](#running-the-flask-app)
  - [Heroku](#heroku)
  - [Using the CO2 Estimator](#using-the-co2-estimator)
  - [Project Structure](#project-structure)
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

## Project Structure

The project is organized as follows:

```
.
├── .github/
│   └── workflows/
├── .vscode/
│   ├── launch.json
│   └── settings.json
├── food_co2_estimator/
│   ├── chains/
│   ├── data/
│   ├── language/
│   ├── output_parsers/
│   ├── prompt_templates/
│   ├── pydantic_models/
│   ├── retrievers/
│   ├── url/
│   ├── __init__.py
│   ├── main.py
├── sandbox/
├── templates/
│   └── index.html
├── tests/
├── .coverage
├── .DS_Store
├── .flake8
├── .gitignore
├── .python-version
├── LICENSE
├── Makefile
├── poetry.lock
├── pyproject.toml
├── README.md
└── app.py
```

## Environment Variables
Set the following environment variables according to template.env file:

# Docker

1. Build image
```bash
docker build -t $APP_NAME:latest --platform linux/amd64 -f Dockerfile.backend  .
```

2. Test locally
```bash
docker run \
  --env-file .env \
  -p 8080:8080 \
  -v "$(pwd)/.credentials:/var/secrets/credentials:ro" \
  -e GOOGLE_APPLICATION_CREDENTIALS=/var/secrets/credentials/$GOOGLE_APPLICATION_CREDENTIALS_FILENAME \
  -it $APP_NAME:latest
```

3. Push to google artifact registry

```bash
docker tag $APP_NAME $REGION-docker.pkg.dev/$PROJECT_ID/foodprint/$APP_NAME:latest
docker push $REGION-docker.pkg.dev/$PROJECT_ID/foodprint/$APP_NAME:latest
```

4. Deploy app to cloud run

```bash
gcloud run deploy foodprint \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/foodprint/$APP_NAME:latest \
  --platform managed \
  --region $REGION \
  --port 8080 \
  --env-vars-file .env-files.yaml \
  --allow-unauthenticated
```

