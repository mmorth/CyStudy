import { Injectable } from '@angular/core';
import { ReplaySubject } from 'rxjs/ReplaySubject';

/**
 * Obtains the group's ID from the route.
 */
@Injectable()
export class GroupIDService {

  /**
   * The source of the group ID.
   */
  public paramSource: ReplaySubject<any> = new ReplaySubject<any>();

  /**
   * Gets the group ID.
   */
  public getParams(params) {
    this.paramSource.next(params);
  }

}
