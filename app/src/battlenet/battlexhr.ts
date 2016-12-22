interface XHRResponse {
  json() : JSON;
}

export class BattleXHR {
  get(url : any) : Promise<XHRResponse> {
    const request = new XMLHttpRequest();
    return new Promise((resolve, reject) => {
      request.open('GET', url, true);

      request.onreadystatechange = () => {
        if(request.readyState === 4) { // done
          if(request.status === 200) { // complete
            resolve({ json: () => { return JSON.parse(request.responseText) } });
          }
        }
      };
      request.send(null);
    });
  }
}
