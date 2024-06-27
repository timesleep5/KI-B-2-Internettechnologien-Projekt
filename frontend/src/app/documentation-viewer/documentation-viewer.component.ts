import {Component, OnInit} from '@angular/core';
import {DomSanitizer, SafeHtml} from "@angular/platform-browser";
import {DocumentationService} from "../documentation.service";

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
