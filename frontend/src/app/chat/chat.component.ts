import {Component, OnInit} from '@angular/core';
import {ChatService} from "../chat.service";
import {ActivatedRoute} from "@angular/router";
import {ChatSession} from "../models/chat-session";

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.css'
})
export class ChatComponent implements OnInit {
  constructor(
    private route: ActivatedRoute,
    private chatService: ChatService,
  ) {
  }

  ngOnInit(): void {
    this.getChat();
  }

  private getChat(): void {
    const chat_id: number = Number(this.route.snapshot.paramMap.get('id'));
    this.chatService.getChat(chat_id)
      .subscribe((chat: ChatSession) => {
        console.log(chat.user.name)
      })
  }
}
