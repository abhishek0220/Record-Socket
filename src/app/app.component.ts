import { Component } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  messages: any[];
  con_color = "red";
  connection$: WebSocketSubject<any>;
  RETRY_SECONDS = 10; 
  myWebSocket: WebSocketSubject<any>;

  constructor() {
    this.messages = [
      {
        text: "sample 1",
        date: new Date(),
        reply: true,
        type: 'text',
        user: {
          name: 'Jonh Doe',
          avatar: 'https://i.gifer.com/no.gif',
        },
      },
      {
        text: "sample 1",
        date: new Date(),
        reply: false,
        type: 'text',
        user: {
          name: 'Jonh Doe',
          avatar: 'https://i.gifer.com/no.gif',
        },
      }
    ];
  }
  connectToServer(){
    console.log("connecting")
    this.myWebSocket = webSocket('ws://localhost:5000/socket')
    this.myWebSocket.subscribe(    
      msg => {
        if(msg['event'] == 'auth') this.authEvent(msg);
        else if(msg['event'] == 'msg'){
          this.pushMsg(msg['msg'], msg['type']);
        }
      },
      // Called whenever there is a message from the server    
      err => {
        this.authEvent({status:'NotOK'})
      }, 
      // Called if WebSocket API signals some kind of error    
      () => console.log('complete') 
      // Called when connection is closed (for whatever reason)  
    );
    this.myWebSocket.next({username: 'some message', password:'passcode'});
  }
  authEvent(msg : object){
    console.log("auth")
    if(msg['status'] == 'ok'){
      this.con_color = 'green';
      console.log("Connected");
    }
    else{
      this.con_color = 'red';
      console.log("Disconnected");
    }
  }
  sendMessage(event: any) {
    var msg : string = event.message;
    this.myWebSocket.next({query : msg});
  }
  pushMsg(msg : string, typ : boolean){
    var name = "Server";
    if(typ) name = "John";
    this.messages.push({
      text: msg,
      date: new Date(),
      reply: typ,
      type: 'text',
      user: {
        name: name,
        avatar: 'https://i.gifer.com/no.gif',
      },
    });
  }
}
