 #!/usr/bin/env python



import socket

import cv2

import json

host = "localhost"

port = 50058

backlog = 5

size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)

vc=cv2.VideoCapture(0)
if vc.isOpened():

    rval, frame = vc.read()

while 1:

    client, address = s.accept()
    rval, frame = vc.read()

    #data = client.recv(size)
    if rval:
        #print "recieved data " + str(data)
        #print "sending data to %s" % str(address)

        #p=json.dumps(frame)
        client.send(frame)
    client.close()