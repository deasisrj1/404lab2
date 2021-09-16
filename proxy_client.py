#!/usr/bin/env python3

import socket

HOST = "localhost"
PORT = 8001
BUFFER_SIZE = 4096

payload = "GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n"

def connect(addr):
    try:
        # create socket, connect, send & recieve, then shutdown
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        s.sendall(payload.encode())
        s.shutdown(socket.SHUT_WR)
        
        full_data = b""
        while True:
            data = s.recv(BUFFER_SIZE)
            if not data:
                 break
            full_data += data
        print(full_data)
        # full_data = s.recv(BUFFER_SIZE)
        # print(full_data)

    except Exception as e:
        print(e)
    finally:
        # remember to close
        s.close()

def main():

    address = (HOST, PORT)
    # establish 10 different connections
    connect(address)

if __name__ == "__main__":
    main()