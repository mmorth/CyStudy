import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AppComponent } from '../../app.component';
import { DashboardComponent } from '../dashboard.component';
import { CourseService } from '../../services/course.service';

/**
 * The form for creating a new study group.
 */
@Component({
  selector: 'app-courses',
  templateUrl: './courses.component.html'
})
export class CoursesComponent implements OnInit {

  courseDepartment: string = "";
  courseTitle: string = "";
  courseNum: number = 0;
  courses: any[] = [];
  keys: string[] = [];
  courseIDtoDelete: number = -1;

  error: string = "";

  constructor(
    private appComponent: AppComponent,
    private courseService: CourseService,
    private router: Router,
    private dashboard: DashboardComponent
  ) {
    appComponent.resetMenu();
  }

  /**
   * Runs when the component initializes.
   * @returns {void}
   */
  ngOnInit() {
    this.getCourseList();
    this.dashboard.hideMobileMenuAfterNavigate();
  }

  getCourseList() {
    this.courseService.getAllCourses().subscribe(
      data => {
        this.courses = {...data};
        this.keys = Object.keys(this.courses);
      }
    );
  }

  /**
   * Calls the service to courses a new study group and navigates to home.
   * @returns {void}
   */
  onSubmit(): void {
    if (this.courseDepartment !== "" && this.courseTitle !== "" && this.courseNum !== 0) {
      this.courseService.createCourse(this.courseDepartment.toUpperCase(), this.courseNum, this.courseTitle)
      .subscribe(() => {
        this.courseDepartment = "";
        this.courseTitle = "";
        this.courseNum = 0;
        alert('Course has been Created');
        this.getCourseList();
      });
    } else {
      error => this.error = error;
    }
  }

  onRemove(): void {
    if(this.courseIDtoDelete > 0) {
      this.courseService.removeCourse(this.courseIDtoDelete)
      .subscribe(
        () => {
          this.courseIDtoDelete = -1;
          alert('Course has been Removed');
          this.getCourseList();
        },
        error => {
          this.error = error;
          alert('There exists at least one studygroup which uses this course. Cannot delete. Please contact the Moderator.');
        }
      );
    }
  }

}
