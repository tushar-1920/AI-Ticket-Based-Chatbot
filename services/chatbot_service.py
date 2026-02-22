from services.ticket_service import create_ticket
from services.intent_service import predict_intent
from services.message_service import save_message


def get_bot_response(message, user_id):

    # Save user message
    save_message(
        user_id=user_id,
        sender="user",
        message=message
    )

    intent, confidence = predict_intent(message)

    create_ticket_flag = False

    if intent == "login_issue":

        response = "I detected a login issue. Creating support ticket."

        create_ticket_flag = True

    elif intent == "network_issue":

        response = "Network issue detected. Creating support ticket."

        create_ticket_flag = True

    elif intent == "payment_issue":

        response = "Payment issue detected. Creating support ticket."

        create_ticket_flag = True

    elif intent == "greeting":

        response = "Hello! How can I help you today?"

    else:

        response = "Support ticket created."

        create_ticket_flag = True

    ticket_id = None

    if create_ticket_flag:

        ticket = create_ticket(
            user_id=user_id,
            issue=message,
            intent=intent
        )

        ticket_id = ticket.id

        response += f"\nTicket ID: #{ticket.id}"

    # Save bot message
    save_message(
        user_id=user_id,
        sender="bot",
        message=response,
        ticket_id=ticket_id
    )

    return response, intent