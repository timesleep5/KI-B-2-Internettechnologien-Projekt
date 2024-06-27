from typing import List

from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    """
    Represents a user in the system.

    Attributes:
        name (str): The name of the user.
    """
    name: str


class Message(BaseModel):
    """
    Represents a message with its timestamp.

    Attributes:
        time_sent (datetime): The timestamp when the message was sent.
        sender: (str): The origin of the message.
        content (str): The content of the message.
        is_bot_message (bool): Shows if the message was sent by the bot.
    """
    time_sent: datetime
    sender: str
    content: str
    is_bot_message: bool


class ChatSession(BaseModel):
    """
    Represents a chat session between a user and a bot.

    Attributes:
        user (User): The user participating in the chat session.
        messages (List[Message]): List of messages exchanged during the chat session.
    """
    user: User
    messages: List[Message]


class LeasingContract(BaseModel):
    """
    Pydantic BaseModel representing a leasing contract with start_date, end_date, km_limit,
    runtime_days, and runtime_months attributes.
    """
    start_date: datetime
    end_date: datetime
    km_limit: int
    runtime_days: int
    runtime_months: int
