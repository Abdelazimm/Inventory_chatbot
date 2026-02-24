import os
import time
import json
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from openai import AsyncOpenAI, AsyncAzureOpenAI
from schema import SYSTEM_PROMPT

load_dotenv()

app = FastAPI(title="Inventory Chatbot API", description="AI chat service answering inventory questions and providing present queries.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load configuration from environment
PROVIDER = os.getenv("PROVIDER", "openai").lower()
MODEL_API_KEY = os.getenv("MODEL_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "")

# Input JSON Model
class ChatRequest(BaseModel):
    session_id: str
    message: str
    context: Optional[Dict[str, Any]] = None

# Output JSON Model
class TokenUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatResponse(BaseModel):
    natural_language_answer: str
    sql_query: str
    token_usage: TokenUsage
    latency_ms: int
    provider: str
    model: str
    status: str

# Initialize OpenAI client based on provider
if PROVIDER == "azure":
    if not AZURE_ENDPOINT or not MODEL_API_KEY or not AZURE_API_VERSION:
         print("Warning: Azure OpenAI selected but missing environment variables (AZURE_OPENAI_ENDPOINT, MODEL_API_KEY, AZURE_OPENAI_API_VERSION). API calls will fail.")
    
    # In Azure OpenAI, MODEL_NAME represents the deployment name.
    aclient = AsyncAzureOpenAI(
        api_key=MODEL_API_KEY,
        api_version=AZURE_API_VERSION,
        azure_endpoint=AZURE_ENDPOINT
    )
elif PROVIDER == "openai":
    if not MODEL_API_KEY:
         print("Warning: Standard OpenAI selected but MODEL_API_KEY is missing. API calls will fail.")
    aclient = AsyncOpenAI(
        api_key=MODEL_API_KEY
    )
elif PROVIDER == "gemini":
    if not MODEL_API_KEY:
         print("Warning: Gemini selected but MODEL_API_KEY is missing. API calls will fail.")
    aclient = AsyncOpenAI(
        api_key=MODEL_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
else:
    raise ValueError(f"Unsupported PROVIDER '{PROVIDER}'. Must be 'openai', 'azure', or 'gemini'.")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    start_time = time.perf_counter()
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": request.message}
    ]
    
    try:
        # Request a JSON object from the model
        response = await aclient.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.0 # Keep it predictable for query generation
        )
        
        # Parse the output
        content = response.choices[0].message.content
        parsed = json.loads(content)
        
        nl_answer = parsed.get("natural_language_answer", "No answer provided.")
        sql_query = parsed.get("sql_query", "")
        
        # Extract token usage
        usage = response.usage
        token_usage_obj = TokenUsage(
            prompt_tokens=usage.prompt_tokens if usage else 0,
            completion_tokens=usage.completion_tokens if usage else 0,
            total_tokens=usage.total_tokens if usage else 0
        )
        status = "ok"

    except Exception as e:
        status = "error"
        nl_answer = "An error occurred while generating the response."
        sql_query = ""
        token_usage_obj = TokenUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0)
        print(f"Error during API call: {e}")
        # Could also raise HTTPException here, but requirement says to return status="error"
        # We will return the object with status error.
        
    end_time = time.perf_counter()
    latency_ms = int((end_time - start_time) * 1000)
    
    return ChatResponse(
        natural_language_answer=nl_answer,
        sql_query=sql_query,
        token_usage=token_usage_obj,
        latency_ms=latency_ms,
        provider=PROVIDER,
        model=MODEL_NAME,
        status=status
    )

# Serve the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")
    
# To run local execution:
# uvicorn main:app --reload
