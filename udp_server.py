import socket
import cv2
import pickle
import time
import threading
from _thread import *
import base64

HEADERSIZE = 4

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "localhost"
port = 49000

try:
    s.bind((ip, port))
    print("[+] Server started on " + ip)
except socket.error as e:
    print("[-] Couldn't start server on " + ip)
connected_clients = set()
video_frames = []
cap = cv2.VideoCapture('video.mp4')


def init_video():
    print("[+] Server is loading the video, please wait...")
    # Read until video is completed 
    for i in range(0, 4096):
        if not cap.isOpened():
            print("Error loading the file.")
            break
        else:
            ret, frame = cap.read()
            if ret:
                ret, buffer = cv2.imencode('.jpg', frame)
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
                # encoded_frame = base64.b64encode(buffer)
                # data = f"{i:04d}"+str(encoded_frame)
                data = cv2.imencode('.jpg', frame, encode_param)[1].tostring()
                video_frames.append(data)

    # When everything done, release  
    # the video capture object 
    cap.release()
    print("[+] Video is loaded, server ready to stream...")
    main()


def client_thread(address):
    try:
        for x in video_frames:
            s.sendto(pickle.dumps(x), address)
            time.sleep(0.016)
        connected_clients.remove(address)
    except Exception as e:
        print(e)


"""
def client_thread(address):
    try:
        for i in range(0,2048):
            if not cap.isOpened():
                print("Error loading the file.")
                break
            else:
                ret, frame = cap.read()
                if ret:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
                    #encoded_frame = base64.b64encode(buffer)
                    #data = f"{i:04d}"+str(encoded_frame)
                    data = cv2.imencode('.jpg', frame, encode_param)[1].tostring()
                    s.sendto(pickle.dumps(data), address)
    except Exception as e:
        print(e)

"""


def main():
    while True:
        data, client = s.recvfrom(2 ** 16)
        if not client in connected_clients:
            print("[+] Now streaming to " + str(client[0]))
            connected_clients.add(client)
            t = threading.Thread(
                target=client_thread,
                args=(client,)

            )
            t.start()


init_video()
