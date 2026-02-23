from models.message import Message
from models import db


def save_message(conversation_id, sender, message):

    msg = Message(
        conversation_id=int(conversation_id),
        sender=sender,
        message=message
    )

    db.session.add(msg)

    db.session.commit()


def get_conversation_messages(conversation_id):

    return Message.query.filter_by(
        conversation_id=conversation_id
    ).order_by(
        Message.created_at
    ).all()