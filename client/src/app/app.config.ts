import { InjectionToken } from '@angular/core';

import { environment } from '../environments/environment';

export let APP_CONFIG = new InjectionToken('app.config');

export interface IAppConfig {
  baseURL: string;
  baseAuthURL: string;
}

const ip = environment.production == true ? '10.25.69.186' : '127.0.0.1';
const baseAuthURL = 'http://' + ip + ':8000/';
const baseURL = baseAuthURL + 'api/';

export const AppConfig: IAppConfig = {
  baseURL: baseURL,
  baseAuthURL: baseAuthURL
};
