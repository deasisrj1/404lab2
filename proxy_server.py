#!/usr/bin/env python3

import socket, time, sys
from multiprocessing import Process

HOST = ""
PORT = 8001
BUFFER_SIZE = 4096

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def handle_request(addr, conn, outgoing):
    print("Connected by", addr)
    #recieve data, wait a bit, then send it back
    try:
        full_data = conn.recv(BUFFER_SIZE)
        print("Sending payload") 
        outgoing.sendall(full_data)
        outgoing.shutdown(socket.SHUT_WR)

        full_data = b""
        while True:
            data = outgoing.recv(BUFFER_SIZE)
            if not data:
                 break
            full_data += data
        outgoing.close()
        conn.sendall(full_data)
        # conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        print("Send successful")
     
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def main():
    host = 'www.google.com'
    port = 80

    # create socket, bind, and set to listening mode
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as incoming:
        # allow reused addresses
        incoming.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        incoming.bind((HOST, PORT))
        incoming.listen(2)

        while True:
            # accept incoming connections 
            conn, addr = incoming.accept()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as outgoing:
                remote_ip = get_remote_ip(host)
                outgoing.connect((remote_ip , port))
                print (f'Socket Connected to {host} on ip {remote_ip}')
                handle_request(addr, conn, outgoing)
     

if __name__ == "__main__":
    main()
