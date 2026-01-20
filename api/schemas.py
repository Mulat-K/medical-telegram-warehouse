from pydantic import BaseModel
from typing import Optional

class TopProduct(BaseModel):
    product: str
    mentions: int

class ChannelActivity(BaseModel):
    channel_name: str
    message_date: str
    total_posts: int

class MessageSearchResult(BaseModel):
    message_id: int
    channel_name: str
    message_text: str
    view_count: int

class VisualContentStat(BaseModel):
    channel_name: str
    image_category: str
    total_images: int
