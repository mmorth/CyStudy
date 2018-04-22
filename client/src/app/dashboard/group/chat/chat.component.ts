import { Component, OnInit, Inject } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { DomSanitizer } from '@angular/platform-browser';

import { GroupIDService } from '../../../services/group-id.service';
import { APP_CONFIG, IAppConfig } from '../../../app.config';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {

  /**
   * The group's unique ID.
   */
  groupID: number;

  /**
   * The username of the logged in user.
   */
  username: string = JSON.parse(localStorage.getItem('currentUser'))['username'];

  /**
   * URL for the chat room with username and groupID passed in.
   */
  chatURL: string;

  constructor(
    @Inject(APP_CONFIG) private config: IAppConfig,
    private route: ActivatedRoute,
    private router: Router,
    private groupIDService: GroupIDService,
    public sanitizer: DomSanitizer
  ) {
    groupIDService.paramSource.subscribe((params) => {
      this.groupID = params.id;
      this.chatURL = this.config.baseURL + 'groupchat/'
        + this.username + '/' + this.groupID + '/chat/';
    });
  }

  /**
   * Runs when the component initializes.
   */
  ngOnInit() {
    this.groupID = +this.route.snapshot.paramMap.get('id');
  }

}
