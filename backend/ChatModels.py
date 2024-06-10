from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    name: str


class Message(BaseModel):
    id: int
    time_sent: datetime
    content: str


class UserMessage(Message):
    user: User


class BotMessage(Message):
    pass



