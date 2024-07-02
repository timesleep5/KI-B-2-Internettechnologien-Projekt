import {Injectable} from '@angular/core';

/*
 * Author: Korbinian Zormeier
 * Date: July 2, 2024
 *
 * Project: Internettechnologien Projektarbeit - JAWA Leasing Bot
 *
 * Description: This file is part of the Internettechnologien project. It
 * contains the implementation of the chat-storage service which is responsible
 * for storing frontend session data, e.g. the chat id or the username, for each tab separately.
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
