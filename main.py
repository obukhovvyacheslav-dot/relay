from fastapi import FastAPI, WebSocket
import json

app = FastAPI()

@app.websocket("/ws")
async def ws(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        print(data)

@app.post("/voice")
async def voice():
    return """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <ConversationRelay
      url="wss://relay-ug27.onrender.com/ws"
      welcomeGreeting="Say something"
    />
  </Connect>
</Response>"""
