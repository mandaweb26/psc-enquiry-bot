"""Translator between WhatsApp's format and ours. No thinking happens here."""

from fastapi import APIRouter

from agent import ask_detailed
import log

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

# this function is the translator - extracting "sender" and sender's text
def extract(payload: dict) -> tuple[str | None, str | None]:
    """Dig the sender and the text out of WhatsApp's nested payload.

    Returns (None, None) for anything that is not a plain text message -
    delivery receipts, reactions and status updates all arrive here too.
    """
    try:
        msg = payload["entry"][0]["changes"][0]["value"]["messages"][0]
        return msg["from"], msg["text"]["body"]
    except (KeyError, IndexError, TypeError):
        return None, None


@router.post("/webhook")
def webhook(payload: dict) -> dict:
    """WhatsApp posts here every time someone messages the club"""
    sender, text = extract(payload)

    if text is None:
        return {"status": "ignored"}

    #reply = ask(text)
    out = ask_detailed(text)
    reply = out["reply"]
    log.record("whatsapp", sender, text, reply, out['tools_used'])

    # A real integration would POST this back to WhatsApp's send API.
    print(f"-> to {sender}: {reply}")
    return {"status":"ok", "to":"sender", "reply":"reply"}