import { Component, OnInit, Inject } from '@angular/core';
import { Router } from '@angular/router';
import { Http, Headers, Response } from '@angular/http';

import { Observable } from 'rxjs';

import { AuthenticationService } from '../services/authentication.service';
import { APP_CONFIG, IAppConfig } from '../app.config';

/**
 * The form for creating a new account.
 */
@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['../login/login.component.css']
})
export class SignUpComponent implements OnInit {

  first_name: string = "";
  last_name:  string = "";
  email:      string = "";
  username:   string = "";
  password:   string = "";
  error:      string = "";

  constructor(
    @Inject(APP_CONFIG) private config: IAppConfig,
    private authenticationService: AuthenticationService,
    private router: Router,
    private http: Http
  ) {}

  /**
   * Runs when the component initializes.
   */
  ngOnInit() {}

  /**
   * Sends the form data to the service to create the account.
   */
  onSubmit(): void {
    var headers = new Headers();
    headers.append('Content-Type','application/json');

    this.http.post(
      this.config.baseURL + "account/create/",
      JSON.stringify(
        {
          username: this.username,
          password: this.password,
          first_name: this.first_name,
          last_name: this.last_name,
          email: this.email
        }
      ),
      { headers: headers }
    ).subscribe(
      () => { this.router.navigate(['/']) },
      error => { console.log(JSON.stringify(error.json)) }
    );
  }
}
