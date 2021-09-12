#! /usr/bin/env python3
# Ping Server
# Name: Edel Barcenas
# UCID: eeb24,  31446886
# CS 356-008
import sys
import socket
import random
import time
import struct

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]  # ip address "unused ports"?
serverPort = int(sys.argv[2])

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # necessary to send/receive data
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))
print("The server is ready to receive on port:  " + str(serverPort) + "\n")

# loop forever listening for incoming UDP messages
while True:
    # Receive and print the client data from "data" socket
    data, address = serverSocket.recvfrom(1024)  # 1024 upper bound of data size
    dataUnpacked = struct.unpack('>HH', data)

    print("Ping from client " + address[0] + ", " + str(address[1]) + ": " + str(dataUnpacked))

    # Artificial Time & Packet Loss
    time.sleep(random.random())
    if(random.random()>0.4):
        # Echo back to client
        data = struct.pack('>HH', 2, dataUnpacked[1])
        print("Pinging client " + address[0] + ", " + str(address[1]) + ": (2, " + str(dataUnpacked[1])+")")
        serverSocket.sendto(data, address)

# LoopBack IP 127.0.0.1
# both client and server using UDP
