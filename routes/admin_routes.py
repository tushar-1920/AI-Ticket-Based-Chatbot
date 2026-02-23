from flask import Blueprint, render_template, session, redirect
from models.ticket import Ticket
from models.user import User
from models import db

admin = Blueprint("admin", __name__)


# Hardcoded admin email
ADMIN_EMAIL = "pinki123@gmail.com"


@admin.route("/admin/dashboard")
def admin_dashboard():

    # Check login
    if not session.get("user_id"):
        return redirect("/login")

    # Get current user
    user = User.query.get(session["user_id"])

    # Allow access ONLY to pinki123@gmail.com
    if user.email != ADMIN_EMAIL:
        return "Access denied. Admin only."

    # Get all tickets
    tickets = Ticket.query.order_by(
        Ticket.created_at.desc()
    ).all()

    return render_template(
        "admin_dashboard.html",
        tickets=tickets
    )

@admin.route("/admin/update-status/<int:ticket_id>", methods=["POST"])
def update_ticket_status(ticket_id):

    from flask import request, redirect

    if not session.get("user_id"):
        return redirect("/login")

    user = User.query.get(session["user_id"])

    if user.email != "pinki123@gmail.com":
        return "Access denied"

    ticket = Ticket.query.get(ticket_id)

    new_status = request.form.get("status")

    ticket.status = new_status

    db.session.commit()

    return redirect("/admin/dashboard")