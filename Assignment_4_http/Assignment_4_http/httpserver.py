#! /usr/bin/env python3
# HTTP Server, HW4
# Name: Edel Barcenas
# UCID: eeb24,  31446886
# CS 356-008

# Dear Professor: I know this is spaghetti code and for that I apologize. I struggled with this assignment and was running out of time. I tried to organize it as best as I could. -Edel :)

import sys
import socket
import datetime
import os.path
import time

########################## START:_Helper_Functions ######################################################################################

def getLastMod(filename):
    secs = os.path.getmtime(filename);
    t = time.gmtime(secs);
    lastMod = time.strftime("%a, %d %b %Y %H:%M:%S GMT", t);
    return lastMod;

def getTime():
    now = datetime.datetime.now();
    dateString = now.strftime("%a, %d %b %Y %H:%M:%S %Z");
    return dateString;

def formatResponse(code, content, lastMod):
    if(code == 200):
        code = "200 OK";
        string = "Last-Modified: " + lastMod + "\\r\\n" \
                "Content-Length: " + str(len(content)) + "\\r\\n" \
                "Content-Type: text/html; charset=UTF-8\\r\\n" \
                "\\r\\n" + content;
    elif (code == 304):
        code = "304 Not Modified";
        string = "\\r\\n";
    elif(code == 404):
        code = "404 Not Modified";
        string = "Content-Length: 0\\r\\n"\
                    "\\r\\n"
    string = "HTTP/1.1 "+code+"\\r\\n" \
                "Date: "+getTime()+"\\r\\n"\
                + string;
    return string;

###################### END:_Helper_Functions #####################################################################################

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1];             # ip address
serverPort = int(sys.argv[2]);      # server port

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

    request = clientsocket.recv(8000).decode("utf-8");

    requestArr = request.split("\\r\\n");
    requestMod = "";
    filename = "";

    for line in requestArr:
        if("GET" in line):
            filename = "."+line.split(" ")[1];
        elif("If-Modified-Since: " in line):
            requestMod = line.split("If-Modified-Since: ")[1];

    fileMod = "";
    fileData = "";

    if(os.path.exists(filename)):
        fileMod = getLastMod(filename);
        if(fileMod == requestMod):
            code = 304;
        else:
            code = 200;
            file = open(filename);
            for line in file:
                fileData = fileData+line;
            file.close();
    else:
        code = 404;

    response = formatResponse(code, fileData, fileMod);
    clientsocket.send(response.encode("utf-8"));


