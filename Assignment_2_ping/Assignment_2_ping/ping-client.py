#! /usr/bin/env python3
# Ping Client
# Name: Edel Barcenas
# UCID: eeb24,  31446886
# CS 356-008
import sys
import socket
import time
import struct

# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]  # ip address
port = int(sys.argv[2])

# Creates UDP client socket. AF_INET: Address from Internet, SOCK_DGRAM: UDP
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# throws TimeoutError after one second
clientsocket.settimeout(1)

sequenceNum = 1
# Packets sent, received, lost
ps, pr, pl = 0, 0, 0
totalTime, minPing, maxPing = 0.0, 10.0, 0.0

while sequenceNum < 11:
    # increment packets sent
    ps += 1
    # encode/pack message
    # h: short int signed, 1: outgoing message
    outgoing = struct.pack('>HH', 1, sequenceNum)

    print("IP " + host + " Port " + str(port), end='')

    # start round trip timer
    timer = time.time()

    # Send data to server
    clientsocket.sendto(outgoing, (host, port))

    try:
        # Receive the server response
        dataEcho, address = clientsocket.recvfrom(1024)
        dataUnpacked = struct.unpack('>HH', dataEcho)

        # end round trip timer
        timer = time.time() - timer
        # update timing records & packets received
        totalTime += timer
        pr += 1
        if timer < minPing:
            minPing = timer
        if timer > maxPing:
            maxPing = timer

        print(" Ping " + str(timer), " Sequence Num: " + str(dataUnpacked[1]))

    except:
        # increment packets lost
        pl += 1
        print(" TIMED OUT   Sequence Num: " + str(sequenceNum))

    sequenceNum += 1

# final print statement
print("\nPackets Sent: "+str(ps)+
      "\nPackets Recieved: "+str(pr)+
      "\nPackets Lost: "+str(pl)+
      "\nLoss Rate: "+str(float(pl)/ps*100)+"%"
      "\nMin Ping: "+str(minPing)+
      "\nMax Ping: "+str(maxPing)+
      "\nAvg Ping: "+str(totalTime/(pr)))

# Close the client socket
clientsocket.close()
