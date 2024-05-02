import socket
import threading

# Server configuration
serverHost = socket.gethostbyname(socket.gethostname()) 
serverPort = 12349        
bufferSize = 1024         

# Create a UDP server socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Server hosting on IP→> {serverHost}")

#handiling error when other server use same port
try:
    serverSocket.bind((serverHost, serverPort))
except OSError as e:
    print(f"Error binding socket : {e}")
    exit(1)

print("Server Running...")


# Dictionary to keep track of connected clients by name
clients = {}

# Function to handle incoming messages and broadcast to all clients
def handle_messages():
    while True:
        # Receive data from a client
        data, client_address = serverSocket.recvfrom(bufferSize)
        message = data.decode()

        # If message is 'exit', remove the client
        if message.lower() == "exit":
            for name, address in list(clients.items()):
                if address == client_address:
                    del clients[name]
                    
                    print("A connection was forcibly closed by the remote host")
            continue

        # Extract client name and content
        if "->" in message:
            name, content = message.split("->", 1)
            name = name.strip("[]")

        # Add the client to the list of known clients if not already present
        if name not in clients:
            clients[name] = client_address
            

        # Display the received message with client IP and port
        print(f"{client_address} [{name}] -> {content}")

        # Broadcast the message to other clients
        broadcast_message(message, client_address)

# Function to broadcast messages to all clients except the sender
def broadcast_message(message, sender_address):
    sent_addresses = set()
    for name, address in clients.items():
        if address != sender_address and address not in sent_addresses:
            serverSocket.sendto(message.encode(), address)
            sent_addresses.add(address)  # Ensure each client gets the message once

# Start a new thread to handle incoming messages
threading.Thread(target=handle_messages, daemon=True).start()

# Keep the server running
while True:
    pass
