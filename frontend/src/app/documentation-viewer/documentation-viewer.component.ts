import {Component, OnInit} from '@angular/core';
import {DomSanitizer, SafeHtml} from "@angular/platform-browser";
import {DocumentationService} from "../documentation.service";

/*
 * Author: Korbinian Zormeier
 * Date: July 2, 2024
 *
 * Project: Internettechnologien Projektarbeit - JAWA Leasing Bot
 *
 * Description: This file is part of the Internettechnologien project. It
 * contains the implementation of the documentation-viewer component which shows the documentation stored in a
 * jupyter notebook.
 *
 * Legal Notice:
 * This source code is subject to the terms and conditions defined in the file
 * 'LICENSE.txt', which is part of this source code package. Unauthorized copying
 * of this file, via any medium, is strictly prohibited.
 *
 * (c) 2024 Technische Hochschule Deggendorf. All rights reserved.
 */

@Component({
  selector: 'app-documentation-viewer',
  standalone: true,
  imports: [],
  templateUrl: './documentation-viewer.component.html',
  styleUrl: './documentation-viewer.component.css'
})
export class DocumentationViewerComponent implements OnInit {
  notebookHtml: SafeHtml | undefined;

  constructor(
    private documentationService: DocumentationService,
    private sanitizer: DomSanitizer) {
  }

  ngOnInit(): void {
    this.documentationService.getDocumentation()
      .subscribe(data => {
        this.notebookHtml = this.sanitizer.bypassSecurityTrustHtml(data);
      });
  }
}
