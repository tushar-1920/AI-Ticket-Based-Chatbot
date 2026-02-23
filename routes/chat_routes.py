from flask import Blueprint, render_template, session, redirect, request, jsonify
from models.conversation import Conversation
from models import db

from services.conversation_service import (
    create_conversation,
    get_user_conversations,
    delete_conversation
)

from services.message_service import (
    get_conversation_messages
)

chat = Blueprint("chat", __name__)

@chat.route("/chat")
def chat_page():

    if not session.get("user_id"):
        return redirect("/login")

    user_id = session["user_id"]

    conversations = get_user_conversations(user_id)

    # AUTO CREATE conversation if none exists
    if not conversations:

        new_conv = create_conversation(user_id)

        conversations = [new_conv]

    return render_template(
        "chat.html",
        conversations=conversations
    )

@chat.route("/conversation/new")
def new_conversation():

    # SAFE login check
    if not session.get("user_id"):
        return redirect("/login")

    user_id = session.get("user_id")

    # Create conversation
    conversation = Conversation(
        user_id=user_id,
        title="New Conversation"
    )

    db.session.add(conversation)
    db.session.commit()

    return redirect("/chat")


@chat.route("/conversation/delete/<int:id>")
def delete_conv(id):

    delete_conversation(id)

    return redirect("/chat")


@chat.route("/conversation/messages/<int:id>")
def get_messages(id):

    messages = get_conversation_messages(id)

    return jsonify([

        {
            "sender": m.sender,
            "message": m.message,
            "time": m.created_at.strftime("%H:%M")
        }

        for m in messages

    ])