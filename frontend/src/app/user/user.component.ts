import {Component, OnDestroy, OnInit} from '@angular/core';
import {User} from "../models/user";
import {UserService} from "../user.service";
import {interval, Subscription, switchMap} from 'rxjs';
import {NgForOf, NgIf} from "@angular/common";
import {ChatStorageService} from "../chat-storage.service";

@Component({
  selector: 'app-user',
  standalone: true,
  imports: [
    NgForOf,
    NgIf
  ],
  templateUrl: './user.component.html',
  styleUrl: './user.component.css'
})
export class UserComponent implements OnInit, OnDestroy {
  private usersSubscription: Subscription | undefined;
  private loggedInUsers: User[] = [];

  constructor(
    private userService: UserService,
    private chatStorageService: ChatStorageService,
  ) {
  }

  ngOnInit() {
    this.subscribeToUsers();
    this.getUsersFromBackend();
  }

  ngOnDestroy(): void {
    this.unsubscribeToUsers();
  }

  private subscribeToUsers(): void {
    this.usersSubscription = interval(5_000).pipe(
      switchMap(() => this.userService.getLoggedInUsers())
    ).subscribe((users: User[]) => {
      this.loggedInUsers = users;
    });
  }

  private getUsersFromBackend() {
    this.userService.getLoggedInUsers().subscribe(
      (users: User[]) => {
        this.loggedInUsers = users
      }
    );
  }

  getUsers(): User[] {
    this.removeUserFromUsers()
    return this.loggedInUsers;
  }

  private removeUserFromUsers() {
    const userName = this.chatStorageService.getUserName();
    if (userName) {
      for (let i = 0; i < this.loggedInUsers.length; i++) {
        if (this.loggedInUsers[i].name === userName) {
          this.loggedInUsers.splice(i, 1);
          break;
        }
      }
    }
  }

  private unsubscribeToUsers(): void {
    if (this.usersSubscription) {
      this.usersSubscription.unsubscribe();
    }
  }

  getUserName(): string {
    return this.chatStorageService.getUserName()
  }
}
