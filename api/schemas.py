from pydantic import BaseModel
from typing import List

class TopProduct(BaseModel):
    detected_class: str
    total_mentions: int

class ChannelActivity(BaseModel):
    channel_name: str
    total_messages: int

class MessageSearch(BaseModel):
    message_id: int
    message_text: str

class VisualContentStats(BaseModel):
    image_category: str
    total_images: int
