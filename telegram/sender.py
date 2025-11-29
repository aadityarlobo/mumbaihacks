import httpx
import asyncio
from .schemas import Message

async def send_text_message(token: str, chat_id: str, message: str):
    """Sends a text message to the Telegram chat."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()

async def send_image_message(token: str, chat_id: str, message: str, image_url: str):
    """Sends a message with an image to the Telegram chat."""
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": image_url, "caption": message}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()

async def send_video_message(token: str, chat_id: str, message: str, video_url: str):
    """Sends a message with a video to the Telegram chat."""
    url = f"https://api.telegram.org/bot{token}/sendVideo"
    payload = {"chat_id": chat_id, "video": video_url, "caption": message}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()

async def handle_message(token: str, default_chat_id: str, message: Message):
    chat_ids = message.chat_id_list or ([message.chat_id] if message.chat_id else [default_chat_id])

    tasks = []
    for chat_id in chat_ids:
        if message.image_url:
            tasks.append(send_image_message(token, chat_id, message.message, message.image_url))
        elif message.video_url:
            tasks.append(send_video_message(token, chat_id, message.message, message.video_url))
        else:
            tasks.append(send_text_message(token, chat_id, message.message))
    
    await asyncio.gather(*tasks)

    count = len(chat_ids)
    return {"status": "success", "message": f"Message sent to {count} chat(s) successfully"}
