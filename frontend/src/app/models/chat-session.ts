import {User} from "./user";
import {Message} from "./message";

export interface Bot {
}


export interface ChatSession {
  user: User,
  bot: Bot,
  message: Message[]
}
