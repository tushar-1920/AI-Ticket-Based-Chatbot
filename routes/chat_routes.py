from flask import Blueprint, render_template, request, jsonify, session
from services.chatbot_service import get_bot_response

chat = Blueprint("chat", __name__)

@chat.route("/chat")
def chat_page():
    return render_template("chat.html")


@chat.route("/api/chat", methods=["POST"])
def chat_api():

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "response": "Please login first."
        })

    data = request.get_json()

    message = data.get("message")

    response, intent = get_bot_response(message, user_id)

    return jsonify({
        "response": response,
        "intent": intent
    })