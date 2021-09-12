#! /usr/bin/env python3
# DNS Client
# Name: Edel Barcenas
# UCID: eeb24,  31446886
# CS 356-008
import sys
import socket
import struct
import random

msgID = int(random.random()*100)
attempts = 0

# Get the server host IP address, port, and hostname of Question Target as command line arguments
hostIP= sys.argv[1]  # ip address
port = int(sys.argv[2]) # port number
hostname = str(sys.argv[3]) # ex: host1.student.test

# Creates UDP client socket. AF_INET: Address from Internet, SOCK_DGRAM: UDP
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# throws TimeoutError after one second
clientsocket.settimeout(1)

# prepare outgoing data
qOut = hostname + " A IN"                               # question outgoing
qOutLen = len(qOut)                                     # outgoing question length
formatString = '>HHIHH'+str(qOutLen)+'s'                # struct format string
# (format, msg type, ret code, msg id, Question len, Answer len, "Question")
outgoing = struct.pack(formatString, 1, 0, msgID, qOutLen, 0, bytes(qOut, 'utf-8'))

print("Sending Request to " + hostIP + " " + str(port) +
        ": \nMessage ID: " + str(msgID) +
        "\nQustion Length: " + str(qOutLen) + " bytes"
        "\nAnswer Length: 0 bytes"
        "\nQuestion: " + qOut + '\n')

while attempts < 3:
    # Send data to server
    clientsocket.sendto(outgoing, (hostIP, port))

    try:
        # Receive the server response
        dataRec, address = clientsocket.recvfrom(1024)
        # (msg type, ret code, msg id, question len, answer len, "question", "answer")
        lengthsUnpacked = struct.unpack('>HH', dataRec[8:12])       # retrieves lengths of q and a for formatIn string
        formatIn = '>HHIHH'+str(lengthsUnpacked[0])+"s"+str(lengthsUnpacked[1])+"s"
        dataUnpacked = struct.unpack(formatIn, dataRec)
        break
    except:
        # No message received
        print("Request Timed Out...")
        print("Resending Request to " + hostIP + " " + str(port))
        attempts += 1
if attempts == 3:
    print("Requests Failed, Exiting Program")
elif dataUnpacked[1] == 1 :
    print("Received Response From " + hostIP + " " + str(port) +
            ":\nMessage ID: " + str(dataUnpacked[2]) +
            "\nReturn Code: 1 (Name Does Not Exist)"
            "\nQuestion Length: " + str(dataUnpacked[3]) + " bytes"
            "\nAnswer Length: " + str(dataUnpacked[4]) +
            "\nQuestion: " + dataUnpacked[5].decode('utf-8'))
else:
    print("Received Response From " + hostIP + " " + str(port) +
            ":\nMessage ID: " + str(dataUnpacked[2]) +
            "\nReturn Code: 0 (No Errors)"
            "\nQuestion Length: " + str(dataUnpacked[3]) + " bytes"
            "\nAnswer Length: " + str(dataUnpacked[4]) +
            "\nQuestion: " + dataUnpacked[5].decode('utf-8') +
            "\nAnswer: " + dataUnpacked[6].decode('utf-8'))

# Close the client socket
clientsocket.close()
