import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AppComponent } from '../../app.component';
import { DashboardComponent } from '../dashboard.component';
import { CourseService } from '../../services/course.service';
import { UserService } from '../../services/user.service';

/**
 * The form for creating a new study group.
 */
@Component({
  selector: 'app-courses',
  templateUrl: './moderation.component.html'
})
export class ModerationComponent implements OnInit {

  users: any[] = [];
  keys: string[] = [];
  userIDtoDelete: number = -1;

  error: string = "";

  constructor(
    private appComponent: AppComponent,
    private courseService: CourseService,
    private userService: UserService,
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
    this.getUserList();
    this.dashboard.hideMobileMenuAfterNavigate();
  }

  getUserList() {
    this.userService.getAllUsers().subscribe(
      data => {
        this.users = {...data};
        this.keys = Object.keys(this.users);
      }
    );
  }

  /**
   * Calls the service to courses a new study group and navigates to home.
   * @returns {void}
   */
  onSubmit(): void {
    if(this.userIDtoDelete > 0) {
      this.userService.removeUser(this.userIDtoDelete)
      .subscribe(
        () => {
          this.userIDtoDelete = -1;
          alert('User has been Removed');
          this.getUserList();
        },
        error => {
          this.error = error;
          alert('Cannot delete user.');
        }
      );
    }
  }

}
