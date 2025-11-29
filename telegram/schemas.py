from pydantic import BaseModel
from typing import Optional

class Message(BaseModel):
    message: str
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    chat_id: Optional[str] = None
    chat_id_list: Optional[list[str]] = None
