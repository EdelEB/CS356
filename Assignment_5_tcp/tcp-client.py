#! /usr/bin/env python3
# TCP Echo Client

import sys
import socket

# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
count = int(sys.argv[3])
data = 'X' * count # Initialize data to be sent

# Create TCP client socket. Note the use of SOCK_STREAM for TCP packet
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create TCP connection to server
print("Connecting to " + host + ", " + str(port))
clientSocket.connect((host, port))

# Send encoded data through TCP connection
print("Sending data to server:   " + data)
clientSocket.send(data.encode())

# Receive the server response
dataEcho = clientSocket.recv(count)  
# Display the decoded server response as an output
print("Receive data from server: " + dataEcho.decode())       

# Close the client socket
clientSocket.close()
 




