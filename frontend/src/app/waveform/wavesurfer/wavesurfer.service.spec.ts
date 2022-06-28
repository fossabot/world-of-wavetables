import { TestBed } from '@angular/core/testing';

import { WavesurferService } from './wavesurfer.service';

describe('WavesurferService', () => {
  let service: WavesurferService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(WavesurferService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
