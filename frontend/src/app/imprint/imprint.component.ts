import {Component, OnInit} from '@angular/core';
import {ImprintService} from "../imprint.service";
import {NgIf} from "@angular/common";

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
