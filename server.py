# import threading
# import socket

# host = '127.0.0.1' 
# port = 5000

# server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# server.bind((host,port))
# server.listen()

# clients =[]
# nicknames =[]

# def broadcast(message):
#     for client in clients:
#         client.send(message)

# def handle(client):
#     while True:
#         try:
#             message = client.recv(1024)
#             broadcast(message)
#         except:
#             index = client.index(client)
#             clients.remove(client)
#             client.close()
#             nickname = nickname[index]
#             broadcast('{} left!'.format(nickname).encode('ascii'))
#             nicknames.remove(nickname)
#             break

# def receive():
#     while True:
#         client, address = server.accept()
#         print("Connected with {}".format(str(address)))

#         client.send('ABHI'.encode('ascii'))
#         nickname = client.recv(1024).decode('ascii')
#         nicknames.append(nickname)
#         clients.append(client)

        
#         print("Nickname is {}".format(nickname))
#         broadcast("{} joined!".format(nickname).encode('ascii'))
#         client.send('Connected to server!'.encode('ascii'))

#         thread = threading.Thread(target=handle, args=(client,))
#         thread.start()
# print('server is listening....')
# receive()
import socket

host = '0.0.0.0'
port = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((host, port))

clients = []

print("Server is listening...")

while True:
    try:
        # Receive message and client address
        message, client_address = server.recvfrom(1024)

        # Add new clients to the list
        if client_address not in clients:
            clients.append(client_address)
            print(f"New client added: {client_address}")

        # Broadcast the message to all clients except the sender
        print(f"Received message from {client_address}: {message.decode('ascii')}")
        for client in clients:
            if client != client_address:
                server.sendto(message, client)
    except Exception as e:
        print(f"An error occurred: {e}")
        break

server.close()
