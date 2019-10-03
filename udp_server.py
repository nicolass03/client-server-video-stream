import socket
import cv2
import pickle
import time
import base64

HEADERSIZE = 4

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "localhost"
port = 49000

try:
    s.bind((ip,port))
    print("[+] Server started on "+ip)
except socket.error as e:
    print("[-] Couldn't start server on "+ip)
connected_clients = set()
cap = cv2.VideoCapture('video.mp4')

def client_thread(address):
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

def main():
    while True:
        data,client = s.recvfrom(2**16)
        if not client in connected_clients:
            print("[+] Now streaming to {client}")
            connected_clients.add(client)
            client_thread(client)

main()
