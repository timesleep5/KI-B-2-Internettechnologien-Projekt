import {ApplicationConfig} from '@angular/core';
import {provideRouter} from '@angular/router';

import {routes} from './app.routes';
import {provideClientHydration} from '@angular/platform-browser';
import {provideHttpClient} from "@angular/common/http";
import {provideToastr} from "ngx-toastr";
import {provideAnimations} from "@angular/platform-browser/animations";
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

/*
 * Author: Korbinian Zormeier
 * Date: July 2, 2024
 *
 * Project: Internettechnologien Projektarbeit - JAWA Leasing Bot
 *
 * Description: This file is part of the Internettechnologien project. It
 * contains the providers for the entire application.
 *
 * Legal Notice:
 * This source code is subject to the terms and conditions defined in the file
 * 'LICENSE.txt', which is part of this source code package. Unauthorized copying
 * of this file, via any medium, is strictly prohibited.
 *
 * (c) 2024 Technische Hochschule Deggendorf. All rights reserved.
 */

export const BASE_URL = "http://127.0.0.1:8080";

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideClientHydration(),
    provideHttpClient(),
    provideAnimations(),
    provideToastr(), provideAnimationsAsync(),
  ]
};
