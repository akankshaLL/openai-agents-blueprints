#!/usr/bin/env python3
import asyncio
import uvicorn
from fastapi import FastAPI
from datetime import datetime
from src.my_agents.specialized.customer_support import CustomerSupportAgent
from agents import Runner

app = FastAPI(title="AI Agent API", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/ready")
async def readiness_check():
    return {"status": "ready", "timestamp": datetime.utcnow()}

@app.post("/chat")
async def chat_endpoint(message: dict):
    agent = CustomerSupportAgent()
    result = await Runner.run(agent.agent, message.get("query", ""))
    return {
        "response": result.final_output.response,
        "sentiment": result.final_output.sentiment,
        "follow_up_needed": result.final_output.follow_up_needed
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
