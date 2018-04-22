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

import { Note } from '../models/note';
import { APP_CONFIG, IAppConfig } from '../app.config';

const HEADERS: any = { headers: { 'Content-Type': 'application/json' }};

/**
 * Contains methods for calling the note API.
 */
@Injectable()
export class NoteService {

  constructor(
    @Inject(APP_CONFIG) private config: IAppConfig,
    private http: HttpClient
  ) {}

  /**
   * Gets all the notes for a study group.
   * @param {number} studyGroupId The study group ID.
   */
  getNotes(studyGroupId: number) {
    return this.http.get<any>(
      this.config.baseURL + "notes/" + studyGroupId + "/"
    );
  }

  /**
   * Creates a new note in a study group.
   * @param {number} studyGroupId The study group ID.
   * @param {Note} note A note object.
   */
  createNote(studyGroupId: number, note: Note) {
    return this.http.post(
      this.config.baseURL + "notes/" + studyGroupId + "/create/",
      JSON.stringify({
        studygroup: studyGroupId,
        text: note.text
      }),
      HEADERS
    );
  }

  /**
   * Deletes a note.
   * @param {number} studyGroupId The study group ID.
   * @param {number} noteID The ID of the note to delete.
   */
  deleteNote(studyGroupId: number, noteID: number) {
    return this.http.delete<any>(
      this.config.baseURL + "notes/" + noteID + "/delete/"
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
