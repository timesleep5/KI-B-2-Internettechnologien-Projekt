import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

/*
 * Author: Korbinian Zormeier
 * Date: July 2, 2024
 *
 * Project: Internettechnologien Projektarbeit - JAWA Leasing Bot
 *
 * Description: This file is part of the Internettechnologien project. It
 * contains the implementation of the documentation service
 * which gets the documentation jupyter html export from the backend.
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
export class DocumentationService {

  constructor(
    private http: HttpClient
  ) { }

  getDocumentation() {
    return this.http.get('assets/documentation.html', {responseType: 'text'})
  }
}
