from fastapi import FastAPI, WebSocket
from fastapi.responses import Response

app = FastAPI()

@app.websocket("/ws")
async def ws(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        print(data)

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
