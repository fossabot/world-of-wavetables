import { TestBed } from '@angular/core/testing';

import { SampleDestructorService } from './sample-destructor.service';

describe('SampleDestructorService', () => {
  let service: SampleDestructorService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SampleDestructorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
