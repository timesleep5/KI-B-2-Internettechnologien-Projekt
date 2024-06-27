import {Injectable} from '@angular/core';
import {catchError, Observable, of} from "rxjs";
import {ChatSession} from "./models/chat-session";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Message} from "./models/message";
import {BASE_URL} from "./app.config";
import {NotificationService} from "./notification.service";

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  readonly SERVICE_URL: string = `${BASE_URL}/chats`;
  private httpOptions = {
    headers: new HttpHeaders({'Content-Type': 'application/json'})
  }

  constructor(
    private http: HttpClient,
    private notificationService: NotificationService,
  ) {
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
      return of(result as T);
    }
  }
}
