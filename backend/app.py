import threading
from typing import Dict, List

from fastapi import FastAPI, Query
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from Bot import Bot
from datastructures.ChatModels import User, ChatSession, Message


class Database:
    """
    Database class manages chat sessions and bots.

    Attributes:
        lock (threading.Lock): Lock to ensure thread safety.
        chat_counter (int): Counter for chat session IDs.
        chat_sessions (Dict[int, ChatSession]): Dictionary mapping chat IDs to ChatSession objects.
        bots (Dict[int, Bot]): Dictionary mapping chat IDs to Bot objects.
    """

    def __init__(self):
        """
        Initializes a new Database instance.

        Attributes:
            lock (threading.Lock): Ensures thread safety when accessing shared data.
            chat_counter (int): Counter for generating unique chat session IDs.
            chat_sessions (Dict[int, ChatSession]): Dictionary to store active chat sessions.
            bots (Dict[int, Bot]): Dictionary to store Bot instances associated with chat sessions.
        """
        self.lock = threading.Lock()
        self.chat_counter: int = 0
        self.chat_sessions: Dict[int, ChatSession] = {}
        self.bots: Dict[int, Bot] = {}

    async def create_chat_session_from_user(self, name: str) -> int:
        """
        Creates a new chat session for a user with the provided name.

        Args:
            name (str): Name of the user creating the chat session.

        Returns:
            int: Unique ID of the created chat session.
        """
        with self.lock:
            self.chat_counter += 1

            bot = Bot()
            greeting = bot.get_greeting()
            start_message = bot.get_start_message()
            self.bots[self.chat_counter] = bot

            user = User(name=name)
            chat_session = ChatSession(user=user, messages=[])
            chat_session.messages.append(greeting)
            chat_session.messages.append(start_message)
            self.chat_sessions[self.chat_counter] = chat_session

            return self.chat_counter

    async def react_to_user_message(self, chat_id: int, message: Message) -> Message:
        """
        Reacts to a user message in an existing chat session and returns a BotMessage response.

        Args:
            chat_id (int): ID of the chat session where the message is sent.
            message (Message): UserMessage object containing user's message.

        Returns:
            Message: Bot's response to the user's message.
        """
        chat_session = self.__get_chat_session_if_valid(chat_id)
        chat_session.messages.append(message)

        bot = self.__get_bot_if_valid(chat_id)
        bot_response = bot.respond_to(message)
        chat_session.messages.append(bot_response)

        return bot_response

    async def get_chat_session(self, chat_id: int):
        """
        Retrieves the chat session details for the given chat ID.

        Args:
            chat_id (int): ID of the chat session to retrieve.

        Returns:
            ChatSession: Details of the chat session with the provided ID.

        Raises:
            HTTPException: Raised if the chat session with the given ID does not exist (404 Not Found).
        """
        return self.__get_chat_session_if_valid(chat_id)

    def __get_chat_session_if_valid(self, chat_id: int) -> ChatSession:
        """
        Private method to retrieve a valid ChatSession object for the given chat ID.

        Args:
            chat_id (int): ID of the chat session to retrieve.

        Returns:
            ChatSession: Valid ChatSession object associated with the provided chat ID.

        Raises:
            HTTPException: Raised if the chat session with the given ID does not exist (404 Not Found).
        """
        if chat_id not in self.chat_sessions:
            raise HTTPException(status_code=404, detail="Chat session not found")
        return self.chat_sessions[chat_id]

    def __get_bot_if_valid(self, chat_id) -> Bot:
        """
        Private method to retrieve a valid Bot object for the given chat ID.

        Args:
            chat_id (int): ID of the chat session to retrieve the associated Bot.

        Returns:
            Bot: Valid Bot object associated with the provided chat ID.

        Raises:
            HTTPException: Raised if the bot with the given ID does not exist (404 Not Found).
        """
        if chat_id not in self.bots:
            raise HTTPException(status_code=404, detail="Bot not found")
        return self.bots[chat_id]

    async def get_logged_in_users(self) -> List[User]:
        """
        Retrieves a list of users currently logged into chat sessions.

        Returns:
            List[User]: List of User objects representing users logged into active chat sessions.
        """
        users = []
        for chat_session in self.chat_sessions.values():
            users.append(chat_session.user)

        return users


database = Database()
app = FastAPI(
    title="LeaseBot API",
    version="1.0",
    description="API for managing chat sessions, messages and user interactions.",
    docs_url="/documentation",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chats/new", response_model=int)
async def create_chat_session_from_user(name: str = Query(None, min_length=1)):
    """
    Endpoint to create a new chat session for a user.

    Args:
        name (str, query parameter): The name of the user initiating the chat session.

    Returns:
        int: The ID of the newly created chat session.

    Raises:
        HTTPException: If the name is not provided or is empty (status code 422).
    """
    return await database.create_chat_session_from_user(name)


@app.post("/chats/id/{chat_id}/message", response_model=Message)
async def react_to_user_message(chat_id: int, message: Message):
    """
    Endpoint to allow the bot to react to a user message within a specific chat session.

    Args:
        chat_id (int, path parameter): The ID of the chat session.
        message (Message): The user message object containing message details.

    Returns:
        Message: The bot's response message to the user.

    Raises:
        HTTPException: If the chat session does not exist (status code 404).
    """
    return await database.react_to_user_message(chat_id, message)


@app.get("/chats/id/{chat_id}", response_model=ChatSession)
async def get_chat_session(chat_id: int):
    """
    Endpoint to retrieve details of a chat session by its ID.

    Args:
        chat_id (int, path parameter): The ID of the chat session.

    Returns:
        ChatSession: Details of the chat session.

    Raises:
        HTTPException: If the chat session does not exist (status code 404).
    """
    return await database.get_chat_session(chat_id)


@app.get("/users", response_model=List[User])
async def get_logged_in_users():
    """
    Endpoint to retrieve a list of logged-in users.

    Returns:
        List[User]: A list of `User` objects representing logged-in users.
    """
    return await database.get_logged_in_users()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
