import { Routes } from '@angular/router';
import { BlankComponent } from './layouts/blank/blank.component';
import { FullComponent } from './layouts/full/full.component';
import { UsersComponent } from './users/users.component';
import { UsersAddComponent } from './users-add/users-add.component';
import { AllTransactionsComponent } from './all-transactions/all-transactions.component';
import { LoginComponent } from './login/login.component';
import { HometComponent } from './homet/homet.component';
export const routes: Routes = [
  {
    path: '',
    component: FullComponent,
    children: [
      {
        path: '',
        redirectTo: '/home',
        pathMatch: 'full',
      },
      {
        path: 'users',
        component : UsersComponent
      },
      {
        path: 'users/add',
        component : UsersAddComponent
      },
      {
        path: 'transactions',
        component : AllTransactionsComponent
      },
      
      {
        path: 'dashboard',
        loadChildren: () =>
          import('./pages/pages.routes').then((m) => m.PagesRoutes),
      },
      {
        path: 'ui-components',
        loadChildren: () =>
          import('./pages/ui-components/ui-components.routes').then(
            (m) => m.UiComponentsRoutes
          ),
      },
      {
        path: 'extra',
        loadChildren: () =>
          import('./pages/extra/extra.routes').then((m) => m.ExtraRoutes),
      },
    ],
  },
  {
    path: '',
    component: BlankComponent,
    children: [
      {
        path: 'authentication',
        loadChildren: () =>
          import('./pages/authentication/authentication.routes').then(
            (m) => m.AuthenticationRoutes
          ),
      },
      { path: 'home', component: HometComponent }, 
      { path: 'login', component: LoginComponent },
      { path: 'register', component: LoginComponent },
    ],
  },
  {
    path: '**',
    redirectTo: 'authentication/error',
  },
];
