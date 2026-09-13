import asyncio
from queue import Queue
import threading
import websockets
import json

from websockets.asyncio.server import ServerConnection

from events import Event

class WebsocketServer:
    def __init__(self, host="0.0.0.0", port=8765):
        self.host = host
        self.port = port
        self.loop = None
        self.thread = None
        self.server = None
        self.events: Queue[Event] = Queue()
        self.handlers = {"test": self.test_handler, "event": self.event_handler}

    async def test_handler(self, message: dict, websocket: ServerConnection):
        print("handling test")

    async def event_handler(self, message: dict, websocket: ServerConnection):
        event_type = message["event_type"]
        if event_type not in Event._member_names_:
            await websocket.send(json.dumps({"type": "error", "error": "json not valid"}))
        self.events.put(Event[event_type])

    async def handler(self, websocket: ServerConnection):
        async for message in websocket:
            json_parsed = None
            try:
                json_parsed = json.loads(message)
            except json.JSONDecodeError:
                await websocket.send(json.dumps({"type": "error", "error": "json not valid"}))
                continue

            if "type" not in json_parsed:
                await websocket.send(json.dumps({"type": "error", "error": "type not found in message"}))
                continue

            type = json_parsed["type"]
            if type not in self.handlers.keys():
                await websocket.send(json.dumps({"type": "error", "error": f"cannot recognise type {type}"}))
                continue

            handler = self.handlers[type]
            await handler(json_parsed, websocket)
            await websocket.send(type)

    async def _run(self):
        self.loop = asyncio.get_running_loop()

        self.server = await websockets.serve(
            self.handler,
            self.host,
            self.port
        )

        await self.server.wait_closed()


    def _thread_main(self):
        asyncio.run(self._run())

    def start(self):
        self.thread = threading.Thread(
            target=self._thread_main,
            daemon=True
        )

        self.thread.start()

    def stop(self):
        if self.loop and self.server:
            self.loop.call_soon_threadsafe(self.server.close)

        if self.thread:
            self.thread.join()
