import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

interface Option {
  value: string;
  viewValue: string;
}

@Component({
  selector: 'app-form-add-user',
  standalone: true,
  imports: [
    MatFormFieldModule,
    MatSelectModule,
    FormsModule,
    ReactiveFormsModule,
    MatButtonModule,
    MatCardModule,
    MatInputModule,
    CommonModule
  ],
  templateUrl: './forms.component.html',
})
export class AppFormsComponent {
  userForm: FormGroup;

  countries: Option[] = [
    { value: 'usa', viewValue: 'USA' },
    { value: 'india', viewValue: 'India' },
    { value: 'france', viewValue: 'France' },
    { value: 'uk', viewValue: 'UK' },
  ];

  states: Option[] = [
    { value: 'california', viewValue: 'California' },
    { value: 'texas', viewValue: 'Texas' },
    { value: 'new-york', viewValue: 'New York' },
    { value: 'florida', viewValue: 'Florida' },
  ];

  cities: Option[] = [
    { value: 'los-angeles', viewValue: 'Los Angeles' },
    { value: 'houston', viewValue: 'Houston' },
    { value: 'chicago', viewValue: 'Chicago' },
    { value: 'miami', viewValue: 'Miami' },
  ];

  constructor(private fb: FormBuilder) {
    this.userForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      country: ['', Validators.required],
      state: ['', Validators.required],
      city: ['', Validators.required],
    });
  }

  onSubmit(): void {
    if (this.userForm.valid) {
      console.log('Form Data:', this.userForm.value);
    } else {
      console.log('Form Invalid');
    }
  }
}
