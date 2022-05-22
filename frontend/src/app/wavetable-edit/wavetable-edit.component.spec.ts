import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WavetableEditComponent } from './wavetable-edit.component';

describe('WavetableEditComponent', () => {
  let component: WavetableEditComponent;
  let fixture: ComponentFixture<WavetableEditComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WavetableEditComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WavetableEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
