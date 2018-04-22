import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/switchMap';

import { StudyGroup } from '../../models/study-group.interface';
import { StudyGroupService } from '../../services/study-group.service';
import { GroupIDService } from '../../services/group-id.service';
import { DashboardComponent } from '../dashboard.component';

/**
 * The parent component a single study group.
 */
@Component({
  selector: 'app-group',
  templateUrl: './group.component.html',
  styleUrls: ['./group.component.css']
})
export class GroupComponent implements OnInit {

  /**
   * The group's ID.
   */
  groupID: number;

  /**
   * The instance of the study group.
   */
  group: StudyGroup;

  /**
   * A list of members in the study group.
   */
  members: string[] = [];

  /**
   * Any error that the service returns.
   */
  error: any;

  /**
   * The user's ID.
   */
  userID: number = JSON.parse(localStorage.getItem('userInfo'))['userID'];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private studyGroupService: StudyGroupService,
    private groupIDService: GroupIDService,
    private dashboard: DashboardComponent
  ) {
    route.params.subscribe(
      (params) => groupIDService.getParams(params)
    );
  }

  /**
   * Runs when the component initializes.
   */
  ngOnInit() {
    this.dashboard.hideMobileMenuAfterNavigate();
    this.groupID = +this.route.snapshot.paramMap.get('id');
    this.studyGroupService.getStudyGroup(this.userID, this.groupID)
      .subscribe(
        data => {
          this.group = data[0];
          this.members = this.dashboard.extractMembers(data);
        },
        error => this.error = error,
      );
  }

}
