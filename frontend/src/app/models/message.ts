import {User} from "./user";

export interface Message {
  id: number,
  time_sent: Date,
  content: string
}

export interface UserMessage extends Message {
  user: User
}

export interface BotMessage extends Message {
}
