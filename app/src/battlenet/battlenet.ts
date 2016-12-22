/// <reference path="../../node_modules/protobufjs/types/protobuf.js.d.ts" />
/// <reference path="../../typings/node/node-0.12.d.ts" />

import * as protobuf from "protobufjs";
import {BattleXHR} from './battlexhr';
import {BattleProto} from './battleproto';
import {sha1} from 'cryptojs';

interface BattleNetSession {
  ACCESS_TOKEN: string;
}

interface Message {
  id : number;
  message : string,
  username: string

}

export class BattleNet  {
  private API_KEY = "h5aed5dvcmbu9cr3zv6wz9quzwp6swjz";
  // can't speak to battlenet directly. Specify the battlechat-server address here.
  private SERVER_ADDR = "http://127.0.0.1";
  private SERVER_PORT = 5000;
  private events : {any?: Function[]} = {};
  private socket : WebSocket;

  static _instance : BattleNet = null;

  public ready: boolean = false;
  public proto : protobuf.Root;
  public http : BattleXHR;
  public messages : BattleProto = {};

  constructor () {
    this.http = new BattleXHR();
  }

  isReady() : Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.get("./protobuf.bundle.json").then((res: XHRResponse) => {
        this.ready = true;
        this.proto = protobuf.Root.fromJSON(res.json());

        this.messages.account = {
          AccountCredential: this.proto.lookup("bnet.protocol.account.AccountCredential")
        };

        resolve();
      });
    });
  }

  getMessages() : Promise<Message[]> {
    return new Promise((resolve) => {
      this.http.get(this.SERVER_ADDR + this.SERVER_PORT + "/messages.json").then((res : XHRResponse) => {
        resolve(res.json());
      });
    });
  }

  getFriends() : Promise<any[]> {
    return new Promise((resolve) => {
      this.http.get(this.SERVER_ADDR + this.SERVER_PORT + "/friends.json").then((res : XHRResponse) => {
        resolve(res.json());
      });
    });
  }

  getAccount() : Promise<any[]> {
    return new Promise((resolve) => {
      this.http.get(this.SERVER_ADDR + this.SERVER_PORT + "/account.json").then((res : XHRResponse) => {
        resolve(res.json());
      });
    });
  }

  sendMessage(id, message){
    alert("to be implemented");
  }

  public static getInstance() : BattleNet {
    if (BattleNet._instance) {
      return BattleNet._instance;
    } else {
      BattleNet._instance = new BattleNet();
      return BattleNet._instance;
    }
  }

  public on(eventName: string, callback : Function){
    if (typeof this.events[eventName] === "undefined"){
      this.events[eventName] = [];
    }
    this.events[eventName].push(callback);
  }
}
