#! /usr/bin/env python3
# TCP Echo Server

import sys
import socket

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
dataLen = 1000000
# Create a TCP "welcoming" socket. Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Assign IP address and port number to socket
serverSocket.bind((serverIP, serverPort))
# Listen for incoming connection requests
serverSocket.listen(1)

print('The server is ready to receive on port:  ' + str(serverPort) + '\n')

# loop forever listening for incoming connection requests on "welcoming" socket
while True:
    # Accept incoming connection requests; allocate a new socket for data communication
    connectionSocket, address = serverSocket.accept()
    print("Socket created for client " + address[0] + ", " + str(address[1]))

    # Receive and print the client data in bytes from "data" socket
    data = connectionSocket.recv(dataLen).decode()
    print("Data from client: " + data)

    # Echo back to client
    connectionSocket.send(data.encode())

        
