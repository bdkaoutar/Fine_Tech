import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HometComponent } from './homet/homet.component';

export const routes: Routes = [
  { path: '', component: HometComponent },
  { path: 'home', component: HometComponent }, 
  { path: 'login', component: LoginComponent },
  { path: 'register', component: LoginComponent }
];