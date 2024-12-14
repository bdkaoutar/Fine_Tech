import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HometComponent } from './homet/homet.component'; // Exemple de route vers HometComponent
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';

const routes: Routes = [
  { path: '', component: HometComponent }, // Route par défaut
  { path: 'home', component: HometComponent }, // Exemple d'une autre route
];



@NgModule({
  
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}


