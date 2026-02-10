from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def ws(ws: WebSocket):
    await ws.accept()
    while True:
        await ws.receive_text()

@app.get("/voice")
def voice():
    return """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <ConversationRelay url="wss://relay-ug27.onrender.com/ws" />
  </Connect>

</Response>"""
