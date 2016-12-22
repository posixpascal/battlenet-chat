import {Component} from '@angular/core';
import { Message } from '../../battlenet/message';
import {NavController} from 'ionic-angular';
import {BattleNet} from '../../battlenet/battlenet';

@Component({
  selector: 'page-chat',
  templateUrl: 'chat.html'
})
export class ChatPage {
  public chatBox : string;
  public messages : Message[];
  public battleNet : BattleNet;
  constructor(public navCtrl: NavController) {
    this.messages = [];
    this.battleNet = BattleNet.getInstance();
  }

  send(message, chatId){

    this.battleNet.isReady().then(() => {
      this.battleNet.sendMessage(chatId, message).then((messages) => {
        this.messages.push({
          sender: "SELF",
          message: message
        })
      });
    });
  }
}
