import socket
import time
import numpy as np
import main

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        start = time.time()
        # Receive the data in small chunks
        fullmessage = bytearray(0)
        while True:
            receive_message = connection.recv(4096)
            if receive_message:
                fullmessage += receive_message
            else:
                break
    finally:
        message = np.frombuffer(fullmessage, dtype=np.complex128).reshape((100, 1024, 11))
        print('time to get the data: ', time.time() - start)
        print(len(message))
        print(len(message[0]))
        print(len(message[0][0]))
        main.makeOp(message)
        # Clean up the connection
        connection.close()
