import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavController } from '@ionic/angular/standalone';
import { IonicModule, LoadingController, ToastController } from '@ionic/angular';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';
import { Storage } from '@ionic/storage-angular';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Usuario } from '../login/usuario.model';

@Component({
  selector: 'app-adicionar-card',
  templateUrl: './adicionar-card.page.html',
  styleUrls: ['./adicionar-card.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, HttpClientModule, FormsModule],
  providers: [HttpClient, Storage]
})
export class AdicionarCardPage implements OnInit {
  public usuario: Usuario = new Usuario();
  public token_usuario: string | undefined; // Declare token_user como uma string
  public deck_id: string | undefined | null;
  public instancia: {frente: string, verso: string} = {
    frente: '',
    verso: ''
  };

  constructor(
    public http: HttpClient,
    private storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController,
    public router: Router,
    public route: ActivatedRoute,
  ) { }

  async ngOnInit() {
    await this.storage.create();

    this.route.paramMap.subscribe(params => {
      let id = params.get('id');
      this.deck_id = id;
    });

    let registro = await this.storage.get('usuario');
    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);
      this.token_usuario = registro.token;
    } else {
      console.error('Usuário não encontrado no armazenamento');
    }
  }

  async adicionarCard() {
    const loading = await this.controle_carregamento.create({ message: 'Adicionando...' });
    await loading.present();

    // Headers com o token de autenticação
    let http_headers: HttpHeaders = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Token ${this.token_usuario}`
    });

    // Realiza a requisição POST para adicionar o deck
    this.http.post(`http://127.0.0.1:8000/decks/api/novocard/${this.deck_id}/`, 
      {
        deck: this.deck_id,
        frente: this.instancia.frente,
        verso: this.instancia.verso || null,
      }, 
      { 
        headers: http_headers 
      })
      .subscribe({
        next: async (resposta: any) => {
          loading.dismiss();
          const mensagem = await this.controle_toast.create({
            message: 'Card adicionado com sucesso!',
            duration: 2000
          });
          mensagem.present();
          this.controle_navegacao.navigateRoot(`/revisar/${this.deck_id}`).then(() => {
            window.location.reload();
          });
        },
        error: async (erro: any) => {
          loading.dismiss();
          console.error('Erro ao adicionar card:', erro); // Exibir o erro completo no console
          const mensagem = await this.controle_toast.create({
            message: `Falha ao adicionar card: ${erro.error}`,
            duration: 2000
          });
          mensagem.present();
        }
      });
  }

  async voltarTela(){
    this.router.navigateByUrl(`/revisar/${this.deck_id}`);
  }
}
