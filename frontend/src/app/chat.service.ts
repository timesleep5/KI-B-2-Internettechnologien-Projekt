import {Injectable} from '@angular/core';
import {catchError, Observable, of} from "rxjs";
import {ChatSession} from "./models/chat-session";
import {HttpClient, HttpHeaders} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  readonly BASE_URL: string = "http://127.0.0.1:8080/chats";

  httpOptions = {
    headers: new HttpHeaders({'Content-Type': 'application/json'})
  }

  constructor(
    private http: HttpClient,
  ) {
  }

  createChatFromName(name: string): Observable<number> {
    const url = `${this.BASE_URL}/new/name/${name}`;
    return this.http.get<number>(url)
      .pipe(
        catchError(this.handleError<number>(`createChatFromName name=${name}`))
      )
  }

  getChat(id: number): Observable<ChatSession> {
    const url = `${this.BASE_URL}/id/${id}`;
    return this.http.get<ChatSession>(url)
      .pipe(
        catchError(this.handleError<ChatSession>(`getChat id=${id}`))
      );
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);

      return of(result as T);
    }
  }
}
