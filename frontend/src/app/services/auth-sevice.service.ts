import { H } from '@angular/cdk/keycodes';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({ // decorator @.....
  providedIn: 'root'
})
export class AuthSeviceService {

  constructor(private http : HttpClient) { }

  register(data : any) : any {
    console.log('Registering user', data); ///

    //send data to server
    // HTTP CLIENT --> Axios : React --> get post put delete patch
      this.http.post('http://localhost:8080/api/v1/auth/register', data).subscribe({
        next: (response) => {
          console.log('Response from server', response);
        },
        error: (error) => {
          console.error('Error in registering user', error);
        }
      })
  }

  login(data : any) : Observable<any>{
    return this.http.post('http://localhost:8080/api/v1/auth/login', data);
  }
}
// -----------> JS --> Observable  : Tsena la response mn server  --> Subscribe --> next --> error

// injection de dependance (CLass) --> (Class) --> 
