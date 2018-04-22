import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';

@Injectable()
export class ModGuard implements CanActivate {

  constructor(private router: Router) { }

  /**
   * Runs before routing.
   * @returns {boolean} True if the user is logged in, false otherwise.
   */
  canActivate() {
    if (JSON.parse(localStorage.getItem('userInfo')).userType === 1) {
      return true;
    }
    this.router.navigate(['/dashboard']);
    return false;
  }

}
