from fastapi import FastAPI, WebSocket
from fastapi.responses import Response
from starlette.websockets import WebSocketDisconnect
import json

app = FastAPI()

def twiml():
    return """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <ConversationRelay
      url="wss://relay-ug27.onrender.com/ws"
      welcomeGreeting="Press any key, then speak"
    />
  </Connect>
</Response>"""

@app.post("/voice")
async def voice_post():
    return Response(content=twiml(), media_type="application/xml")

@app.get("/voice")
async def voice_get():
    return Response(content=twiml(), media_type="application/xml")

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            raw = await ws.receive()
            print("RAW EVENT:", raw)

            text = raw.get("text")
            if text is None and raw.get("bytes") is not None:
                text = raw["bytes"].decode("utf-8", errors="ignore")

            if text:
                print("TEXT EVENT:", text)

                # попробуем распарсить
                try:
                    data = json.loads(text)
                    print("JSON TYPE:", data.get("type"))
                except:
                    pass

    except WebSocketDisconnect:
        print("WS DISCONNECT")
