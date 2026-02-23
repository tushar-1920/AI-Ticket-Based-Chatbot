from models import db
from datetime import datetime


class Conversation(db.Model):

    __tablename__ = "conversations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    title = db.Column(
        db.String(200),
        default="New Conversation"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )