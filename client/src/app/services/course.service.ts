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

import { APP_CONFIG, IAppConfig } from '../app.config';

const HEADERS: any = { headers: { 'Content-Type': 'application/json' }};

/**
 * The service for calling the courses API.
 */
@Injectable()
export class CourseService {

  courseDepartment: string = "";
  courseTitle: string = "";
  courseNum: number = 0;

  constructor(
    @Inject(APP_CONFIG) private config: IAppConfig,
    private http: HttpClient
  ) {}

  /**
   * Get all available courses.
   */
  getAllCourses() {
    return this.http.get<any>(
      this.config.baseURL + 'studygroup/courses/list/'
    );
  }

  createCourse(courseDepartment: string, courseNum: number, courseTitle: string) {
    return this.http.post(
      this.config.baseURL + 'studygroup/course/create/',
      JSON.stringify({ course_number: courseNum,  course_department: courseDepartment, course_name: courseTitle }),
      HEADERS
    );
  }

  removeCourse(courseID: number) {
    return this.http.post(
      this.config.baseURL + 'studygroup/course/' + courseID + '/remove/',
      JSON.stringify({ course_id: courseID }),
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
