import { Component } from '@angular/core';
import {DocumentationViewerComponent} from "../documentation-viewer/documentation-viewer.component";
import {MatCard} from "@angular/material/card";

/*
 * Author: Korbinian Zormeier
 * Date: July 2, 2024
 *
 * Project: Internettechnologien Projektarbeit - JAWA Leasing Bot
 *
 * Description: This file is part of the Internettechnologien project. It
 * contains the implementation of the documentation component which shows the documentation.
 *
 * Legal Notice:
 * This source code is subject to the terms and conditions defined in the file
 * 'LICENSE.txt', which is part of this source code package. Unauthorized copying
 * of this file, via any medium, is strictly prohibited.
 *
 * (c) 2024 Technische Hochschule Deggendorf. All rights reserved.
 */

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
