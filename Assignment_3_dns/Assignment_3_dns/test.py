
import sys
import struct
import random

q = "Hello World"
x =  bytes(q, 'utf-8')

print(x)

p = struct.pack('>12s', x)

print(p)

u = struct.unpack('>12s', p)

print(u)
print(u[0])
print(str(u[0]))
print(u[0].decode('utf-8'))


"""
# Get the server host IP address, port, and hostname of Question Target as command line arguments
hostIP= sys.argv[1]  # ip address
port = int(sys.argv[2]) # port number
hostname = str(sys.argv[3]) # ex: host1.student.test

# prepare outgoing data
qOut = hostname + " A IN"                               # question outgoing
qOutLen = len(qOut)                                     # outgoing question length
formatString = '>HHIHH'+str(qOutLen)+'s'                # struct format string
# (format, msg type, ret code, msg id, Question len, Answer len, "Question")
outgoing = struct.pack(formatString, 1, 0, 4294967295, qOutLen, 0, bytes(qOut, 'utf-8'))

x = outgoing[8:10]
y = struct.unpack(">H", outgoing[8:10])
#z = outgoing[1:3]

print(x)
print(y[0])
#print(z)
"""