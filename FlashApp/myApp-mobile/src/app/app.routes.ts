import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'home',
    loadComponent: () => import('./home/home.page').then((m) => m.HomePage),
  },
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full',
  },
  {
    path: 'login',
    loadComponent: () => import('./login/login.page').then( m => m.LoginPage)
  },
  {
    path: 'cadastro',
    loadComponent: () => import('./cadastro/cadastro.page').then( m => m.CadastroPage)
  },
  {
    path: 'decks',
    loadComponent: () => import('./decks/decks.page').then( m => m.DecksPage)
  },
  {
    path: 'adicionar-deck',
    loadComponent: () => import('./adicionar-deck/adicionar-deck.page').then( m => m.AdicionarDeckPage)
  },
  {
    path: 'revisar',
    loadComponent: () => import('./revisar/revisar.page').then( m => m.RevisarPage)
  },
];
