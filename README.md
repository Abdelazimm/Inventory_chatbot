# Inventory AI Chatbot

A smart, natural language chatbot designed to answer complex inventory and business questions. 
This project uses an AI language model (Gemini, OpenAI, or Azure) combined with a provided SQL Server database schema to not only answer user queries in plain English but also provide the exact T-SQL query that would generate the result in a real database.

## Features
- **Natural Language Interface**: Ask questions like "How many assets do I have?" or "List all my customers."
- **Present Query Functionality**: For every answer, the AI provides the exact `SELECT` SQL query required to fetch that data from an SQL Server database.
- **Provider Agnostic**: Easily switch between standard OpenAI, Azure OpenAI, and Google Gemini architectures by changing the `.env` configuration.
- **Modern Web UI**: A sleek, responsive chat interface built with HTML/CSS/JS.
- **FastAPI Backend**: High-performance asynchronous API endpoints returning JSON tracking token usage and latency.

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- An API Key from Google Gemini (or OpenAI)

### 2. Installation
Clone the repository:
```bash
git clone https://github.com/Abdelazimm/Inventory_chatbot.git
cd Inventory_chatbot
```

Create a virtual environment and install dependencies:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configuration
Copy the `.env.example` file and rename it to `.env`:
```bash
cp .env.example .env
```
Open the massive `.env` file and replace `your_key_here` with your actual API key.

### 4. Running the Server
Start the local FastAPI server using Uvicorn:
```bash
uvicorn main:app --reload
```

### 5. Usage
Open your web browser and navigate to:
`http://127.0.0.1:8000/`

You can also test the API endpoint directly using tools like `curl` or PowerShell:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/chat" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"session_id": "test", "message": "List all my purchase orders", "context": {}}'
```

## Architecture
- `main.py`: The core FastAPI application handling routing, CORS, and AI inference calls.
- `schema.py`: Contains the `SYSTEM_PROMPT`, the exact SQL Server DDL definitions, and sample data instances injected into the LLM context to ensure high-accuracy query generation.
- `static/index.html`: The frontend user interface for the chatbot.
