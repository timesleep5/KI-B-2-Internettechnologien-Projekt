import {Routes} from '@angular/router';
import {WelcomeComponent} from "./welcome/welcome.component";
import {ChatComponent} from "./chat/chat.component";
import {ImprintComponent} from "./imprint/imprint.component";
import {ChatNotFoundComponent} from "./chat-not-found/chat-not-found.component";
import {DocumentationComponent} from "./documentation/documentation.component";

/*
 * Author: Korbinian Zormeier
 * Date: July 2, 2024
 *
 * Project: Internettechnologien Projektarbeit - JAWA Leasing Bot
 *
 * Description: This file is part of the Internettechnologien project. It
 * contains the implementation of the router paths to the different components.
 *
 * Legal Notice:
 * This source code is subject to the terms and conditions defined in the file
 * 'LICENSE.txt', which is part of this source code package. Unauthorized copying
 * of this file, via any medium, is strictly prohibited.
 *
 * (c) 2024 Technische Hochschule Deggendorf. All rights reserved.
 */

export const routes: Routes = [
  {path: '', redirectTo: 'welcome', pathMatch: 'full'},
  {path: 'welcome', component: WelcomeComponent},
  {path: 'chat', component: ChatComponent},
  {path: 'chat-not-found', component: ChatNotFoundComponent},
  {path: 'imprint', component: ImprintComponent},
  {path: 'doc', component: DocumentationComponent}
];
