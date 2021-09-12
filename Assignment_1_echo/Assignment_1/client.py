#! /usr/bin/env python3
# Echo Client
# Name: Edel Barcenas
# UCID: eeb24,  31446886
# CS 356-008
import sys
import socket

# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]  # ip address
port = int(sys.argv[2])
count = int(sys.argv[3])
data = 'X' * count  # Initialize data to be sent
attempts = 0
# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# throws TimeoutError after one second
clientsocket.settimeout(1)

while attempts < 3:
    # Send data to server
    print("Sending data to   " + host + ", " + str(port) + ": " + data)
    clientsocket.sendto(data.encode(), (host, port))
    try:
        # Receive the server response
        dataEcho, address = clientsocket.recvfrom(count)
        print("Received data from " + address[0] + ", " + str(address[1]) + ": " + dataEcho.decode())
        break
    except:
        print("Error connecting to server \nretrying...")
        attempts += 1
if attempts == 3:
    print("Could not connect to server \nPlease try again later\n")

# Close the client socket
clientsocket.close()
