import { Component } from '@angular/core';
import {
  FormGroup,
  FormControl,
  Validators,
  FormsModule,
  ReactiveFormsModule,
} from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { MaterialModule } from '../../../material.module';
import { MatButtonModule } from '@angular/material/button';
import { AuthSeviceService } from 'src/app/services/auth-sevice.service';

@Component({
  selector: 'app-side-login',
  standalone: true,
  imports: [
    RouterModule,
    MaterialModule,
    FormsModule,
    ReactiveFormsModule,
    MatButtonModule,
  ],
  templateUrl: './side-login.component.html',
})
export class AppSideLoginComponent {
  constructor(private router: Router, private authService : AuthSeviceService ) {}

  form = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.minLength(6)]),
    password: new FormControl('', [Validators.required]),
  });

  get f() {
    return this.form.controls;
  }

  submit() {
    if (this.form.valid) {
      //console.log('Login Successful:', this.form.value);
      this.authService.login(this.form.value).subscribe({
        next: (response) => {
          console.log('Response from server', response);
          this.router.navigate(['/']);
        },
        error: (error) => {
          console.error('Error in registering user', error);
        }
      })
      //this.router.navigate(['/']); // Redirection vers la page d'accueil après connexion
    } else {
      console.log('Form is invalid');
    }
  }
}
