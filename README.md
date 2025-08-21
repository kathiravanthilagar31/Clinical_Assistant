# Medical Research Data Processing Workspace

This repository provides tools and scripts for processing, storing, and analyzing medical research data, including PDF parsing, database management, and a web interface.

---

## Tech Stack

- **Backend**: Python, Flask
- **AI & Machine Learning**: OpenAI, ChromaDB, Retrieval-Augmented Generation (RAG)
- **Frontend**: HTML
- **Database**: ChromaDB (Vector Store)
- **Deployment & CI/CD**: Docker, GitHub Actions, Azure Web App Service
- **Server**: Waitress (WSGI)

---

## Getting Started

Follow these steps to set up the project and run it locally.

### 1. Install Dependencies

Install all project dependencies using the `setup.py` file.

```bash
pip install -e .
```

### 2. Configure the OpenAI API Key

Create a file named `.env` in the root directory of the project and add your OpenAI API key to it like this:

```env
OPENAI_API_KEY="your_api_key_here"
```

### 3. Run the Application

The Flask application is configured to run with a production WSGI server. From your project root, run the following command:

```bash
waitress-serve --listen=0.0.0.0:8080 app:app
```

Your chatbot will be live at [http://localhost:8080](http://localhost:8080).

---

## Azure CI/CD Deployment

This project supports automated deployment to Azure Web App using Docker and GitHub Actions.

### Setting up Azure Credentials for CI/CD

1. **Create a Service Principal in Azure:**
   Open Azure Cloud Shell and run:
   ```sh
   az ad sp create-for-rbac --name "<your-app-name>" --role contributor --scopes /subscriptions/<your-subscription-id> --sdk-auth
   ```
   Replace `<your-app-name>` and `<your-subscription-id>` with your values.

2. **Copy the JSON output.**  
   It will look like:
   ```json
   {
     "clientId": "...",
     "clientSecret": "...",
     "subscriptionId": "...",
     "tenantId": "..."
   }
   ```

3. **Add the secret to GitHub:**
   - Go to your repository’s **Settings > Secrets and variables > Actions**.
   - Click **New repository secret**.
   - Name it `AZURE_CREDENTIALS`.
   - Paste the JSON output as the value.

---

## Features

- **Retrieval-Augmented Generation (RAG):** Uses a medical dataset to provide context-aware answers.
- **Conversation Memory:** Maintains chat history for a natural conversation flow.
- **Flask API:** Exposes a RESTful API for interaction with the frontend.
- **Docker Support:** Containerizes the application for a consistent environment.
- **CI/CD Integration:** Automates the build and deployment process via GitHub Actions.
