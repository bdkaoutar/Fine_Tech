import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-branding',
  standalone: true,
  imports: [RouterModule],
  template: `
    <div class="branding">
      <a [routerLink]="['/home']">
        <img
          src="./assets/images/logos/logo.svg"
          class="align-middle m-2 logo-img"
          alt="logo"
        />
      </a>
    </div>
  `,
  styleUrls: ['./navbar.scss'], 
})
export class BrandingComponent {
  constructor() {}
}
