export interface Message {
  time_sent: Date,
  sender: string,
  content: string
  is_bot_message: boolean
}
