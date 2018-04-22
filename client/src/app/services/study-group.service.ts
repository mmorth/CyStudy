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

import { StudyGroup } from '../models/study-group.interface';
import { APP_CONFIG, IAppConfig } from '../app.config';

const HEADERS: any = { headers: { 'Content-Type': 'application/json' }};

/**
 * Contains methods for calling the study group API.
 */
@Injectable()
export class StudyGroupService {

  /**
   * The username of the logged in user.
   */
  USERNAME: string = JSON.parse(localStorage.getItem('currentUser'))['username'];

  constructor(
    @Inject(APP_CONFIG) private config: IAppConfig,
    private http: HttpClient
  ) {}

  /**
   * Gets the details for a single study group.
   * @param {number} id The group ID.
   * @returns {Observable}
   */
  getStudyGroup(userID: number, groupID: number): Observable<StudyGroup[]> {
    return this.http.get<StudyGroup[]>(
      this.config.baseURL + 'studygroup/show/' + userID + '/' + groupID + '/'
    );
  }

  /**
   * Gets the study groups that a user belongs to.
   * @returns {Observable}
   */
  getUserStudyGroups(): Observable<StudyGroup[]> {
    return this.http.get<StudyGroup[]>(
      this.config.baseURL + 'studygroup/student/' + this.USERNAME + '/studygroups/'
    );
  }

  /**
   * Gets the study groups that a user does not belong to.
   * @returns {Observable}
   */
  getAllNotJoined(): Observable<StudyGroup[]> {
    return this.http.get<StudyGroup[]>(
      this.config.baseURL + 'studygroup/student/' + this.USERNAME + '/studygroups/notmember/'
    );
  }

  /**
   * Gets all study groups.
   * @returns {Observable}
   */
  getAllStudyGroups(): Observable<StudyGroup[]> {
    return this.http.get<StudyGroup[]>(
      this.config.baseURL + 'studygroup/list/'
    );
  }

  /**
   * Joins a study group.
   * @param {number} studyGroupId The ID of the group to join.
   */
  joinStudyGroup(studyGroupId: number) {
    return this.http.post(
      this.config.baseURL + 'studygroup/join/',
      JSON.stringify({ username: this.USERNAME, studygroup_id: studyGroupId }),
      HEADERS
    );
  }

  /**
   * Creates a new study group.
   * @param {number} courseId The course to create a study group for.
   */
  createStudyGroup(courseId: number) {
    return this.http.post(
      this.config.baseURL + 'studygroup/' + this.USERNAME + '/group/create/',
      JSON.stringify({ course_id: courseId }),
      HEADERS
    );
  }

  /**
   * Leaves a study group.
   * @param {number} studyGroupId The ID of the group to leave.
   */
  leaveStudyGroup(studyGroupId: number) {
    return this.http.post(
      this.config.baseURL + 'studygroup/' + studyGroupId + '/leave/',
      JSON.stringify({ username: this.USERNAME }),
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
