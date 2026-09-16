"""The front door: one HTTP endpoint, so many channel can reach the bot."""

from fastapi import FastAPI
from pydantic import BaseModel

from agent import ask
from channels import whatsapp
from agent import ask_detailed
import log

# create the web application
app = FastAPI(title="PSC Enquiry Bot")

log.setup()

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
    out = ask_detailed(req.message)
    log.record("web", req.thread_id, req.message, out["reply"], out["tools_used"])
    return ChatResponse(reply=out["reply"])

#def chat(req: ChatRequest) -> ChatResponse:
#    """One customer message in, one reply out"""
#    # call the bot, wrap the answer, send it back.
#    return ChatResponse(reply=ask(req.message))

@app.get("/stats")
def stats() -> dict:
    """What are customers actually asking us?"""
    return {"by_intent": dict(log.summary())}







