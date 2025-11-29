import os
import asyncio
from schemas import TelegramStatus
from state import AgentState
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from telegram.sender import handle_message
from telegram.schemas import Message
import logging

logger = logging.getLogger(__name__)

def telegram_node(state: AgentState):
    print("--- TELEGRAM BOT AGENT ---")
    
    infographic = state.get("infographic")
    if not infographic:
        return {"messages": ["Telegram: Skipped (No Content)"]}

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set. Skipping actual Telegram message send.")
        
        # Fallback to mock send if token/chat_id is not available
        msg_body = f"📢 **{infographic.title}**\n\n"
        for stat in infographic.key_stats:
            msg_body += f"• {stat}\n"
        print(f"\n[TELEGRAM MOCK SEND] To Group: {TELEGRAM_CHAT_ID or 'HealthAlerts_Mumbai'}\n{msg_body}\n[Image: {infographic.visual_description}]\n")

        result = TelegramStatus(
            sent=True,
            message_id="mock_msg_12345",
        )
        return {"telegram_status": result, "messages": ["Telegram: Alert sent to group (MOCK)."]}

    # Construct the message body
    msg_body = f"📢 **{infographic.title}**\n\n"
    for stat in infographic.key_stats:
        msg_body += f"• {stat}\n"
    
    # Create the message object for the sender
    message = Message(
        message=msg_body,
        chat_id=TELEGRAM_CHAT_ID,
        # In a real scenario, the infographic might have an image_path that can be converted to a public URL
        # For now, we are not sending an image.
        image_url=None 
    )

    try:
        # Call the sender logic directly
        send_result = asyncio.run(handle_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message))
        logger.info(f"Telegram send result: {send_result}")

        result = TelegramStatus(
            sent=True,
            # The sender function does not return a message_id, so we use a placeholder.
            message_id="sent_via_api",
        )
        message = "Telegram: Alert sent to group."

    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")
        result = TelegramStatus(
            sent=False,
            message_id=None,
        )
        message = f"Telegram: Failed to send alert. Error: {e}"

    return {"telegram_status": result, "messages": [message]}