#!/usr/bin/env python

"""
A simple echo client
"""

import socket
import cv2
import json

host = '169.254.132.51'
port = 50058
size = 1024000000
cv2.namedWindow("preview")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
while True:

    data = s.recv()
    #frame=json.loads(data)


    cv2.imshow("preview", data)

s.close()