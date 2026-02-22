from flask import Blueprint, render_template, session, redirect
from models.ticket import Ticket
from models import db
from sqlalchemy import func

analytics_bp = Blueprint(
    "analytics_bp",
    __name__,
    template_folder="../templates"
)


@analytics_bp.route("/analytics")
def analytics_dashboard():

    # Require login
    if not session.get("user_id"):
        return redirect("/login")

    # Get stats safely
    total = Ticket.query.count()

    open_tickets = Ticket.query.filter(
        Ticket.status == "Open"
    ).count()

    resolved = Ticket.query.filter(
        Ticket.status == "Resolved"
    ).count()

    priority_rows = db.session.query(
        Ticket.priority,
        func.count(Ticket.id)
    ).group_by(Ticket.priority).all()

    intent_rows = db.session.query(
        Ticket.intent,
        func.count(Ticket.id)
    ).group_by(Ticket.intent).all()

    # Convert safely
    priority_labels = []
    priority_values = []

    for row in priority_rows:
        priority_labels.append(row[0])
        priority_values.append(row[1])

    intent_labels = []
    intent_values = []

    for row in intent_rows:
        intent_labels.append(row[0])
        intent_values.append(row[1])

    print("DEBUG priority:", priority_labels, priority_values)
    print("DEBUG intent:", intent_labels, intent_values)

    return render_template(
        "analytics.html",
        total=total,
        open_tickets=open_tickets,
        resolved=resolved,
        priority_labels=priority_labels,
        priority_values=priority_values,
        intent_labels=intent_labels,
        intent_values=intent_values
    )