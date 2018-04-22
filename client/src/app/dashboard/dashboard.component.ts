import { Component, OnInit } from '@angular/core';

import { AppComponent } from '../app.component';

declare var mui: any;

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent implements OnInit {

  constructor(app: AppComponent) {
    app.resetMenu();
  }

  ngOnInit() {}

  extractMembers(data: any): string[] {
    let members: string[] = [];

    for (let i = 0; i < data.length; i++) {
      members[i] = (data[i].members.map(m => m.first_name).join(", "));
    };

    return members;
  }

  hideMobileMenuAfterNavigate(): void {
    let menu = document.getElementById('sidedrawer');
    menu.classList.remove('active');
    mui.overlay('off');
  }

}
