import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { Observable } from 'rxjs';
import 'rxjs/add/operator/catch';

import { AuthenticationService } from '../services/authentication.service';

/**
 * The form for logging in.
 */
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  /**
   * The entered username.
   */
  username: string = "";

  /**
   * The entered password.
   */
  password: string = "";

  /**
   * The user's id.
   */
  user_id: any;

  /**
   * Any error that the service returns.
   */
  error: string = "";

  constructor(
    private authenticationService: AuthenticationService,
    private router: Router,
  ) {}

  /**
   * Runs when the component initializes.
   */
  ngOnInit() {
    this.authenticationService.logout();
  }

  /**
   * Calls the auth service with the entered username and password and redirects
   * to the home page upon successful login.
   */
  onSubmit(): void {
    if (this.username !== "" && this.password !== "") {
      this.authenticationService.login(this.username, this.password)
        .catch(error => {
          this.error = error._body.replace(/\\/g, '');
          return Observable.throw(error._body);
        })
        .subscribe(result => {
          if (result === true) {
            this.router.navigate(['/dashboard']);
          } else {
            this.error = "Incorrect username or password.";
          }
        });
      this.authenticationService.getUser(this.username).subscribe(() => { });
    } else {
      this.error = "Please enter a username and password.";
    }
  }

}
