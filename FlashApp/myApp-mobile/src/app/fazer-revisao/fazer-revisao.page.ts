import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { IonicModule, LoadingController, NavController, ToastController} from '@ionic/angular';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClientModule, HttpClient, HttpHeaders } from '@angular/common/http';
import { Storage } from '@ionic/storage-angular';

import { Usuario } from '../login/usuario.model';
import { Card } from '../revisar/card.model';

@Component({
  selector: 'app-fazer-revisao',
  templateUrl: './fazer-revisao.page.html',
  styleUrls: ['./fazer-revisao.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule, HttpClientModule],
  providers: [HttpClient, Storage]
})
export class FazerRevisaoPage implements OnInit {
  public usuario: Usuario = new Usuario();
  cardAtual: Card | undefined;
  deck_id: string | undefined | null;
  showBack: boolean = false;
  erros: number = 0;
  acertos: number = 0;
  lista_cards: Card[] = [];

  constructor(
    public http: HttpClient,
    public storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController,
    public router: Router,
    public route: ActivatedRoute,
  ) { 
    this.erros = 0;
    this.acertos = 0;
    this.showBack = false;
  }

  async ngOnInit() {
    // Verifica se existe registro de configuração para o último usuário autenticado
    await this.storage.create();
    const registro = await this.storage.get('usuario');

    this.route.paramMap.subscribe(params => {
      let id = params.get('id');
      this.deck_id = id;
    });

    if(registro) {
      if (registro.token == ""){
        //gerar novo token
        console.log(registro);
      }

      this.usuario = Object.assign(new Usuario(), registro);
      this.consultarCardsWeb();
    }
    else{
      this.controle_navegacao.navigateRoot('/home');
    }
  }

  async consultarCardsWeb(){
    const loading = await this.controle_carregamento.create({message: 'Reunindo informações...', duration: 60000});
    await loading.present();

    let http_headers: HttpHeaders = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization':`Token ${this.usuario.token}`
    });

    this.http.get(
      `http://127.0.0.1:8000/decks/api/revisar/${this.deck_id}/`,
      {
        headers: http_headers
      }
    ).subscribe({
      next: async (resposta: any) => {

        this.lista_cards = resposta; 
        this.cardAtual = this.lista_cards[0];       
        // Finaliza interface com efeito de carregamento
        loading.dismiss();
      },
      error: async (erro: any) => {
        loading.dismiss();
        const mensagem = await this.controle_toast.create({
          message: `Falha ao consultar cards: ${erro.message}`,
          cssClass: 'ion-text-center',
          duration: 2000
        });
        mensagem.present();
      }
    });
  }

  virarCard() {
    this.showBack = !this.showBack;
  }

  responder(correct: boolean) {
    if (this.cardAtual) {
      if (correct){
        this.acertos += 1;
      } else {
        this.erros += 1;
      }
  
      this.showBack = false; // Garante que o card volte para o lado da pergunta
      const indexAtual = this.lista_cards.indexOf(this.cardAtual);
      if (indexAtual !== -1) {
        this.lista_cards.splice(indexAtual, 1); // Remove o card da lista
        this.cardAtual = this.lista_cards.length > 0 ? this.lista_cards[0] : undefined; // Próximo card
      }
    }
  }

  async voltarCards(){
    let http_headers: HttpHeaders = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization':`Token ${this.usuario.token}`
    });
    const dataAtual = new Date().toISOString();
  
    await this.http.post(
      `http://127.0.0.1:8000/api/revisao/${this.deck_id}/`,
      {
        usuario: this.usuario.id,
        deck: this.deck_id,
        erros: this.erros,
        acertos: this.acertos,
        data_revisao: dataAtual
      }, 
      { 
        headers: http_headers 
      }).toPromise();
  
    // Reinicializa variáveis
    this.erros = 0;
    this.acertos = 0;
    this.showBack = false;
    this.lista_cards = [];
  
    // Navega para a página de decks
    this.router.navigate(['/decks']);
  }
}
