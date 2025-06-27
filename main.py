from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
import json

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "WebSocket server is running"}
clients: List[WebSocket] = []
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    username = await websocket.receive_text()  
    print(f"User {username} connected")
    clients.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()  
            message_data = json.loads(data)
            for client in clients:
                if client != websocket:  
                    await client.send_text(json.dumps(message_data))
    except WebSocketDisconnect:
        clients.remove(websocket)
        print(f"User {username} disconnected")
