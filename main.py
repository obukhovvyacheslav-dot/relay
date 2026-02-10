from fastapi import FastAPI, WebSocket
from fastapi.responses import Response
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            msg = await ws.receive_text()
            print(msg)
    except WebSocketDisconnect:
        pass

def twiml():
    return """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <ConversationRelay
      url="wss://relay-ug27.onrender.com/ws"
      welcomeGreeting="Say something"
    />
  </Connect>
</Response>"""

@app.post("/voice")
async def voice_post():
    return Response(content=twiml(), media_type="application/xml")

@app.get("/voice")
async def voice_get():
    return Response(content=twiml(), media_type="application/xml")
