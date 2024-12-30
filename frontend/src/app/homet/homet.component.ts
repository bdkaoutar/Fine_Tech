import { Component } from '@angular/core';

@Component({
  selector: 'app-homet',
  standalone: true,
  templateUrl: './homet.component.html',
  styleUrls: ['./homet.component.css']

})
export class HometComponent {
  onLogin() {
    alert('Login button clicked!');
    // Logique de connexion ici
  }
}
