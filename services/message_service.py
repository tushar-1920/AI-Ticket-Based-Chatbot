from models import db
from models.message import Message


def save_message(user_id, sender, message, ticket_id=None):

    msg = Message(

        user_id=user_id,

        sender=sender,

        message=message,

        ticket_id=ticket_id

    )

    db.session.add(msg)

    db.session.commit()