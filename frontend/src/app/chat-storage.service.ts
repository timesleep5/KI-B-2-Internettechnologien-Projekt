import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ChatStorageService {

  private chatIdKey = 'chatId';
  private userNameKey = 'userName';

  constructor() {
  }

  private isSessionStorageAvailable(): boolean {
    try {
      const testKey = '__test__';
      sessionStorage.setItem(testKey, testKey);
      sessionStorage.removeItem(testKey);
      return true;
    } catch (e) {
      return false;
    }
  }

  setId(id: number): void {
    if (this.isSessionStorageAvailable()) {
      sessionStorage.setItem(this.chatIdKey, String(id));
    }
  }

  getId(): number {
    let id: string | null = '';
    if (this.isSessionStorageAvailable()) {
      id = sessionStorage.getItem(this.chatIdKey);
    }
    return id !== null ? Number(id) : 0;
  }

  setUserName(userName: string): void {
    if (this.isSessionStorageAvailable()) {
      sessionStorage.setItem(this.userNameKey, userName)
    }
  }

  getUserName(): string {
    let userName: string | null = '';
    if (this.isSessionStorageAvailable()) {
      userName = sessionStorage.getItem(this.userNameKey);
    }
    return userName ? userName : '';
  }
}
