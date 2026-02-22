from flask import Blueprint, render_template, session, redirect
from models.ticket import Ticket

# Blueprint name
ticket_bp = Blueprint("ticket_bp", __name__)


@ticket_bp.route("/my-tickets")
def my_tickets():

    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")

    tickets = Ticket.query.filter_by(
        user_id=user_id
    ).order_by(
        Ticket.created_at.desc()
    ).all()

    return render_template(
        "my_tickets.html",
        tickets=tickets
    )