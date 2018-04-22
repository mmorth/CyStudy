import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AppComponent } from '../../app.component';
import { StudyGroup } from '../../models/study-group.interface';
import { DashboardComponent } from '../dashboard.component';
import { StudyGroupService } from '../../services/study-group.service';
import { CourseService } from '../../services/course.service';

/**
 * The form for creating a new study group.
 */
@Component({
  selector: 'app-create',
  templateUrl: './create.component.html'
})
export class CreateComponent implements OnInit {

  courses: any[] = [];
  keys: string[] = [];
  courseID: number = -1;

  constructor(
    private appComponent: AppComponent,
    private studyGroupService: StudyGroupService,
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
    this.courseService.getAllCourses().subscribe(
      data => {
        this.courses = {...data};
        this.keys = Object.keys(this.courses);
      }
    );
    this.dashboard.hideMobileMenuAfterNavigate();
  }

  /**
   * Calls the service to create a new study group and navigates to home.
   * @returns {void}
   */
  onSubmit(): void {
    if (this.courseID !== -1) {
      this.studyGroupService.createStudyGroup(this.courseID)
      .subscribe(() => {
        this.router.navigate(['/dashboard']);
      });
    } else {
      console.log(this.courseID);
    }
  }

}
