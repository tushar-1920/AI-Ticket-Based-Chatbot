from models import db
from models.ticket import Ticket


def create_ticket(user_id, issue, intent):

    # Auto priority based on intent
    if intent in ["network_issue", "payment_issue"]:
        priority = "High"
    elif intent in ["login_issue"]:
        priority = "Medium"
    else:
        priority = "Low"

    ticket = Ticket(
        user_id=user_id,
        issue=issue,
        intent=intent,
        priority=priority,
        status="Open"
    )

    db.session.add(ticket)
    db.session.commit()

    return ticket