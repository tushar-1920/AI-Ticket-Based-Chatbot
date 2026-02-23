from models.conversation import Conversation
from models import db


def create_conversation(user_id):

    conv = Conversation(
        user_id=user_id,
        title="New Conversation"
    )

    db.session.add(conv)
    db.session.commit()

    return conv


def get_user_conversations(user_id):

    return Conversation.query.filter_by(
        user_id=user_id
    ).order_by(
        Conversation.created_at.desc()
    ).all()


def delete_conversation(conv_id):

    conv = Conversation.query.get(conv_id)

    db.session.delete(conv)

    db.session.commit()