"""WebSocket - WebSocket handling for real-time communication."""

from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
import json


class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_rooms: Dict[str, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str) -> None:
        """Connect a new WebSocket client."""
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    def disconnect(self, client_id: str) -> None:
        """Disconnect a WebSocket client."""
        self.active_connections.pop(client_id, None)
        
        for room_id, clients in self.user_rooms.items():
            clients.discard(client_id)
    
    async def send_personal_message(self, message: str, client_id: str) -> None:
        """Send message to specific client."""
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)
    
    async def broadcast(self, message: str) -> None:
        """Broadcast message to all connected clients."""
        for connection in self.active_connections.values():
            await connection.send_text(message)
    
    async def broadcast_json(self, data: dict) -> None:
        """Broadcast JSON data to all clients."""
        await self.broadcast(json.dumps(data))
    
    def join_room(self, client_id: str, room_id: str) -> None:
        """Add client to a room."""
        if room_id not in self.user_rooms:
            self.user_rooms[room_id] = set()
        self.user_rooms[room_id].add(client_id)
    
    def leave_room(self, client_id: str, room_id: str) -> None:
        """Remove client from a room."""
        if room_id in self.user_rooms:
            self.user_rooms[room_id].discard(client_id)
    
    async def send_to_room(self, message: str, room_id: str) -> None:
        """Send message to all clients in a room."""
        if room_id in self.user_rooms:
            for client_id in self.user_rooms[room_id]:
                await self.send_personal_message(message, client_id)


manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint handler."""
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast_json({
                "type": "message",
                "client_id": client_id,
                "data": data
            })
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast_json({
            "type": "disconnect",
            "client_id": client_id
        })