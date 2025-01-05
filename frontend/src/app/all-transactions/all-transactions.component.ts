import { Component } from '@angular/core';
import { AppTransactionsComponent } from "../components/transactions-user-table/transactions-user-table.component";

@Component({
  selector: 'app-all-transactions',
  standalone: true,
  imports: [AppTransactionsComponent],
  templateUrl: './all-transactions.component.html',
  styleUrl: './all-transactions.component.scss'
})
export class AllTransactionsComponent {

}
