import threading
from typing import List, Dict

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from Bot import Bot
from datastructures.ChatModels import *

from datastructures.ChatModels import UserMessage, BotMessage, User


class ChatSession(BaseModel):
    user: User
    messages: List[Message]


class Database:
    def __init__(self):
        self.lock = threading.Lock()
        self.chat_counter: int = 0
        self.chat_sessions: Dict[int, ChatSession] = {}
        self.bots: Dict[int, Bot] = {}

    async def create_chat_session_from_user(self, name: str) -> int:
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

    async def react_to_user_message(self, chat_id: int, message: UserMessage) -> BotMessage:
        chat_session = self.__get_chat_session_if_valid(chat_id)
        chat_session.messages.append(message)

        bot = self.__get_bot_if_valid(chat_id)
        bot_response = bot.respond_to(message)
        chat_session.messages.append(bot_response)

        return bot_response

    async def get_chat_session(self, chat_id: int):
        return self.__get_chat_session_if_valid(chat_id)

    def __get_chat_session_if_valid(self, chat_id: int) -> ChatSession:
        if chat_id not in self.chat_sessions:
            raise HTTPException(status_code=404, detail="Chat session not found")
        return self.chat_sessions[chat_id]

    def __get_bot_if_valid(self, chat_id) -> Bot:
        if chat_id not in self.bots:
            raise HTTPException(status_code=404, detail="Bot not found")
        return self.bots[chat_id]

    async def get_logged_in_users(self) -> List[User]:
        users = []
        for chat_session in self.chat_sessions.values():
            users.append(chat_session.user)

        return users


database = Database()
app = FastAPI()

origins = [
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chats/new", response_model=int)
async def create_chat_session_from_user(name: str = Query(None, min_length=1)):
    return await database.create_chat_session_from_user(name)


@app.post("/chats/id/{chat_id}/message", response_model=BotMessage)
async def react_to_user_message(chat_id: int, message: UserMessage):
    return await database.react_to_user_message(chat_id, message)


@app.get("/chats/id/{chat_id}", response_model=ChatSession)
async def get_chat_session(chat_id: int):
    return await database.get_chat_session(chat_id)


@app.get("/users", response_model=List[User])
async def get_logged_in_users():
    return await database.get_logged_in_users()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
