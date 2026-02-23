from flask import Flask, render_template, session, redirect
from flask_socketio import SocketIO, emit

from config import Config
from models import db

# Models
from models.user import User
from models.ticket import Ticket
from models.message import Message
from models.conversation import Conversation

# Blueprints
from routes.auth_routes import auth
from routes.chat_routes import chat
from routes.admin_routes import admin
from routes.ticket_routes import ticket_bp
from routes.analytics_routes import analytics_bp

# Services
from services.chatbot_service import get_bot_response
from services.message_service import save_message


# Initialize SocketIO properly
socketio = SocketIO(
    cors_allowed_origins="*",
    manage_session=False
)


# Create Flask app
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

    # Create tables
    with app.app_context():

        db.create_all()

        print("✅ Database created successfully.")

    # Initialize socket
    socketio.init_app(app)

    return app


# Create app instance
app = create_app()


# Home route
@app.route("/")
def home():

    if session.get("user_id"):
        return redirect("/chat")

    return redirect("/login")


# SocketIO event handler
@socketio.on("send_message")
def handle_message(data):

    try:

        print("Received:", data)

        user_id = session.get("user_id")

        if not user_id:

            emit("receive_message", {
                "message": "Please login first."
            })

            return


        message = data.get("message")

        conversation_id = data.get("conversation_id")


        if not message or not conversation_id:

            emit("receive_message", {
                "message": "Invalid conversation."
            })

            return


        # Save user message
        save_message(
            conversation_id,
            "user",
            message
        )


        # Generate bot response
        response, intent = get_bot_response(
            message,
            user_id
        )


        # Save bot response
        save_message(
            conversation_id,
            "bot",
            response
        )


        print("Bot response:", response)


        # Send response
        emit("receive_message", {
            "message": response
        })


    except Exception as e:

        print("SOCKET ERROR:", str(e))

        emit("receive_message", {
            "message": "Server error occurred."
        })


# Run server
if __name__ == "__main__":

    socketio.run(
        app,
        debug=True
    )