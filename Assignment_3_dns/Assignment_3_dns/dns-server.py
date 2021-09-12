#! /usr/bin/env python3
# DNS Server
# Name: Edel Barcenas
# UCID: eeb24,  31446886
# CS 356-008
import sys
import socket
import struct

# establishes hostname database in dictionary format ("'hostname' A IN" : "port_number IP_Address")
f  = open("dns-master.txt", "r")
hostDict = {}
for line in f:
    if line[0] == "#" or line.isspace():
        continue
    hostDict[line[0:line.index(" IN ")+3]] = line[line.index(" IN ")+4:len(line)-1]

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]  # ip address
serverPort = int(sys.argv[2])   # server port

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # necessary to send/receive data

# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))
print("The server is ready to receive on port:  " + str(serverPort) + "\n")

# loop forever listening for incoming UDP messages
while True:
    # Receive and print the client data from "data" socket
    data, address = serverSocket.recvfrom(1024)  # 1024 upper bound of data size

    # (format string, msg type, ret code, msg id, Question len, Answer len, "Question")
    qLen = struct.unpack('>H', data[8:10])[0]            # find incoming question length
    formatIn = '>HHIHH' + str(qLen) + "s"        # applies question string length to format
    dataUnpacked = struct.unpack(formatIn, data)

    q = dataUnpacked[5].decode('utf-8')    # question

    a = ""                      # answer

    #Check if host is in database
    if q in hostDict:
        a = q + " " + hostDict[q]   # answer = key/Question + keyValue/answer
        retCode = 0                 # 0 means Name Found
    else:
        retCode = 1                 # 1 means Name Not Found

    aLen = len(a)    # answer len

    # Respond to client
    # prepare Format String
    formatOut = '>HHIHH'+str(qLen)+"s"+str(aLen)+"s"
    # (msg type, ret code, msg id, question len, answer len, "question", "answer")
    data = struct.pack(formatOut, 2, retCode, dataUnpacked[2], qLen, aLen, bytes(q, 'utf-8'), bytes(a, 'utf-8'))
    serverSocket.sendto(data, address)

# LoopBack IP 127.0.0.1
# both client and server using UDP

