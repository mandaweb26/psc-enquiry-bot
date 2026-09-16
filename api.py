"""The front door: one HTTP endpoint, so many channel can reach the bot."""

from fastapi import FastAPI
from pydantic import BaseModel

from agent import ask
from channels import whatsapp

# create the web application
app = FastAPI(title="PSC Enquiry Bot")

# attach the whatsapp channel to the service - our bot.
app.include_router(whatsapp.router)

# describes what a valid incoming request looks like
class ChatRequest(BaseModel):
    # Required. A request without it is rejected automatically.
    message: str
    # optional.
    # thread_id is used for memory later.
    thread_id: str | None = None

class ChatResponse(BaseModel):
    reply: str

# Cloud Run pings this to check the service is alive.
@app.get("/health")
def health():
    """Is the service alive? Used by Cloud Run later."""
    return {"status":"ok"}

# FastAPI reads the incoming JSON and hands you a checked ChatRequest object.
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    """One customer message in, one reply out"""
    # call the bot, wrap the answer, send it back.
    return ChatResponse(reply=ask(req.message))


