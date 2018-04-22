import { Injectable, Inject } from '@angular/core';
import { Http, Headers, Response } from '@angular/http';

import { Observable } from 'rxjs';
import 'rxjs/add/operator/map';

import { APP_CONFIG, IAppConfig } from '../app.config';

/**
 * Service for calling the API to authenticate the user.
 */
@Injectable()
export class AuthenticationService {

  /**
   * The JSON web token.
   */
  public token: string = "";
 
  constructor(
    @Inject(APP_CONFIG) private config: IAppConfig,
    private http: Http
  ) {
    var currentUser = JSON.parse(localStorage.getItem('currentUser'));
    this.token = currentUser && currentUser.token;
  }

  /**
   * Sends the username and password to the API for authentication.
   * @param {string} username The value entered into the username field.
   * @param {string} password The value entered into the password field.
   * @return {Observable}
   */
  login(username: string, password: string): Observable<boolean> {
    var headers = new Headers();
    headers.append('Content-Type','application/json');

    return this.http.post(
      this.config.baseAuthURL + 'api-token-auth/',
      JSON.stringify({ username: username, password: password }),
      {headers: headers}
    ).map((response: Response) => {
      let token = response.json() && response.json().token;
      if (token) {
        this.token = token;
        localStorage.setItem('currentUser', JSON.stringify({ username: username, token: token }));
        return true;
      } else {
        return false;
      }
    });
  }

  getUser(username: string){
    return this.http.get(
      this.config.baseURL + 'user/' + username + '/home/'
    ).map((r: Response) => {
      localStorage.setItem(
        'userInfo',
        JSON.stringify(
          {
            userType: r.json().user_type,
            userID:   r.json().user_id
          }
        )
      );
    });
  }

  /**
   * Deletes the JWT from local storage.
   */
  logout(): void {
    this.token = null;
    if (localStorage.getItem('currentUser')) {
      localStorage.removeItem('currentUser');
      localStorage.removeItem('userInfo');
      location.reload();
    }
  }

}
