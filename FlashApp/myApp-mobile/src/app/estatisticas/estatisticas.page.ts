import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { IonicModule, LoadingController, NavController, ToastController} from '@ionic/angular';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClientModule, HttpClient, HttpHeaders } from '@angular/common/http';
import { Storage } from '@ionic/storage-angular';

import { Usuario } from '../login/usuario.model';
import { Deck } from '../decks/deck.model';

@Component({
  selector: 'app-estatisticas',
  templateUrl: './estatisticas.page.html',
  styleUrls: ['./estatisticas.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule, HttpClientModule],
  providers: [HttpClient, Storage]
})
export class EstatisticasPage {
  public usuario: Usuario = new Usuario();
  deck_id: string | undefined | null;
  decks: Deck[] = [];
  taxa_acertos: number | undefined;
  taxa_erros: number | undefined;
  ultima_revisao: string | undefined;

  constructor(
    public http: HttpClient,
    public storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController,
    public router: Router,
    public route: ActivatedRoute,
  ) { }

  async ionViewWillEnter() {
     // Verifica se existe registro de configuração para o último usuário autenticado
     await this.storage.create();
     const registro = await this.storage.get('usuario');
 
     this.route.paramMap.subscribe(params => {
       let id = params.get('id');
       this.deck_id = id;
     });
 
     if(registro) {
       this.usuario = Object.assign(new Usuario(), registro);
       this.consultarDeckEstatistica();
     }
     else{
       this.controle_navegacao.navigateRoot('/home');
     }
  }

  async consultarDeckEstatistica(){
    // Inicializa interface com efeito de carregamento
    const loading = await this.controle_carregamento.create({message: 'Reunindo informações...', duration: 60000});
    await loading.present();

    let http_headers: HttpHeaders = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization':`Token ${this.usuario.token}`
    });

    // Requisita lista de veículos para a API do sistema web
    this.http.get(
      `http://127.0.0.1:8000/decks/api/estatisticas/${this.deck_id}/`,
      {
        headers: http_headers
      }
    ).subscribe({
      next: async (resposta: any) => {
        console.log(resposta[0].acertos);
        this.decks = resposta;
        let total_cards = resposta[0].acertos + resposta[0].erros;
        this.taxa_acertos = (resposta[0].acertos / total_cards) * 100;
        this.taxa_erros = (resposta[0].erros / total_cards) * 100;

        // Converta a string para um objeto Date
        const ultimaRevisaoDate = new Date(resposta[0].ultima_revisao);
        const meses = [
          "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
          "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ];
        const dia = ultimaRevisaoDate.getDate();
        const mes = meses[ultimaRevisaoDate.getMonth()];
        const ano = ultimaRevisaoDate.getFullYear();
        let hora = ultimaRevisaoDate.getHours();
        let minutos = ultimaRevisaoDate.getMinutes();
        const minutosFormatados = minutos < 10 ? '0' + minutos : minutos;

        // Construa a string formatada
        this.ultima_revisao = `${dia} de ${mes} de ${ano} às ${hora}:${minutosFormatados}`;
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

  async voltarDecks(){
    this.router.navigate(['/decks']);
  }
}
