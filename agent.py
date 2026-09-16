""" The brain: a model, plus tools, plus instructions """

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

from prompts import SYSTEM_PROMPT
from tools import TOOLS

load_dotenv()

model = init_chat_model(
    "claude-haiku-4-5-20251001",
    model_provider="anthropic",
)

agent = create_agent(
    model=model,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT,
)

def ask(message: str) -> str:
    """Send one customer message to the bot, get the reply text back."""
    result = agent.invoke({"messages":[{"role":"user", "content":message}]})
    return str(result["messages"][-1].text)

def ask_verbose(message: str) -> str:
    """Same as ask(), but shows every step the agent took"""
    # run the agent.
    # result["messages"] is the whole conversation, not just the answer.
    result = agent.invoke({"messages":[{"role":"user", "content":message}]})
    # walkthrough each message in that conversation, one at a time.
    # from customer asking to AI's respond.
    for m in result["messages"]:
        # each message is an object of some class: HumanMessage, AIMessage, ToolMessage
        # type(m).__name__ gives that class name as text, chop off the word "Message"
        # so the prinout stays short: Human, AI, Tool
        kind = type(m).__name__.replace("Message", "")
        # does this message contain tool calls?
        if getattr(m, "tool_calls", None):
            for tc in m.tool_calls:
                # this is the evidence.
                # tc['name'] is which tool, tc['args'] is the arguments it chose.
                print(f" [{kind}] calls {tc['name']}({tc['args']})")
        # if this message has actual words in it, print those.
        elif m.content:
            # print the text, cut to the first 80 characters.
            print(f" [{kind}] {str(m.text)[:80]}")
    return str(result["messages"][-1].text)

# for the memory block
def ask_detailed(message: str) -> dict:
    """Like ask(), but also reports which tools the agent used."""
    result = agent.invoke({"messages":[{"role":"user","content":message}]})
    tools_used = [
        tc["name"]
        for m in result["messages"]
        for tc in (getattr(m, "tool_calls", None) or [])
    ]
    return {"reply": str(result["messages"][-1].text), "tools_used": tools_used}

    

if __name__ == "__main__":
    tests = [
        "hi how much for covered court on saturday evening ah",
        "do u have beginner lesson for my daughter, she 9 yo",
        "i want to cancel my membership how?",
    ]
    for t in tests:
        print(f"\nCustomer: {t}")
        print(f"Bot: {ask_verbose(t)}")