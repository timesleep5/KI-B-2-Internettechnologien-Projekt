import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

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
