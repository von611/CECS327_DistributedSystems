import socket
import sys
import threading
import time
import random
import os

#local address of computer
HOST = '192.168.1.179'
#random port
PORT = 3333
#create tuple for connect
address = (HOST, PORT)

#file to transfer to client(s)
filename = ""

peers = ['192.168.1.192']

files = []

directory = os.getcwd()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(address)
s.listen(5)

def main():
    while True:
        sync = threading.Thread(target=filesync)
        sync.daemon = True
        sync.start()
        make_request()
        
        #s.shutdown(2)
        print("shutdown...")
        #s.close()
        print("close...")

def filesync():   
    while True:

        #accept connection from client
        clientsocket, address = s.accept()
        #print(f"[{address}] has connected.")

        peers.append(address)

        for filename in os.listdir(directory):
            if filename.endswith(".png"):
                files.append(filename)
                
                #open file to send as binary
                file = open(filename, 'rb')
                filedata = file.read(1024)

                #send file
                while True:
                    clientsocket.sendall(filedata)
                    filedata = file.read(1024)
                    if not filedata:
                        break
                print("File sent: " + str(filename))
                continue
        else:
            continue

    file.close()
    #close and end

def make_request():
    #connect to socket using address
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    counter = 0    

    for peer in peers:
        counter = counter + 1
        filename = str(counter) + ".png"
                    
        s.connect((peer,PORT))
        file = open(filename, 'wb')
                    
        msg = s.recv(1024)
        file.write(msg)
        while True:
            msg = s.recv(1024)
            file.write(msg)
                        
            if not msg:
                file.close()
                break
                    
if __name__ == "__main__":
    main()
