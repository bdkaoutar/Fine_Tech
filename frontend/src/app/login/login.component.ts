import { Component, ElementRef, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  @ViewChild('container')
  container!: ElementRef;

  constructor(private router: Router) {

  }

  signIn() {
    if (!this.container.nativeElement.classList.contains('right-panel-active')) {
      window.location.href = '/dashboard'
    }
    this.container.nativeElement.classList.remove('right-panel-active');
  }

  signUp() {
    if (this.container.nativeElement.classList.contains('right-panel-active')) {
      window.location.href = '/dashboard'
    }
    this.container.nativeElement.classList.add('right-panel-active');
  }
}
