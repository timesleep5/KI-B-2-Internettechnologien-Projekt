import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {catchError, Observable, of} from "rxjs";
import {User} from "./models/user";
import {NotificationService} from "./notification.service";
import {ConfigService} from "./config.service";

/*
 * Author: Korbinian Zormeier
 * Date: July 2, 2024
 *
 * Project: Internettechnologien Projektarbeit - JAWA Leasing Bot
 *
 * Description: This file is part of the Internettechnologien project. It
 * contains the implementation of the user service which gets all data needed for users from the backend.
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
export class UserService {
  private readonly SERVICE_ROUTE: string = '/users';
  private readonly SERVICE_URL: string;

  constructor(
    private http: HttpClient,
    private configService: ConfigService,
    private notificationService: NotificationService,
  ) {
    this.SERVICE_URL = this.configService.getApiHost() + this.SERVICE_ROUTE;
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
