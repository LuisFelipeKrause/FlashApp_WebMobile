import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavController } from '@ionic/angular/standalone';
import { IonicModule, LoadingController, ToastController } from '@ionic/angular';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';
import { Storage } from '@ionic/storage-angular';
import { Router } from '@angular/router';

import { Usuario } from '../login/usuario.model';
import { Deck } from './deck.model';

@Component({
  selector: 'app-decks',
  templateUrl: './decks.page.html',
  styleUrls: ['./decks.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, HttpClientModule],
  providers: [HttpClient, Storage]
})
export class DecksPage {
  alertButtons = ['Action'];
  public usuario: Usuario = new Usuario();
  public lista_decks: Deck[] = [];

  constructor(
    public http: HttpClient,
    public storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController,
    public router: Router
  ) { }

  async ionViewWillEnter() {
     // Verifica se existe registro de configuração para o último usuário autenticado
     await this.storage.create();
     const registro = await this.storage.get('usuario');
 
     if(registro) {
       this.usuario = Object.assign(new Usuario(), registro);
       this.consultarDecksWeb();
     }
     else{
       this.controle_navegacao.navigateRoot('/home');
     }
  }

  async revisarDeck(id: number){
    this.router.navigateByUrl(`/revisar/${id}`);
  }

  async consultarDecksWeb(){
    // Inicializa interface com efeito de carregamento
    const loading = await this.controle_carregamento.create({message: 'Reunindo informações...', duration: 60000});
    await loading.present();

    let http_headers: HttpHeaders = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization':`Token ${this.usuario.token}`
    });

    // Requisita lista de veículos para a API do sistema web
    this.http.get(
      'http://127.0.0.1:8000/decks/api/',
      {
        headers: http_headers
      }
    ).subscribe({
      next: async (resposta: any) => {

        this.lista_decks = resposta;
        
        // Finaliza interface com efeito de carregamento
        loading.dismiss();
      },
      error: async (erro: any) => {
        loading.dismiss();
        const mensagem = await this.controle_toast.create({
          message: `Falha ao consultar veículos: ${erro.message}`,
          cssClass: 'ion-text-center',
          duration: 2000
        });
        mensagem.present();
      }
    });
  }

  async adicionarDeck(){
    this.router.navigate(['/adicionar-deck']);
  }

  async excluirDeck(id: number) {
    // Inicializa interface com efeito de carregamento
    const loading = await this.controle_carregamento.create({message: 'Excluindo...', duration: 30000});
    await loading.present();

    let http_headers: HttpHeaders = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization':`Token ${this.usuario.token}`
    });

    // Deleta instância de veículo via API do sistema web
    this.http.delete(
      `http://127.0.0.1:8000/decks/api/${id}/`,
      {
        headers: http_headers
      }
    ).subscribe({
      next: async (resposta: any) => {

        this.consultarDecksWeb();

        // Finaliza interface com efeito de carregamento
        loading.dismiss();
      },
      error: async (erro: any) => {
        loading.dismiss();
        const mensagem = await this.controle_toast.create({
          message: `Falha ao excluir o deck: ${erro.message}`,
          cssClass: 'ion-text-center',
          duration: 2000
        });
        mensagem.present();
      }
    });
  }

  async realizarLogout() {
    const loading = await this.controle_carregamento.create({ message: 'Saindo...', duration: 15000 });
    await loading.present();
  
    let http_headers: HttpHeaders = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization':`Token ${this.usuario.token}`  // Substitua 'this.token' pela variável que armazena o token do usuário
    });
  
    this.http.get(
      'http://127.0.0.1:8000/api/logout/',  // URL do endpoint de logout
      {
        headers: http_headers
      }
    ).subscribe({
      next: async (resposta: any) => {
        console.log('Logout realizado:', resposta);
  
        // Limpar o token localmente ou realizar outras ações de limpeza necessárias
  
        await loading.dismiss();
        this.controle_navegacao.navigateRoot('/home');
      },
      error: async (erro: any) => {
        console.error('Erro ao realizar logout:', erro);
        await loading.dismiss();
        const mensagem = await this.controle_toast.create({
          message: 'Erro ao sair: ' + erro.message,
          cssClass: 'ion-text-center',
          duration: 2000
        });
        mensagem.present();
      }
    });
  }

  async verEstatisticas(id: number){
    this.router.navigateByUrl(`/estatisticas/${id}`);
  }
}
