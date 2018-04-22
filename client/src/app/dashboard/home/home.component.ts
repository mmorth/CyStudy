import { Component, OnInit } from '@angular/core';

import { AppComponent } from '../../app.component';
import { DashboardComponent } from '../dashboard.component';
import { StudyGroup } from '../../models/study-group.interface';
import { StudyGroupService } from '../../services/study-group.service';
import { UserService } from '../../services/user.service';

declare var $: any;

/**
 * The home page for listing the study groups that a user belongs to.
 */
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html'
})
export class HomeComponent implements OnInit {

  /**
   * An array of study groups.
   */
  studyGroups: StudyGroup[] = [];

  /**
   * The keys for displaying study groups in the template.
   */
  studyGroupsKeyArray: String[] = [];

  /**
   * The members of a groups.
   */
  members: string[] = [];

  /**
   * HTTP request headers.
   */
  headers: any;

  /**
   * Any error that returns from the call to the service.
   */
  error: any;

  constructor(
    private studyGroupService: StudyGroupService,
    private app: AppComponent,
    private userService: UserService,
    private dashboard: DashboardComponent
  ) {
      app.resetMenu();
  }

  /**
   * Runs when the component initializes.
   */
  ngOnInit() {
    this.showUserStudyGroups();
    this.dashboard.hideMobileMenuAfterNavigate();
  }

  /**
   * Calls the service to get the study groups that a user belongs to.
   */
  showUserStudyGroups() {
    this.studyGroupService.getUserStudyGroups()
      .subscribe(
        data => {
          this.studyGroups = { ...data };
          this.studyGroupsKeyArray = Object.keys(this.studyGroups);
          this.members = this.dashboard.extractMembers(data);
        },
        error => this.error = error,
      );
  }

  /**
   * Calls the service to leave a study group and removes that group from the
   * screen.
   * @param {number} studyGroupId The ID of the group to leave.
   */
  leaveStudyGroup(studyGroupId: number) {
    this.studyGroupService.leaveStudyGroup(studyGroupId)
      .subscribe(
        () => $("#sg-" + studyGroupId).prop("hidden", true)
      );
  }

}
