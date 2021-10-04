import socket
import time
import numpy as np
import main

operationController = main.Main()
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
                if(fullmessage[-3:] == b'end'):
                    fullmessage = fullmessage[:-3]
                    break
                else:
                    fullmessage = bytearray(0)
                    raise Exception
    except:
        print("error: conection lost")
        connection.close()
        break
    else:
        header = fullmessage[:32].decode("utf-8").split(';')
        message = np.frombuffer(fullmessage[32:], dtype=eval(header[0])).reshape(eval(header[1]))
        print('time to get the data: ', time.time() - start)
        operationController.makeOp(message)
        # Clean up the connection
        connection.close()
operationController.close()
