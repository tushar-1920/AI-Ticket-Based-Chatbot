from services.ticket_service import create_ticket


def safe_predict_intent(message):
    """
    Safe intent prediction without ML dependency crash
    """

    message = message.lower()

    if "login" in message:
        return "login_issue", 0.95

    elif "network" in message:
        return "network_issue", 0.95

    elif "payment" in message:
        return "payment_issue", 0.95

    elif "hi" in message or "hello" in message:
        return "greeting", 0.99

    else:
        return "general", 0.80


def get_bot_response(message, user_id):

    try:

        # Safe intent prediction
        intent, confidence = safe_predict_intent(message)

        create_ticket_flag = False

        # Response logic
        if intent == "login_issue":

            response = "🔐 Login issue detected. Creating support ticket."
            create_ticket_flag = True

        elif intent == "network_issue":

            response = "🌐 Network issue detected. Creating support ticket."
            create_ticket_flag = True

        elif intent == "payment_issue":

            response = "💳 Payment issue detected. Creating support ticket."
            create_ticket_flag = True

        elif intent == "greeting":

            response = "👋 Hello! How can I help you today?"

        else:

            response = "🛠️ Issue detected. Creating support ticket."
            create_ticket_flag = True


        # Ticket creation safely
        if create_ticket_flag:

            try:

                ticket = create_ticket(
                    user_id=user_id,
                    issue=message,
                    intent=intent
                )

                response += f"\n\n🎫 Ticket ID: #{ticket.id}"

            except Exception as ticket_error:

                print("Ticket error:", ticket_error)

                response += "\n\n⚠️ Ticket system temporarily unavailable."


        return response, intent


    except Exception as e:

        print("Chatbot error:", e)

        return "⚠️ AI system error. Please try again.", "error"