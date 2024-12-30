import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HometComponent } from './homet/homet.component';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  standalone: true,
  imports: [HometComponent]  // Include both components in the imports array
})
export class AppComponent {
  title = 'maprojet';
}

