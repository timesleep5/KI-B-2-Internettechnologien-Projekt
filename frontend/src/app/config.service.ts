import {Injectable} from '@angular/core';
import {API_BASE_URL, API_PORT} from "./app.config";

/*
 * Author: Korbinian Zormeier
 * Date: July 2, 2024
 *
 * Project: Internettechnologien Projektarbeit - JAWA Leasing Bot
 *
 * Description: This file is part of the Internettechnologien project. It
 * contains the implementation of the config service which is responsible for providing the right host addresses.
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
export class ConfigService {
  private readonly host: string;

  constructor() {
    this.host = window.location.hostname === 'localhost'
      ? API_BASE_URL
      : `http://${window.location.hostname}:${API_PORT}`;
  }

  getApiHost(): string {
    return this.host;
  }
}
