import { Component } from '@angular/core';
import { BattleNet } from '../../battlenet/battlenet';
import { NavController } from 'ionic-angular';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {
  private username : string;
  private password : string;
  constructor(public navCtrl: NavController) {

  }

  signIn(event : Event){
    // hardcode values first
    this.username = "";
    this.password = "";

    const battleNet = BattleNet.getInstance();
    battleNet.isReady().then(() => {
      battleNet.getMessages().then((messages) => {
        console.log(messages);
      });
    });
  }
}
