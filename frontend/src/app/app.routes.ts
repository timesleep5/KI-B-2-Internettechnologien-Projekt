import {Routes} from '@angular/router';
import {WelcomeComponent} from "./welcome/welcome.component";
import {ChatComponent} from "./chat/chat.component";
import {ImprintComponent} from "./imprint/imprint.component";
import {ChatNotFoundComponent} from "./chat-not-found/chat-not-found.component";
import {DocumentationComponent} from "./documentation/documentation.component";

export const routes: Routes = [
  {path: '', redirectTo: 'welcome', pathMatch: 'full'},
  {path: 'welcome', component: WelcomeComponent},
  {path: 'chat', component: ChatComponent},
  {path: 'chat-not-found', component: ChatNotFoundComponent},
  {path: 'imprint', component: ImprintComponent},
  {path: 'doc', component: DocumentationComponent}
];
