import { Routes } from '@angular/router';
import {WelcomeComponent} from "./welcome/welcome.component";
import {ChatComponent} from "./chat/chat.component";
import {ImprintComponent} from "./imprint/imprint.component";

export const routes: Routes = [
  {path: '', redirectTo: 'welcome', pathMatch: 'full'},
  {path: 'welcome', component: WelcomeComponent},
  {path: 'chat/:id', component: ChatComponent},
  {path: 'imprint', component: ImprintComponent},
];
