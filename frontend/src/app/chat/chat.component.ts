import {AfterViewChecked, Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {ChatService} from "../chat.service";
import {ActivatedRoute} from "@angular/router";
import {ChatSession} from "../models/chat-session";
import {BotMessage, Message, UserMessage} from "../models/message";
import {DatePipe, NgClass, NgForOf, NgStyle} from "@angular/common";
import {User} from "../models/user";
import {FormsModule} from "@angular/forms";
import {UserComponent} from "../user/user.component";
import {NotificationService} from "../notification.service";
import {MatButton} from "@angular/material/button";
import {MatFormField, MatLabel} from "@angular/material/form-field";
import {MatInput} from "@angular/material/input";

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [
    NgClass,
    NgForOf,
    DatePipe,
    FormsModule,
    NgStyle,
    UserComponent,
    MatButton,
    MatLabel,
    MatFormField,
    MatInput
  ],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.css'
})
export class ChatComponent implements OnInit, AfterViewChecked {
  private chatId: number;
  private chatSession?: ChatSession;
  protected user?: User;
  protected newMessageContent: string = '';
  @ViewChild('chatContainer') private chatContainer!: ElementRef;

  constructor(
    private route: ActivatedRoute,
    private chatService: ChatService,
    private notificationService: NotificationService,
  ) {
    this.chatId = 0;
  }

  ngOnInit(): void {
    this.getChat();
  }

  ngAfterViewChecked(): void {
    this.scrollToBottom();
  }

  private getChat(): void {
    this.chatId = Number(this.route.snapshot.paramMap.get('id'));
    this.chatService.getChat(this.chatId)
      .subscribe((chat: ChatSession) => {
        this.chatSession = chat
        this.user = chat.user;
      });
  }

  sendMessage(): void {
    if (this.newMessageContent.trim()) {
      const userMessage = this.getUserMessage()
      this.chatService.sendMessage(this.chatId, userMessage)
        .subscribe(
          (botResponse: BotMessage) => this.processBotResponse(botResponse)
        );
    } else {
      this.notificationService.showError("Messages has to have a content", "Sending message failed");
    }
  }

  private getUserMessage(): UserMessage {
    const userMessage: UserMessage = this.createUserMessage()
    this.chatSession?.messages.push(userMessage);
    this.newMessageContent = '';
    return userMessage;
  }

  private createUserMessage(): UserMessage {
    return {
      time_sent: new Date(),
      content: this.newMessageContent.trim(),
      user: this.chatSession?.user
    } as UserMessage;
  }

  private processBotResponse(response: BotMessage) {
    if (response) {
      this.chatSession?.messages.push(response);
    } else {
      this.notificationService.showError("No answer from the bot.", "Server Error");
    }
  }

  getMessages(): Message[] {
    if (this.chatSession) {
      return this.chatSession.messages;
    } else {
      return []
    }
  }

  isUserMessage(message: Message): boolean {
    return 'user' in message;
  }

  private scrollToBottom() {
    try {
      this.chatContainer.nativeElement.scrollTop = this.chatContainer.nativeElement.scrollHeight;
    } catch (err) { }
  }
}
