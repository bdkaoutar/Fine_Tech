import { Component } from '@angular/core';
import { MaterialModule } from '../../material.module';
import { MatMenuModule } from '@angular/material/menu';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

export interface UserData {
  id: number;
  uname: string;
  position: string;
  hrate: number;
  skills: string;
  priority: string;
  progress: string;
}

const USER_DATA: UserData[] = [
  {
    id: 1,
    uname: 'Jason Roy',
    position: 'Developer',
    skills: '3.5',
    hrate: 73.2,
    priority: 'Low',
    progress: 'success',
  },
  {
    id: 2,
    uname: 'Mathew Flintoff',
    position: 'Project Manager',
    skills: '4.0',
    hrate: 81.5,
    priority: 'Medium',
    progress: 'warning',
  },
  {
    id: 3,
    uname: 'Anil Kumar',
    position: 'Designer',
    skills: '2.8',
    hrate: 68.3,
    priority: 'High',
    progress: 'error',
  },
  {
    id: 4,
    uname: 'George Cruize',
    position: 'Analyst',
    skills: '3.9',
    hrate: 75.0,
    priority: 'Very High',
    progress: 'accent',
  },
];

@Component({
  selector: 'app-users-table',
  standalone: true,
  imports: [MaterialModule, MatMenuModule, MatButtonModule, CommonModule],
  templateUrl: './users.component.html',
})
export class AppUsersComponent {
  displayedColumns: string[] = ['name', 'position', 'progress', 'priority', 'skills'];
  dataSource = USER_DATA;

  constructor(private router : Router) {}

  goToAddUsers() {
    this.router.navigate(['/users/add']);
  }
}
