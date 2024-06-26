import { Component } from '@angular/core';
import { IonApp, IonRouterOutlet } from '@ionic/angular/standalone';
import { IonIcon } from '@ionic/angular/standalone';
import { play, add, arrowBackCircle, trash, refreshOutline, checkmarkCircle, closeCircle } from 'ionicons/icons';
import { addIcons } from 'ionicons';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  standalone: true,
  imports: [IonApp, IonRouterOutlet, IonIcon],
})
export class AppComponent {
  constructor() {
    addIcons({play, add, arrowBackCircle, trash, refreshOutline, checkmarkCircle, closeCircle});
  }
}
