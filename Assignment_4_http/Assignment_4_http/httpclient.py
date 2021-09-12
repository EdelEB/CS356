#! /usr/bin/env python3
# HTTP Client, HW4
# Name: Edel Barcenas
# UCID: eeb24,  31446886
# CS 356-008

# Dear Professor: I know this is spaghetti code and for that I apologize. I struggled with this assignment and was running out of time. I tried to organize it as best as I could. -Edel :)

import os
import sys
import socket
import datetime

########################## START:_Helper_Functions ######################################################################################

def getTime():
    now = datetime.now();
    dateString = now.strftime("%a, %d %b %Y %H:%M:%S %Z");
    return dateString;

def formatRequest(hostName, port, fileName, date):
    request = "GET /" + fileName + " HTTP/1.1\\r\\n" \
            "Host: " + hostName + ":" + port + "\\r\\n";
    if(date != ""):
        request = request + "If-Modified-Since: " + date + "\\r\\n";
    request = request + "\\r\\n";
    return request;

def isCached():
    cached = False;
    if (not os.path.exists("cache.txt")):   # if cache.txt does not exist
        cache = open("cache.txt", 'w');     # creates "cache.txt" file to write into
        cache.write("# Cache Format: '%'+URL+'%%'+DateLastModified+'%%%'+FileData+%%%%\n");
    else:
        cache = open("cache.txt", 'r')      # open "cache.txt" for reading and writing
        for line in cache:
            if ('%' + url + '%%' in line):
                cached = True;
                break;
    cache.close();
    return cached;

###################### END:_Helper_Functions #########################################################################


########## START:_Command-line_URL--->"hostName","port","fileName ####################################################

url = sys.argv[1];                          # URL command line input, ex: www.example.com:12000/subHeader/filename.html
url_split = url.split("/")                  # --> ['www.example.com:12000', 'subHeader', 'filename.html']

if (':' in url_split[0]):                   # ':' in "www.example.com:12000" ?
    tempArr = url_split[0].split(':');      # --> ["www.example.com" , "12000"]
    hostName = tempArr[0];                      # ex: www.example.com
    port = tempArr[1];                      # port number ex: 12000
else:                                       # if no port specified
    port = 40;                              # default: HTTP 40 , HTTPS 443
    hostName = url_split[0];

fileName = url_split[1];                    # ex: subHeader/fileName.html
for i in range(2, len(url_split)):          # absolute path to filename
    fileName += '/' + url_split[i];

########## END:_Command-line_URL--->"hostName","port","fileName ####################################################

# prepare message

cacheMod = "";                                                              # last modified date of cached file

if isCached():
    cache = open("cache.txt", "r");
    tempCache = open("tempCache.txt", "w");
    for line in cache:
        if(f"%{url}%%" in line):
            cacheMod = line.split("%%")[1];                                 # last modified date of cached file
            cacheData = line.split("%%%")[1];                                   # data already in cached file
            for line2 in cache:
                if("%%%%" in line2):
                    cacheData = cacheData+line2;
                    break;
        else:                                                                   # tempCache is used to delete the the line from the old cache
            tempCache.write(line);
    cache.close();
    tempCache.close();

    cache = open("cache.txt", "w");
    tempCache = open("tempCache.txt", "r");
    for line in tempCache:
        cache.write(line);
    cache.close();
    tempCache.close();

# Creates TCP client socket. AF_INET: Address from Internet, SOCK_STREAM: TCP
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
clientsocket.connect(('127.0.0.1', 12000));
# Waits to recieve connection confirmation
response = clientsocket.recv(1024).decode("utf-8");
print(response);

request = formatRequest(hostName, port, fileName, cacheMod);
print(request.replace("\\r\\n", "\\r\\n\n"));
clientsocket.sendto(request.encode("utf-8"), ('127.0.0.1', 12000));

response = clientsocket.recv(8000).decode("utf-8");
print(response.replace("\\r\\n", "\\r\\n\n"));

cache = open("cache.txt", "a");
resArr = response.split("\\r\\n");
if("200" in resArr[0]):
    cacheData = resArr[len(resArr) - 1]
    cacheMod = response.split("Last-Modified: ")[1].split("\\r\\n")[0];
    cache.write(f"%{url}%%{cacheMod}%%%{cacheData}%%%%\n")
elif("304" in resArr[0]):
    cache.write(f"%{url}%%{cacheMod}%%%{cacheData}%%%%\n")
cache.close()

# Close the client socket
clientsocket.close()