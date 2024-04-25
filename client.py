import socket
import threading

# Server configuration
serverName = 'localhost'  # Use the same as server's host
serverPort = 12349        # Use the same as server's port
bufferSize = 1024         # Buffer size for data transmission

# Initialize the UDP client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Client connection details
clientAddress = ('localhost', 0)  # Use a random port for the client
clientSocket.bind(clientAddress)

# Get the client's name and send it to the server to register
client_name = input("Please write your name here: ")
registration_message = f"Client->{client_name}"
clientSocket.sendto(registration_message.encode(), (serverName, serverPort))

print(f"Client IP->{clientAddress[0]} Port->{clientAddress[1]}")

# Function to listen for incoming messages from the server
def receive_messages():
    while True:
        try:
            data, _ = clientSocket.recvfrom(bufferSize)
            print(data.decode())
        except Exception as e:
            print("Error receiving message:", e)
            break

# Start a separate thread to receive messages
threading.Thread(target=receive_messages, daemon=True).start()

# Allow the user to send messages
while True:
    message = input()
    if message.lower() == "exit":
        exitMsg = "exit"
        clientSocket.sendto(exitMsg.encode(), (serverName, serverPort))
        break
    send_message = f"[{client_name}]->{message}"
    clientSocket.sendto(send_message.encode(), (serverName, serverPort))

clientSocket.close()
