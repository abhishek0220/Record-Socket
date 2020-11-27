import { Component } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  messages: any[];
  toAuth= false;
  userGot = "";
  con_color = "red";
  conActive = false;
  RETRY_SECONDS = 10; 
  myWebSocket: WebSocketSubject<any>;
  userName = new FormControl();
  password = new FormControl();

  constructor() {
    this.userName.setValue("");
    this.password.setValue("");
    
    this.messages = [
      {
        text: "Hi, I`m a Query application built using Websockets. Pls Connect to server",
        date: new Date(),
        reply: false,
        type: 'text',
        user: {
          name: 'Server',
          avatar: 'https://i.gifer.com/no.gif',
        },
      }
    ];
  }
  async connectToServer(){
    console.log("connecting")
    this.myWebSocket = await this.connectionStart();
    this.myWebSocket.subscribe(    
      async(msg) => {
        if(msg['event'] == 'auth') this.authEvent(msg);
        else if(msg['event'] == 'msg'){
          this.pushMsg(msg['msg'], msg['type']);
        }
      },   
      err => {
        this.closeConnection();
      },     
      () => console.log("terminated"),
    );
    this.myWebSocket.next({auth : this.toAuth ,username: this.userName.value, password:this.password.value});
  }
  async connectionStart(){
    if(this.conActive){
      this.closeConnection();
    }
    return webSocket('ws://localhost:5000/socket');
  }
  authEvent(msg : object){
    console.log("auth")
    if(msg['status'] == 'ok'){
      this.password.setValue("");
      this.conActive = true;
      this.con_color = 'green';
      console.log("Connected");
      if(msg['message'] == 201){
        this.userGot = msg['user'];
        this.getMessage(msg['log']);
      }
      else this.userGot = "Guest";
    }
    else{
      this.closeConnection();
    }
  }
  getMessage(arr){
    this.messages = []
    for(var i in arr){
      this.pushMsg(arr[i]['msg'], arr[i]['type'])
    }
  }
  async closeConnection(){
    this.conActive = false;
    this.myWebSocket.complete();
    this.con_color = 'red';
    console.log("Disconnected");
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
