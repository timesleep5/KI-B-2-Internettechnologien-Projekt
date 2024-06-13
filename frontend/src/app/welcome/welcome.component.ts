import {Component} from '@angular/core';
import {Router, RouterLink} from "@angular/router";
import {ChatService} from "../chat.service";
import {NgIf} from "@angular/common";
import {NotificationService} from "../notification.service";

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
    private notificationService: NotificationService,
    private router: Router
  ) {
  }

  createChatSessionFromName(name: string): void {
    if (name.trim().length > 4) {
      this.chatService.createChatSessionFromName(name)
        .subscribe((chatId: number) => {
            this.currentChatId = chatId;
            this.router.navigateByUrl(`/chat/${this.currentChatId}`);
          }
        );
    } else {
      this.notificationService.showError("Your username has to have at least 5 letters!", "Chat creation failed");
    }
  }
}
