from starlette.applications import Starlette
from starlette.websockets import WebSocketDisconnect
import json
import logging
import uvicorn
import os, time
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

def sendMsg(msg, typ, isauth, uname):
    resp = {
        'event':'msg',
        'msg' : f'{msg}',
        'type' : typ,
        'time' : int(time.time()//1)
    }
    if(isauth):
        db.users.update_one({'username': uname}, {'$push': {'log': resp}}, upsert=True)
    return json.dumps(resp)

def query(msg, isauth):
    arr = msg.split()
    if(arr[0] == "FETCH" and len(arr) == 3):
        person = db.details.find_one({'entry' : arr[2].upper()})
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
    authenticated = False
    username = message['username']
    password = message['password']
    resp = {
        'event' : 'auth',
        'status' : 'ok',
        'message' : 200
    }
    if(message['auth'] == True):
        resp['message'] = 201
        resp['status'] = 'notOk'
        user = db.users.find_one({'username':username})
        if(user and user['password'] == password):
            authenticated = True
            resp['status'] = 'ok' 
            resp['user'] = username   
            resp['log'] = user.get('log',[])
    await websocket.send_text(json.dumps(resp))
    logger.info(f'Client connected')
    while (True):
        try:
            message = await receive_json(websocket)
            quer = message['query']
            await websocket.send_text(sendMsg(quer, True, authenticated,username))
            msg = query(quer, authenticated)
            await websocket.send_text(sendMsg(msg, False,authenticated, username))
        except WebSocketDisconnect:
            break
    await websocket.close()
    logger.info(f'Disconnected')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host='0.0.0.0', port=port, debug=True)