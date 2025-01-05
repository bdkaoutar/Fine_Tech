import { Component } from '@angular/core';
import { AppUsersComponent } from "../components/user-table/users.component";

@Component({
  selector: 'app-users',
  standalone: true,
  imports: [AppUsersComponent],
  templateUrl: './users.component.html',
  styleUrl: './users.component.scss'
})
export class UsersComponent {

}
