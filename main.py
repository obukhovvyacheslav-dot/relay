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
      welcomeGreeting="Press any key, then say something"
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

    did_setup = False

    try:
        while True:
            msg = await ws.receive_text()
            print("IN RAW:", msg)

            try:
                data = json.loads(msg)
            except:
                continue

            t = data.get("type")

            if t == "setup" and not did_setup:
                did_setup = True

                # говоришь по-русски → распознавание по-русски
                await ws.send_text(json.dumps({
                    "type": "language",
                    "transcriptionLanguage": "ru-RU",
                    "ttsLanguage": "en-US"
                }))

                # один раз сказать "OK"
                await ws.send_text(json.dumps({
                    "type": "text",
                    "token": "OK. Say something.",
                    "last": True
                }))

            if t == "prompt":
                vp = data.get("voicePrompt")
                print("PROMPT:", vp)

                await ws.send_text(json.dumps({
                    "type": "text",
                    "token": "I heard you.",
                    "last": True
                }))

    except WebSocketDisconnect:
        pass
