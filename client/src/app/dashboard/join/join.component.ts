import { Component, OnInit } from '@angular/core';

import { AppComponent } from '../../app.component';
import { DashboardComponent } from '../dashboard.component';
import { StudyGroup } from '../../models/study-group.interface';
import { StudyGroupService } from '../../services/study-group.service';

declare var $: any;

/**
 * The page for joining a study group.
 */
@Component({
  selector: 'app-join',
  templateUrl: './join.component.html',
  styleUrls: ['./join.component.css']
})
export class JoinComponent implements OnInit {

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
   * The message to display if there are no groups to join.
   */
  noGroups: string = "";

  /**
   * Any error that the service returns.
   */
  error: string = "";

  constructor(
    private appComponent: AppComponent,
    private studyGroupService: StudyGroupService,
    private dashboard: DashboardComponent
  ) {
    appComponent.resetMenu();
  }

  /**
   * Runs when the component initializes.
   */
  ngOnInit() {
    this.listStudyGroups();
    this.dashboard.hideMobileMenuAfterNavigate();
  }

  /**
   * Calls the service to get all the study groups the user is not a member of.
   */
  listStudyGroups() {
    this.studyGroupService.getAllNotJoined()
      .subscribe(
        data => {
          this.studyGroups = { ...data };
          this.studyGroupsKeyArray = Object.keys(this.studyGroups);
          if (!this.studyGroupsKeyArray.length) {
            this.noGroups = "There are no groups to join.";
          }
          this.members = this.dashboard.extractMembers(data);
        },
        error => this.error = error,
      );
  }

  /**
   * Calls the service to join a study group.
   * @param {number} studyGroupId The ID of the group to join.
   */
  joinStudyGroup(studyGroupId: number) {
    this.studyGroupService.joinStudyGroup(studyGroupId)
      .subscribe(() => $("#join-btn-" + studyGroupId).prop("disabled", true));
  }

}
