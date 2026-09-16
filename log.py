"""Remember every enquiry, so the club learns what people actually ask."""

import sqlite3
from datetime import datetime, timezone

DB = "enquiries.db"

INTENTS = {
    "court_price" : "pricing",
    "lesson_price" : "lesson",
    "escalate_to_staff" : "escalated",
}

def setup() -> None:
    """Create the table if it doesn't exists yet.
    
    Safe to call every startup.
    """
    con = sqlite3.connect(DB)
    con.execute("""
        CREATE TABLE IF NOT EXISTS enquiries (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            ts        TEXT    NOT NULL,
            channel   TEXT    NOT NULL,
            sender    TEXT,
            message   TEXT    NOT NULL,
            intent    TEXT    NOT NULL,
            escalated INTEGER NOT NULL,
            reply     TEXT    NOT NULL
        )
    """)
    con.commit()
    con.close()

def classify(tools_used: list[str]) -> str:
    """Work out what the customer wanted from which tools the agent called."""
    for name in tools_used:
        if name in INTENTS:
            return INTENTS[name]
    return "other"

def record(channel: str, sender: str | None, message: str,
            reply: str, tools_used: list[str]) -> None:
    """Save one enquiry."""
    con = sqlite3.connect(DB)
    con.execute(
        "INSERT INTO enquires (ts, channel, sender, message, intent, escalated, reply)"
        " VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            datetime.now(timezone.utc).isoformat(timespec="seconds"),
            channel,
            sender,
            message,
            classify(tools_used),
            int("escalate_to_staff" in tools_used),
            reply,
        )
    )
    con.commit()
    con.close()

def summary() -> list[tuple[str, int]]:
    """How many of each intent, most common first."""
    con = sqlite3.connect(DB)
    rows = con.execute(
        "SELECT intent, COUNT(*) FROM enquiries GROUP BY intent"
        " ORDER BY COUNT(*) DESC"
    ).fetchall()
    con.close()
    return rows