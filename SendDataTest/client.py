import socket
import csv
import numpy as np

# Declaración de matriz que contiene todas las iteraciones
h = []

ChannelRealizationFileName = "./ChannelRealizations/realizationArray"
for i in range(0, 100):
    fileRoute = ChannelRealizationFileName + str(i+1) + ".csv"
    with open(fileRoute) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        temph = []
        for row in csv_reader:
            temprow = []
            for column in row:
                column = column.replace(" ","")
                column = column.replace("i","j")
                column = column.split("+")
                if column[1][0] == '-':
                    column = column[0] + column[1]
                else:
                    column = column[0] + "+" + column[1]
                temprow.append(complex(column))
            temph.append(temprow)
        h.append(temph)

print(len(h))
print(len(h[0]))
print(len(h[0][0]))

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:
    # Send data
    # Send data
    h2 = np.array(h, dtype=np.complex64)
    header = f"np.{h2.dtype.name};{h2.shape}"
    header = f"{header:<{32}}"
    print(header)
    msg = bytes(header, "utf-8") + h2.tobytes() + bytes("end","utf-8")
    print(f'sending {len(msg)} bytes')
    sock.sendall(msg)
finally:
    print('closing socket')
    sock.close()
