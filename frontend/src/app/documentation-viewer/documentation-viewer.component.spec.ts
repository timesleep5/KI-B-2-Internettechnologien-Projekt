import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DocumentationViewerComponent } from './documentation-viewer.component';

describe('DocumentationViewerComponent', () => {
  let component: DocumentationViewerComponent;
  let fixture: ComponentFixture<DocumentationViewerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DocumentationViewerComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(DocumentationViewerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
