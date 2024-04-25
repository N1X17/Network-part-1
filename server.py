import socket
import threading
import time

# Server configuration
serverHost = 'localhost'  # Set the server's IP address
serverPort = 12349           # Port number for the server
bufferSize = 1024             # Buffer size for receiving data

# Create a UDP server socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((serverHost, serverPort))

print(f"Server hosting on IP→> {serverHost}")
print("Server Running...")

# Dictionary to keep track of connected clients by name
clients = {}

# Function to handle incoming messages and broadcast to all clients
def handle_messages():
    while True:
        # Receive data from a client
        data, client_address = serverSocket.recvfrom(bufferSize)
        message = data.decode()
        
        if message.lower() == "exit":
            print("Connection cloesd")
            break

        # Extract client name and content
        if "->" in message:
            name, content = message.split("->", 1)
            name = name.strip("[]")

        # Display the received message with client IP and port
        print(f"{client_address} [{name}]->{content}")

        # Add the client to the list of known clients if not already present
        if name not in clients:
            clients[name] = client_address
            # Announce new client connection to others
            join_message = f"{name} has joined the chat!"
            broadcast_message(join_message, client_address)

        # Broadcast the message to other clients
        broadcast_message(message, client_address)
        
    

# Function to broadcast messages to all clients except the sender
def broadcast_message(message, sender_address):
    for address in clients.values():
        if address != sender_address:
            serverSocket.sendto(message.encode(), address)

# Start a new thread to handle incoming messages
threading.Thread(target=handle_messages, daemon=True).start()

# Keep the server running
while True:
    pass
