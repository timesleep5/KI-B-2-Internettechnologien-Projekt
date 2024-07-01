import {Component} from '@angular/core';
import {Router, RouterLink} from "@angular/router";
import {ChatService} from "../chat.service";
import {NgIf} from "@angular/common";
import {NotificationService} from "../notification.service";
import {
  MatCard,
  MatCardAvatar,
  MatCardContent,
  MatCardFooter,
  MatCardHeader,
  MatCardSubtitle,
  MatCardTitle
} from "@angular/material/card";
import {MatError, MatFormField, MatHint, MatLabel} from "@angular/material/form-field";
import {MatInput} from "@angular/material/input";
import {MatButton, MatIconButton} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {MatProgressSpinner} from "@angular/material/progress-spinner";
import {ChatStorageService} from "../chat-storage.service";
import {MatTextColumn} from "@angular/material/table";


@Component({
  selector: 'app-welcome',
  standalone: true,
  imports: [
    RouterLink,
    NgIf,
    MatCard,
    MatCardHeader,
    MatCardContent,
    MatFormField,
    MatInput,
    MatButton,
    MatLabel,
    MatCardTitle,
    MatIcon,
    MatProgressSpinner,
    MatError,
    MatCardFooter,
    MatHint,
    MatIconButton,
    MatTextColumn,
    MatCardSubtitle,
    MatCardAvatar
  ],
  templateUrl: './welcome.component.html',
  styleUrl: './welcome.component.css'
})
export class WelcomeComponent {
  loading = false;
  currentChatId?: number;

  constructor(
    private chatService: ChatService,
    private notificationService: NotificationService,
    private chatStorageService: ChatStorageService,
    private router: Router
  ) {
  }

  createChatSessionFromName(name: string): void {
    if (name.trim().length > 4) {
      this.loading = true;
      this.chatService.createChatSessionFromName(name)
        .subscribe((chatId: number) => {
            this.loading = false;
            this.currentChatId = chatId;
            this.chatStorageService.setId(chatId)
            this.chatStorageService.setUserName(name)
            this.router.navigateByUrl(`/chat`);
          }
        );
    } else {
      this.notificationService.showError("Your username has to have at least 5 letters!", "Chat creation failed");
    }
  }
}
