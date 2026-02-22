from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit

from config import Config
from models import db

# Models
from models.user import User
from models.ticket import Ticket
from models.message import Message

# Blueprints
from routes.auth_routes import auth
from routes.chat_routes import chat
from routes.admin_routes import admin
from routes.ticket_routes import ticket_bp
from routes.analytics_routes import analytics_bp

# Services
from services.chatbot_service import get_bot_response


# Initialize SocketIO
socketio = SocketIO()


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(chat)
    app.register_blueprint(admin)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(analytics_bp)
    

    with app.app_context():
        db.create_all()
        print("✅ Database created successfully.")

    socketio.init_app(app)

    return app


app = create_app()


# Home
@app.route("/")
def home():
    return render_template("base.html")

from flask import Blueprint, render_template, request, jsonify, session
from services.chatbot_service import get_bot_response

# ✅ FIRST create Blueprint
chat = Blueprint("chat", __name__)

@chat.route("/chat")
def chat_page():
    return render_template("chat.html")


# Chat page route
@chat.route("/chat")
def chat_page():
    return render_template("chat.html")


# Chat API route
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
# SOCKET EVENT
@socketio.on("send_message")
def handle_message(data):

    user_id = session.get("user_id")

    if not user_id:
        emit("receive_message", {
            "message": "Please login first."
        })
        return

    message = data["message"]

    response, intent = get_bot_response(
        message,
        user_id
    )

    emit("receive_message", {
        "message": response
    })


if __name__ == "__main__":
    socketio.run(
        app,
        debug=True
    )