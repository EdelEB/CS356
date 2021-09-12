#! /usr/bin/env python3
# HTTP Client, HW4
# Name: Edel Barcenas
# UCID: eeb24,  31446886
# CS 356-008
import sys
import socket
from datetime import datetime
import os

# Parses URL from command line argument into "hostName", "port", "fileName
input = sys.argv[1];

# Creates TCP client socket. AF_INET: Address from Internet, SOCK_STREAM: TCP
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
clientsocket.connect(('127.0.0.1', 12000));

response = clientsocket.recv(1024).decode("utf-8");

print(response);

clientsocket.sendto(input.encode("utf-8"), ('127.0.0.1', 12000));

# Close the client socket
clientsocket.close()
