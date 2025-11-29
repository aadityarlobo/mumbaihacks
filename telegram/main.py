import os
import httpx
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pathlib import Path

from .schemas import Message
from .sender import handle_message

# Load environment variables from .env file in the root directory
dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

# Get Telegram Bot Token and Chat ID from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Initialize FastAPI app
app = FastAPI()

@app.post("/send_message")
async def send_message(message: Message):
    """
    Sends a message to Telegram.
    The message can be a simple text message, or a message with an image or a video.

    Example Usage:
    - Text only: `{"message": "Hello from FastAPI!"}`
    - Text and Image: `{"message": "Check out this awesome image!", "image_url": "https://source.unsplash.com/3tYZjGSBwbk"}`
    - Text and Video: `{"message": "Watch this cool video!", "video_url": "https://videos.pexels.com/video-files/2099386/2099386-hd_1280_720_25fps.mp4"}`
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise HTTPException(status_code=500, detail="Telegram bot token and chat ID are not configured.")

    try:
        return await handle_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Failed to send message to Telegram: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Alive"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
