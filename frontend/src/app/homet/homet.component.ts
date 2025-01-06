import { Component } from '@angular/core';
import { LoginComponent } from '../login/login.component';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-homet',
  standalone: true,
  imports:[LoginComponent,RouterModule],
  templateUrl: './homet.component.html',
  styleUrls: ['./homet.component.css']

})
export class HometComponent {
  onLogin() {
    alert('Login button clicked!');
    // Logique de connexion ici
  }
}
