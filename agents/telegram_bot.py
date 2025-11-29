import os
from schemas import TelegramStatus
from state import AgentState

def telegram_node(state: AgentState):
    print("--- TELEGRAM BOT AGENT ---")
    
    infographic = state.get("infographic")
    if not infographic:
        return {"messages": ["Telegram: Skipped (No Content)"]}
    
    # Simulate sending to Telegram
    # In production: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", ...)
    
    msg_body = f"📢 **{infographic.title}**\n\n"
    for stat in infographic.key_stats:
        msg_body += f"• {stat}\n"
    
    print(f"\n[TELEGRAM MOCK SEND] To Group: HealthAlerts_Mumbai\n{msg_body}\n[Image: {infographic.visual_description}]\n")
    
    result = TelegramStatus(
        sent=True,
        message_id="msg_12345",
    )
    
    return {"telegram_status": result, "messages": ["Telegram: Alert sent to group."]}
