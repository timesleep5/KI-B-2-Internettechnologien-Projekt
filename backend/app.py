from typing import List, Dict

from fastapi import FastAPI, HTTPException

from Bot import Bot
from ChatModels import *


class ChatSession(BaseModel):
    user: User
    bot: Bot
    messages: List[Message]


class Database:
    def __init__(self):
        self.chat_counter: int = 0
        self.chat_sessions: Dict[int, ChatSession] = {}

    def create_chat_session_from_user(self, name: str) -> int:
        self.chat_counter += 1
        user = User(name=name)
        bot = Bot()
        chat_session = ChatSession(user=user, bot=bot, messages=[])
        self.chat_sessions[self.chat_counter] = chat_session

        return self.chat_counter

    def react_to_user_mesage(self, chat_id: int, message: UserMessage) -> BotMessage:
        chat_session = self.__get_chat_session_if_valid(chat_id)
        chat_session.messages.append(message)

        bot = chat_session.bot
        bot_response = bot.respond_to(message)
        chat_session.messages.append(bot_response)

        return bot_response

    def get_chat_session(self, chat_id: int):
        return self.__get_chat_session_if_valid(chat_id)

    def __get_chat_session_if_valid(self, chat_id: int) -> ChatSession:
        if chat_id not in self.chat_sessions:
            raise HTTPException(status_code=404, detail="Chat session not found")
        return self.chat_sessions[chat_id]


database = Database()
app = FastAPI()


@app.post("/chats/new/name/{name}", response_model=int)
def create_chat_session_from_user(name: str):
    return database.create_chat_session_from_user(name)


@app.post("/chats/id/{chat_id}/message", response_model=BotMessage)
def react_to_user_mesage(chat_id: int, message: UserMessage):
    return database.react_to_user_mesage(chat_id, message)


@app.get("/chats/id/{chat_id}", response_model=ChatSession)
def get_chat_session(chat_id: int):
    return database.get_chat_session(chat_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
