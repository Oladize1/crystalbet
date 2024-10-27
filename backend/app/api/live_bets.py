from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

class ConnectionManager:
    """Manage WebSocket connections."""
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept a new connection and store it."""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"New connection. Total active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove a connection when the client disconnects."""
        self.active_connections.remove(websocket)
        print(f"Client disconnected. Total active connections: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        """Send a message to all active connections."""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Failed to send message: {e}")

# Instantiate the connection manager
manager = ConnectionManager()

@router.websocket("/ws/live-bets")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for live betting data."""
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive and wait for messages
            data = await websocket.receive_text()
            # Process incoming data from clients, if necessary
            await manager.broadcast(f"Live update: {data}")
            # Optionally send an acknowledgment back to the sender
            await websocket.send_text("Message received and broadcasted.")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Unexpected error: {e}")
        await websocket.close()

