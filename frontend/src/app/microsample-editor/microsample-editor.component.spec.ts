import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MicrosampleEditorComponent } from './microsample-editor.component';

describe('MicrosampleEditorComponent', () => {
  let component: MicrosampleEditorComponent;
  let fixture: ComponentFixture<MicrosampleEditorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MicrosampleEditorComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MicrosampleEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
