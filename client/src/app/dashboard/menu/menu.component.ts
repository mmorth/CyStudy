import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AuthenticationService } from '../../services/authentication.service';
import { DashboardComponent } from '../dashboard.component';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {

  USERTYPE: number = JSON.parse(localStorage.getItem('userInfo'))['userType'];
  isMod:   boolean = 1 === this.USERTYPE;
  isAdmin: boolean = 2 === this.USERTYPE;

  constructor(
    private router: Router,
    private authenticationService: AuthenticationService,
    private dashboard: DashboardComponent
  ) {}

  ngOnInit() {}

  logout(): void {
    this.router.navigate(['/']);
    this.dashboard.hideMobileMenuAfterNavigate();
  }

}
