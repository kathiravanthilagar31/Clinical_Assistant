# Medical Chatbot

This repository provides tools and scripts for processing, storing, and analyzing medical research data, including PDF parsing, database management, and a web interface.

---

## Tech Stack

- **Backend:** Python, Flask
- **AI & Machine Learning:** OpenAI, ChromaDB, Retrieval-Augmented Generation (RAG)
- **Frontend:** HTML
- **Database:** ChromaDB (Vector Store)
- **Deployment & CI/CD:** Docker, GitHub Actions, Azure Web App Service
- **Server:** Waitress (WSGI)

---

## Getting Started

Follow these steps to set up the project and run it locally.

### 1. Install Dependencies

Install all project dependencies using the `setup.py` file.

```bash
pip install -e .
```

### 2. Configure the OpenAI API Key

Create a file named `.env` in the root directory of the project and add your OpenAI API key:

```env
OPENAI_API_KEY="your_api_key_here"
```

### 3. Run the Application Locally

The Flask application is configured to run with a production WSGI server. From your project root, run:

```bash
waitress-serve --listen=0.0.0.0:8080 app:app
```

Your chatbot will be live at [http://localhost:8080](http://localhost:8080).

---

## CI/CD Pipeline: Deploying to Azure

This project supports automated deployment to Azure Web App using Docker and GitHub Actions.

### Prerequisites

- An [Azure Container Registry (ACR)](https://portal.azure.com/#create/Microsoft.ContainerRegistry) and [Azure Web App for Containers](https://portal.azure.com/#create/Microsoft.WebSite).
- Azure credentials for GitHub Actions authentication.

### 1. Create Azure Resources

If you haven't already:
- **Create an Azure Container Registry (ACR):**  
  In Azure Portal, go to *Container Registries* > *Create*.
- **Create an Azure Web App for Containers:**  
  In Azure Portal, go to *App Services* > *Create*, select *Docker Container* as the publish option.

### 2. Get Azure Container Registry Credentials

- Go to your Azure Container Registry in the Azure Portal.
- Under **Access keys**, copy your **username** and **password**.

### 3. Add Secrets to GitHub

In your GitHub repository, go to **Settings > Secrets and variables > Actions** and add these secrets:

- `CLINICALAPP_REGISTRY_USERNAME` — your ACR username
- `CLINICALAPP_REGISTRY_PASSWORD` — your ACR password
- `CLINICALAPP_AZURE_CREDENTIALS` — your Azure login credentials (Service Principal JSON or username/password, as required)
- `OPENAI_API_KEY` — your OpenAI API key

### 4. Configure Workflow Environment Variables

In your `.github/workflows/main.yml`, set these environment variables:

```yaml
env:
  RESOURCE_GROUP: '<your-resource-group>'
  CONTAINER_APP_NAME: '<your-webapp-name>'
  CONTAINER_REGISTRY: '<your-acr-name>.azurecr.io'
  IMAGE_NAME: '<your-image-name>'
```

Replace the placeholders with your actual Azure resource names.

### 5. How the Pipeline Works

On every push to the `main` branch:
- The workflow logs into Azure using your credentials.
- It logs in to your Azure Container Registry using the username and password.
- It builds your Docker image and pushes it to your Azure Container Registry.
- It deploys the image to your Azure Web App for Containers.

---

## Features

- **Retrieval-Augmented Generation (RAG):** Uses a medical dataset to provide context-aware answers.
- **Conversation Memory:** Maintains chat history for a natural conversation flow.
- **Flask API:** Exposes a RESTful API for interaction with the frontend.
- **Docker Support:** Containerizes the application for a consistent environment.
- **CI/CD Integration:** Automates the build and deployment process via GitHub Actions.

---

## Troubleshooting

If deployment fails, check:
- Your Azure resource names and registry URL in the workflow file.
- That your GitHub secrets are correctly set and named.
- The Actions log for error messages.
