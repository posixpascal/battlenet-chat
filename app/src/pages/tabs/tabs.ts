import { Component } from '@angular/core';

import { HomePage } from '../home/home';
import { ChatPage } from '../chat/chat';
import { SettingsPage } from '../settings/settings';

@Component({
  templateUrl: 'tabs.html'
})
export class TabsPage {
  // this tells the tabs component which Pages
  // should be each tab's root Page
  tab1Root: any = HomePage;
  tab2Root: any = ChatPage;
  tab3Root: any = SettingsPage;

  constructor() {

  }
}
