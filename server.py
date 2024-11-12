import asyncio
import websockets

clients = set()

# Broadcast message to all connected clients
async def broadcast(message):
    for client in clients:
        await client.send(message)

# Handle individual client connections
async def handle_client(websocket, path):
    clients.add(websocket)
    try:
        # Send a welcome message to the new client
        await websocket.send("Welcome to the WebSocket server!")
        
        # Listen for incoming messages from the client
        async for message in websocket:
            # Broadcast received message to all clients
            await broadcast(message)
    except:
        pass
    finally:
        # Remove client when disconnected
        clients.remove(websocket)

# Start the WebSocket server on port 5000
async def main():
    server = await websockets.serve(handle_client, '0.0.0.0', 5000)
    print("Server is listening on ws://0.0.0.0:5000")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
