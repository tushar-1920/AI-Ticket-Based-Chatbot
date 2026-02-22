from flask import Blueprint, render_template, request, redirect, url_for
from models.ticket import Ticket
from models import db

admin = Blueprint("admin", __name__)


@admin.route("/admin/dashboard")
def admin_dashboard():

    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()

    return render_template(
        "admin_dashboard.html",
        tickets=tickets
    )


@admin.route("/admin/update-status/<int:ticket_id>", methods=["POST"])
def update_ticket_status(ticket_id):

    new_status = request.form.get("status")

    ticket = Ticket.query.get(ticket_id)

    if ticket:
        ticket.status = new_status
        db.session.commit()

    return redirect(url_for("admin.admin_dashboard"))