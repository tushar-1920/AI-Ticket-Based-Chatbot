from models import db
from datetime import datetime


class Ticket(db.Model):

    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    issue = db.Column(db.Text, nullable=False)

    intent = db.Column(db.String(100))

    status = db.Column(db.String(50), default="Open")

    priority = db.Column(db.String(50), default="Medium")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f"<Ticket {self.id}>"