from starlette.applications import Starlette
from starlette.websockets import WebSocketDisconnect
import json
import logging
import uvicorn
import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()
uri = os.getenv('MONGODB')
mongodb = MongoClient(uri)
db = mongodb['record']

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
app = Starlette()

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
        person = db.details.find_one({'entry' : arr[2]})
        if(person == None):
            return "Doesn`t exist"
        if(arr[1] == "EMAIL"):
            return person['email']
        elif(arr[1] == 'NAME'):
            return person['name']
    return "Invalid Query"

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
            quer = message['query']
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