import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { IonicModule} from '@ionic/angular';
import { Router } from '@angular/router';


@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule],
})
export class HomePage {
  constructor(private router: Router) {}

  redirecionarLogin(){
    this.router.navigate(['/login']);
  }

  redirecionarCadastro(){
    this.router.navigate(['/cadastro']);
  }
}
