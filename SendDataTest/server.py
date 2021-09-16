import socket
import _pickle as cPickle
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

#while True:
# Wait for a connection
print('waiting for a connection')
connection, client_address = sock.accept()
try:
    print('connection from', client_address)
    start = time.time()
    # Receive the data in small chunks
    fullmessage = bytearray(0)
    while True:
        receive_message = connection.recv(4056)
        if receive_message:
            fullmessage += receive_message
        else:
            break
finally:
    print('time: ', time.time() - start)
    message = cPickle.loads(fullmessage)
    print(len(message))
    print(len(message[0]))
    print(len(message[0][0]))
    # Clean up the connection
    connection.close()