#! /usr/bin/env python3
# HTTP Server, HW4
# Name: Edel Barcenas
# UCID: eeb24,  31446886
# CS 356-008
import sys
import socket
import datetime
import time

import struct

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1];  # ip address
serverPort = int(sys.argv[2]);   # server port

# Create a UDP socket. Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort));
serverSocket.listen(5);

print(f"Server listening on port: {str(serverPort)}\n");


# loop forever listening for incoming TCP messages
while True:
    clientsocket, ip_port = serverSocket.accept()           # Receive a client socket
    print(f"Connection with {ip_port} established");
    response = "Connection to Server established\n";
    clientsocket.send(response.encode("utf-8"));

# LoopBack IP 127.0.0.1
# both client and server using TCP

