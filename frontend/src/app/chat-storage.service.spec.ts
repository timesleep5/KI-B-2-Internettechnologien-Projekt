import { TestBed } from '@angular/core/testing';

import { ChatStorageService } from './chat-storage.service';

describe('ChatIdStorageService', () => {
  let service: ChatStorageService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ChatStorageService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
