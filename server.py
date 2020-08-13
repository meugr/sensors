"""
Simple TCP listener
"""

import socket

host = "192.168.1.100"
port = 5000
print('Start listener')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()
print(f'Listen {host}:{port}')
while 1:
    print('Waiting connect...')
    conn, client_addr = s.accept()
    print(f'Start connect with {client_addr[0]}:{client_addr[1]}')
    incom_msg = conn.recv(1024).decode().rstrip('\n')
    print(f'INCOME: {incom_msg}')
    conn.close()
