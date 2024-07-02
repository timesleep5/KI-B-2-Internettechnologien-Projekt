import {Injectable} from '@angular/core';
import {catchError, Observable, of} from "rxjs";
import {ChatSession} from "./models/chat-session";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Message} from "./models/message";
import {NotificationService} from "./notification.service";
import {ConfigService} from "./config.service";
import {Router} from "@angular/router";

/*
 * Author: Korbinian Zormeier
 * Date: July 2, 2024
 *
 * Project: Internettechnologien Projektarbeit - JAWA Leasing Bot
 *
 * Description: This file is part of the Internettechnologien project. It
 * contains the implementation of the chat service which gets all data needed for the chat from the backend.
 *
 * Legal Notice:
 * This source code is subject to the terms and conditions defined in the file
 * 'LICENSE.txt', which is part of this source code package. Unauthorized copying
 * of this file, via any medium, is strictly prohibited.
 *
 * (c) 2024 Technische Hochschule Deggendorf. All rights reserved.
 */

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private readonly SERVICE_ROUTE: string = '/chats';
  private readonly SERVICE_URL: string;
  private httpOptions = {
    headers: new HttpHeaders({'Content-Type': 'application/json'})
  }

  constructor(
    private http: HttpClient,
    private router: Router,
    private configService: ConfigService,
    private notificationService: NotificationService,
  ) {
    this.SERVICE_URL = this.configService.getApiHost() + this.SERVICE_ROUTE;
  }

  createChatSessionFromName(name: string): Observable<number> {
    const url = `${this.SERVICE_URL}/new?name=${name}`;
    return this.http.post<number>(url, this.httpOptions)
      .pipe(
        catchError(this.handleError<number>(`createChatFromName name=${name}`))
      )
  }

  getChat(id: number): Observable<ChatSession> {
    const url = `${this.SERVICE_URL}/id/${id}`;
    return this.http.get<ChatSession>(url)
      .pipe(
        catchError(this.handleError<ChatSession>(`getChat id=${id}`))
      );
  }

  sendMessage(chatId: number, message: Message): Observable<Message> {
    const url = `${this.SERVICE_URL}/id/${chatId}/message`;
    return this.http.post<Message>(url, message, this.httpOptions)
      .pipe(
        catchError(this.handleError<Message>(`sendMessage to chat id=${chatId}`))
      )
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);
      this.notificationService.showError(`${operation} failed`, 'ChatService Error')
      this.router.navigateByUrl('/chat-not-found');
      return of(result as T);
    }
  }
}
