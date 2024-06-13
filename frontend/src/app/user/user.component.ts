import {Component, OnDestroy, OnInit} from '@angular/core';
import {User} from "../models/user";
import {UserService} from "../user.service";
import {interval, Subscription, switchMap} from 'rxjs';
import {NgForOf} from "@angular/common";

@Component({
  selector: 'app-user',
  standalone: true,
  imports: [
    NgForOf
  ],
  templateUrl: './user.component.html',
  styleUrl: './user.component.css'
})
export class UserComponent implements OnInit, OnDestroy {
  private usersSubscription: Subscription | undefined;
  loggedInUsers: User[] = [];

  constructor(
    private userService: UserService,
  ) {
  }

  ngOnInit() {
    this.subscribeToUsers();
    this.getUsers();
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

  private getUsers() {
    this.userService.getLoggedInUsers().subscribe(
      (users: User[]) => this.loggedInUsers = users
    );
  }

  private unsubscribeToUsers(): void {
    if (this.usersSubscription) {
      this.usersSubscription.unsubscribe();
    }
  }
}
