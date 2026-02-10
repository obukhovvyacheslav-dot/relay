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

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            raw = await ws.receive()

            text = raw.get("text")
            if text is None and raw.get("bytes") is not None:
                text = raw["bytes"].decode("utf-8", errors="ignore")

            if not text:
                continue

            print("IN:", text)

            try:
                msg = json.loads(text)
            except:
                continue

            t = msg.get("type")

            if t == "setup":
                out = {"type": "text", "token": "OK. Say something.", "last": True}
                await ws.send_text(json.dumps(out))
                print("OUT:", out)

            if t == "prompt":
                # просто подтверждение, чтобы проверить TTS
                out1 = {"type": "text", "token": "I heard you.", "last": True}
                await ws.send_text(json.dumps(out1))
                print("OUT:", out1)

    except WebSocketDisconnect:
        pass
