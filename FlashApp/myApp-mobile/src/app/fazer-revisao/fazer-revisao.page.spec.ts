import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FazerRevisaoPage } from './fazer-revisao.page';

describe('FazerRevisaoPage', () => {
  let component: FazerRevisaoPage;
  let fixture: ComponentFixture<FazerRevisaoPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(FazerRevisaoPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
