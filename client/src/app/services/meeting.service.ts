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

import { Meeting } from '../models/meeting';
import { APP_CONFIG, IAppConfig } from '../app.config';

const HEADERS: any = { headers: { 'Content-Type': 'application/json' }};

/**
 * Contains methods for calling the meeting API.
 */
@Injectable()
export class MeetingService {

  constructor(
    @Inject(APP_CONFIG) private config: IAppConfig,
    private http: HttpClient
  ) {}

  /**
   * Gets all meetings for a study group.
   * @param {number} studyGroupId The group ID to get meetings for.
   */
  getMeetings(studyGroupId: number) {
    return this.http.get<any>(
      this.config.baseURL + "calendar/" + studyGroupId + "/meetings/list/"
    );
  }

  /**
   * Creates a new meeting.
   * @param {number} studyGroupId The study group ID.
   * @param {Meeting} meeting The meeting object to be sent to the API.
   */
  createMeeting(studyGroupId: number, meeting: Meeting) {
    let date = meeting.date.split('-');
    let time = meeting.time.split(':');

    let day = +date[2];
    let month = +date[1];
    let year = +date[0];
    let hour = +time[0];
    let minute = +time[1];

    return this.http.post(
      this.config.baseURL + "calendar/" + studyGroupId + "/meeting/",
      JSON.stringify({
        day: day,
        month: month,
        year: year,
        hour: hour,
        minute: minute,
        location: meeting.location,
        description: meeting.description
      }),
      HEADERS
    );
  }

  /**
   * Deletes a meeting.
   * @param {number} studyGroupId - The study group ID.
   * @param {number} meetingId - The ID of the meeting to delete.
   */
  deleteMeeting(studyGroupId: number, meetingId: number) {
    return this.http.delete<any>(
      this.config.baseURL + "calendar/" + studyGroupId + "/meeting/" + meetingId + "/delete/"
    );
  }

  /**
   * Sends an image to the server for classification.
   * @param {string} dataURI - The image in data URI form.
   */
  sendImageForClassification(dataURI: string) {
    return this.http.post(
      this.config.baseURL + "building_id/get/",
      JSON.stringify({ image: dataURI }),
      HEADERS
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
