import { Component } from '@angular/core';
import {DocumentationViewerComponent} from "../documentation-viewer/documentation-viewer.component";
import {MatCard} from "@angular/material/card";

@Component({
  selector: 'app-documentation',
  standalone: true,
  imports: [
    DocumentationViewerComponent,
    MatCard
  ],
  templateUrl: './documentation.component.html',
  styleUrl: './documentation.component.css'
})
export class DocumentationComponent {

}
