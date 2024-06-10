from datetime import datetime
from typing import List

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


class Message(BaseModel):
    id: int
    time_sent: datetime
    content: str


class UserMessage(Message):
    user: User


class BotMessage(Message):
    pass


class ChatSession(BaseModel):
    id: int
    user: User
    messages: List[Message]


class LeasingContract(BaseModel):
    start_date: datetime
    end_date: datetime
    km_limit: int
    runtime_days: int
    runtime_months: int
