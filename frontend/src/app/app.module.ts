import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HometComponent } from './homet/homet.component'; // Exemple de route vers HometComponent
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';

const routes: Routes = [
  { path: '', component: HometComponent }, // Route par défaut
  { path: '/home', component: HometComponent }, 
  {path: '/login' , component : LoginComponent},
  { path: '/register', component :LoginComponent },
  
  
  // Exemple d'une autre route
];



@NgModule({
  
  
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}


