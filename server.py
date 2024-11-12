import socket
import threading
import os

# Get port from environment variable (if available), fallback to 5000
port = int(os.environ.get("PORT", 5000))  # Dynamically get port
host = '0.0.0.0'  # Accept connections from all IPs
port = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)  # Listen for up to 5 clients

clients = []

# Broadcast message to all clients except the sender
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

# Handle individual client connections
def handle(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket)
        except:
            break

    clients.remove(client_socket)
    client_socket.close()

# Main server loop to accept new clients
def receive():
    while True:
        client_socket, address = server.accept()
        print(f"New connection: {address}")
        clients.append(client_socket)
        threading.Thread(target=handle, args=(client_socket,)).start()

# Start the server
print("Server is listening...")
receive()
