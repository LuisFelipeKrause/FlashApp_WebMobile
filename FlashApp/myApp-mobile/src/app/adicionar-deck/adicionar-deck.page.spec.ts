import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AdicionarDeckPage } from './adicionar-deck.page';

describe('AdicionarDeckPage', () => {
  let component: AdicionarDeckPage;
  let fixture: ComponentFixture<AdicionarDeckPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(AdicionarDeckPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
