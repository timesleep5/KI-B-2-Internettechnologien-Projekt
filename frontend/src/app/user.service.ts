import {Injectable} from '@angular/core';
import {BASE_URL} from "./app.config";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {catchError, Observable, of} from "rxjs";
import {User} from "./models/user";
import {NotificationService} from "./notification.service";

@Injectable({
  providedIn: 'root'
})
export class UserService {
  readonly SERVICE_URL: string = `${BASE_URL}/users`;
  private httpOptions = {
    headers: new HttpHeaders({'Content-Type': 'application/json'})
  }

  constructor(
    private http: HttpClient,
    private notificationService: NotificationService,
  ) {
  }

  getLoggedInUsers(): Observable<User[]> {
    const url = this.SERVICE_URL;
    return this.http.get<User[]>(url)
      .pipe(
        catchError(this.handleError<User[]>('getLoggedInUsers', []))
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
