import {Component, OnInit} from '@angular/core';
import {ImprintService} from "../imprint.service";
import {NgIf} from "@angular/common";

/*
 * Author: Korbinian Zormeier
 * Date: July 2, 2024
 *
 * Project: Internettechnologien Projektarbeit - JAWA Leasing Bot
 *
 * Description: This file is part of the Internettechnologien project. It
 * contains the implementation of the imprint component.
 *
 * Legal Notice:
 * This source code is subject to the terms and conditions defined in the file
 * 'LICENSE.txt', which is part of this source code package. Unauthorized copying
 * of this file, via any medium, is strictly prohibited.
 *
 * (c) 2024 Technische Hochschule Deggendorf. All rights reserved.
 */

@Component({
  selector: 'app-imprint',
  standalone: true,
  imports: [
    NgIf
  ],
  templateUrl: './imprint.component.html',
  styleUrl: './imprint.component.css'
})
export class ImprintComponent implements OnInit {
  imprintData: any;

  constructor(
    private imprintService: ImprintService
  ) {
  }

  ngOnInit(): void {
    this.getImprintDataFromBackend();
  }

  private getImprintDataFromBackend(): void {
    this.imprintService.getImprintData().subscribe(data => {
      this.imprintData = data;
    })
  }

  getImprintData() {
    this.getImprintDataFromBackend();
    return this.imprintData;
  }
}
