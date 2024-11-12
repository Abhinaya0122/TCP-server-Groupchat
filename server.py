import socket
import threading
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Define the TCP server details
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000
clients = []  # Keep track of connected TCP clients

# Function to handle communication between clients via TCP
def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received message from {client_address}: {message}")
            # Broadcast the message to all other clients
            for client in clients:
                if client != client_socket:  # Do not send back to sender
                    client.send(message.encode('utf-8'))
        except:
            break

    clients.remove(client_socket)
    client_socket.close()
    print(f"Connection closed: {client_address}")

# TCP Server Thread (Runs in the background)
def start_tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"TCP Server listening on {SERVER_HOST}:{SERVER_PORT}")
    
    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Flask route for the chat UI (serves the HTML page)
@app.route('/')
def index():
    return render_template('index.html')  # Chat UI HTML page

# Flask route for sending a message (via AJAX or WebSocket)
@app.route('/send', methods=['POST'])
def send_message():
    message = request.form.get('message')
    for client in clients:
        try:
            client.send(message.encode('utf-8'))  # Send message to all clients
        except:
            continue
    return jsonify({'status': 'Message sent'})

# Run Flask and TCP server concurrently
if __name__ == '__main__':
    # Start TCP server in a background thread
    tcp_thread = threading.Thread(target=start_tcp_server)
    tcp_thread.start()

    # Start Flask server
    app.run(host='0.0.0.0', port=5001, debug=True)
