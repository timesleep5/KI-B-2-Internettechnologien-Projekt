import {Component} from '@angular/core';
import {RouterLink} from "@angular/router";
import {ChatService} from "../chat.service";
import {NgIf} from "@angular/common";
import {Router} from "@angular/router";

@Component({
  selector: 'app-welcome',
  standalone: true,
  imports: [
    RouterLink,
    NgIf
  ],
  templateUrl: './welcome.component.html',
  styleUrl: './welcome.component.css'
})
export class WelcomeComponent {

  currentChatId?: number;

  constructor(
    private chatService: ChatService,
    private router: Router
  ) {
  }

  createChatSessionFromName(name: string): void {
    this.chatService.createChatSessionFromName(name)
      .subscribe((chatId: number) => {
          this.currentChatId = chatId;
          this.router.navigateByUrl(`/chat/${this.currentChatId}`);
        }
      )
  }
}
