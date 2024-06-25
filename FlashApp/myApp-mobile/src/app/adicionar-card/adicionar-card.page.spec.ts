import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AdicionarCardPage } from './adicionar-card.page';

describe('AdicionarCardPage', () => {
  let component: AdicionarCardPage;
  let fixture: ComponentFixture<AdicionarCardPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(AdicionarCardPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
