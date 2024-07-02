import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {ChatService} from "../chat.service";
import {Router} from "@angular/router";
import {ChatSession} from "../models/chat-session";
import {Message} from "../models/message";
import {DatePipe, NgClass, NgForOf, NgStyle} from "@angular/common";
import {User} from "../models/user";
import {FormsModule} from "@angular/forms";
import {UserComponent} from "../user/user.component";
import {NotificationService} from "../notification.service";
import {MatButton} from "@angular/material/button";
import {MatFormField, MatLabel} from "@angular/material/form-field";
import {MatInput} from "@angular/material/input";
import {ChatStorageService} from "../chat-storage.service";

/*
 * Author: Korbinian Zormeier
 * Date: July 2, 2024
 *
 * Project: Internettechnologien Projektarbeit - JAWA Leasing Bot
 *
 * Description: This file is part of the Internettechnologien project. It
 * contains the implementation of the chat component which shows the entire chat interface.
 *
 * Legal Notice:
 * This source code is subject to the terms and conditions defined in the file
 * 'LICENSE.txt', which is part of this source code package. Unauthorized copying
 * of this file, via any medium, is strictly prohibited.
 *
 * (c) 2024 Technische Hochschule Deggendorf. All rights reserved.
 */

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  standalone: true,
  imports: [
    NgStyle,
    DatePipe,
    MatFormField,
    MatLabel,
    FormsModule,
    MatInput,
    MatButton,
    UserComponent,
    NgForOf,
    NgClass
  ],
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  private chatId: number;
  private chatSession?: ChatSession;
  protected user?: User;
  protected newMessageContent: string = '';
  @ViewChild('chatContainer') private chatContainerRef: ElementRef | undefined;

  constructor(
    private chatService: ChatService,
    private notificationService: NotificationService,
    private chatStorageService: ChatStorageService,
    private router: Router
  ) {
    this.chatId = 0;
  }

  ngOnInit(): void {
    this.getChat();
  }

  private getChat(): void {
    this.chatId = this.chatStorageService.getId();
    if (this.chatId !== 0) {
      this.chatService.getChat(this.chatId)
        .subscribe(
          (chat: ChatSession) => {
            this.chatSession = chat;
            this.user = chat.user;
          }
        );
    } else {
      this.router.navigateByUrl('/chat-not-found');
    }
  }

  sendMessage(): void {
    if (this.newMessageContent.trim()) {
      const userMessage = this.getUserMessage();
      this.chatService.sendMessage(this.chatId, userMessage)
        .subscribe(
          (botResponse: Message) => this.processBotResponse(botResponse)
        );
    } else {
      this.notificationService.showError("Messages has to have a content", "Sending message failed");
    }
  }

  private getUserMessage(): Message {
    const userMessage: Message = this.createUserMessage();
    this.chatSession?.messages.push(userMessage);
    this.newMessageContent = '';
    setTimeout(() => {
      this.scrollToBottom();
    });
    return userMessage;
  }

  private createUserMessage(): Message {
    return {
      time_sent: new Date(),
      content: this.newMessageContent.trim(),
      sender: this.chatSession?.user.name,
      is_bot_message: false
    } as Message;
  }

  private processBotResponse(response: Message) {
    if (response) {
      this.chatSession?.messages.push(response);
      setTimeout(() => {
        this.scrollToBottom();
      });
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

  isBotMessage(message: Message): boolean {
    return message.is_bot_message;
  }

  private scrollToBottom(): void {
    try {
      if (this.chatContainerRef) {
        this.chatContainerRef.nativeElement.scrollTop = this.chatContainerRef.nativeElement.scrollHeight;
      }
    } catch (err) {
    }
  }
}
