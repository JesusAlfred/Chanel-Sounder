import socket
import csv
import numpy as np
import random as rd
import time

# # Create a TCP/IP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Connect the socket to the port where the server is listening
# server_address = ('localhost', 10000)
# print('connecting to {} port {}'.format(*server_address))
# sock.connect(server_address)

#Dosificar Realizaciones

while(True):
    h = []

    ChannelRealizationFileName = "./ChannelRealizations/realizationArray"
    rand_Index = rd.randrange(1,100)
    fileRoute = ChannelRealizationFileName + str(rand_Index) + ".csv"
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

    #Espera en tiempo real 
    snooze = rd.randrange(0,2)
    time.sleep(snooze)

    #Intentar enviar algo
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
    try:
        # Send data
        # send_message = json.dumps(h, cls=ComplexEncoder)
        print('sending')
        h2 = np.array(h)
        header = f"np.{h2.dtype.name};{h2.shape}"
        header = f"{header:<{32}}"
        print(header)
        msg = bytes(header, "utf-8") + h2.tobytes() + bytes("end","utf-8")
        sock.sendall(msg)
    finally:
        print('closing socket')
        sock.close()

# Declaración de matriz que contiene todas las iteraciones


##### Tomar Realizaciones de Archivo #####

# ChannelRealizationFileName = "./ChannelRealizations/realizationArray"
# for i in range(0, 100):
#     fileRoute = ChannelRealizationFileName + str(i+1) + ".csv"
#     with open(fileRoute) as csv_file:
        # csv_reader = csv.reader(csv_file, delimiter=',')
        # line_count = 0
        # temph = []
        # for row in csv_reader:
        #     temprow = []
        #     for column in row:
        #         column = column.replace(" ","")
        #         column = column.replace("i","j")
        #         column = column.split("+")
        #         if column[1][0] == '-':
        #             column = column[0] + column[1]
        #         else:
        #             column = column[0] + "+" + column[1]
        #         temprow.append(complex(column))
        #     temph.append(temprow)
        # h.append(temph)

# print(len(h))
# print(len(h[0]))
# print(len(h[0][0]))

##### Tomar Realizaciones de Archivo #####