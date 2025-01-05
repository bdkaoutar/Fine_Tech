import { TestBed } from '@angular/core/testing';

import { AuthSeviceService } from '../auth-sevice.service';

describe('AuthSeviceService', () => {
  let service: AuthSeviceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AuthSeviceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
