import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';

/**
 * Prevents access to certain routes if unauthorized.
 */
@Injectable()
export class AuthGuard implements CanActivate {

  constructor(private router: Router) { }

  /**
   * Runs before routing.
   * @returns {boolean} True if the user is logged in, false otherwise.
   */
  canActivate() {
    if (localStorage.getItem('currentUser')) {
      return true;
    }
    this.router.navigate(['/']);
    return false;
  }

}
