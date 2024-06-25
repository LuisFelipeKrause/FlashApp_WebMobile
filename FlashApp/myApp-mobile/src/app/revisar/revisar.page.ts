import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { IonicModule, LoadingController, NavController, ToastController } from '@ionic/angular';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClientModule, HttpClient, HttpHeaders } from '@angular/common/http';
import { Storage } from '@ionic/storage-angular';

import { Usuario } from '../login/usuario.model';
import { Card } from './card.model';

@Component({
  selector: 'app-revisar',
  templateUrl: './revisar.page.html',
  styleUrls: ['./revisar.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule, HttpClientModule],
  providers: [HttpClient, Storage]
})
export class RevisarPage implements OnInit {
  public usuario: Usuario = new Usuario();
  public lista_cards: Card[] = [];
  public deck_id: string | undefined | null;

  constructor(
    public http: HttpClient,
    public storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController,
    public router: Router,
    public route: ActivatedRoute
  ) { }

  async ngOnInit() {
    // Verifica se existe registro de configuração para o último usuário autenticado
    await this.storage.create();
    const registro = await this.storage.get('usuario');

    this.route.paramMap.subscribe(params => {
      let id = params.get('id');
      this.deck_id = id;
      console.log('ID recebido:', id);
    });

    if(registro) {
      this.usuario = Object.assign(new Usuario(), registro);
      this.consultarCardsWeb();
    }
    else{
      this.controle_navegacao.navigateRoot('/home');
    }
  }

  async consultarCardsWeb(){
    // Inicializa interface com efeito de carregamento
    const loading = await this.controle_carregamento.create({message: 'Reunindo informações...', duration: 60000});
    await loading.present();

    let http_headers: HttpHeaders = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization':`Token ${this.usuario.token}`
    });

    // Requisita lista de veículos para a API do sistema web
    this.http.get(
      `http://127.0.0.1:8000/decks/api/revisar/${this.deck_id}/`,
      {
        headers: http_headers
      }
    ).subscribe({
      next: async (resposta: any) => {

        this.lista_cards = resposta;
        console.log(this.lista_cards);
        
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
}
