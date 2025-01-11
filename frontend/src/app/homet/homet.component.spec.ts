import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HometComponent } from './homet.component';

describe('HometComponent', () => {
  let component: HometComponent;
  let fixture: ComponentFixture<HometComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HometComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(HometComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
