import { Injectable, Inject } from '@angular/core';
import {
  HttpClient,
  HttpHeaders,
  HttpResponse,
  HttpErrorResponse
} from '@angular/common/http';

import { Observable } from 'rxjs/Observable';
import { ErrorObservable } from 'rxjs/observable/ErrorObservable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';

import { AuthenticationService } from '../services/authentication.service';
import { APP_CONFIG, IAppConfig } from '../app.config';

const HEADERS: any = { headers: { 'Content-Type': 'application/json' }};

/**
 * Service for the user.
 */
@Injectable()
export class UserService {

  constructor(
    @Inject(APP_CONFIG) private config: IAppConfig,
    private http: HttpClient,
    private authenticationService: AuthenticationService
  ) {}

  getAllUsers() {
    return this.http.get<any>(
      this.config.baseURL + 'user/list/'
    );
  }

  removeUser(userID: number) {
    return this.http.delete(
      this.config.baseURL + 'account/' + userID + '/delete/'
    );
  }

}
