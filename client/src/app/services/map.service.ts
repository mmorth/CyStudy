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

/**
 * Contains methods for calling the Google Maps API.
 */
@Injectable()
export class MapService {

  constructor(
    private http: HttpClient
  ) {}

  /**
   * Calls the Google Maps API to get data about a location.
   * @param {string} location The location.
   */
  getLocationData(location: string) {
    return this.http.get<any>(
      'https://maps.googleapis.com/maps/api/geocode/json?address='
       + location + '&key=AIzaSyBfqgkKAkaJIhtQQ20ZeO7nr8N9yw9hLOg'
    );
  }

  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      console.error('An error occurred:', error.error.message);
    } else {
      console.error(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error}`
      );
    }
    return new ErrorObservable(
      'Something bad happened; please try again later.'
    );
  };

}
