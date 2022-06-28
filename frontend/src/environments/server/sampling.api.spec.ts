import { TestBed } from '@angular/core/testing';

import { SamplingApi } from './sampling.api';

describe('SamplingAPIService', () => {
  let service: SamplingApi;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SamplingApi);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
