""" Everything the PSC bot is allowed to do.

Prices here are real, from picklesocialclub.co. They live in code,
not in prompt, so the model can never invent or misquote a number.
"""

from langchain_core.tools import tool

@tool
def court_price(day_type: str, court_type: str) -> str:
    """ Get the hourly court rental price at Pickle Social Club.
    day_type: 'peak' for weekday evenings after 5pm, weekends and
               public holidays.
              'off peak' for weekdays 7am to 5pm.
    court_type: 'covered' or 'outdoor'.

    Prices exclude 8% SST. Students and seniors over 50 get RM15 off,
    off peak only.
    """
    prices = {
        ("peak", "covered"): 70,
        ("peak", "outdoor"): 55,
        ("offpeak", "covered"): 50,
        ("offpeak", "outdoor"): 35,
    }
    rate = prices.get((day_type, court_type))
    if rate is None:
        return f"No price found for day_type={day_type}, court_type={court_type}."
    return f"RM{rate} per hour, excluding 8% SST."

@tool
def lesson_price(lesson_type: str) -> str:
    """ Get the price of a coaching session or open play at Pickle Social Club.

    lesson_type must be one of:
        'junior'        - children's group lesson
        'beginner'      - adult beginner group lesson
        'intermediate'  - intermediate group lesson
        'private'       - one-to-one coaching
        'open_play'     - drop-in social play session

    All prices are per session and exclude 8% SST. Multi-session packages
    are cheaper; tell the customer to ask staff for package rates.
    """
    prices = {
        "junior": 85,
        "beginner": 95,
        "intermediate": 80,
        "private": 250,
        "open_play": 55,
    }
    rate = prices.get(lesson_type)
    if rate is None:
        return f"No price found for lesson_type={lesson_type}."
    return f"RM{rate} per session, excluding 8% SST."

@tool
def escalate_to_staff(reason: str) -> str:
    """ Hand the conversation over to a human team member.

    Use this for complaints, cancellations, refunds, membership changes,
    anything urgent, or anything you are not confident about.
    It is always better to escalate the to guess.

    reason: a short sentence explaining why, for the staff member to read.
    """
    return f"Escalated to staff. Reason: {reason}"


TOOLS = [court_price, lesson_price, escalate_to_staff]

if __name__ == "__main__":
    for t in TOOLS:
        print(t.name, "->", list(t.args.keys()))

    print(court_price.invoke({"day_type":"peak", "court_type":"covered"}))
    print(lesson_price.invoke({"lesson_type":"private"}))
    print(escalate_to_staff.invoke({"reason":"customer wants to cancel"}))