import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';

export interface TransactionData {
  id: number;
  fromAccount: string;
  toAccount: string;
  amount: number;
  date: string;
  status: string; // "success" or "failed"
}

const TRANSACTIONS_DATA: TransactionData[] = [
  {
    id: 1,
    fromAccount: '1234567890',
    toAccount: '0987654321',
    amount: 5000,
    date: '2023-12-01',
    status: 'success',
  },
  {
    id: 2,
    fromAccount: '1234567890',
    toAccount: '1234987654',
    amount: 12000,
    date: '2023-12-02',
    status: 'failed',
  },
  {
    id: 3,
    fromAccount: '5678123456',
    toAccount: '9876543210',
    amount: 7500,
    date: '2023-12-03',
    status: 'success',
  },
  {
    id: 4,
    fromAccount: '1111222233',
    toAccount: '3333222211',
    amount: 2000,
    date: '2023-12-04',
    status: 'success',
  },
];

@Component({
  selector: 'app-transactions-user-table',
  standalone: true,
  imports: [CommonModule, MatTableModule, MatButtonModule, MatCardModule],
  templateUrl: './transactions-user-table.component.html',
})
export class AppTransactionsComponent {
  displayedColumns: string[] = ['fromAccount', 'toAccount', 'amount', 'date', 'status', 'actions'];
  dataSource = TRANSACTIONS_DATA;

  constructor(private router: Router) {}

  viewDetails(transactionId: number): void {
    // Navigate to a detailed view of the transaction
    this.router.navigate(['/transactions/details', transactionId]);
  }
}
