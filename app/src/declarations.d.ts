declare module '*';

interface Message {
  sender : string;
  message : string;
}

interface XHRResponse {
  json() : JSON;
}

interface BattleXHR {
  get(url : string) : Promise<XHRResponse> ;
}
