import { Component } from '@angular/core';
import { AppFormsComponent } from "../components/forms-add-user/forms.component";

@Component({
  selector: 'app-users-add',
  standalone: true,
  imports: [AppFormsComponent],
  templateUrl: './users-add.component.html',
  styleUrl: './users-add.component.scss'
})
export class UsersAddComponent {

}
