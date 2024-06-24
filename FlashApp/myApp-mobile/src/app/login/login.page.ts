import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { IonicModule, LoadingController, NavController, ToastController } from '@ionic/angular';
import { Router } from '@angular/router';
import { HttpClientModule, HttpClient, HttpHeaders } from '@angular/common/http';
import { Storage } from '@ionic/storage-angular';

import { Usuario } from './usuario.model';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule, HttpClientModule],
  providers: [HttpClient, Storage]
})
export class LoginPage implements OnInit {
  public instancia: {username: string, password: string} = {
    username: '',
    password: ''
  };

  constructor(
    private router: Router,
    private controle_carregamento: LoadingController,
    private controle_navegacao: NavController,
    private controle_toast: ToastController,
    private storage: Storage,
    private http: HttpClient
  ) {}

  async ngOnInit() {
    await this.storage.create(); // Criação de banco de dados local
  }

  async autenticarUsuario(){
    // Inicializa interface com efeito de carregamento
    const loading = await this.controle_carregamento.create({message: 'Autenticando...', duration: 15000});
    await loading.present();

    // Define informações do cabeçalho da requisição
    let http_headers: HttpHeaders = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    // Autentica usuário junto a API do sistema web
    this.http.post(
      'http://127.0.0.1:8000/autenticacao-api/',
      this.instancia,
      {
        headers: http_headers
      }
    ).subscribe({
      next: async (resposta: any) => {
        // Armazena localmente as credenciais do usuário
        let usuario = Object.assign(new Usuario(), resposta);
        await this.storage.set('usuario', usuario);

        // Finaliza autenticação e redireciona para interface inicial
        loading.dismiss();
        this.controle_navegacao.navigateRoot('/home');
      },
      error: async (erro: any) => {
        loading.dismiss();
        const mensagem = await this.controle_toast.create({
          message: `Falha ao autenticar usuário: ${erro.message}`,
          cssClass: 'ion-text-center',
          duration: 2000
        });
        mensagem.present();
      }
    })
  }

  cancelarLogin() {
    this.router.navigate(['/home']);
  }
}
