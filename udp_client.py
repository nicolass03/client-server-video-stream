import socket
import time
import cv2
import numpy as np
import base64
import pickle

HEADERSIZE = 4

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "localhost"
port = 49000

def start_video():
    #cv2.startWindowThread()
    try:
        while True:
            data, client = s.recvfrom(2**16)
            print(data)
            nparr = np.frombuffer(pickle.loads(data), np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            #encoded_frame = data[HEADERSIZE:]
            #encoded_frame = data[1]
            #frame = base64.b64decode(encoded_frame)
            cv2.imshow('Ad', frame)
            cv2.waitKey(1)
    except Exception as e:
        print(e)

    cv2.destroyAllWindows()
    s.close()

def main():
    s.sendto(bytes("connect", "utf-8"),(ip,port))
    print(f'[+] Connected to server...')
    start_video()

main()
