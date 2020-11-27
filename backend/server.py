from starlette.applications import Starlette
from starlette.websockets import WebSocketDisconnect
import json
import logging
import uvicorn
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
app = Starlette()

db = {
    '2018UCS0087': {
        'name' : 'Abhishek',
        'email' : 'abhishek0220@outlook.com'
    },
    '2018UCS0083': {
        'name' : 'Deepansh',
        'email' : 'deepansh.lodhi@random.email'
    }
}

async def receive_json(websocket):
    message = await websocket.receive_text()
    return json.loads(message)

def sendMsg(msg, typ):
    resp = {
        'event':'msg',
        'msg' : f'{msg}',
        'type' : typ
    }
    return json.dumps(resp)

def query(msg):
    arr = msg.split()
    if(arr[0] == "FETCH"):
        if(arr[2] not in db):
            return "Doesn`t exist"
        if(arr[1] == "EMAIL"):
            return db[arr[2]]['email']
        elif(arr[1] == 'NAME'):
            return db[arr[2]]['name']
    return "Doesn`t exist"

@app.websocket_route('/socket')
async def websocket_endpoint(websocket):
    await websocket.accept()
    message = await receive_json(websocket)
    username = message['username']
    password = message['password']
    resp = {
        'event' : 'auth',
        'status' : 'ok'
    }
    await websocket.send_text(json.dumps(resp))
    logger.info(f'Client connected')
    while (True):
        try:
            message = await receive_json(websocket)
            quer = message['query'].upper()
            await websocket.send_text(sendMsg(quer, True))
            msg = query(quer)
            await websocket.send_text(sendMsg(msg, False))
        except WebSocketDisconnect:
            break
        except:
            print("unknown error")
            break
    await websocket.close()
    logger.info(f'Disconnected')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host='0.0.0.0', port=port)